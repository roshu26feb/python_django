'''
Created on 12 Dec 2017

@author: anil.kumar
'''
from flask.globals import request
from delivery_db_api.models.host_type import HostTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class HostType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to host type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('host_type_id', type=int, required=False)
        parser.add_argument('host_name', type=str, required=False)

    def get_model(self):
        return HostTypeModel

    @authenticate
    def post(self):
        '''
        This method creates host_type store type in the delivery database
        '''
        request_data = request.get_json()
        host_name = request_data["host_name"]
        if HostTypeModel.find_by_name(host_name) is not None:
            return return_object_already_exist_errr(
                "host_type", "host name:", host_name)
        host_type = HostTypeModel(
            host_name=host_name)
        return {"host_type_id": host_type.save_to_db()}
