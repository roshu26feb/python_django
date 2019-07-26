'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class DeploymentTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for deployment table and\
     methods for retrieving and saving the records into deployment table.

    '''
    __tablename__ = 'deployment_type'

    deployment_type_id = db.Column(db.Integer, primary_key=True)
    deployment_type_description = db.Column(db.String(255))
    components = db.relationship(
        'ComponentModel', backref='deployment_type', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup deployment from database, based on provided deployment_type_id
        '''
        deployment = cls.query.filter_by(deployment_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            deployment, "Deployment", _id)
        return deployment

    @classmethod
    def find_by_description(cls, name):
        '''
        This method is used to lookup deployment from database, based on provided deployment_type_description
        '''
        deployment = cls.query.filter_by(
            deployment_type_description=name).first()
        return deployment

    def save_to_db(self):
        '''
        This method save Deployment record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.deployment_type_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "deployment_type_id": self.deployment_type_id,
            "deployment_type_description": self.deployment_type_description,
        }
