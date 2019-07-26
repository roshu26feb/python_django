'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class HostTypeModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for host table and\
     methods for retrieving and saving the records into host table.

    '''
    __tablename__ = 'host_type'

    host_type_id = db.Column(db.Integer, primary_key=True)
    host_name = db.Column(db.String(255))
    infrastructure_templates = db.relationship(
        'InfrastructureTemplateModel', backref='host_type', lazy=True)
    disk_types = db.relationship(
        'DiskTypeModel',
        backref='host_type',
        lazy=True)
    host_regions = db.relationship(
        'HostRegionModel',
        backref='host_type',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup host from database, based on provided host_type_id
        '''
        host = cls.query.filter_by(host_type_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(host, "Host", _id)
        return host

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup host from database, based on provided host_name
        '''
        host = cls.query.filter_by(host_name=name).first()
        return host

    def save_to_db(self):
        '''
        This method save Host record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.host_type_id

    def json(self, details_required=True, host_region=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        host_type_json = {
            "host_type_id": self.host_type_id,
            "host_name": self.host_name,
        }

        if details_required:
            if host_region:
                host_type_json["host_regions"] = list(
                    map(lambda x: x.json(host_type=False), self.host_regions))
                host_type_json["infrastructure_templates"] = list(
                    map(lambda x: x.json(detail_required=False), self.infrastructure_templates))
                host_type_json["disk_types"] = list(
                    map(lambda x: x.json(), self.disk_types))

        return host_type_json
