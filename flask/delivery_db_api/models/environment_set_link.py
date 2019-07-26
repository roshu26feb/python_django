'''
Created on 7 Feb 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db


class EnvironmentSetLinkModel(db.Model):
    '''
    This model class defines the database mapping for environment_set_link table and\
     methods for retrieving and saving the records into environment_set_link table.

    '''
    __tablename__ = 'environment_set_link'

    environment_set_link_id = db.Column(db.Integer, primary_key=True)
    environment_set_id = db.Column(
        db.Integer, db.ForeignKey('environment_set.environment_set_id'))
    environment_id = db.Column(db.Integer,
                               db.ForeignKey('environment.environment_id'))

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "environment": self.environment.json(),
        }
