'''
Created on 1 Nov 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models import infrastructure_template
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ReleaseItemModel(db.Model, AbstractModel):
    '''This model class defines the database mapping for release item table.'''

    __tablename__ = 'release_item'
    release_item_id = db.Column(db.Integer, primary_key=True)
    release_note_url = db.Column(db.String(255))
    system_version_id = db.Column(
        db.ForeignKey('system_version.system_version_id'))
    release_version_id = db.Column(
        db.ForeignKey('release_version.release_version_id'))

    @classmethod
    def get_identifier(cls):
        return cls.release_item_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        release_dict = {
            "release_item_id": self.release_item_id,
            "release_note_url": self.release_note_url,
            "system_version": self.system_version.json(),
        }
        return release_dict
