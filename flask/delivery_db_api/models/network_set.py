'''
Created on 02 Jan 2018

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class NetworkSetModel(db.Model, AbstractModel):
    ''' This class defines data model for network set and provides method to
    store and retrieve data from database'''
    __tablename__ = 'network_set'

    network_set_id = db.Column(db.Integer, primary_key=True)
    network_set_name = db.Column(db.String(255))
    ip_range_start = db.Column(db.String(255))
    ip_range_end = db.Column(db.String(20))
    subnet = db.Column(db.String(2000))
    host_site_id = db.Column(db.Integer, db.ForeignKey(
        'host_site.host_site_id'))
    host_subscription_id = db.Column(db.Integer, db.ForeignKey(
        'host_subscription.host_subscription_id'))
    environment_type_id = db.Column(db.Integer, db.ForeignKey(
        'environment_type.environment_type_id'))
    system_element_type_id = db.Column(db.Integer, db.ForeignKey(
        'system_element_type.system_element_type_id'))
    instances = db.relationship(
        'InstanceModel',
        backref='network_set',
        lazy=True)
    deployments = db.relationship(
        'DeploymentModel',
        backref='network_set',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup network set id from database, based on provided network_set_id
        '''
        network_set = cls.query.filter_by(network_set_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            network_set, "NetworkSet", _id)
        return network_set

    @classmethod
    def get_identifier(cls):
        return cls.network_set_id

    def save_to_db(self):
        '''
        This method save NetworkSet record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.network_set_id

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup network set from database, based on provided network_set_name
        '''
        network_set_name = cls.query.filter_by(network_set_name=name).first()
        return network_set_name

    @staticmethod
    def get_nsv_networkset():
        '''
        get list of network-sets  
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select ns.network_set_id, ns.network_set_name, ns.host_site_id, hs.host_site_name, ns.environment_type_id, et.environment_type_name, ns.system_element_type_id,setyp.system_element_type_name, ns.ip_range_start, ns.ip_range_end, ns.subnet from network_set ns join host_site hs on ns.host_site_id = hs.host_site_id join environment_type et on ns.environment_type_id = et.environment_type_id join system_element_type setyp on ns.system_element_type_id = setyp.system_element_type_id order by ns.network_set_id desc;")
        for row in result:
            data.append(row)
        return data

    def json(
            self,
            detail_required=True,
            host_site=True,
            host_subscription=True,
            environment_type=True,
            system_element_type=True):
        '''
          This method provides Json representation of this model class
        '''
        network_set_json = {
            "network_set_id": self.network_set_id,
            "network_set_name": self.network_set_name,
            "ip_range_start": self.ip_range_start,
            "ip_range_end": self.ip_range_end,
            "subnet": self.subnet
        }
        if detail_required:
            if host_site:
                network_set_json["host_site"] = self.host_site.json(
                    detail_required=False)
            if host_subscription:
                network_set_json["host_subscription"] = self.host_subscription.json(
                    detail_required=False)
            if environment_type:
                network_set_json["environment_type"] = self.environment_type.json(
                    detail_required=False)
            if system_element_type and self.system_element_type is not None:
                network_set_json["system_element_type"] = self.system_element_type.json(
                    detail_required=False)
        return network_set_json
