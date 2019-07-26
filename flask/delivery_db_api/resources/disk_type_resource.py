'''
Created on 16 Jan 2018

@author: anil.kumar
'''
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.disk_type import DiskTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate


class DiskType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to disk type
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('disk_type_id', type=int, required=False)
        parser.add_argument('disk_type_description', type=str, required=False)
        parser.add_argument('min_size', type=int, required=False)
        parser.add_argument('max_size', type=int, required=False)
        parser.add_argument('host_type_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return DiskTypeModel

    @authenticate
    def post(self):
        '''
        This post method will get details in Json format and creates a new
        Disk type in the delivery database
        '''
        request_data = request.get_json()
        disk_type_description = request_data["disk_type_description"]
        min_size = request_data["min_size"]
        max_size = request_data["max_size"]
        host_type_id = request_data["host_type_id"]

        disk_type = DiskTypeModel(
            disk_type_description=disk_type_description,
            min_size=min_size,
            max_size=max_size,
            host_type_id=host_type_id)
        search_keys = {"disk_type_description": disk_type_description,
                       "host_type_id": host_type_id
                       }
        try:
            if DiskTypeModel.find_generic(
                    **search_keys) is not None:
                return return_object_already_exist_errr(
                    "Disk type",
                    "description:",
                    disk_type_description +
                    " with host_type_id " +
                    str(host_type_id))
        except ObjectNotFound as exception:
            return {"disk_type_id": disk_type.save_to_db()}
