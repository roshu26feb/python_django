'''
Created on 15 May 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class SystemElementTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for system_element_type table and\
     methods for retrieving and saving the records into system_element_type table.

    '''
    __tablename__ = 'system_element_type'

    system_element_type_id = db.Column(db.Integer, primary_key=True)
    system_element_type_name = db.Column(db.String(255))
    system_element_type_short_name = db.Column(db.String(50))
    system_elements = db.relationship(
        'SystemElementModel', backref='system_element_type', lazy=True)
    network_sets = db.relationship(
        'NetworkSetModel',
        backref='system_element_type',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup system_element_type from database, based on provided system_element_type_id
        '''
        system_element_type = cls.query.filter_by(
            system_element_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            system_element_type, "SystemElementType", _id)
        return system_element_type

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup system_element_type from database, based on provided system_element_type
        '''
        system_element_type = cls.query.filter_by(
            system_element_type_name=name).first()
        return system_element_type

    def save_to_db(self):
        '''
        This method save SystemElementType record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self, detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        system_element_type_json = {
            "system_element_type_id": self.system_element_type_id,
            "system_element_type_name": self.system_element_type_name,
            "system_element_type_short_name": self.system_element_type_short_name}
        return system_element_type_json
