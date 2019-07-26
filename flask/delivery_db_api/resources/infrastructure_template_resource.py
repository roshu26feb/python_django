'''
Created on 2 Nov 2017

@author: neeraj.mahajan
'''

from flask import jsonify
from flask_restful import reqparse, Resource
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.infrastructure_template import InfrastructureTemplateModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate
from flask.globals import request

from delivery_db_api.models.infrastructure_type import InfrastructureTypeModel


class InfrastructureTemplate(AbstractResource):
    '''
    This method creates a new Infrastructure template in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('infra_template_id', type=int, required=False)
        parser.add_argument('infra_template_name', type=str, required=False)
        parser.add_argument(
            'host_template_description',
            type=str,
            required=False)
        parser.add_argument('memory_size', type=float, required=False)
        parser.add_argument('cpu', type=int, required=False)
        parser.add_argument('max_no_disk', type=int, required=False)
        parser.add_argument('host_type_id', type=int, required=False)
        parser.add_argument('infrastructure_type_id', type=int, required=False)

    def get_model(self):
        ''' Returns the model class used'''
        return InfrastructureTemplateModel

    @authenticate
    def post(self):
        '''
        This post method will get details in Json format and creates a new
        Infra template in the delivery database
        '''
        request_data = request.get_json()
        infra_type_id = request_data["infrastructure_type_id"]
        infra_template_name = request_data["infra_template_name"]
        host_type_id = request_data["host_type_id"]
        host_template_description = request_data["host_template_description"]
        search_keys = {'infrastructure_type_id': infra_type_id}
        infra_type = InfrastructureTypeModel.find_generic(**search_keys)
        if infra_type[0].infrastructure_type_name == "PaaS":
            memory_size = None
            cpu = None
            max_no_disk = None
        else:
            memory_size = request_data["memory_size"]
            cpu = request_data["cpu"]
            max_no_disk = request_data["max_no_disk"]

        infrastructure_template = InfrastructureTemplateModel(
            infra_template_name=infra_template_name,
            host_template_description=host_template_description,
            memory_size=memory_size,
            cpu=cpu,
            max_no_disk=max_no_disk,
            host_type_id=host_type_id,
            infrastructure_type_id=infra_type_id)
        search_keys = {
            "infra_template_name": infra_template_name,
            "host_type_id": host_type_id}
        try:
            if InfrastructureTemplateModel.find_generic(
                    **search_keys) is not None:
                return return_object_already_exist_errr(
                    "Infrastructure template",
                    "name:",
                    infra_template_name +
                    " with host_type_id " +
                    str(host_type_id))
        except ObjectNotFound as exception:
            return {
                "infrastructure_template_id": infrastructure_template.save_to_db()}

class InfrastructureTemplatesList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Infrastructure Templates
        '''
        itemplts_list = InfrastructureTemplateModel.get_itv_infrastructure_templates()
        return_data = []
        for data in itemplts_list:
            json_data = {
                'infraTemplateId' : data[0],
                'infraTemplateName' : data[1],
                'infrastructureTypeId' : data[2],
                'infrastructureTypeName' : data[3],
                'hostTemplateDescription' : data[4],
                'memorySize' : data[5],
                'cpu' : data[6],
                'maxNoDisk' : data[7],
                'hostTypeId' : data[8],
                'hostName' : data[9]
            }
            return_data.append(json_data)
        return jsonify(return_data)