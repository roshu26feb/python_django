'''
Created on 6 Mar 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ParameterValueModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for parameter_value table and\
     methods for retrieving and saving the records into parameter_value table.

    '''
    __tablename__ = 'parameter_value'

    parameter_value_id = db.Column(db.Integer, primary_key=True)
    parameter_value = db.Column(db.String(255))
    parameter_id = db.Column(
        db.Integer, db.ForeignKey('parameter.parameter_id'))

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup parameter_value from database, based on provided parameter_value_id
        '''
        parameter = cls.query.filter_by(parameter_value_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            parameter, "parameter", _id)
        return parameter

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup parameter from database, based on provided parameter_value
        '''
        parameter_value = cls.query.filter_by(parameter_value=name).first()
        return parameter_value

    def save_to_db(self):
        '''
        This method save parameter record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        json_p_values = {
            "parameter_value_id": self.parameter_value_id,
            "parameter_value": self.parameter_value,
            "parameter_id": self.parameter_id,
        }
        return json_p_values
