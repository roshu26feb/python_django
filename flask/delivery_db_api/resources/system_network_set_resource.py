'''
Created on 16 May 2018

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.models.system_network_set import SystemNetworkSetModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class SystemNetworkSet(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system element type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('system_network_set_id', type=int, required=False)
        parser.add_argument(
            'system_network_set_name',
            type=str,
            required=False)
        parser.add_argument(
            'system_network_set_short_name',
            type=str,
            required=False)

    def get_model(self):
        return SystemNetworkSetModel

    @authenticate
    def post(self):
        '''
        This method creates system_network_set store type in the delivery database
        '''
        request_data = request.get_json()
        system_network_set_name = request_data["system_network_set_name"]
        system_network_set_short_name = request_data["system_network_set_short_name"]

        if SystemNetworkSetModel.find_by_name(
                system_network_set_name) is not None:
            return return_object_already_exist_errr(
                "system_network_set",
                "system_network_set_name:",
                system_network_set_name)
        system_network_set = SystemNetworkSetModel(
            system_network_set_name=system_network_set_name,
            system_network_set_short_name=system_network_set_short_name)
        return {
            "system_network_set_id": system_network_set.save_to_db().system_network_set_id}
