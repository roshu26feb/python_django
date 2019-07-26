'''
Created on 20 March 2018

@author: neeraj.mahajan
'''
from flask.globals import request
from delivery_db_api.models.infrastructure_type import InfrastructureTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class InfrastructureType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to infrastructure type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('infrastructure_type_id', type=int, required=False)
        parser.add_argument(
            'infrastructure_type_name',
            type=str,
            required=False)

    def get_model(self):
        return InfrastructureTypeModel

    @authenticate
    def post(self):
        '''
        This method creates infrastructure_type store type in the delivery database
        '''
        request_data = request.get_json()
        infrastructure_type_name = request_data["infrastructure_type_name"]
        if InfrastructureTypeModel.find_by_name(
                infrastructure_type_name) is not None:
            return return_object_already_exist_errr(
                "infrastructure_type",
                "infrastructure_type_name:",
                infrastructure_type_name)
        infrastructure_type = InfrastructureTypeModel(
            infrastructure_type_name=infrastructure_type_name)
        return {"infrastructure_type_id": infrastructure_type.save_to_db()}
