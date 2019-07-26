'''
Created on 29 Jan 2018

@author: neeraj.mahajan
'''
import ast

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.models.status import StatusModel
from delivery_db_api.models.system_element_component import SystemElementComponentModel


class SystemElementModel(db.Model, AbstractModel):
    '''
    This class defined the SystemElement model which represent the SystemElement table.
    '''

    __tablename__ = 'system_element'

    system_element_id = db.Column(db.Integer, primary_key=True)
    system_element_name = db.Column(db.String(255))
    system_element_short_name = db.Column(db.String(7))
    system_id = db.Column(
        db.Integer,
        db.ForeignKey('system.system_id'),
        nullable=False)
    system_element_type_id = db.Column(db.Integer, db.ForeignKey(
        'system_element_type.system_element_type_id'))
    system_element_components = db.relationship(
        'SystemElementComponentModel', backref='system_element', lazy=True)
    deployments = db.relationship('DeploymentModel',
                                  backref='system_element',
                                  lazy=True)

    @classmethod
    def get_identifier(cls):
        return cls.system_element_id

    @staticmethod
    def get_latest_version_deployed(instance_id, system_element_id, env_id):
        '''
        This method is used to lookup latest_version_deployed
        '''
        kwargs = {
            'status_description': 'Completed',
            'status_type': "Deployment"
        }
        defined_components_count, deployed_components_count = 0, 0
        deployed_system_version = ""
        system_version_id = []
        status_id = 4
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "SELECT system_version_id,count(*) FROM system_element_component WHERE system_element_component_id IN (SELECT dc.system_element_component_id FROM deployment d JOIN deployment_component dc ON (d.deployment_id=dc.deployment_id AND d.instance_id={} AND d.system_element_id={} and d.environment_id={} AND dc.deployment_component_status_id={})) GROUP BY system_version_id ORDER BY system_version_id DESC LIMIT 2;".format(
                instance_id,
                system_element_id,
                env_id,
                status_id))       
        for row in result:
            system_version_id.append(row[0])
            
        if len(system_version_id) > 0:
            defined_components_count = SystemElementComponentModel.get_component_count_by_system_element_and_version(
                system_element_id, system_version_id[0])
            deployed_components = SystemElementComponentModel.get_latest_component_version_deployed(
                instance_id, system_element_id, env_id)
            if (set(defined_components_count) <= set(deployed_components['component_version_ids'])): 
                deployed_system_version = system_version_id[0]
            elif len(system_version_id) > 1:
                deployed_system_version = system_version_id[1]
        return {"system_version_id": deployed_system_version}

    def save_to_db(self):
        '''
        This method save SystemElement record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(
            self,
            instances_detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        system_element_json = {
            "system_element_id": self.system_element_id,
            "system_element_name": self.system_element_name,
            "system_element_short_name": self.system_element_short_name,
            "system_element_type": self.system_element_type.json()
        }
        system_element_json["system"] = self.system.json(
            system_version_required=False)
        if instances_detail_required is True:
            instance_set = set()
            for deployment in self.deployments:
                instance = deployment.instance      
                if instance is not None:
                    instance_dict = {
                        "instance_id": instance.instance_id,
                        "assigned_ip": instance.assigned_ip,
                        "instance_name": instance.instance_name,
                        "host_instance_name": instance.host_instance_name,
                        "instance_state":instance.instance_state,
                        "environment_id":deployment.environment_id,
						"system_version_id":deployment.system_version_id,
                        #"deployment_status":deployment_status
                        }
                    instance_set.add(str(instance_dict))

            instances = [ast.literal_eval(instance)
                         for instance in instance_set]
            system_element_json["instances"] = instances
        return system_element_json
