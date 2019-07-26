'''
Created on 31 Oct 2017

@author: anil.kumar
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class StatusModel(db.Model, AbstractModel):
    '''
      This model class defines the database mapping for status table and\
      methods for retrieving and saving the records into Status table.
    '''
    __tablename__ = 'status'

    status_id = db.Column(db.Integer, primary_key=True)
    status_description = db.Column(db.String(255))
    status_type = db.Column(db.String(50))
    deployments = db.relationship(
        'DeploymentAuditModel',
        backref='deployment_status',
        lazy=True)
    release_versions = db.relationship(
        'ReleaseVersionModel',
        backref='status',
        lazy=True)
    deployment_components = db.relationship(
        'DeploymentComponentModel',
        backref='status',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup status_type from database, based on provided status_id
        '''
        status_id = cls.query.filter_by(status_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            status_id, "Status ID", _id)
        return status_id

    @classmethod
    def find_by_status_desc(cls, status_description):
        '''
        This method is used to lookup status_description from database, based on provided status_id
        '''
        status_desc = cls.query.filter_by(
            status_description=status_description).first()
        return status_desc

    def save_to_db(self):
        '''
        This method status record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.status_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "status_id": self.status_id,
            "status_description": self.status_description,
            "status_type": self.status_type,
        }
