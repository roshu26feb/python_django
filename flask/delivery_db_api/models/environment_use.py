'''
Created on 03 April 2018

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class EnvironmentUseModel(db.Model, AbstractModel):
    ''' This class defines the data model for environment_use and provides method to store and retrieve data from database'''

    __tablename__ = 'environment_use'

    environment_use_id = db.Column(db.Integer, primary_key=True)
    environment_use_name = db.Column(db.String(255))
    environment_use_short_name = db.Column(db.String(255))
    route_to_live = db.relationship(
        'RouteToLiveModel', backref='environment_use', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup environment_use from database, based on provided instance_id
        '''
        instance = cls.query.filter_by(environment_use_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            instance, "Environment", _id)
        return instance

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup Environment from database, based on provided infra_template_id
        '''
        return cls.query.filter_by(environment_use_name=name).first()

    @classmethod
    def get_identifier(cls):
        return cls.environment_use_id

    def save_to_db(self):
        '''
        This method save Environment record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.environment_use_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        environment_use_json = {
            "environment_use_id": self.environment_use_id,
            "environment_use_name": self.environment_use_name,
            "environment_use_short_name": self.environment_use_short_name,
        }
        return environment_use_json
