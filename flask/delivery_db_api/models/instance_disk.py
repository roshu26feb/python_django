'''
Created on 1 December 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db


class InstanceDiskModel(db.Model):
    '''
    This model class defines the database mapping for disk_type table and\
     methods for retrieving and saving the records into disk_type table.

    '''
    __tablename__ = 'instance_disk'

    instance_disk_id = db.Column(db.Integer, primary_key=True)
    disk_size = db.Column(db.Integer)
    disk_size_type = db.Column(db.String(10))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.instance_id'))
    disk_type_id = db.Column(db.Integer,
                             db.ForeignKey('disk_type.disk_type_id'))

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "instance_disk_id": self.instance_disk_id,
            "instance_id": self.instance_id,
            "disk_size": self.disk_size,
            "disk_size_type": self.disk_size_type,
            "disk_type": self.disk_type.json(),
        }
