'''
Created on 2 Nov 2017

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.system import SystemModel
from delivery_db_api.models.system_element_component import SystemElementComponentModel
from delivery_db_api.models.system_version import SystemVersionModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate
from delivery_db_api.utils import DateUtils


class System(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system resource
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('system_id', type=int, required=False)
        parser.add_argument('system_name', type=str, required=False)
        parser.add_argument('system_short_name', type=str, required=False)
        parser.add_argument('system_network_set_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return SystemModel

    @authenticate
    def post(self):
        '''
        This method creates a new system in the delivery database
        '''
        request_data = request.get_json()
        system_name = request_data["system_name"]
        system_short_name = request_data["system_short_name"]
        creation_date = DateUtils.create_date_from_input_string(
            request_data.get("creation_date", None))
        system_network_set_id = request_data["system_network_set_id"]
        if SystemModel.find_by_name(system_name) is not None:
            return return_object_already_exist_errr(
                "System", "system_name:", system_name)
        system = SystemModel(
            system_name=system_name,
            system_short_name=system_short_name,
            creation_date=creation_date,
            system_network_set_id=system_network_set_id)
        return {"system_id": system.save_to_db()}


class SystemVersion(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system resource
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('system_version_id', type=int, required=False)
        parser.add_argument('system_version_name', type=str, required=False)
        parser.add_argument('system_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return SystemVersionModel

    @authenticate
    def post(self):
        '''
        This method creates a new system in the delivery database
        '''
        request_data = request.get_json()
        system_id = request_data["system_id"]
        system_version_name = request_data["system_version_name"]
        creation_date = DateUtils.create_date_from_input_string(
            request_data.get("creation_date", None))

        try:
            system_from_db = SystemModel.find_by_id(system_id)
        except ObjectNotFound as exception:
            return exception.message, exception.status_code

        if system_from_db is not None:
            if list(
                    filter(
                        lambda x: x.system_version_name == system_version_name,
                        system_from_db.system_versions)):
                return return_object_already_exist_errr(
                    "System Version", "system_version_name:", system_version_name)
 
        system_version = SystemVersionModel(
            system_version_name=system_version_name,
            creation_date=creation_date)
        system_version.system = system_from_db
        return {"system_version_id": system_version.save_to_db()}

class SystemViewSystemsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Systems
        '''
        systems_list = SystemModel.get_sv_systems()
        return_data = []
        for data in systems_list:
            json_data = {
                'systemId' : data[0],
                'systemName' : data[1],
                'systemShortName' : data[2]
            }
            return_data.append(json_data)
        return jsonify(return_data)

class EnvironmentAvailabilityViewSystemsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Systems which has environment
        '''
        systems_list = SystemModel.get_eav_systems()
        return_data = []
        for data in systems_list:
            json_data = {
                'systemId' : data[0],
                'systemName' : data[1],
                'systemShortName' : data[2]
            }
            return_data.append(json_data)
        return jsonify(return_data)

class SystemViewSystemVersionsList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('systemId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all system versions
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        system_id = args['systemId']
        system_versions_list = SystemModel.get_sv_system_versions(system_id)
        return_data = []
        for data in system_versions_list:
            json_data = {
                'systemVersionId' : data[0], 
                'systemVersionName' : data[1],
                'creationDate' : data[2]

            }
            return_data.append(json_data)
        return jsonify(return_data)

class SystemViewSystemElementsList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('systemId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all system versions
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        system_id = args['systemId']
        system_elements_list = SystemModel.get_sv_system_elements(system_id)
        return_data = []
        for data in system_elements_list:
            json_data = {
                'systemElementId' : data[0], 
                'systemElementName' : data[1],
                'systemElementShortName' : data[2],
                'systemElementTypeId' : data[3], 
                'systemElementTypeName' : data[4]

            }
            return_data.append(json_data)
        return jsonify(return_data)

class SystemViewComponentsList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('systemVersionId', type=int, required=True)
        parser.add_argument('systemElementId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all components
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        system_version_id = args['systemVersionId']
        system_element_id = args['systemElementId']
        components_list = SystemModel.get_sv_components(system_version_id, system_element_id)
        return_data = []
        for data in components_list:
            json_data = {
                'componentId' : data[0], 
                'componentName' : data[1],
                'componentVersionId' : data[2],
                'componentVersionName' : data[3],
                'componentShortName' : data[4],
                'componentTypeId' : data[5],
                'componentTypeDescription' : data[6],
                'artifactStoreUrl' : data[7],
                'artifactStoreTypeId' : data[8],
                'artifactStoreTypeDesc' : data[9],
                'sourceCodeRepositoryUrl' : data[10],
                'sourceTagReference' : data[11],
                'stableFlag' : data[12],
                'creationDate' : data[13],
                'deploymentTypeId' : data[14],
                'deploymentTypeDescription' : data[15],
                'installOrder' : data[16],
                'linkedCiFlag' : data[17]

            }
            return_data.append(json_data)
        return jsonify(return_data)