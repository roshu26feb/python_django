'''
Created on 7 Apr 2018

@author: anil.kumar
'''
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate
from flask.globals import request

from delivery_db_api.models.environment_subscription_type import EnvironmentSubscriptionTypeModel


class EnvironmentSubscriptionType(AbstractResource):

    '''
    This class defines the handler for handing the requests related to EnvironmentSubscriptionType
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument(
            'environment_subscription_type_id',
            type=int,
            required=False)
        parser.add_argument(
            'environment_subscription_type_name',
            type=str,
            required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return EnvironmentSubscriptionTypeModel

    @authenticate
    def post(self):
        '''
        This method creates environment_data_type in the delivery database
        '''
        request_data = request.get_json()
        environment_subscription_type_name = request_data["environment_subscription_type_name"]
        if EnvironmentSubscriptionTypeModel.find_by_env_subscription_type_name(
                environment_subscription_type_name) is not None:
            return return_object_already_exist_errr(
                "Environment subscription type ",
                "Environment subscription type name:",
                environment_subscription_type_name)
        environment_data_type = EnvironmentSubscriptionTypeModel(
            environment_subscription_type_name=environment_subscription_type_name)
        return {
            "environment_subscription_type_id": environment_data_type.save_to_db()}
