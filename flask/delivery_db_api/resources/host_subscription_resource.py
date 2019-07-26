'''
Created on 21 May 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask_restful import reqparse, Resource
from flask.globals import request
from delivery_db_api.models.host_subscription import HostSubscriptionModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class HostSubscription(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system element type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('host_subscription_id', type=int, required=False)
        parser.add_argument('host_subscription_key', type=str, required=False)
        parser.add_argument(
            'host_subscription_description',
            type=str,
            required=False)
        parser.add_argument('host_region_id', type=int, required=False)
        parser.add_argument('system_network_set_id', type=int, required=False)
        parser.add_argument(
            'environment_subscription_type_id',
            type=int,
            required=False)
        parser.add_argument('environment_type_id', type=int, required=False)

    def get_model(self):
        return HostSubscriptionModel

    @authenticate
    def post(self):
        '''
        This method creates host_subscription store type in the delivery database
        '''
        request_data = request.get_json()
        host_subscription_key = request_data["host_subscription_key"]
        host_subscription_description = request_data["host_subscription_description"]
        host_region_id = request_data["host_region_id"]
        system_network_set_id = request_data.get("system_network_set_id", None)
        environment_subscription_type_id = request_data.get(
            "environment_subscription_type_id", None)
        environment_type_id = request_data.get("environment_type_id", None)
        if HostSubscriptionModel.find_by_name(
                host_subscription_key) is not None:
            return return_object_already_exist_errr(
                "host_subscription", "host_subscription_key:", host_subscription_key)
        host_subscription = HostSubscriptionModel(
            host_subscription_key=host_subscription_key,
            host_subscription_description=host_subscription_description,
            host_region_id=host_region_id,
            system_network_set_id=system_network_set_id,
            environment_subscription_type_id=environment_subscription_type_id,
            environment_type_id=environment_type_id)
        return {
            "host_subscription_id": host_subscription.save_to_db().host_subscription_id}

class HostSubscriptionList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Host Subscriptions 
        '''
        host_sub_list = HostSubscriptionModel.get_hsv_host_subscriptions()
        return_data = []
        for data in host_sub_list:
            json_data = {
                'hostSubscriptionId' : data[0],
                'hostSubscriptionKey' : data[1],
                'hostSubscriptionDescription' : data[2],
                'hostRegionId' : data[3],
                'hostRegionDescription' : data[4],
                'systemNetworkSetId' : data[5],
                'systemNetworkSetName' : data[6],
                'environmentSubscriptionTypeId' : data[7],
                'environmentSubscriptionTypeName' : data[8],
                'environmentTypeId' : data[9],
                'environmentTypeName' : data[10]
            }
            return_data.append(json_data)
        return jsonify(return_data)
