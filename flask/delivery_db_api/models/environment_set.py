'''
Created on 7 Feb 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel


class EnvironmentSetModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for Environment set table and\
     methods for retrieving and saving the records into Environment_set table.

    '''
    __tablename__ = 'environment_set'

    environment_set_id = db.Column(db.Integer, primary_key=True)
    environment_set_name = db.Column(db.String(255))
    environment_set_link = db.relationship(
        'EnvironmentSetLinkModel',
        backref='environment_set',
        lazy=True,
        cascade="all,delete-orphan")

    def save_to_db(self):
        '''
        This method save Environment set record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self, env_set_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        env_set_dict = {
            "environment_set_id": self.environment_set_id,
            "environment_set_name": self.environment_set_name,
        }
        if env_set_required:
            env_set_dict["environments_linked"] = list(
                map(lambda x: x.json(), self.environment_set_link))
        return env_set_dict
