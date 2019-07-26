'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.models.component_type import ComponentTypeModel
from delivery_db_api.models.deployment import DeploymentModel
from delivery_db_api.models.component_version import ComponentVersionModel
from delivery_db_api.utils import ExceptionUtils


class ComponentModel(db.Model, AbstractModel):
    '''
      This class defines the representation of Component entity
    '''
    __tablename__ = 'component'
    component_id = db.Column(db.Integer, primary_key=True)
    component_name = db.Column(db.String(255))
    component_short_name = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)
    linked_ci_flag = db.Column(db.Boolean)
    component_type_id = db.Column(
        db.Integer, db.ForeignKey('component_type.component_type_id'))
    deployment_type_id = db.Column(
        db.Integer, db.ForeignKey('deployment_type.deployment_type_id'))
    component_versions = db.relationship(
        'ComponentVersionModel', backref='component', lazy=True)
    parameters = db.relationship(
        'ParameterModel',
        backref='component',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup component from database, based on provided component_id
        '''
        component = cls.query.filter_by(component_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            component, "component_id", _id)
        return component

    @classmethod
    def get_identifier(cls):
        return cls.component_id

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup component from database, based on provided component_name
        '''
        component = cls.query.filter_by(component_name=name).first()
        return component

    def save_to_db(self):
        '''
        This method saves component record to database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_cv_components():
        '''
        get list of components to show on components screen 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select com.component_id, com.component_name, com.component_short_name, com.component_type_id,  ct.component_type_description from component com join component_type ct on com.component_type_id = ct.component_type_id order by com.component_id desc;")
        for row in result:
            data.append(row)
        return data
    
    @staticmethod
    def get_cv_component_versions(component_id):
        '''
        get list of component versions
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select cv.component_version_id, cv.component_version_name, cv.creation_date, cv.artefact_store_url, ast.artefact_store_type_id, ast.artefact_store_type_desc, cv.source_code_repository_url, cv.source_tag_reference, cv.test_set_uri, cv.stable_flag, com.linked_ci_flag, com. deployment_type_id, dt.deployment_type_description from component_version cv join artefact_store_type ast on cv.artefact_store_type_id = ast.artefact_store_type_id join component com on cv.component_id = com.component_id join deployment_type dt on com.deployment_type_id = dt.deployment_type_id where cv.component_id= {} order by cv.component_version_id desc;".format(component_id))
        for row in result:
            data.append(row)
        return data

    def json(self, relationship_details=True, component_versions_requird=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        component_dict = {
            "component_id": self.component_id,
            "component_name": self.component_name,
            "creation_date": self.creation_date,
            "component_short_name": self.component_short_name,
            "linked_ci_flag": self.linked_ci_flag

        }
        if relationship_details is False:
            return component_dict

        component_dict["component_type"] = self.component_type.json()
        component_dict["deployment_type"] = self.deployment_type.json()
        if component_versions_requird:
            component_dict["component_versions"] = list(
                map(lambda x: x.json(False), self.component_versions))
        return component_dict


# This is the test comment for checking build - Delivery DB API