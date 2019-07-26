'''
Created on 19 April 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class UserModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for user table and\
     methods for retrieving and saving the records into user table.

    '''
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    user_display_name = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    user_roles = db.relationship('UserRoleModel', backref='user', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup user from database, based on provided user_id
        '''
        user = cls.query.filter_by(user_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(user, "User", _id)
        return user

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup user from database, based on provided user_name
        '''
        user = cls.query.filter_by(user_name=name).first()
        return user

    def save_to_db(self):
        '''
        This method save User record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "email_address": self.email_address,
            "user_roles": list(map(lambda user_role: user_role.json(), self.user_roles))
        }
