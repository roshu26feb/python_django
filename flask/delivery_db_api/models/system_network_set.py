'''
Created on 16 May 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class SystemNetworkSetModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for system_network_set table and\
     methods for retrieving and saving the records into system_network_set table.

    '''
    __tablename__ = 'system_network_set'

    system_network_set_id = db.Column(db.Integer, primary_key=True)
    system_network_set_name = db.Column(db.String(255))
    system_network_set_short_name = db.Column(db.String(50))
    systems = db.relationship(
        'SystemModel', backref='system_network_set', lazy=True)
    host_subscriptions = db.relationship(
        'HostSubscriptionModel',
        backref='system_network_set',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup system_network_set from database, based on provided system_network_set_id
        '''
        system_network_set = cls.query.filter_by(
            system_network_set_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            system_network_set, "LineOfBusiness", _id)
        return system_network_set

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup system_network_set from database, based on provided system_network_set
        '''
        system_network_set = cls.query.filter_by(
            system_network_set_name=name).first()
        return system_network_set

    def save_to_db(self):
        '''
        This method save LineOfBusiness record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self, detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        system_network_set_json = {
            "system_network_set_id": self.system_network_set_id,
            "system_network_set_name": self.system_network_set_name,
            "system_network_set_short_name": self.system_network_set_short_name
        }

        # if detail_required:
        #system_network_set_json["host_subscriptions"] = list(map(lambda x: x.json(detail_required=False), self.host_subscriptions))

        return system_network_set_json
