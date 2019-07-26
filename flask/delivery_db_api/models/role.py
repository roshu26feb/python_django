'''
Created on 20 April 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class RoleModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for role table and\
     methods for retrieving and saving the records into role table.

    '''
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255))
    user_roles = db.relationship('UserRoleModel', backref='role', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup role from database, based on provided role_id
        '''
        role = cls.query.filter_by(role_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(role, "Role", _id)
        return role

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup role from database, based on provided role_name
        '''
        role = cls.query.filter_by(role_name=name).first()
        return role

    def save_to_db(self):
        '''
        This method save Role record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "role_id": self.role_id,
            "role_name": self.role_name,
        }
