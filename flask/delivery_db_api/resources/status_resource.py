'''
Created on 23 Jan 2018

@author: anil.kumar
'''
from flask.globals import request
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.status import StatusModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class Status(AbstractResource):
    '''
    This class defines the handler for handing the requests related to status
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('status_id', type=int, required=False)
        parser.add_argument('status_description', type=str, required=False)
        parser.add_argument('status_type', type=str, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return StatusModel

    @authenticate
    def post(self):
        '''
        This method creates staus to store  in the delivery database
        '''
        request_data = request.get_json()
        status_description = request_data["status_description"]
        status_type = request_data["status_type"]
        status = StatusModel(
            status_description=status_description,
            status_type=status_type)
        search_keys = {"status_description": status_description,
                       "status_type": status_type
                       }
        try:
            if StatusModel.find_generic(
                    **search_keys) is not None:
                return return_object_already_exist_errr(
                    "Status",
                    "",
                    status_description +
                    " with status_type " +
                    str(status_type))
        except ObjectNotFound as exception:
            return {"status_id": status.save_to_db()}
