'''
Created on 22 Feb 2018

@author: neeraj.mahajan
'''
from flask.globals import request
from delivery_db_api.models.method_creation_type import MethodCreationTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class MethodCreationType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to host type
    '''

    def add_argument_for_parsing(self, parser):
        ''' parameters for lookup'''
        parser.add_argument(
            'method_creation_type_id',
            type=int,
            required=False)
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)

    def get_model(self):
        return MethodCreationTypeModel

    @authenticate
    def post(self):
        '''
        This method creates method_creation_type store type in the delivery database
        '''
        request_data = request.get_json()
        name = request_data["name"]
        description = request_data["description"]
        if MethodCreationTypeModel.find_by_name(name) is not None:
            return return_object_already_exist_errr(
                "method_creation_type", "name:", name)
        method_creation_type = MethodCreationTypeModel(
            name=name, description=description)
        return {"method_creation_type_id": method_creation_type.save_to_db()}
