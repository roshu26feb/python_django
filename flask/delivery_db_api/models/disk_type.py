'''
Created on 1 December 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel


class DiskTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for disk_type table and\
     methods for retrieving and saving the records into disk_type table.

    '''
    __tablename__ = 'disk_type'

    disk_type_id = db.Column(db.Integer, primary_key=True)
    disk_type_description = db.Column(db.String(255))
    min_size = db.Column(db.Integer)
    max_size = db.Column(db.Integer)
    host_type_id = db.Column(db.Integer,
                             db.ForeignKey('host_type.host_type_id'))
    instance_disks = db.relationship(
        'InstanceDiskModel',
        backref='disk_type',
        lazy=True)

    def save_to_db(self):
        '''
        This method save Disk Type record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.disk_type_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "disk_type_id": self.disk_type_id,
            "disk_type_description": self.disk_type_description,
            "min_size": self.min_size,
            "max_size": self.max_size,
            "host_type_id": self.host_type_id
        }
