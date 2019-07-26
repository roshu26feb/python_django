'''
Created on 20 April 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class UserRoleModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for user_role table and\
     methods for retrieving and saving the records into user_role table.

    '''
    __tablename__ = 'user_role'

    user_role_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "user_role_id": self.user_role_id,
            "role": self.role.json(),
        }
