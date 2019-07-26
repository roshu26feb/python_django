'''
Created on 4 Dec 2017

@author: anil.kumar
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.component_type import ComponentTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate


class ComponentType(AbstractResource):

    '''
    This class defines the handler for handing the requests related to Component Type
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('component_type_id', type=int, required=False)
        parser.add_argument(
            'component_type_description',
            type=str,
            required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return ComponentTypeModel

    @authenticate
    def post(self):
        '''
        This method creates Component type in the delivery database
        '''
        request_data = request.get_json()
        component_type_description = request_data["component_type_description"]
        if ComponentTypeModel.find_by_description(
                component_type_description) is not None:
            return return_object_already_exist_errr(
                "component type ", "component type:", component_type_description)
        componenet_type = ComponentTypeModel(
            component_type_description=component_type_description)
        return {"component_type_id": componenet_type.save_to_db().component_type_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of component_type for the changed state
        '''
        request_data = request.get_json()
        component_type_id = request_data["component_type_id"]
        try:
            component_type = ComponentTypeModel.find_by_id(component_type_id)
            component_type_description = request_data.get(
                "component_type_description", None)
            if component_type_description is not None and component_type.component_type_description != component_type_description:
                if ComponentTypeModel.find_by_description(
                        component_type_description) is not None:
                    return return_object_already_exist_errr(
                        "component_type", "component_type name:", component_type_description)
                component_type.component_type_description = component_type_description
            return jsonify(component_type.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code

    @authenticate
    def delete(self):
        '''
        This method delete the component_type from db
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('component_type_id', type=int, required=False)
        args = parser.parse_args(strict=True)
        return ComponentTypeModel.delete(args.get('component_type_id'))
