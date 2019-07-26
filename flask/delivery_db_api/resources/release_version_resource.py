'''
Created on 5 March 2018

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.models.release_item import ReleaseItemModel
from delivery_db_api.models.release_version import ReleaseVersionModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate
from delivery_db_api.utils import DateUtils


class ReleaseVersion(AbstractResource):
    '''
    This method creates a new ReleaseVersion in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('release_version_id', type=int, required=False)
        parser.add_argument('release_id', type=int, required=False)
        parser.add_argument('release_version_name', type=str, required=False)
        self.add_date_to_parser(parser, 'creation_date')
        self.add_date_to_parser(parser, 'target_release_date')
        parser.add_argument('remarks', type=str, required=False)
        parser.add_argument(
            'release_version_status_id',
            type=int,
            required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return ReleaseVersionModel

    @authenticate
    def post(self):
        '''
        This post method will get details in Json format and creates a new
        ReleaseVersion in the delivery database
        '''
        request_data = request.get_json()
        release_version_name = request_data["release_version_name"]
        release_id = request_data["release_id"]

        if ReleaseVersionModel.check_if_release_exist(
                release_id, release_version_name):
            return return_object_already_exist_errr(
                "release_version", "name:", release_version_name)

        creation_date = DateUtils.create_date_from_input_string(
            request_data.get("creation_date", None))
        target_release_date = DateUtils.create_date_from_input_string(
            request_data["target_release_date"])
        remarks = request_data["remarks"]
        release_version_status_id = request_data["release_version_status_id"]
        release_items = request_data["release_items"]

        release_version = ReleaseVersionModel(
            release_version_name=release_version_name,
            release_id=release_id,
            creation_date=creation_date,
            target_release_date=target_release_date,
            remarks=remarks,
            release_version_status_id=release_version_status_id)
        release_version.release_items = list(
            map(
                lambda x: ReleaseItemModel(
                    system_version_id=x['system_version_id'],
                    release_note_url=x['release_note_url']),
                release_items))
        return {"release_version_id": release_version.save_to_db()}
