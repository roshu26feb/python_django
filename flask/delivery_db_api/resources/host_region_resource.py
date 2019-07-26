'''
Created on 21 May 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource
from delivery_db_api.models.host_region import HostRegionModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class HostRegion(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system element type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('host_region_id', type=int, required=False)
        parser.add_argument('host_region_name', type=str, required=False)
        parser.add_argument(
            'host_region_description',
            type=str,
            required=False)
        parser.add_argument('host_type_id', type=int, required=False)

    def get_model(self):
        return HostRegionModel

    @authenticate
    def post(self):
        '''
        This method creates host_region store type in the delivery database
        '''
        request_data = request.get_json()
        host_region_name = request_data["host_region_name"]
        host_region_description = request_data["host_region_description"]
        host_type_id = request_data["host_type_id"]
        if HostRegionModel.find_by_name(host_region_name) is not None:
            return return_object_already_exist_errr(
                "host_region", "host_region_name:", host_region_name)
        host_region = HostRegionModel(
            host_region_name=host_region_name,
            host_region_description=host_region_description,
            host_type_id=host_type_id)
        return {"host_region_id": host_region.save_to_db().host_region_id}

class HostRegionsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Host Regions
        '''
        host_regions = HostRegionModel.get_hrv_host_regions()
        return_data = []
        for data in host_regions:
            json_data = {
                'hostRegionId' : data[0],
                'hostRegionName' : data[1],
                'hostRegionDescription' : data[2],
                'hostTypeId' : data[3],
                'hostName' : data[4]
            }
            return_data.append(json_data)
        return jsonify(return_data)