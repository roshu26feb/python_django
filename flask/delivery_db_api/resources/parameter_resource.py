'''
Created on 10 April 2018

@author: neeraj.mahajan
'''
import os

from flask import jsonify
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.parameter import ParameterModel
from delivery_db_api.models.parameter_value import ParameterValueModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class Parameter(AbstractResource):
    '''
    This class defines the handler for handing the requests related to parameter type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('parameter_id', type=int, required=False)
        parser.add_argument('parameter_name', type=str, required=False)
        parser.add_argument(
            'parameter_internal_name',
            type=str,
            required=False)
        parser.add_argument('mandatory', type=bool, required=False)
        parser.add_argument('active', type=bool, required=False)
        parser.add_argument('parameter_type_id', type=int, required=False)
        parser.add_argument('component_type_id', type=int, required=False)
        parser.add_argument('component_id', type=int, required=False)
        parser.add_argument('component_version_id', type=int, required=False)

    def get_model(self):
        return ParameterModel

    @authenticate
    def post(self):
        '''
        This method creates parameter store type in the delivery database
        '''
        request_data = request.get_json()
        parameter_name = request_data["parameter_name"]
        parameter_internal_name = request_data["parameter_internal_name"]
        mandatory = request_data["mandatory"]
        active = request_data["active"]
        parameter_type_id = request_data["parameter_type_id"]

        component_type_id = request_data.get("component_type_id", None)
        component_id = request_data.get("component_id", None)
        component_version_id = request_data.get("component_version_id", None)

        if ParameterModel.find_by_name(parameter_name) is not None:
            return return_object_already_exist_errr(
                "parameter", "parameter name:", parameter_name)
        parameter = ParameterModel(
            parameter_name=parameter_name,
            parameter_internal_name=parameter_internal_name,
            mandatory=mandatory,
            active=active,
            parameter_type_id=parameter_type_id)
        value_required = False
        if component_type_id is not None and component_type_id != '':
            parameter.component_type_id = component_type_id
            value_required = True

        if component_id is not None and component_id != '':
            parameter.component_id = component_id
            value_required = True

        elif component_version_id is not None:
            parameter.component_version_id = component_version_id
            value_required = True
        if value_required:
            if parameter_type_id in os.getenv(
                    'MANDATORY_PARAMETER_TYPES', (3, 4, 5)):
                parameter_values = request_data["parameter_values"]
            else:
                parameter_values = request_data.get("parameter_values", [])
            parameter.parameter_values = list(
                map(
                    lambda value: ParameterValueModel(parameter_value=value), parameter_values))
        return {"parameter_id": parameter.save_to_db().parameter_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of parameter for the changed state
        '''
        request_data = request.get_json()
        parameter_id = request_data["parameter_id"]
        try:
            parameter = ParameterModel.find_by_id(parameter_id)
            parameter_name = request_data.get("parameter_name", None)
            parameter_internal_name = request_data.get(
                "parameter_internal_name", None)
            mandatory = request_data.get("mandatory", None)
            active = request_data.get("active", None)
            parameter_type_id = request_data.get("parameter_type_id", None)
            component_type_id = request_data.get("component_type_id", None)
            component_id = request_data.get("component_id", None)
            component_version_id = request_data.get(
                "component_version_id", None)

            if parameter_name is not None and parameter.parameter_name != parameter_name:
                if ParameterModel.find_by_name(parameter_name) is not None:
                    return return_object_already_exist_errr(
                        "parameter", "parameter name:", parameter_name)
                parameter.parameter_name = parameter_name

            if parameter_internal_name is not None:
                parameter.parameter_internal_name = parameter_internal_name
            if mandatory is not None:
                parameter.mandatory = mandatory
            if active is not None:
                parameter.active = active
            if parameter_type_id is not None:
                parameter.parameter_type_id = parameter_type_id

            if component_type_id is not None:
                parameter.component_type_id = component_type_id
                parameter.component_id = None
                parameter.component_version_id = None

            elif component_id is not None:
                parameter.component_type_id = None
                parameter.component_id = component_id
                parameter.component_version_id = None

            elif component_version_id is not None:
                parameter.component_type_id = None
                parameter.component_id = None
                parameter.component_version_id = component_version_id

            parameter_values = parameter_values = request_data.get(
                "parameter_values", None)
            if parameter_values is not None:
                parameter.parameter_values = list(
                    map(
                        lambda value: ParameterValueModel(parameter_value=value), parameter_values))
            return jsonify(parameter.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code
