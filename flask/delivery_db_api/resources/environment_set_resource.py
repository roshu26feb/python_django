'''
Created on 7 Feb 2018

@author: anil.kumar
'''
from flask import jsonify
from flask.globals import request
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.environment_set import EnvironmentSetModel
from delivery_db_api.models.environment_set_link import EnvironmentSetLinkModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class EnvironmentSet(AbstractResource):
    '''
    This class defines the handler for handing the requests related to environment_set
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('environment_set_id', type=int, required=False)
        parser.add_argument('environment_set_name', type=str, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return EnvironmentSetModel

    @authenticate
    def post(self):
        '''
        This post method will creates a new Environment set in the delivery database
        '''
        request_data = request.get_json()
        environment_set_name = request_data["environment_set_name"]
        environment_ids = request_data["environment_ids"]

        temp_environment_ids = list(
            map(lambda x: x['environment_id'], environment_ids))

        if len(temp_environment_ids) != len(set(temp_environment_ids)):
            return {"message": "Duplicate Environment ids specified"}, 400

        search_keys = {"environment_set_name": environment_set_name}

        try:
            if EnvironmentSetModel.find_generic(**search_keys) is not None:
                return return_object_already_exist_errr(
                    "environment_set", "environment set name:", environment_set_name)
        except ObjectNotFound:
            new_environment_set_name = EnvironmentSetModel(
                environment_set_name=environment_set_name)
            new_environment_set_name.environment_set_link = list(map(
                lambda x: EnvironmentSetLinkModel(environment_id=x['environment_id']), environment_ids))
            new_environment_set_name.save_to_db()
            return {
                "environment_set_id": new_environment_set_name.environment_set_id}

    @authenticate
    def put(self):
        '''
        This method updates environment_set, it will add and remove
        environmet_id from environment set as per provide payload
        '''
        request_data = request.get_json()
        environment_set_id = request_data["environment_set_id"]
        ids_to_add = request_data["environment_ids_to_add"]
        ids_for_del = request_data["environment_ids_to_del"]
        search_env_set_id = {"environment_set_id": environment_set_id}
        environment_add = EnvironmentSetModel.find_generic(**search_env_set_id)
        linked_env = environment_add[0].environment_set_link
        common_env_id_in_payload = list(set(ids_to_add) & set(ids_for_del))
        if not common_env_id_in_payload:
            if ids_for_del or ids_to_add:
                if ids_for_del:
                    i = 1
                    while i <= len(ids_for_del):
                        EnvironmentSet.remove_env(linked_env, ids_for_del)
                        i += 1
                ids_from_db = list()
                if ids_to_add:
                    for env in linked_env:
                        ids_from_db.append(env.environment_id)
                    env_ids_to_be_added = set(
                        ids_to_add).difference(set(ids_from_db))
                    for _id in env_ids_to_be_added:
                        linked_env.append(
                            EnvironmentSetLinkModel(
                                environment_id=_id))
                return jsonify(environment_add[0].save_to_db().json())
            return {"message": "Invalid Data"}, 400
        return {"message": "Duplicate data in payload"}, 400

    @staticmethod
    def remove_env(linked_env, ids_for_del):
        ''' Remove requested environment from existing environment list'''
        for env in linked_env:
            if env.environment_id in ids_for_del:
                linked_env.remove(env)
                break
