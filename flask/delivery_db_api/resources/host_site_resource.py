'''
Created on 21 May 2018

@author: neeraj.mahajan
'''
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource
from delivery_db_api.models.host_site import HostSiteModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class HostSite(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system element type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('host_site_id', type=int, required=False)
        parser.add_argument('host_site_name', type=str, required=False)
        parser.add_argument('host_site_description', type=str, required=False)
        parser.add_argument('host_region_id', type=int, required=False)

    def get_model(self):
        return HostSiteModel



    @authenticate
    def post(self):
        '''
        This method creates host_site store type in the delivery database
        '''
        request_data = request.get_json()
        host_site_name = request_data["host_site_name"]
        host_site_description = request_data["host_site_description"]
        host_region_id = request_data["host_region_id"]
        if HostSiteModel.find_by_name(host_site_name) is not None:
            return return_object_already_exist_errr(
                "host_site", "host_site_name:", host_site_name)
        host_site = HostSiteModel(
            host_site_name=host_site_name,
            host_site_description=host_site_description,
            host_region_id=host_region_id)
        return {"host_site_id": host_site.save_to_db().host_site_id}

class HostSitesList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Host Sites
        '''
        host_sites = HostSiteModel.get_hsv_host_sites()
        return_data = []
        for data in host_sites:
            json_data = {
                'hostSiteId' : data[0],
                'hostSiteName' : data[1],
                'hostSiteDescription' : data[2],
                'hostRegionId' : data[3],
                'hostRegionName' : data[4],
                'hostRegionDescription' : data[5]
            }
            return_data.append(json_data)
        return jsonify(return_data)