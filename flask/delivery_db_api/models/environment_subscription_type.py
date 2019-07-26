'''
Created on 6 Apr 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils

from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class EnvironmentSubscriptionTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for EnvironmentSubcriptionTypeModel table and\
     methods for retrieving and saving the records into host table.
    '''
    __tablename__ = 'environment_subscription_type'
    environment_subscription_type_id = db.Column(db.Integer, primary_key=True)
    environment_subscription_type_name = db.Column(db.String(255))
    environment_type = db.relationship(
        'EnvironmentTypeModel',
        backref='environment_subscription_type',
        lazy=True)
    host_subscriptions = db.relationship(
        'HostSubscriptionModel',
        backref='environment_subscription_type',
        lazy=True)

    @classmethod
    def get_identifier(cls):
        return cls.environment_subscription_type_id

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup environment_data_type from database, based on provided environment_subscription_type_id
        '''
        subcription_type = cls.query.filter_by(
            environment_subscription_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            subcription_type, "Environment Subscription type id", _id)
        return subcription_type

    @classmethod
    def find_by_env_subscription_type_name(cls, name):
        '''
        This method is used to lookup environment_data_type from database, based on provided environment_subscription_type_id
        '''
        subcription_type = cls.query.filter_by(
            environment_subscription_type_name=name).first()
        return subcription_type

    def save_to_db(self):
        '''
        This method save component_type record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.environment_subscription_type_id

    def json(self, detail_required=False):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        environment_subscription_type_json = {
            "environment_subscription_type_id": self.environment_subscription_type_id,
            "environment_subscription_type_name": self.environment_subscription_type_name,
        }
        if detail_required:
            environment_subscription_type_json["host_subscriptions"] = list(
                map(lambda x: x.json(detail_required=False), self.host_subscriptions))
        return environment_subscription_type_json
