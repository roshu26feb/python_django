'''
Created on 6 Mar 2018

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ParameterModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for parameter type table and\
     methods for retrieving and saving the records into parameter table.

    '''
    __tablename__ = 'parameter'

    parameter_id = db.Column(db.Integer, primary_key=True)
    parameter_name = db.Column(db.String(255))
    parameter_internal_name = db.Column(db.String(255))
    mandatory = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    parameter_type_id = db.Column(
        db.Integer, db.ForeignKey('parameter_type.parameter_type_id'))
    component_type_id = db.Column(
        db.Integer, db.ForeignKey('component_type.component_type_id'))
    component_id = db.Column(db.Integer,
                             db.ForeignKey('component.component_id'))
    component_version_id = db.Column(db.Integer, db.ForeignKey(
        'component_version.component_version_id'))
    parameter_values = db.relationship(
        'ParameterValueModel',
        backref='parameter',
        lazy=True,
        cascade="all,delete-orphan")
    deployment_parameters = db.relationship(
        'DeploymentParameterModel', backref='parameter', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup parameter from database, based on provided parameter_id
        '''
        parameter = cls.query.filter_by(parameter_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            parameter, "parameter", _id)
        return parameter

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup parameter from database, based on provided parameter_name
        '''
        parameter = cls.query.filter_by(parameter_name=name).first()
        return parameter

    def save_to_db(self):
        '''
        This method save parameter record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        json_ptype = {
            "parameter_id": self.parameter_id,
            "parameter_name": self.parameter_name,
            "parameter_internal_name": self.parameter_internal_name,
            "mandatory": self.mandatory,
            "active": self.active,
            "parameter_type": self.parameter_type.json(),
        }
        linked_item = {}
        if self.component_id is not None:
            linked_item["component"] = self.component.json(
                    component_versions_requird=False)
        elif self.component_type_id is not None:
            linked_item["component_type"] = self.component_type.json()
        
        elif self.component_version_id is not None:
            linked_item["component_version"] = self.component_version.json(
                    component_required=False)

        json_ptype["linked_element"] = linked_item

        json_ptype["parameter_values"] = list(
            map(lambda x: x.json(), self.parameter_values))
        return json_ptype
