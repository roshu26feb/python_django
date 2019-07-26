'''
Created on 2 Nov 2017

@author: neeraj.mahajan
'''
import os

from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.deployment import DeploymentModel
from delivery_db_api.models.instance import InstanceModel
from delivery_db_api.models.instance_disk import InstanceDiskModel
from delivery_db_api.resources.abstract_resource import AbstractResource, \
    return_object_already_exist_errr
from delivery_db_api.security import authenticate
from delivery_db_api.utils import DateUtils


class Instance(AbstractResource):
    '''
    This class defines the handler for handing the requests related to instance resource
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('instance_id', type=int, required=False)
        parser.add_argument('instance_name', type=str, required=False)
        parser.add_argument('host_instance_name', type=str, required=False)
        parser.add_argument('assigned_ip', type=str, required=False)
        parser.add_argument('infra_template_id', type=int, required=False)
        parser.add_argument('remarks', type=str, required=False)
        parser.add_argument('instance_state', type=str, required=False)
        parser.add_argument(
            'method_creation_type_id',
            type=int,
            required=False)
        parser.add_argument('network_set_id', type=int, required=False)
        self.add_date_to_parser(parser)

    def get_model(self):
        ''' Returns the model class used'''
        return InstanceModel

    @authenticate
    def post(self):
        '''
        This method creates a new instance in the delivery database
        '''
        request_data = request.get_json()
        instance_name = request_data["instance_name"]
        host_instance_name = request_data["host_instance_name"]
        assigned_ip = request_data["assigned_ip"]
        instance_state = request_data["instance_state"]
        remarks = request_data["remarks"]
        infra_template_id = request_data["infra_template_id"]
        method_creation_type_id = request_data["method_creation_type_id"]
        network_set_id = request_data.get("network_set_id", None)
        deployment_id = request_data.get("deployment_id", None)
        creation_date = DateUtils.create_date_from_input_string(
            request_data.get("creation_date", None))
        instance_disks = request_data["instance_disks"]
        if InstanceModel.find_by_name(instance_name, "UP") is not None:
            return return_object_already_exist_errr(
                "instance", "instance name:", instance_name)
        instance = InstanceModel(
            instance_name=instance_name,
            host_instance_name=host_instance_name,
            creation_date=creation_date,
            last_update_date=DateUtils().get_current_date_time(),
            assigned_ip=assigned_ip,
            instance_state=instance_state,
            remarks=remarks,
            infra_template_id=infra_template_id,
            method_creation_type_id=method_creation_type_id,
            network_set_id=network_set_id)
        instance.instance_disks = list(
            map(
                lambda x: InstanceDiskModel(
                    disk_type_id=x['disk_type_id'],
                    disk_size=x['disk_size'],
                    disk_size_type=x['disk_size_type']),
                instance_disks))
        DEPLOYMENT_PIPELINE = 2
        status_code = 200
        #if os.getenv(
        #    'DEPLOYMENT_INTEGREATED',
        #        'False') == 'True' and method_creation_type_id is DEPLOYMENT_PIPELINE:
        if deployment_id is not None:
            instance.deployments.append(
                DeploymentModel.find_by_id(deployment_id))
        #else:
        #    status_code = 400

        return {"instance_id": instance.save_to_db().instance_id}, status_code

    @authenticate
    def put(self):
        '''
        This method updates the details of an instance for the changed state
        '''
        request_data = request.get_json()
        instance_id = request_data["instance_id"]
        instance_state = request_data.get("instance_state", None)
        infra_template_id = request_data.get("infra_template_id", None)
        remarks = request_data["remarks"]
        try:
            instance = InstanceModel.find_by_id(instance_id)
            if instance.instance_state == "Destroyed":
                return ("Instance cannot be updated, This instance was destroyed on " +
                        instance.last_update_date.__str__()), 400
            if instance_state is not None:
                instance.instance_state = instance_state
            if infra_template_id is not None:
                instance.infra_template_id = infra_template_id
            instance.remarks = remarks
            instance.last_update_date = DateUtils().get_current_date_time()
            return jsonify(instance.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code


class InstanceList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all instances
        '''
        #all_instance = list(map(lambda x: x.json(), InstanceModel.query.all()))
        all_instance = [x.json(False,False) for x in InstanceModel.query.all()]
        return jsonify(all_instance)

class InstanceListWithoutDestroyed(Resource):
    
    def get(self):
        '''
        This method used to get the list of all instances
        '''
        #all_instance = list(map(lambda x: x.json(), InstanceModel.query.all()))
        all_instance = [x.json(True,False) for x in InstanceModel.query.filter(InstanceModel.instance_state != 'Destroyed')]
        return jsonify(all_instance)


class InstanceViewInstanceList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Instances for List of Instances Screen
        '''
        inst_list = InstanceModel.get_iv_instances()
        return_data = []
        for data in inst_list:
            json_data = {
                'instanceId' : data[0],
                'instanceName' : data[1],
                'hostInstanceName' : data[2],
                'assignedIp' : data[3],
                'instanceState' : data[4],
                'methodCreationTypeId' : data[5],
                'description' : data[6],
                'hostTypeId' : data[7],
                'hostName' : data[8],
                'infraTemplateId' : data[9],
                'hostTemplateDescription' : data[10],
                'infraTemplateName' : data[11],
                'cpu' : data[12],
                'memorySize' : data[13],
                'maxNoDisk' : data[14]
            }
            return_data.append(json_data)
        return jsonify(return_data)


class InstanceViewInstanceDisks(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('instanceId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all instance disks
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        instance_id = args['instanceId']
        instance_disks =  InstanceModel.get_iv_instance_disks(instance_id)
        return_data = []
        for data in instance_disks:
            json_data = {
                'instanceDiskId' : data[0], 
                'diskSize' : data[1],
                'diskSizeType' : data[2],
                'diskTypeId' : data[3],
                'diskTypeDescription' : data[4]
            }
            return_data.append(json_data)
        return jsonify(return_data)
