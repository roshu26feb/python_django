'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ComponentVersionModel(db.Model, AbstractModel):
    '''
      This model class defines the database mapping for component_version table and\
      methods for retrieving and saving the records into component_version table.
    '''
    __tablename__ = 'component_version'
    component_version_id = db.Column(db.Integer, primary_key=True)
    component_version_name = db.Column(db.String(255))
    stable_flag = db.Column(db.Integer)
    artefact_store_url = db.Column(db.String(2000))
    source_code_repository_url = db.Column(db.String(2000))
    source_tag_reference = db.Column(db.String(255))
    test_set_uri = db.Column(db.String(2000))
    creation_date = db.Column(db.DateTime)
    component_id = db.Column(db.Integer,
                             db.ForeignKey('component.component_id'))
    artefact_store_type_id = db.Column(db.Integer, db.ForeignKey(
        'artefact_store_type.artefact_store_type_id'))
    system_element_components = db.relationship(
        'SystemElementComponentModel',
        backref='component_version',
        lazy=True)
    parameters = db.relationship(
        'ParameterModel',
        backref='component_version',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup component_version from database, based on provided component_version_id
        '''
        component_version = cls.query.filter_by(
            component_version_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            component_version, "component_version_id", _id)
        return component_version

    @classmethod
    def find_by_component_id(cls, _id):
        '''
        This method is used to lookup component_version from database, based on provided component_version_id
        '''
        component_version = cls.query.filter_by(component_id=_id).first()
        return component_version

    @classmethod
    def find_by_id_version(cls, _id, version):
        '''
        This method is used to lookup component_version from database, based on provided component_version_id
        '''
        component_version = cls.query.filter_by(
            component_id=_id, component_version_name=version).first()
        return component_version

    def save_to_db(self):
        '''
        This method save component_version record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.component_version_id

    def json(self, component_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        comp_ver_dict = {
            "component_version_id": self.component_version_id,
            "component_version_name": self.component_version_name,
            "stable_flag": self.stable_flag,
            "artefact_store_url": self.artefact_store_url,
            "source_code_repository_url": self.source_code_repository_url,
            "test_set_url": self.test_set_uri,
            "source_tag_reference": self.source_tag_reference,
            "creation_date": self.creation_date,
            "artefact_store_type": self.artefact_store_type.json(),
            #"component": self.component.json() if component_required else '',
        }
        if component_required:
            comp_ver_dict["component"] = self.component.json(
                component_versions_requird=False)

        return comp_ver_dict
