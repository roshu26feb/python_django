'''
Created on 5 Apr 2018

@author: anil.kumar
'''
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate
from flask.globals import request
from delivery_db_api.models.environment_data_type import EnvironmentDataTypeModel


class EnvironmentDataType(AbstractResource):

    '''
    This class defines the handler for handing the requests related to EnvironmentDataType
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument(
            'environment_data_type_id',
            type=int,
            required=False)
        parser.add_argument(
            'environment_data_type_name',
            type=str,
            required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return EnvironmentDataTypeModel

    @authenticate
    def post(self):
        '''
        This method creates environment_data_type in the delivery database
        '''
        request_data = request.get_json()
        environment_data_type_name = request_data["environment_data_type_name"]
        if EnvironmentDataTypeModel.find_by_env_data_type_name(
                environment_data_type_name) is not None:
            return return_object_already_exist_errr(
                "Environment data type ",
                "Environment data type name:",
                environment_data_type_name)
        environment_data_type = EnvironmentDataTypeModel(
            environment_data_type_name=environment_data_type_name)
        return {"environment_data_type_id": environment_data_type.save_to_db()}
