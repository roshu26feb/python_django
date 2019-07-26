'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.models.system_element_component import SystemElementComponentModel
from delivery_db_api.utils import ExceptionUtils


class SystemVersionModel(db.Model, AbstractModel):
    '''
      This class defines the representation of SystemVersion entity
    '''
    __tablename__ = 'system_version'

    system_version_id = db.Column(db.Integer, primary_key=True)
    system_version_name = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)
    system_id = db.Column(db.Integer, db.ForeignKey('system.system_id'))
    system_element_component_versions = db.relationship(
        'SystemElementComponentModel',
        backref='system_version',
        lazy=True,
        cascade="all,delete-orphan")
    release_items = db.relationship(
        'ReleaseItemModel',
        backref='system_version',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup systerm version from database, based on provided system_version_id
        '''
        system_version = cls.query.filter_by(system_version_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            system_version, "System Version", _id)
        return system_version

    @classmethod
    def find_by_system_id(cls, _id):
        '''
        This method is used to lookup system_version from database, based on provided system_id
        '''
        system_version = cls.query.filter_by(system_id=_id).first()
        return system_version

    def save_to_db(self):
        '''
        This method component system record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.system_version_id

    def json(
            self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        my_dict = {
            "system_version_id": self.system_version_id,
            "system_id": self.system_id,
            "system_name": self.system.system_name,
            "system_version_name": self.system_version_name,
            "creation_date": self.creation_date
        }
        return my_dict
