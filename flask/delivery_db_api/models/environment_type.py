'''
Created on 9 Jan 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class EnvironmentTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for environment type table and\
     methods for retrieving and saving the records into environment type table.

    '''
    __tablename__ = 'environment_type'

    environment_type_id = db.Column(db.Integer, primary_key=True)
    environment_type_name = db.Column(db.String(255))
    environment_type_short_name = db.Column(db.String(5))
    identifier = db.Column(db.String(1))
    environment_subscription_type_id = db.Column(db.ForeignKey(
        'environment_subscription_type.environment_subscription_type_id'))
    environments = db.relationship(
        'EnvironmentModel',
        backref='environment_type',
        lazy=True)
    host_subscriptions = db.relationship(
        'HostSubscriptionModel',
        backref='environment_type',
        lazy=True)
    network_sets = db.relationship(
        'NetworkSetModel',
        backref='environment_type',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup Environment from database, based on provided environment_type_id
        '''
        envronment_type = cls.query.filter_by(environment_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            envronment_type, "Environment type", _id)
        return envronment_type

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup environment_type_id from database, based on provided host_name
        '''
        envronment_type = cls.query.filter_by(
            environment_type_name=name).first()
        return envronment_type

    def save_to_db(self):
        '''
        This method save Host record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.environment_type_id

    @staticmethod
    def get_esv_environment_types(system_id):
        '''
        get list of environment types
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select et.environment_type_id, et.environment_type_name from environment_type et join environment e on et.environment_type_id = e.environment_type_id where e.system_id = {} group by et.environment_type_id, et.environment_type_name;".format(system_id))
        for row in result:
            data.append(row)
        return data

    def json(self, detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        environment_type_json = {
            "environment_type_id": self.environment_type_id,
            "environment_type_name": self.environment_type_name,
            "environment_type_short_name": self.environment_type_short_name,
            "identifier": self.identifier,
            "environment_subscription_type": self.environment_subscription_type.json(),
        }
        # if detail_required:
        #environment_type_json["host_subscriptions"] = list(map(lambda x: x.json(detail_required=False), self.host_subscriptions))
        return environment_type_json
