'''
Created on 21 May 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class HostSubscriptionModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for host_subscription table and\
     methods for retrieving and saving the records into host_subscription table.

    '''
    __tablename__ = 'host_subscription'

    host_subscription_id = db.Column(db.Integer, primary_key=True)
    host_subscription_key = db.Column(db.String(255))
    host_subscription_description = db.Column(db.String(255))
    host_region_id = db.Column(db.Integer, db.ForeignKey(
        'host_region.host_region_id'))
    system_network_set_id = db.Column(db.Integer, db.ForeignKey(
        'system_network_set.system_network_set_id'))
    environment_subscription_type_id = db.Column(db.Integer, db.ForeignKey(
        'environment_subscription_type.environment_subscription_type_id'))
    environment_type_id = db.Column(db.Integer, db.ForeignKey(
        'environment_type.environment_type_id'))
    network_sets = db.relationship(
        'NetworkSetModel',
        backref='host_subscription',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup host_subscription from database, based on provided host_subscription_id
        '''
        host_subscription = cls.query.filter_by(
            host_subscription_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            host_subscription, "HostSubscription", _id)
        return host_subscription

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup host_subscription from database, based on provided host_subscription
        '''
        host_subscription = cls.query.filter_by(
            host_subscription_key=name).first()
        return host_subscription

    def save_to_db(self):
        '''
        This method save HostSubscription record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_hsv_host_subscriptions():
        '''
        get list of host subscriptions for list of host subscriptions screen
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select hs.host_subscription_id, hs.host_subscription_key, hs.host_subscription_description, hs.host_region_id, hr.host_region_description, hs.system_network_set_id, sns.system_network_set_name, hs.environment_subscription_type_id, est.environment_subscription_type_name, hs.environment_type_id, et.environment_type_name from host_subscription hs join host_region hr on hs.host_region_id = hr.host_region_id join system_network_set sns on hs.system_network_set_id = sns.system_network_set_id join environment_subscription_type est on hs.environment_subscription_type_id = est.environment_subscription_type_id join environment_type et on hs.environment_type_id = et.environment_type_id;")
        for row in result:
            data.append(row)
        return data

    def json(self, detail_required=True, host_region=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        host_subscription_json = {
            "host_subscription_id": self.host_subscription_id,
            "host_subscription_key": self.host_subscription_key,
            "host_subscription_description": self.host_subscription_description,
        }

        if detail_required:
            if host_region:
                host_subscription_json["host_region"] = self.host_region.json(
                    detail_required=False)
            if self.system_network_set is not None:
                host_subscription_json["system_network_set"] = self.system_network_set.json(
                    detail_required=False)
            if self.environment_subscription_type is not None:
                host_subscription_json["environment_subscription_type"] = self.environment_subscription_type.json(
                    detail_required=False)
            if self.environment_type is not None:
                host_subscription_json["environment_type"] = self.environment_type.json(
                    detail_required=False)
            host_subscription_json["network_sets"] = list(map(lambda x: x.json(
                detail_required=True, host_subscription=False), self.network_sets))
        return host_subscription_json
