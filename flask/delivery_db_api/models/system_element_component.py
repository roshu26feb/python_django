'''
Created on 29 Jan 2018

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.models.component_version import ComponentVersionModel
from delivery_db_api.models.status import StatusModel

class SystemElementComponentModel(db.Model, AbstractModel):
    '''
    This class defined the SystemElementComponent model which represent the SystemElementComponent table.
    '''

    __tablename__ = 'system_element_component'

    system_element_component_id = db.Column(db.Integer, primary_key=True)
    install_order = db.Column(db.Integer)
    system_element_id = db.Column(db.Integer, db.ForeignKey(
        'system_element.system_element_id'), nullable=False)
    system_version_id = db.Column(db.Integer, db.ForeignKey(
        'system_version.system_version_id'), nullable=False)
    component_version_id = db.Column(db.Integer, db.ForeignKey(
        'component_version.component_version_id'))
    deployment_components = db.relationship('DeploymentComponentModel',
                                            backref='system_element_component',
                                            lazy=True)

    @classmethod
    def get_identifier(cls):
        return cls.system_element_component_id

    @staticmethod
    def get_component_count_by_system_element_and_version(
            system_element_id, system_version_id):
        '''
        This method is used to lookup latest_version_deployed
        '''
        component_version_ids = []
        result = db.engine.connect().execute(
            "SELECT component_version_id FROM system_element_component WHERE system_element_id={} and system_version_id={};".format(
                system_element_id, system_version_id))
        for row in result:
            component_version_ids.append(row[0])
        return component_version_ids

    @staticmethod
    def get_latest_component_version_deployed(instance_id, system_element_id, env_id):
        '''
        This method is used to lookup latest_component_version_deployed
        '''
        kwargs = {
            'status_description': 'Completed',
            'status_type': "Deployment"
        }
        component_version_ids, component_ids, component_version_dic = [], [], {}
        status_id = 4
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "SELECT component_version_id,count(*) FROM system_element_component WHERE system_element_component_id IN (SELECT dc.system_element_component_id FROM deployment d JOIN deployment_component dc ON (d.deployment_id=dc.deployment_id AND d.instance_id={} AND d.system_element_id={} and d.environment_id={} AND dc.deployment_component_status_id={})) GROUP BY component_version_id ORDER BY system_version_id;".format(
                instance_id,
                system_element_id,
                env_id,
                status_id))       
        for row in result:
            component_version_ids.append(row[0])
            comp_ver_obj = ComponentVersionModel.find_by_id(row[0])
            if comp_ver_obj:
                component_ids.append(comp_ver_obj.component_id)
                component_version_dic.update({comp_ver_obj.component_id:comp_ver_obj})
        return {"component_version_ids": component_version_ids, "component_ids":component_ids, "component_version_dic": component_version_dic} 

    def save_to_db(self):
        '''
        This method saves system_element_component record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.system_element_component_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        system_element_component_json = {
            "system_element_component_id": self.system_element_component_id,
            "system_element_id": self.system_element_id,
            "system_version_id": self.system_version_id,
            "install_order": self.install_order,
            "component_version": self.component_version.json(
            )
        }
        return system_element_component_json
