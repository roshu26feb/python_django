'''
Created on 30 Jan 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.system import SystemModel
from delivery_db_api.models.system_element import SystemElementModel
from delivery_db_api.models.system_element_component import SystemElementComponentModel
from delivery_db_api.models.system_version import SystemVersionModel
from delivery_db_api.resources.abstract_resource import AbstractResource
from delivery_db_api.security import authenticate


class SystemElement(AbstractResource):
    '''
    This method creates a new System Element in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('system_element_id', type=int, required=False)
        parser.add_argument('system_element_name', type=str, required=False)
        parser.add_argument(
            'system_element_short_name',
            type=str,
            required=False)
        parser.add_argument('system_element_type_id', type=int, required=False)
        parser.add_argument('system_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return SystemElementModel

    @authenticate
    def post(self):
        '''
        This post method will creates a new System Element in the delivery database
        '''
        request_data = request.get_json()
        system_id = request_data["system_id"]
        system_element_name = request_data["system_element_name"]
        system_element_short_name = request_data["system_element_short_name"]
        system_element_type_id = request_data["system_element_type_id"]

        search_keys = {"system_id": system_id}

        try:
            systems_from_db = SystemModel.find_generic(
                **search_keys)
            systems_from_db = systems_from_db[0]
            for system_element in systems_from_db.system_elements:
                if system_element.system_element_name == system_element_name:
                    return {"message": "System Element with name " +
                            system_element_name + " already exist"}, 400

            new_system_element = SystemElementModel(
                system_element_name=system_element_name,
                system_element_short_name=system_element_short_name,
                system_element_type_id=system_element_type_id)

            systems_from_db.system_elements.append(new_system_element)
            systems_from_db.save_to_db()
            return {"system_element_id": new_system_element.system_element_id}

        except ObjectNotFound as exception:
            return exception.message, exception.status_code

import ast
class SystemElementDetailsByEnvID(Resource):
    '''
    This method get System Element, System version in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('system_id', type=int, required=False)
        parser.add_argument('env_id', type=int, required=False)

    def get(self):
        '''
        This method retrieves system_element deployed on a specific environment and returns the output in JSON format.
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        env_id = args['env_id']
        system_id = args['system_id']
        resp_data = {}
        sys_ele_obj = SystemElementModel.query.filter_by(system_id=system_id)
        obj = []
        for sys_ele in sys_ele_obj:  
            system_element_component_obj = SystemElementComponentModel.query.filter_by(system_element_id=sys_ele.system_element_id).group_by(SystemElementComponentModel.system_version_id).order_by("system_element_component_id desc").first()
            data = {}
            data['system_element_name'] = sys_ele.system_element_name
            data['system_element_type_name'] = sys_ele.system_element_type.system_element_type_name            
            data['system_version_id'] = system_element_component_obj.system_version_id
            data['system_element_id'] = sys_ele.system_element_id
            data['system_id'] = int(system_id)
            data['env_id'] = int(env_id)
            
            instance_set = set()
            for deployment in sys_ele.deployments:
                instance_data = {}
                instance = deployment.instance
                if (instance is not None and (int(deployment.environment_id) == int(env_id)) ):
                    system_version = sys_ele.get_latest_version_deployed(deployment.instance.instance_id,sys_ele.system_element_id,env_id)
                    if system_version['system_version_id']  :
                        system_version_known_obj = SystemVersionModel.query.filter_by(system_version_id=system_version['system_version_id']).first()
                        data['system_version_name'] = system_version_known_obj.system_version_name
                    else: 
                        data['system_version_name'] = 'Unknown'
                    data['instance_id'] = instance.instance_id
                    data['instance_name'] = instance.instance_name
                    data['assigned_ip'] = instance.assigned_ip
                    data['instance_state'] = instance.instance_state
                    instance_set.add(str(data))
            instances = [ast.literal_eval(instance)
                         for instance in instance_set]
            if len(instances) > 0:
                for ints in instances:        
                    obj.append(ints)
            else:
                obj.append(data)
        return jsonify(obj)
