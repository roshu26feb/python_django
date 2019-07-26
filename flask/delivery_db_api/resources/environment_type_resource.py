'''
Created on 9 Jan 2018

@author: anil.kumar
'''
from flask.globals import request
from flask import jsonify
from flask_restful import reqparse, Resource
from delivery_db_api.models.environment_type import EnvironmentTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate


class EnvironmentType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to  environment_type
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('environment_type_id', type=int, required=False)
        parser.add_argument('environment_type_name', type=str, required=False)
        parser.add_argument(
            'environment_type_short_name',
            type=str,
            required=False)
        parser.add_argument('identifier', type=str, required=False)
        parser.add_argument(
            'environment_subscription_type_id',
            type=int,
            required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return EnvironmentTypeModel

    @authenticate
    def post(self):
        '''
        This method creates environment_type store type in the delivery database
        '''
        request_data = request.get_json()
        environment_type_name = request_data["environment_type_name"]
        environment_type_short_name = request_data["environment_type_short_name"]
        identifier = request_data["identifier"]
        environment_subscription_type_id = request_data["environment_subscription_type_id"]
        if EnvironmentTypeModel.find_by_name(
                environment_type_name) is not None:
            return return_object_already_exist_errr(
                "environment_type", "environment type name:", environment_type_name)
        environment_type = EnvironmentTypeModel(
            environment_type_name=environment_type_name,
            environment_type_short_name=environment_type_short_name,
            identifier=identifier,
            environment_subscription_type_id=environment_subscription_type_id)
        return {"environment_type_id": environment_type.save_to_db()}

class EnvironmentTypeList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('systemId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all Environment Types
        '''

        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        system_id = args['systemId']

        env_list = EnvironmentTypeModel.get_esv_environment_types(system_id)
        return_data = []
        for data in env_list:
            json_data = {
                'environmentTypeId' : data[0],
                'environmentTypeName' : data[1]
            }
            return_data.append(json_data)
        return jsonify(return_data)
