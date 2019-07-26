'''
Created on 06 Feb 2018

@author: neeraj.mahajan
'''
from flask.globals import request
from delivery_db_api.models.deployment_type import DeploymentTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class DeploymentType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to deployment type
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('deployment_type_id', type=int, required=False)
        parser.add_argument(
            'deployment_type_description',
            type=str,
            required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return DeploymentTypeModel

    @authenticate
    def post(self):
        '''
        This method creates deployment_type store type in the delivery database
        '''
        request_data = request.get_json()
        deployment_type_description = request_data["deployment_type_description"]
        if DeploymentTypeModel.find_by_description(
                deployment_type_description) is not None:
            return return_object_already_exist_errr(
                "deployment_type",
                "deployment type description:",
                deployment_type_description)
        deployment_type = DeploymentTypeModel(
            deployment_type_description=deployment_type_description)
        return {"deployment_type_id": deployment_type.save_to_db()}
