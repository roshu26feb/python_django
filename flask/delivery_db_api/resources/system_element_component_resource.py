'''
Created on 30 Jan 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models import system_element_component
from delivery_db_api.models.system_element_component import SystemElementComponentModel
from delivery_db_api.models.deployment_component import DeploymentComponentModel
from delivery_db_api.models.deployment import DeploymentModel
from delivery_db_api.models.component_version import ComponentVersionModel
from delivery_db_api.models.status import StatusModel 
from delivery_db_api.resources.abstract_resource import AbstractResource, \
    return_object_already_exist_errr
from delivery_db_api.security import authenticate


class SystemElementComponent(AbstractResource):
    '''
    This method creates a new System Element Component in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument(
            'system_element_component_id',
            type=int,
            required=False)
        parser.add_argument('install_order', type=str, required=False)
        parser.add_argument('system_element_id', type=str, required=False)
        parser.add_argument('system_version_id', type=str, required=False)
        parser.add_argument('component_version_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return SystemElementComponentModel

    @authenticate
    def post(self):
        '''
        This post method will creates a new System Element in the delivery database
        '''
        request_data = request.get_json()
        install_order = request_data["install_order"]
        system_element_id = request_data["system_element_id"]
        system_version_id = request_data["system_version_id"]
        component_version_id = request_data["component_version_id"]

        search_keys = {
            "system_element_id": system_element_id,
            "system_version_id": system_version_id,
            "component_version_id": component_version_id}

        try:
            SystemElementComponentModel.find_generic(**search_keys)
            return return_object_already_exist_errr(
                "SystemElementComponent",
                "",
                'system_element_id ' +
                str(system_element_id) +
                ' system_version_id ' +
                str(system_version_id))
        except ObjectNotFound as exception:
            system_element_component = SystemElementComponentModel(
                system_element_id=system_element_id,
                system_version_id=system_version_id,
                component_version_id=component_version_id,
                install_order=install_order)
            return {
                "system_element_component_id": system_element_component.save_to_db()}



class SystemElementComponentEnv(Resource):
    '''
    This method get System Element, System version in the delivery database ESMT-926
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('system_version_id', type=int, required=False)
        parser.add_argument('system_element_id', type=int, required=False)
        parser.add_argument('env_id' , type=int, required=False)
        parser.add_argument('instance_id' , type=int, required=False)

    def get(self):
        '''
        This method retrieves system_element deployed on a specific environment and returns the output in JSON format.
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        system_version_id = args['system_version_id']
        system_element_id = args['system_element_id']
        environment_id = args['env_id']
        instance_id = args['instance_id']
        resp_data = []

        system_element_component_obj = SystemElementComponentModel.query.filter_by(system_element_id=system_element_id,system_version_id = system_version_id )
        for sys_ele_comp in system_element_component_obj:
            system_element_componentrow = {}
            system_element_components = {}
            system_element_components['install_order'] = sys_ele_comp.install_order
            system_element_components['system_element_id'] = sys_ele_comp.system_element_id
            system_element_components['system_version_id'] = sys_ele_comp.system_version_id
            system_element_components['system_element_component_id'] = sys_ele_comp.system_element_component_id
            system_element_components['deployment_component'] = ''


            component_version_obj = [x.json(True) for x in ComponentVersionModel.query.filter_by(component_version_id=sys_ele_comp.component_version_id).order_by(ComponentVersionModel.component_id).group_by(ComponentVersionModel.component_id)]

            component_version_ids = sys_ele_comp.get_latest_component_version_deployed(instance_id,system_element_id,environment_id)
            
            for comp_ver in component_version_obj:
                system_element_components['component_version'] = comp_ver
                if comp_ver['component']['component_id'] in component_version_ids['component_ids']:
                    comp_ver_obj = component_version_ids['component_version_dic'][comp_ver['component']['component_id']]
                    system_element_components['component_version']['component_version_name'] = comp_ver_obj.component_version_name
                    system_element_components['component_version']['source_code_repository_url'] = comp_ver_obj.source_code_repository_url
                    system_element_components['component_version']['source_tag_reference'] = comp_ver_obj.source_tag_reference
                    system_element_components['component_version']['artefact_store_url'] = comp_ver_obj.artefact_store_url
                    system_element_components['component_version']['artefact_store_type']['artefact_store_type_desc'] = comp_ver_obj.artefact_store_type.artefact_store_type_desc
                    system_element_components['deployment_component'] = 'Completed'

            system_element_componentrow['system_element_components'] = system_element_components

            resp_data.append(system_element_componentrow)
        return jsonify(resp_data)