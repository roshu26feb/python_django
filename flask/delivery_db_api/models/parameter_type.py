'''
Created on 09 April 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel


class ParameterTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for parameter_type table and\
     methods for retrieving and saving the records into parameter_type table.

    '''
    __tablename__ = 'parameter_type'

    parameter_type_id = db.Column(db.Integer, primary_key=True)
    parameter_type = db.Column(db.String(255))
    parameters = db.relationship(
        'ParameterModel', backref='parameter_type', lazy=True)

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup parameter from database, based on provided parameter_type
        '''
        parameter = cls.query.filter_by(parameter_type=name).first()
        return parameter

    def save_to_db(self):
        '''
        This method save Parameter Type record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.parameter_type_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "parameter_type_id": self.parameter_type_id,
            "parameter_type": self.parameter_type,
        }
