'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class InstanceModel(db.Model, AbstractModel):
    '''
    This class defined the Instance model which represent the Instance table.
    '''

    __tablename__ = 'instance'

    instance_id = db.Column(db.Integer, primary_key=True)
    instance_name = db.Column(db.String(255))
    host_instance_name = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)
    last_update_date = db.Column(db.DateTime)
    instance_state = db.Column(db.String(255))
    assigned_ip = db.Column(db.String(20))
    remarks = db.Column(db.String(2000))
    infra_template_id = db.Column(db.Integer, db.ForeignKey(
        'infrastructure_template.infra_template_id'))
    method_creation_type_id = db.Column(db.Integer, db.ForeignKey(
        'method_creation_type.method_creation_type_id'))
    network_set_id = db.Column(db.Integer, db.ForeignKey(
        'network_set.network_set_id'))
    deployments = db.relationship(
        'DeploymentModel',
        backref='instance',
        lazy=True)
    instance_disks = db.relationship(
        'InstanceDiskModel',
        backref='instance',
        lazy=True)

    def __init__(
            self,
            instance_name,
            host_instance_name,
            creation_date,
            last_update_date,
            instance_state,
            assigned_ip,
            remarks,
            infra_template_id,
            method_creation_type_id,
            network_set_id):
        self.instance_name = instance_name
        self.host_instance_name = host_instance_name
        self.creation_date = creation_date
        self.last_update_date = last_update_date
        self.instance_state = instance_state
        self.assigned_ip = assigned_ip
        self.remarks = remarks
        self.infra_template_id = infra_template_id
        self.method_creation_type_id = method_creation_type_id
        self.network_set_id = network_set_id

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup host from database, based on provided instance_id
        '''
        instance = cls.query.filter_by(instance_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            instance, "Instance", _id)
        return instance

    @classmethod
    def find_by_name(cls, name, state=None):
        '''
        This method is used to lookup instance from database, based on provided instance_name
        '''
        if state is None:
            instance = cls.query.filter_by(instance_name=name).first()
        else:
            instance = cls.query.filter_by(instance_name=name, instance_state=state).first()
        return instance

    @classmethod
    def get_identifier(cls):
        return cls.instance_id

    def save_to_db(self):
        '''
        This method save Instance record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_iv_instances():
        '''
        get list of instances  
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select i.instance_id, i.instance_name, i.host_instance_name, i.assigned_ip, i.instance_state, i.method_creation_type_id, mct.description, it.host_type_id, ht.host_name, i.infra_template_id, it.host_template_description, it.infra_template_name, it.`cpu`, it.memory_size, it.max_no_disk from instance i join method_creation_type mct on i.method_creation_type_id = mct.method_creation_type_id join infrastructure_template it on i.infra_template_id = it.infra_template_id join host_type ht on it.host_type_id = ht.host_type_id where i.instance_state != 'Destroyed' order by instance_state desc, instance_id desc;")
        for row in result:
            data.append(row)
        return data
    
    @staticmethod
    def get_iv_instance_disks(instance_id):
        '''
        get list of instance disks
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select id.instance_disk_id, id.disk_size, id.disk_size_type, id.disk_type_id, dt.disk_type_description  from instance_disk id join disk_type dt on id.disk_type_id = dt.disk_type_id where id.instance_id = {};".format(instance_id))
        for row in result:
            data.append(row)
        return data

    def json(self, detail_required=True, deployment=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        instance_json = {
            "instance_id": self.instance_id,
            "instance_name": self.instance_name,
            "host_instance_name": self.host_instance_name,
            "creation_date": self.creation_date,
            "last_update_date": self.last_update_date,
            "instance_state": self.instance_state,
            "assigned_ip": self.assigned_ip,
            "remarks": self.remarks,
        }

        if detail_required is True:
            instance_json["infrastructure_template"] = self.infrastructure_template.json(
            )
            instance_json["method_creation_type"] = self.method_creation_type.json()
            if self.network_set_id is not None:
                instance_json["network_set"] = self.network_set.json()
            instance_json["instance_disks"] = list(
                map(lambda x: x.json(), self.instance_disks))
            if deployment is True:
                instance_json["deployments"] = list(
                    map(lambda x: x.json(instance=False), self.deployments))
        return instance_json
