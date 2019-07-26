'''
Created on 22 Feb 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel


class MethodCreationTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for method_creation_type table and\
     methods for retrieving and saving the records into method_creation_type table.

    '''
    __tablename__ = 'method_creation_type'

    method_creation_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    instances = db.relationship(
        'InstanceModel', backref='method_creation_type', lazy=True)

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup method_creation_type from database, based on provided name
        '''
        method_creation_type = cls.query.filter_by(name=name).first()
        return method_creation_type

    def save_to_db(self):
        '''
        This method save MethodCreationType record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.method_creation_type_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "method_creation_type_id": self.method_creation_type_id,
            "name": self.name,
            "description": self.description
        }
