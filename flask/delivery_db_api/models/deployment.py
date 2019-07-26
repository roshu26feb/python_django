'''
Created on 1 Nov 2017

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.models.status import StatusModel
from delivery_db_api.utils import ExceptionUtils


class DeploymentModel(db.Model, AbstractModel):
    '''
      This model class defines the database mapping for Deployment table and\
      methods for retrieving and saving the records into deployment table.
    '''
    __tablename__ = 'deployment'

    deployment_id = db.Column(db.Integer, primary_key=True)
    deployment_name = db.Column(db.String(255))
    planned_deployment_date = db.Column(db.DateTime)
    deployer_name = db.Column(db.String(255))
    requested_date = db.Column(db.DateTime)
    infra_code_flag = db.Column(db.Boolean)
    infra_config_flag = db.Column(db.Boolean)
    app_flag = db.Column(db.Boolean)
    system_element_id = db.Column(
        db.Integer, db.ForeignKey('system_element.system_element_id'))
    system_version_id = db.Column(
        db.Integer, db.ForeignKey('system_version.system_version_id'))
    infra_template_id = db.Column(db.Integer, db.ForeignKey(
        'infrastructure_template.infra_template_id'))

    instance_id = db.Column(db.Integer,
                            db.ForeignKey('instance.instance_id'))
    environment_id = db.Column(db.Integer,
                               db.ForeignKey('environment.environment_id'))
    network_set_id = db.Column(db.Integer,
                               db.ForeignKey('network_set.network_set_id'))
    deployment_audit_history = db.relationship(
        'DeploymentAuditModel',
        backref='deployment',
        lazy=True)
    deployment_parameters = db.relationship(
        'DeploymentParameterModel',
        backref='deployment',
        lazy=True)
    deployment_components = db.relationship(
        'DeploymentComponentModel',
        backref='deployment',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup deployment id from database,
        based on provided deployment_id
        '''
        deployment = cls.query.filter_by(deployment_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            deployment, "Deployment", _id)
        return deployment

    @classmethod
    def check_if_deployment_exist(cls, name):
        '''
        This method is if deployment already exist in the DB
        '''
        deployment = cls.query.filter_by(deployment_name=name).first()
        return True if deployment is not None else False

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup deployment name from database
        based on provided deployment_name
        '''
        deployment = cls.query.filter_by(deployment_name=name).first()
        return deployment

    def save_to_db(self):
        '''
        This method  save deployment details to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_identifier(cls):
        return cls.deployment_id

    @staticmethod
    def get_dv_deployments():
        '''
        get list of deployments to show on deployments screen 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select da1.deployment_id, d.deployment_name, d.deployer_name, sys.system_id, sys.system_name, se.system_element_id, se.system_element_name, env.environment_id, env.environment_name, sts.status_description, d.instance_id, d.planned_deployment_date from deployment_audit da1 left join deployment_audit da2 on (da1.deployment_id = da2.deployment_id and da1.deployment_audit_id < da2.deployment_audit_id) left join `status` sts on  da1.deployment_status_id = sts.status_id join deployment d on da1.deployment_id = d.deployment_id left join environment env on d.environment_id = env.environment_id left join system sys on env.system_id = sys.system_id left join system_element se on d.system_element_id = se.system_element_id where da2.deployment_audit_id is null and status_type = 'Deployment' order by da1.deployment_audit_id desc;")
        for row in result:
            data.append(row)
        return data
    
    @staticmethod
    def get_dv_components(deployment_id):
        '''
        get list of components for deployment view
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select com.component_id, com.component_name, cv.component_version_id, cv.component_version_name, ct.component_type_id, ct.component_type_description, dt.deployment_type_id, dt.deployment_type_description, sec.install_order, sts.status_description from deployment_component dc join system_element_component sec on dc.system_element_component_id = sec.system_element_component_id join component_version cv on sec.component_version_id = cv.component_version_id join component com on cv.component_id = com.component_id join component_type ct on com.component_type_id = ct.component_type_id join deployment_type dt on com.deployment_type_id = dt.deployment_type_id left join `status` sts on  dc.deployment_component_status_id = sts.status_id where dc.deployment_id = {} and status_type = 'Deployment' order by ct.component_type_id desc, sec.install_order;".format(deployment_id))
        for row in result:
            data.append(row)
        return data

    def json(self, instance=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        deployment_dict = {
            "deployment_id": self.deployment_id,
            "deployment_name": self.deployment_name,
            "planned_deployment_date": self.planned_deployment_date,
            "requested_date": self.requested_date,
            "infra_code_flag": self.infra_code_flag,
            "infra_config_flag": self.infra_config_flag,
            "app_flag": self.app_flag,
            "infra_template_id": self.infra_template_id,
            "instance_id": self.instance_id,
            "environment_id": self.environment_id,
            "system_element_id": self.system_element_id,
            "system_version_id" : self.system_version_id
        }
        if self.deployer_name is not None:
            deployment_dict["deployer_name"] = self.deployer_name

        if self.instance_id is not None and instance is True:
            deployment_dict["instance"] = self.instance.json(deployment=False)

        deployment_dict["deployment_audit_history"] = list(
            map(lambda x: x.json(), self.deployment_audit_history))

        deployment_dict["deployment_parameters"] = list(
            map(lambda x: x.json(), self.deployment_parameters))

        deployment_dict["deployment_components"] = list(
            map(lambda x: x.json(), self.deployment_components))

        deployment_dict["system_element"] = self.system_element.json()
        deployment_dict["environment"] = self.environment.json(
            instance_required=False, system_required=False)
        if self.network_set is not None:
            deployment_dict["network_set"] = self.network_set.json()
        return deployment_dict
