'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ComponentTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for ComponentType table and\
     methods for retrieving and saving the records into host table.
    '''
    __tablename__ = 'component_type'
    component_type_id = db.Column(db.Integer, primary_key=True)
    component_type_description = db.Column(db.String(255))
    components = db.relationship(
        'ComponentModel',
        backref='component_type',
        lazy=True)
    parameters = db.relationship(
        'ParameterModel',
        backref='component_type',
        lazy=True)

    @classmethod
    def get_identifier(cls):
        return cls.component_type_id

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup component_type from database, based on provided component_type_id
        '''
        component_type = cls.query.filter_by(component_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            component_type, "Component Type", _id)
        return component_type

    @classmethod
    def find_by_description(cls, description):
        '''
        This method is used to lookup component_type from database, based on provided component_type_id
        '''
        component_type = cls.query.filter_by(
            component_type_description=description).first()
        return component_type

    def save_to_db(self):
        '''
        This method save component_type record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def delete(cls, component_type_id):
        '''
        This method deletes component_type record from the database
        '''
        component_type = cls.query.filter_by(
            component_type_id=component_type_id).first()
        if component_type is None:
            return {"message": "No component type found in the database"}, 400
        elif len(component_type.components) == 0:
            db.session.delete(component_type)
            db.session.commit()
            return {"message": "component_type deleted successfully"}, 200
        else:
            return {
                "message": "Cannot delete component_type because it is already in use"}, 400

    def json(self, relationship_details=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "component_type_id": self.component_type_id,
            "component_type_description": self.component_type_description,
        }
