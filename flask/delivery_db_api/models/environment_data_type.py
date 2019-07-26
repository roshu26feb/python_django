'''
Created on 5 Apr 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class EnvironmentDataTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for EnvironmentDataType table and\
     methods for retrieving and saving the records into host table.
    '''
    __tablename__ = 'environment_data_type'
    environment_data_type_id = db.Column(db.Integer, primary_key=True)
    environment_data_type_name = db.Column(db.String(255))
    environment_datatypes = db.relationship(
        'EnvironmentModel',
        backref='environment_data_type',
        lazy=True)

    @classmethod
    def get_identifier(cls):
        return cls.environment_data_type_id

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup environment_data_type from database, based on provided environment_data_type_id
        '''
        environment_data_type = cls.query.filter_by(
            environment_data_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            environment_data_type, "Environment Data Type", _id)
        return environment_data_type

    @classmethod
    def find_by_env_data_type_name(cls, name):
        '''
        This method is used to lookup environment_data_type from database, based on provided environment_data_type_id
        '''
        environment_data_type = cls.query.filter_by(
            environment_data_type_name=name).first()
        return environment_data_type

    def save_to_db(self):
        '''
        This method save component_type record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.environment_data_type_id

    def json(self, detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "environment_data_type_id": self.environment_data_type_id,
            "environment_data_type_name": self.environment_data_type_name,
        }
