'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class SystemModel(db.Model, AbstractModel):
    '''
      This model class defines the database mapping for System table and\
      methods for retrieving and saving the records into System table.
    '''
    __tablename__ = 'system'

    system_id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(255))
    system_short_name = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime)
    system_network_set_id = db.Column(db.Integer, db.ForeignKey(
        'system_network_set.system_network_set_id'))
    system_versions = db.relationship(
        'SystemVersionModel', backref='system', lazy=True)
    system_elements = db.relationship(
        'SystemElementModel', backref='system', lazy=True)
    environment = db.relationship(
        'EnvironmentModel', backref='system', lazy=True)
    route_to_live = db.relationship(
        'RouteToLiveModel', backref='system', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup System from database, based on provided system_id
        '''
        system = cls.query.filter_by(system_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            system, "System", _id)
        return system

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup system from database, based on provided system_name
        '''
        system = cls.query.filter_by(system_name=name).first()
        return system

    def save_to_db(self):
        '''
        This method saves system record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.system_id

    @classmethod
    def get_identifier(cls):
        return cls.system_id

    @staticmethod
    def get_sv_systems():
        '''
        get list of systems to show on systems screen 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select system_id, system_name, system_short_name from system order by system_id desc")
        for row in result:
            data.append(row)
        return data
    
    @staticmethod
    def get_eav_systems():
        '''
        get list of systems to show on environment availability screen 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select s.system_id, s.system_name, s.system_short_name from system s join environment e on s.system_id = e.system_id group by s.system_id order by s.system_name;")
        for row in result:
            data.append(row)
        return data
    
    @staticmethod
    def get_sv_system_versions(system_id):
        '''
        get list of system versions
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select system_version_id, system_version_name, creation_date from system_version where system_id= {} order by system_version_id desc;".format(system_id))
        for row in result:
            data.append(row)
        return data
    
    @staticmethod
    def get_sv_system_elements(system_id):
        '''
        get list of system elements
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select se.system_element_id, se.system_element_name, se.system_element_short_name, se.system_element_type_id, setp.system_element_type_name from system_element se join system_element_type setp on se.system_element_type_id = setp.system_element_type_id where system_id= {} order by se.system_element_id desc;".format(system_id))
        for row in result:
            data.append(row)
        return data

    @staticmethod
    def get_sv_components(system_version_id, system_element_id):
        '''
        get list of system components
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select com.component_id, com.component_name, sec.component_version_id, cv.component_version_name, com.component_short_name, com.component_type_id, ct.component_type_description,cv.artefact_store_url, cv.artefact_store_type_id, ast.artefact_store_type_desc, cv.source_code_repository_url, cv.source_tag_reference, cv.stable_flag, com.creation_date, com.deployment_type_id, dt.deployment_type_description, sec.install_order, com.linked_ci_flag from system_element_component sec join component_version cv on sec.component_version_id = cv.component_version_id join component com on cv.component_id = com.component_id join component_type ct on com.component_type_id = ct.component_type_id join artefact_store_type ast on cv.artefact_store_type_id = ast.artefact_store_type_id join deployment_type dt on com.deployment_type_id = dt.deployment_type_id where sec.system_version_id = {} and sec.system_element_id = {} order by com.component_type_id desc, install_order;".format(system_version_id, system_element_id))
        for row in result:
            data.append(row)
        return data

    def json(self, system_version_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        json_dict = {
            "system_id": self.system_id,
            "system_name": self.system_name,
            "system_short_name": self.system_short_name,
            "creation_date": self.creation_date,
            "system_network_set": self.system_network_set.json()
        }

        if system_version_required:
            json_dict["system_versions"] = list(
                map(lambda x: x.json(), self.system_versions))
        return json_dict
