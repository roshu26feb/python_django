'''
Created on 15 May 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.system_element import SystemElementModel
from delivery_db_api.resources.abstract_resource import AbstractResource


class SystemElementDeploymentVersion(Resource):
    '''
    This class defines the method to retrive latest system_version deployed  '''

    def get(self):
        '''
        This method retrieves the system_version_id of the system_element deployed on a specific instance and returns the output in JSON format. In case all the components for system_version are not deployed the system_version will be returned as Unknown
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        instance_id = args['instance_id']
        system_element_id = args['system_element_id']
        return SystemElementModel.get_latest_version_deployed(
            instance_id, system_element_id)

    def add_argument_for_parsing(self, parser):
        parser.add_argument('instance_id', type=int, required=True)
        parser.add_argument('system_element_id', type=int, required=True)
