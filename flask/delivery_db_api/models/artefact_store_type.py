'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ArtefactStoreTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for artefact_store_type table and\
     methods for retrieving and saving the records into artefact_store_type table.

    '''
    __tablename__ = 'artefact_store_type'
    artefact_store_type_id = db.Column(db.Integer, primary_key=True)
    artefact_store_type_desc = db.Column(db.String(255))
    components = db.relationship(
        'ComponentVersionModel',
        backref='artefact_store_type',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup artefact_store_type from database, based on provided artefact_store_type_id
        '''
        artefact_store_type = cls.query.filter_by(
            artefact_store_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            artefact_store_type, "Artefact Store Type", _id)
        return artefact_store_type

    @classmethod
    def find_by_description(cls, description):
        '''
        This method is used to lookup artefact_store_type from database, based on provided artefact_store_type_id
        '''
        artefact_store_type = cls.query.filter_by(
            artefact_store_type_desc=description).first()
        return artefact_store_type

    def save_to_db(self):
        '''
        This method save artefact_store_type record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.artefact_store_type_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "artefact_store_type_id": self.artefact_store_type_id,
            "artefact_store_type_desc": self.artefact_store_type_desc
        }
