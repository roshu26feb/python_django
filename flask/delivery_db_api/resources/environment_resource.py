'''
Created on 02 Jan 2018

@author: neeraj.mahajan
'''
from flask.globals import request
from flask import jsonify
from flask_restful import reqparse, Resource
from delivery_db_api.models.environment import EnvironmentModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate
from delivery_db_api.utils import DateUtils


class Environment(AbstractResource):
    '''
    This class defines the handler for handing the requests related to environment resource
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('environment_id', type=int, required=False)
        parser.add_argument('environment_name', type=str, required=False)
        parser.add_argument('environment_type_id', type=int, required=False)
        parser.add_argument(
            'environment_data_type_id',
            type=int,
            required=False)
        parser.add_argument('system_id', type=int, required=False)
        self.add_date_to_parser(parser)

    def get_model(self):
        ''' Returns the model class used'''
        return EnvironmentModel

    @authenticate
    def post(self):
        '''
        This method creates a new environment in the delivery database
        '''
        request_data = request.get_json()
        environment_name = request_data["environment_name"]
        if EnvironmentModel.find_by_name(
                environment_name) is not None:
            return return_object_already_exist_errr(
                "Environment", "name:", environment_name)

        environment_type_id = request_data["environment_type_id"]
        creation_date = DateUtils.create_date_from_input_string(
            request_data.get("creation_date", None))
        environment_data_type_id = request_data["environment_data_type_id"]
        system_id = request_data["system_id"]
        input_environment = self.get_environment(
            environment_name,
            environment_type_id,
            creation_date,
            environment_data_type_id,
            system_id)
        return {"environment_id": input_environment.save_to_db()}

    def get_environment(
            self,
            environment_name,
            environment_type_id,
            creation_date,
            environment_data_type_id,
            system_id):
        '''
        Convenience Method for post request
        '''
        return EnvironmentModel(
            environment_name=environment_name,
            creation_date=creation_date,
            environment_type_id=environment_type_id,
            environment_data_type_id=environment_data_type_id,
            system_id=system_id)

class EnvironmentsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Environments
        '''
        env_list = EnvironmentModel.get_ev_environments()
        return_data = []
        for data in env_list:
            json_data = {
                'environmentId' : data[0],
                'environmentName' : data[1],
                'environmentTypeId' : data[2],
                'environmentTypeName' : data[3],
                'systemId' : data[4],
                'systemName' : data[5],
                'environmentDataTypeId' : data[6],
                'environmentDataTypeName' : data[7],
                'evEnvironmentVersion' : data[8]
            }
            return_data.append(json_data)
        return jsonify(return_data)

class EnvironmentsListBySystem(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('systemId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all environments for list of environment availability screen
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        system_id = args['systemId']
        
        env_list = EnvironmentModel.get_eav_environments(system_id)
        return_data = []
        for data in env_list:
            json_data = {
                'environmentId' : data[0],
                'environmentName' : data[1],
                'systemId' : data[2],
                'systemName' : data[3],
                'environmentDataTypeId' : data[4],
                'environmentDataTypeName' : data[5],
                'evEnvironmentVersion' : data[6]
            }
            return_data.append(json_data)
        return jsonify(return_data)

class EnvironmentSystemelementsList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('environmentId', type=int, required=True)
        #parser.add_argument('systemId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all system elements in system
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        environment_id = args['environmentId']
        #system_id = args['systemId']
        
        #env_sys_ele_list = EnvironmentModel.get_ev_system_elements(environment_id, system_id)
        env_sys_ele_list = EnvironmentModel.get_ev_system_elements(environment_id)
        return_data = []
        for data in env_sys_ele_list:
            json_data = {
                'systemElementId' : data[0],
                'systemElementName' : data[1],
                'systemElementTypeId' : data[2],
                'systemElementTypeName' : data[3],
                'instanceId' : data[4],
                'instanceName' : data[5],
                'assignedIp' : data[6],
                'instanceState' : data[7],
                'systemVersionId' : data[8],
                'systemVersionName' : data[9],
                'systemId' : data[10],
                'evSystemVersionName' : data[11]

            }
            return_data.append(json_data)
        return jsonify(return_data)

class EnvironmentSystemelementComponentsList(Resource):
    def add_argument_for_parsing(self, parser):
        parser.add_argument('environmentId', type=int, required=True)
        parser.add_argument('systemElementId', type=int, required=True)
        #parser.add_argument('systemVersionId', type=int, required=False)
        #parser.add_argument('systemVersionId', type=int, required=True)
        parser.add_argument('instanceId', type=int, required=True)
    
    def get(self):
        '''
        This method used to get the list of all components in system element for environment view page
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        environment_id = args['environmentId']
        systemElement_id = args['systemElementId']
        #systemVersionId = args['systemVersionId']
        instance_id = args['instanceId']

        env_comp_list = []

        #if systemVersionId is None:
        #    env_comp_list = EnvironmentModel.get_ev_components_by_system_element(environmentId, systemElementId)
        #else:
        #    env_comp_list = EnvironmentModel.get_ev_components(environmentId, systemElementId, systemVersionId)
        env_comp_list = EnvironmentModel.get_ev_components(environment_id, systemElement_id, instance_id)
        return_data = []
        for data in env_comp_list:
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
                'linkedCiFlag' : data[16],
                'isDeployed' : data[17]

            }
            return_data.append(json_data)
        return jsonify(return_data)
