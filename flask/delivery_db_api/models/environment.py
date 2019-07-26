'''
Created on 08 Jan 2018

@author: neeraj.mahajan
'''
import ast
import json

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class EnvironmentModel(db.Model, AbstractModel):
    ''' This class defines the data model for environment and provides method to store and retrieve data from database'''

    __tablename__ = 'environment'

    environment_id = db.Column(db.Integer, primary_key=True)
    environment_name = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)
    environment_type_id = db.Column(
        db.Integer, db.ForeignKey('environment_type.environment_type_id'))
    environment_data_type_id = db.Column(db.Integer, db.ForeignKey(
        'environment_data_type.environment_data_type_id'))
    environment_set_links = db.relationship(
        'EnvironmentSetLinkModel', backref='environment', lazy=True)
    system_id = db.Column(
        db.Integer, db.ForeignKey('system.system_id'))
    deployments = db.relationship(
        'DeploymentModel', backref='environment', lazy=True)
    route_to_live = db.relationship(
        'RouteToLiveModel', backref='environment', lazy=True)
    environment_bookings = db.relationship(
        'EnvironmentBookingModel',
        backref='environment',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup environment from database, based on provided instance_id
        '''
        instance = cls.query.filter_by(environment_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            instance, "Environment", _id)
        return instance

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup Environment from database, based on provided infra_template_id
        '''
        return cls.query.filter_by(environment_name=name).first()

    @classmethod
    def get_identifier(cls):
        return cls.environment_id

    def save_to_db(self):
        '''
        This method save Environment record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.environment_id

    @staticmethod
    def get_ev_environments():
        '''
        get list of environments 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select environment_id, environment_name, environment_type_id, environment_type_name, system_id, system_name, environment_data_type_id,environment_data_type_name, ev_environment_version_name from `nev_environments`;")
        for row in result:
            data.append(row)
        return data

    @staticmethod
    def get_ev_system_elements(environment_id):
        '''
        get list of system elements 
        '''
        data = []
        sql_connection = db.engine.connect()
        #"select se.system_element_id, se.system_element_name, se.system_element_type_id, setp.system_element_type_name, sv.system_version_id, sv.system_version_name, se.system_id from system_element se join system_element_type setp on se.system_element_type_id = setp.system_element_type_id join system_version sv on se.system_id = sv.system_id join environment env on se.system_id = env.system_id where env.environment_id = {} and env.system_id = {};".format(environment_id,system_id))
        
        result = sql_connection.execute(
            "select system_element_id, system_element_name, system_element_type_id, system_element_type_name, instance_id, instance_name, assigned_ip,instance_state, system_version_id, system_version_name, system_id, ev_system_version_name from nev_system_elements where environment_id = {};".format(environment_id))
        for row in result:
            data.append(row)
        return data
        
    @staticmethod
    def get_ev_components(environment_id, system_element_id, instance_id):
        '''
        get list of components by system element & system version
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select component_id, component_name, component_version_id, component_version_name, component_short_name, component_type_id, component_type_description, artefact_store_url, artefact_store_type_id, artefact_store_type_desc, source_code_repository_url,source_tag_reference, stable_flag, creation_date, deployment_type_id, deployment_type_description, linked_ci_flag, is_deployed from nev_components where environment_id = {} and system_element_id = {} and (instance_id = {} or instance_id is null) order by component_type_id desc, install_order;".format(environment_id, system_element_id, instance_id))
        for row in result:
            data.append(row)
        return data

    @staticmethod
    def get_eav_environments(system_id):
        '''
        get list of environments by system
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select environment_id, environment_name, system_id, system_name, environment_data_type_id, environment_data_type_name, ev_environment_version_name from nev_environments where system_id = {} order by environment_name;".format(system_id))
        for row in result:
            data.append(row)
        return data

    def json(
            self,
            system_version_required=True,
            instance_required=True,
            system_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        environment_json = {
            "environment_id": self.environment_id,
            "environment_name": self.environment_name,
            "creation_date": self.creation_date,

        }

        if system_required:
            environment_json["system"] = self.system.json()
            environment_json["environment_type"] = self.environment_type.json()
            environment_json["environment_data_type"] = self.environment_data_type.json()
        if instance_required:
            instance_set = set()
            for deployment in self.deployments:
                instance = deployment.instance
                if instance is not None:
                    instance_dict = {
                        "instance_id": instance.instance_id,
                        "assigned_ip": instance.assigned_ip,
                        "instance_name": instance.instance_name,
                        "host_instance_name": instance.host_instance_name}
                    instance_set.add(str(instance_dict))

            instances = [ast.literal_eval(instance)
                         for instance in instance_set]
            environment_json["instances"] = instances

        #"release_versions": list(map(lambda x: x.json(release=False), self.release_versions)),
        return environment_json
