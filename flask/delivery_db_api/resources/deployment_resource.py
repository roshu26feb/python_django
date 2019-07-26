'''
Created on 1 Nov 2017

@author: anil.kumar
'''
import datetime
import os

from flask import jsonify
from flask.globals import request
from flask_restful import Resource, reqparse
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.component_version import ComponentVersionModel
from delivery_db_api.models.component import ComponentModel
from delivery_db_api.models.deployment import DeploymentModel
from delivery_db_api.models.deployment_audit import DeploymentAuditModel
from delivery_db_api.models.deployment_component import DeploymentComponentModel
from delivery_db_api.models.deployment_parameter import DeploymentParameterModel
from delivery_db_api.resources.abstract_resource import AbstractResource, \
    return_object_already_exist_errr
from delivery_db_api.security import authenticate
from delivery_db_api.utils import DateUtils


class Deployment(AbstractResource):
    '''
    This class defines methods for the API
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('deployment_id', type=int, required=False)
        parser.add_argument('system_element_id', type=int, required=False)
        parser.add_argument('system_version_id', type=int, required=False)
        parser.add_argument('deployment_name', type=str, required=False)
        parser.add_argument('deployer_name', type=str, required=False)
        parser.add_argument('instance_id', type=int, required=False)
        parser.add_argument('environment_id', type=int, required=False)
        parser.add_argument('app_flag', type=int, required=False)
        parser.add_argument('infra_code_flag', type=int, required=False)
        parser.add_argument('infra_config_flag', type=int, required=False)
        parser.add_argument('infra_template_id', type=int, required=False)
        parser.add_argument('network_set_id', type=int, required=False)
        self.add_date_to_parser(parser, 'requested_date')

    def get_model(self):
        ''' Returns the model class used'''
        return DeploymentModel

    @authenticate
    def post(self):
        '''
        This post methos will get details in Json format and creates a new
        deployment in the delivery database
        '''
        request_data = request.get_json()
        deployment_name = request_data["deployment_name"]
        system_element_id = request_data["system_element_id"]
        system_version_id = request_data["system_version_id"]
        if DeploymentModel.check_if_deployment_exist(deployment_name):
            return return_object_already_exist_errr(
                "deployment", "name:", deployment_name)
        c_planned_deployment_date = request_data["planned_deployment_date"]
        planned_deployment_date = datetime.datetime.strptime(
            c_planned_deployment_date, "%d/%m/%y %H:%M:%S")
        c_requested_date = request_data["requested_date"]
        requested_date = datetime.datetime.strptime(
            c_requested_date, "%d/%m/%y %H:%M:%S")
        deployment_status_id = request_data["deployment_status_id"]
        deployment_remarks = request_data["deployment_remarks"]
        user_name = request_data["user_name"]
        environment_id = request_data["environment_id"]
        infra_code_flag = request_data["infra_code_flag"]
        infra_config_flag = request_data["infra_config_flag"]
        instance_id = request_data.get("instance_id", None)
        app_flag = request_data["app_flag"]
        infra_template_id = request_data["infra_template_id"]
        network_set_id = request_data.get("network_set_id", None)
        deployment_components = request_data["deployment_components"]
        if len(deployment_components) <= 0:
            return {"message": "No data provide for deployment components"}, 400

        deployment_parameters = request_data["deployment_parameters"]
        #if len(deployment_parameters) <= 0:
        #    return {"message": "No data provide for deployment parameters"}, 400

        #if not infra_code_flag and instance_id is None:
        #    return {
        #        "message": "Instance ID missing in the deployment request"}, 400
        if infra_code_flag and os.getenv(
            'DEPLOYMENT_INTEGREATED',
                'False') == 'True' and network_set_id is None:
            return {
                "message": "Network Set ID missing in the deployment request"}, 400

        deployment_model = DeploymentModel(
            deployment_name=deployment_name,
            planned_deployment_date=planned_deployment_date,
            environment_id=environment_id,
            system_element_id=system_element_id,
            system_version_id=system_version_id,
            requested_date=requested_date,
            infra_code_flag=infra_code_flag,
            infra_config_flag=infra_config_flag,
            app_flag=app_flag,
            infra_template_id=infra_template_id,
            instance_id=instance_id,
            network_set_id=network_set_id
        )
        if len(deployment_parameters) > 0:
            deployment_model.deployment_parameters = list(
                map(
                    lambda x: DeploymentParameterModel(
                        parameter_id=x['parameter_id'],
                        deployment_parameter_value=x['deployment_parameter_value']),
                    deployment_parameters))
        deployment_model.deployment_components = list(
            map(
                lambda x: DeploymentComponentModel(
                    system_element_component_id=x['system_element_component_id'],
                    deployment_component_status_id=x['deployment_component_status_id']),
                deployment_components))
        deployment_audit_model = DeploymentAuditModel(
            deployment_status_id=deployment_status_id,
            deployment_remarks=deployment_remarks,
            user_name=user_name,
            audit_date=DateUtils().get_current_date_time(),
        )

        deployment_model.deployment_audit_history.append(
            deployment_audit_model)
        return {"deployment_id": deployment_model.save_to_db().deployment_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of an deployment for the changed state
        '''
        request_data = request.get_json()
        planned_deployment_date = request_data.get(
            "planned_deployment_date", None)
        deployer_name = request_data.get("deployer_name", None)
        instance_id = request_data.get("instance_id", None)

        deployment_status_id = request_data["deployment_status_id"]
        deployment_remarks = request_data["deployment_remarks"]
        user_name = request_data["user_name"]
        deployment_id = request_data["deployment_id"]
        deployment_component_changed_status = request_data["deployment_component_changed_status"]

        try:
            deployment = DeploymentModel.find_by_id(deployment_id)

            if deployer_name is not None:
                deployment.deployer_name = deployer_name
            if planned_deployment_date is not None:
                deployment.planned_deployment_date = planned_deployment_date
            if instance_id is not None:
                deployment.instance_id = instance_id

            if deployment_component_changed_status is not None and len(
                    deployment_component_changed_status) > 0:
                for deployment_component_json in deployment_component_changed_status:
                    for deployment_component in deployment.deployment_components:
                        if deployment_component.deployment_component_id == deployment_component_json[
                                'deployment_component_id']:
                            deployment_component.deployment_component_status_id = deployment_component_json[
                                'deployment_component_status_id']

            deployment_audit_model = DeploymentAuditModel(
                deployment_status_id=deployment_status_id,
                deployment_remarks=deployment_remarks,
                user_name=user_name,
                audit_date=DateUtils().get_current_date_time()
            )
            deployment.deployment_audit_history.append(deployment_audit_model)
            return jsonify(deployment.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code


def historic_deployment_component_status(deployment_obj, component_version_ids):
    """
    Change deployment component status to historic
    """
    historic_comp_ver_objs = component_version_ids
    if historic_comp_ver_objs:
        deployment_objs = DeploymentModel.query.filter_by(environment_id=deployment_obj.environment_id,system_element_id=deployment_obj.system_element_id,instance_id=deployment_obj.instance_id).filter(DeploymentModel.deployment_id != deployment_obj.deployment_id)

        for deployment2 in deployment_objs:
            for deployment_component_obj2 in deployment2.deployment_components:
                if deployment_component_obj2 is not None:
                    deployment_component2 = deployment_component_obj2.json()
                    comp_version_id = deployment_component2["system_element_component"]["component_version"]["component_version_id"]
                    for historic_comp_ver_obj in historic_comp_ver_objs:
                        if historic_comp_ver_obj.component_version_id == comp_version_id:
                            deployment_component_obj2.deployment_component_status_id = 9
                            deployment_component_obj2.save_to_db()


class UpdateDeploymentStatus(Resource):
    '''
    This class defines methods for the API
    '''
    @authenticate
    def put(self):
        '''
        This method updates the details of an deployment for the changed state
        '''
        request_data = request.get_json()
        deployment_remarks = request_data.get("deployment_remarks", "Called from Jenkins")
        user_name = request_data.get("user_name", "admin")
        deployment_id = request_data["deployment_id"]
        deployment_component_changed_status = request_data["deployment_component_changed_status"]
        component_version_ids = []
        try:
            deployment = DeploymentModel.find_by_id(deployment_id)
            no_deploy_cmp = len(deployment_component_changed_status)
            no_deploy_cmp_success_cnt = 0
            if deployment_component_changed_status is not None and no_deploy_cmp > 0:
                for deployment_component_json in deployment_component_changed_status:
                    for deployment_component in deployment.deployment_components:
                        if deployment_component.deployment_component_id == deployment_component_json[
                                'deployment_component_id']:
                            deployment_component.deployment_component_status_id = deployment_component_json[
                                'deployment_component_status_id']
                            deployment_component_data = deployment_component.json()
                            comp_ver_objs  = ComponentVersionModel.query.filter(ComponentVersionModel.component_version_id!=deployment_component_data['system_element_component']['component_version']['component_version_id']).filter(ComponentVersionModel.component_id == deployment_component_data['system_element_component']['component_version']['component']['component_id'])
                            for comp_ver_obj in comp_ver_objs:
                                component_version_ids.append(comp_ver_obj)
                            if deployment_component_json['deployment_component_status_id'] == 4:
                                no_deploy_cmp_success_cnt = no_deploy_cmp_success_cnt + 1 

            deployment_status_id = 5
            message = "Failed"
            # To DO record into log file 
            if no_deploy_cmp == no_deploy_cmp_success_cnt :
                deployment_status_id = 4
                message = "Successful"

            deployment_audit_model = DeploymentAuditModel(
                deployment_status_id=deployment_status_id,
                deployment_remarks=deployment_remarks,
                user_name=user_name,
                audit_date=DateUtils().get_current_date_time()
            )
            deployment.deployment_audit_history.append(deployment_audit_model)
            historic_deployment_component_status(deployment, component_version_ids)

            return {"deployment_id": deployment.save_to_db().deployment_id, "message":message}
        except ObjectNotFound as exception:
            # To DO record into log file
            print (exception.message, exception.status_code)
            return {"deployment_id": "", "message":"Failed"}


class UpdateInstanceForDeployment(Resource):
    '''
    This class defines methods for the API
    '''
    @authenticate
    def put(self):
        request_data = request.get_json()
        deployment_id = request_data["deployment_id"]
        instance_id = request_data["instance_id"]
        try:
            deployment = DeploymentModel.find_by_id(deployment_id)
            deployment.instance_id = instance_id
            return {"deployment_id": deployment.save_to_db().deployment_id, "message":"Successful"}
        except ObjectNotFound as exception:
            # To DO record into log file
            print (exception.message, exception.status_code)
            return {"deployment_id": deployment_id, "message":"Failed"}


class HistoricComponentStatus(Resource):
    '''
    This class defines methods for the API
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('deployment_id', type=int, required=True)
        parser.add_argument('comp_id', type=int, required=True)
    
    def get(self):
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        deployment_id = args['deployment_id']
        comp_id  = args['comp_id']
        component_version_ids = [] 
        try:
            deployment_obj = DeploymentModel.find_by_id(deployment_id)
            for deployment_component in deployment_obj.deployment_components:
                deployment_component_data = deployment_component.json()
                if int(comp_id) == int(deployment_component_data['deployment_component_id']): 
                    comp_ver_objs  = ComponentVersionModel.query.filter(ComponentVersionModel.component_version_id!=deployment_component_data['system_element_component']['component_version']['component_version_id']).filter(ComponentVersionModel.component_id == deployment_component_data['system_element_component']['component_version']['component']['component_id'])
                    for comp_ver_obj in comp_ver_objs:
                        component_version_ids.append(comp_ver_obj)
                elif comp_id == 0:
                    comp_ver_objs  = ComponentVersionModel.query.filter(ComponentVersionModel.component_version_id!=deployment_component_data['system_element_component']['component_version']['component_version_id']).filter(ComponentVersionModel.component_id == deployment_component_data['system_element_component']['component_version']['component']['component_id'])
                    for comp_ver_obj in comp_ver_objs:
                        component_version_ids.append(comp_ver_obj)
            historic_deployment_component_status(deployment_obj, component_version_ids)
        except ObjectNotFound as exception:
            # To DO record into log file
            print (exception.message, exception.status_code)
            return { "message":"Failed"}

class DeploymentViewDeploymentsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all deployment requests
        '''
        deployments_list =  DeploymentModel.get_dv_deployments()
        return_data = []
        for data in deployments_list:
            json_data = {
                'deploymentId' : data[0], 
                'deploymentName' : data[1],
                'deployerName' : data[2],
                'systemId' : data[3],
                'systemName' : data[4],
                'systemElementId' : data[5],
                'systemElementName' : data[6],
                'environmentId' : data[7],
                'environmentName' : data[8],
                'statusDescription' : data[9],
                'instanceId' : data[10],
                'plannedDeploymentDate' : data[11]
            }
            return_data.append(json_data)
        return jsonify(return_data)

class DeploymentViewComponentsList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('deploymentId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all deployment components
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        deployment_id = args['deploymentId']
        component_list = DeploymentModel.get_dv_components(deployment_id)
        return_data = []
        for data in component_list:
            json_data = {
                'componentId' : data[0], 
                'componentName' : data[1],
                'componentVersionId' : data[2],
                'componentVersionName' : data[3],
                'componentTypeId' : data[4],
                'componentTypeDescription' : data[5],
                'deploymentTypeId' : data[6],
                'deploymentTypeDescription' : data[7],
                'installOrder' : data[8],
                'statusDescription' : data[9]

            }
            return_data.append(json_data)
        return jsonify(return_data)