'''
Created on 2 Nov 2017

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.models.release import ReleaseModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class Release(AbstractResource):
    '''
    This method creates a new Release in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('release_id', type=int, required=False)
        parser.add_argument('release_name', type=str, required=False)
        parser.add_argument('release_owner', type=str, required=False)
        parser.add_argument('release_summary', type=str, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return ReleaseModel

    @authenticate
    def post(self):
        '''
        This post method will get details in Json format and creates a new
        Release in the delivery database
        '''
        request_data = request.get_json()
        release_name = request_data["release_name"]
        release_owner = request_data["release_owner"]
        release_summary = request_data["release_summary"]

        release = ReleaseModel(
            release_name=release_name,
            release_owner=release_owner,
            release_summary=release_summary)
        if ReleaseModel.check_if_release_exist(release_name):
            return return_object_already_exist_errr(
                "release", "name:", release_name)
        return {"release_id": release.save_to_db()}
