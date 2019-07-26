'''
Created on 02 Jan 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource
from delivery_db_api.models.network_set import NetworkSetModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class NetworkSet(AbstractResource):
    '''
    This class defines the handler for handing the requests related to network set resource
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('network_set_id', type=int, required=False)
        parser.add_argument('network_set_name', type=str, required=False)
        parser.add_argument('ip_range_start', type=str, required=False)
        parser.add_argument('ip_range_end', type=str, required=False)
        parser.add_argument('subnet', type=str, required=False)
        parser.add_argument('host_site_id', type=int, required=False)
        parser.add_argument('host_subscription_id', type=int, required=False)
        parser.add_argument('environment_type_id', type=int, required=False)
        parser.add_argument('system_element_type_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return NetworkSetModel

    @authenticate
    def post(self):
        '''
        This method creates a new network_set in the delivery database
        '''
        request_data = request.get_json()
        network_set_name = request_data["network_set_name"]
        ip_range_start = request_data["ip_range_start"]
        ip_range_end = request_data["ip_range_end"]
        subnet = request_data["subnet"]
        host_site_id = request_data["host_site_id"]
        host_subscription_id = request_data["host_subscription_id"]
        environment_type_id = request_data["environment_type_id"]
        system_element_type_id = request_data.get(
            "system_element_type_id", None)

        net_set_frm_db = NetworkSetModel.find_by_name(network_set_name)
        if net_set_frm_db is not None:
            return return_object_already_exist_errr(
                "Netowork set", "nework_set_name:", network_set_name)
        else:
            network_set = NetworkSetModel(
                network_set_name=network_set_name,
                ip_range_start=ip_range_start,
                ip_range_end=ip_range_end,
                subnet=subnet,
                host_site_id=host_site_id,
                host_subscription_id=host_subscription_id,
                environment_type_id=environment_type_id,
                system_element_type_id=system_element_type_id
            )
            return {"network_set_id": network_set.save_to_db()}

class NetworkSetsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all network-sets for List of network-sets Screen
        '''
        networkset_list = NetworkSetModel.get_nsv_networkset()
        return_data = []
        for data in networkset_list:
            json_data = {
                'networkSetId' : data[0],
                'networkSetName' : data[1],
                'hostSiteId' : data[2],
                'hostSiteName' : data[3],
                'environmentTypeId' : data[4],
                'environmentTypeName' : data[5],
                'systemElementTypeId' : data[6],
                'systemElementTypeName' : data[7],
                'ipRangeStart' : data[8],
                'ipRangeEnd' : data[9],
                'subnet' : data[10]
            }
            return_data.append(json_data)
        return jsonify(return_data)
