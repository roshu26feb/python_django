'''
Created on 19 sept 2018

@author: bharat.rathod
'''
from flask.globals import request
from flask import jsonify
from flask_restful import reqparse, Resource
from delivery_db_api.models.instance_allocation import InstanceAllocationModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate
from delivery_db_api.models.environment import EnvironmentModel
from delivery_db_api.models.system import SystemModel
from delivery_db_api.models.system_element import SystemElementModel
from delivery_db_api.models.system_version import SystemVersionModel

class InstanceAllocation(AbstractResource):
    '''
    This class defines the handler for handing the requests related to instance allocation resource
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('instance_allocation_id', type=int, required=False)
        parser.add_argument('environment_id', type=int, required=False)
        parser.add_argument('system_id', type=int, required=False)
        parser.add_argument('system_element_id', type=int, required=False)
        #parser.add_argument('system_version_id', type=int, required=False)
        parser.add_argument('instance_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return InstanceAllocationModel

    @authenticate
    def post(self):
        '''
        This method creates a new instance_allocation in the delivery database
        '''
        request_data = request.get_json()
        environment_id = request_data["environment_id"]
        system_id = request_data["system_id"]
        system_element_id = request_data["system_element_id"]
        #system_version_id = request_data["system_version_id"]
        instance_id = request_data["instance_id"]
        instance_allocation = InstanceAllocationModel(
                environment_id=environment_id,
                system_id=system_id,
                system_element_id=system_element_id,
                #system_version_id=system_version_id,
                instance_id=instance_id
            )
        insytance_obj = instance_allocation.save_to_db()
        message = "{} is mapped successfully.".format(insytance_obj.instance_allocation_id)
        return jsonify({"instance_allocation_id": message })

class MapInstance(Resource):
    '''
    This class defines the method to retrive Map instance details '''

    def get(self):
        '''
        This method retrieves the system_version_id of the system_element deployed on a specific instance and returns the output in JSON format. In case all the components for system_version are not deployed the system_version will be returned as Unknown
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        print ('args', args)
        env_id = args['env_id']
        system_id = args['system_id']
        #system_version_id = args['system_version_id']
        system_element_id = args['system_element_id']
        data = {}
        data['env_id'] = list(map(lambda x: x.json(), EnvironmentModel.query.filter_by(environment_id=env_id)))
 
        data['system_id'] = list(map(lambda x: x.json(), SystemModel.query.filter_by(system_id=system_id)))
        data['system_element_id'] = list(map(lambda x: x.json(), SystemElementModel.query.filter_by(system_element_id=system_element_id)))
        #data['system_version_id'] = list(map(lambda x: x.json(), SystemVersionModel.query.filter_by(system_version_id=system_version_id)))
        #list(map(lambda x: x.json(), self.get_model().find_generic(**request_parameters)))
        return jsonify(data)

    def add_argument_for_parsing(self, parser):
        parser.add_argument('env_id', type=int, required=True)
        parser.add_argument('system_id', type=int, required=True)
        #parser.add_argument('system_version_id', type=int, required=True)
        parser.add_argument('system_element_id', type=int, required=True)