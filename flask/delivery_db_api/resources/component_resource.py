'''
Created on 2 Nov 2017

@author: neeraj.mahajan
'''
import datetime

from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.artefact_store_type import ArtefactStoreTypeModel
from delivery_db_api.models.component import ComponentModel
from delivery_db_api.models.component_type import ComponentTypeModel
from delivery_db_api.models.component_version import ComponentVersionModel
from delivery_db_api.resources.abstract_resource import \
    return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate
from delivery_db_api.utils import ExceptionUtils, DateUtils


class Component(AbstractResource):
    '''
    This method creates a new Component in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('component_id', type=int, required=False)
        parser.add_argument('component_name', type=str, required=False)
        parser.add_argument('component_short_name', type=str, required=False)
        parser.add_argument('component_type_id', type=int, required=False)
        parser.add_argument('linked_ci_flag', type=int, required=False)
        parser.add_argument('deployment_type_id', type=int, required=False)
        self.add_date_to_parser(parser)

    def get_model(self):
        return ComponentModel

    @authenticate
    def post(self):
        '''
        This post methos will get details in Json format and creates a new
        Component in the delivery database
        '''
        request_data = request.get_json()
        component_name = request_data["component_name"]
        component_short_name = request_data["component_short_name"]
        component_type_description = request_data["component_type_description"]
        linked_ci_flag = request_data.get("linked_ci_flag", 0)
        deployment_type_id = request_data["deployment_type_id"]
        creation_date = DateUtils.create_date_from_input_string(
            request_data.get("creation_date", None))
        component = ComponentModel(
            component_name=component_name,
            component_short_name=component_short_name,
            creation_date=creation_date,
            linked_ci_flag=linked_ci_flag,
            deployment_type_id=deployment_type_id,
            component_type_id=ComponentTypeModel.find_by_description
            (component_type_description).component_type_id)
        component_from_db = ComponentModel.find_by_name(component_name)

        if component_from_db is not None:
            return return_object_already_exist_errr(
                "Component name", "component_name:", component_name)
        return {"component_id": component.save_to_db().component_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of component_type for the changed state
        '''
        request_data = request.get_json()
        component_id = request_data["component_id"]
        try:
            component = ComponentModel.find_by_id(component_id)
            component_type_id = request_data.get("component_type_id", None)
            if component_type_id is not None:
                component.component_type_id = component_type_id
            return jsonify(component.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code


class ComponentVersion(AbstractResource):
    '''
    This method creates a new Component Version in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        ''' Method to add arguments required for request parsing'''
        parser.add_argument('component_version_id', type=int, required=False)
        parser.add_argument('component_version_name', type=str, required=False)
        parser.add_argument('component_id', type=int, required=False)
        parser.add_argument('artefact_store_type_id', type=int, required=False)
        parser.add_argument('source_tag_reference', type=str, required=False)
        parser.add_argument('stable_flag', type=str, required=False)
        parser.add_argument(
            'source_code_repository_url',
            type=str,
            required=False)
        parser.add_argument(
            'test_set_uri',
            type=str,
            required=False)
        parser.add_argument('stable_flag', type=str, required=False)
        parser.add_argument(
            'creation_date',
            type=self.convert_to_date_time_type(),
            required=False)

    def get_model(self):
        return ComponentVersionModel

    def post(self):
        '''
        This method creats new component version
        '''
        request_data = request.get_json()
        component_name = request_data["component_name"]
        artefact_store_type_desc = request_data["artefact_store_type_desc"]
        component_version_name = request_data["component_version_name"]
        stable_flag = request_data["stable_flag"]
        artefact_store_url = request_data["artefact_store_url"]
        source_code_repository_url = request_data["source_code_repository_url"]
        test_set_uri = request_data.get("test_set_uri", None)
        source_tag_reference = request_data["source_tag_reference"]
        creation_date_string = request_data["creation_date"]
        creation_date = datetime.datetime.strptime(
            creation_date_string, "%d/%m/%y %H:%M:%S")
        component_version = ComponentVersionModel(
            component_version_name=component_version_name,
            stable_flag=stable_flag,
            artefact_store_url=artefact_store_url,
            source_code_repository_url=source_code_repository_url,
            test_set_uri=test_set_uri,
            source_tag_reference=source_tag_reference,
            creation_date=creation_date,
            artefact_store_type_id=ArtefactStoreTypeModel.find_by_description
            (artefact_store_type_desc).artefact_store_type_id)

        component_from_db = ComponentModel.find_by_name(component_name)

        if component_from_db is not None:
            if list(
                    filter(
                        lambda x: x.component_version_name == component_version_name,
                        component_from_db.component_versions)):
                return return_object_already_exist_errr(
                    "Component Version", "component_version_name:", component_version_name)
            component_version.component = component_from_db
        else:
            try:
                ExceptionUtils.raise_exception_if_object_not_found(
                    component_from_db, "Component", component_name)
            except ObjectNotFound as exception:
                return exception.message, exception.status_code
        return {"component Version id": component_version.save_to_db()}

class ComponentsList(Resource):
    
    def get(self):
        '''
        This method used to get the list of all Components
        '''
        comp_list = ComponentModel.get_cv_components()
        return_data = []
        for data in comp_list:
            json_data = {
                'componentId' : data[0],
                'componentName' : data[1],
                'componentShortName' : data[2],
                'componentTypeId' : data[3],
                'componentTypeDescription' : data[4]
            }
            return_data.append(json_data)
        return jsonify(return_data)

class CompopnentVersionsList(Resource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('componentId', type=int, required=True)

    def get(self):
        '''
        This method used to get the list of all component versions
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        component_id = args['componentId']
        component_versions_list = ComponentModel.get_cv_component_versions(component_id)
        return_data = []
        for data in component_versions_list:
            json_data = {
                'componentVersionId' : data[0], 
                'componentVersionName' : data[1],
                'creationDate' : data[2],
                'artifactStoreUrl' : data[3],
                'artifactStoreTypeId' : data[4],
                'artifactStoreTypeDesc' : data[5],
                'sourceCodeRepositoryUrl' : data[6],
                'sourceTagReference' : data[7],
                'testSetUri' : data[8],
                'stableFlag' : data[9],
                'linkedCiFlag' : data[10],
                'deploymentTypeId' : data[11],
                'deploymentTypeDescription' : data[12]

            }
            return_data.append(json_data)
        return jsonify(return_data)