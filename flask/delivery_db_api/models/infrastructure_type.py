'''
Created on 20 March 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel


class InfrastructureTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for infrastructure table and\
     methods for retrieving and saving the records into infrastructure table.

    '''
    __tablename__ = 'infrastructure_type'

    infrastructure_type_id = db.Column(db.Integer, primary_key=True)
    infrastructure_type_name = db.Column(db.String(255))
    infra_templates = db.relationship(
        'InfrastructureTemplateModel',
        backref='infrastructure_type',
        lazy=True)

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup infrastructure from database, based on provided infrastructure_type_name
        '''
        infrastructure = cls.query.filter_by(
            infrastructure_type_name=name).first()
        return infrastructure

    def save_to_db(self):
        '''
        This method save Infrastructure record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.infrastructure_type_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "infrastructure_type_id": self.infrastructure_type_id,
            "infrastructure_type_name": self.infrastructure_type_name,
        }
