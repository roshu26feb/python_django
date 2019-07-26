'''
Created on 19 April 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.user import UserModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate
from delivery_db_api.models.user_role import UserRoleModel


class User(AbstractResource):
    '''
    This class defines the handler for handing the requests related to user type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('user_id', type=int, required=False)
        parser.add_argument('user_name', type=str, required=False)
        parser.add_argument('user_display_name', type=str, required=False)
        parser.add_argument('email_address', type=str, required=False)

    def get_model(self):
        return UserModel

    @authenticate
    def post(self):
        '''
        This method creates user store type in the delivery database
        '''
        request_data = request.get_json()
        user_name = request_data["user_name"]
        user_display_name = request_data["user_display_name"]
        email_address = request_data["email_address"]
        user_roles = request_data["user_roles"]
        if UserModel.find_by_name(user_name) is not None:
            return return_object_already_exist_errr(
                "user", "user name:", user_name)
        user = UserModel(
            user_name=user_name,
            user_display_name=user_display_name,
            email_address=email_address)

        user.user_roles = list(
            map(lambda role_id: UserRoleModel(role_id=role_id), user_roles))

        return {"user_id": user.save_to_db().user_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of user for the changed state
        '''
        request_data = request.get_json()
        user_id = request_data["user_id"]
        try:
            user = UserModel.find_by_id(user_id)
            user_name = request_data.get("user_name", None)
            user_display_name = request_data.get("user_display_name", None)
            email_address = request_data.get("email_address", None)
            user_roles = request_data.get("user_roles", None)

            if user_name is not None and user.user_name != user_name:
                if UserModel.find_by_name(user_name) is not None:
                    return return_object_already_exist_errr(
                        "user", "user name:", user_name)
                user.user_name = user_name

            if user_display_name is not None:
                user.user_display_name = user_display_name

            if email_address is not None:
                user.email_address = email_address

            if user_roles is not None and len(user_roles) != 0:
                user.user_roles = list(
                    map(lambda role_id: UserRoleModel(role_id=role_id), user_roles))
            return jsonify(user.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code
