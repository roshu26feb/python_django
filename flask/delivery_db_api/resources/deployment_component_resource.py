'''
Created on 10 Oct 2018

@author: bharat.rathod
'''
import datetime
import os

from flask import jsonify
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.deployment_component import DeploymentComponentModel
from delivery_db_api.resources.abstract_resource import AbstractResource, \
    return_object_already_exist_errr
from delivery_db_api.security import authenticate


class DeploymentComponent(AbstractResource):
    '''
    This class defines methods for the API
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('deployment_component_id', type=int, required=False)
        parser.add_argument('deployment_id', type=int, required=False)
        parser.add_argument('system_element_component_id', type=int, required=False)
        parser.add_argument('deployment_component_status_id', type=str, required=False)
        self.add_date_to_parser(parser, 'requested_date')

    def get_model(self):
        ''' Returns the model class used'''
        return DeploymentComponentModel