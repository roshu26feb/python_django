'''
Created on 19 April 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.role import RoleModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class Role(AbstractResource):
    '''
    This class defines the handler for handing the requests related to role type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('role_id', type=int, required=False)
        parser.add_argument('role_name', type=str, required=False)

    def get_model(self):
        return RoleModel

    @authenticate
    def post(self):
        '''
        This method creates role store type in the delivery database
        '''
        request_data = request.get_json()
        role_name = request_data["role_name"]
        if RoleModel.find_by_name(role_name) is not None:
            return return_object_already_exist_errr(
                "role", "role name:", role_name)
        role = RoleModel(
            role_name=role_name)
        return {"role_id": role.save_to_db().role_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of role for the changed state
        '''
        request_data = request.get_json()
        role_id = request_data["role_id"]
        try:
            role = RoleModel.find_by_id(role_id)
            role_name = request_data.get("role_name", None)
            if role_name is not None and role.role_name != role_name:
                if RoleModel.find_by_name(role_name) is not None:
                    return return_object_already_exist_errr(
                        "role", "role name:", role_name)
                role.role_name = role_name
            return jsonify(role.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code
