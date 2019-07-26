'''
Created on 04 April 2018

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.models.environment_use import EnvironmentUseModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class EnvironmentUse(AbstractResource):
    '''
    This class defines the handler for handing the requests related to host type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('environment_use_id', type=int, required=False)
        parser.add_argument('environment_use_name', type=str, required=False)
        parser.add_argument(
            'environment_use_short_name',
            type=str,
            required=False)

    def get_model(self):
        return EnvironmentUseModel

    @authenticate
    def post(self):
        '''
        This method creates environment_use store type in the delivery database
        '''
        request_data = request.get_json()
        environment_use_name = request_data["environment_use_name"]
        environment_use_short_name = request_data["environment_use_short_name"]
        if EnvironmentUseModel.find_by_name(environment_use_name) is not None:
            return return_object_already_exist_errr(
                "environment_use", "environment_use_name name:", environment_use_name)
        environment_use = EnvironmentUseModel(
            environment_use_name=environment_use_name,
            environment_use_short_name=environment_use_short_name
        )
        return {"environment_use_id": environment_use.save_to_db()}
