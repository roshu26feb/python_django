'''
Created on 2 Feb 2018

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ReleaseVersionModel(db.Model, AbstractModel):
    '''
        This model class defines the database mapping for release_version table and\
        methods for retrieving and saving the records into host table.

    '''
    __tablename__ = 'release_version'

    release_version_id = db.Column(db.Integer, primary_key=True)
    release_version_name = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)
    target_release_date = db.Column(db.DateTime)
    remarks = db.Column(db.String(255))
    release_id = db.Column(db.ForeignKey('release.release_id'))
    release_version_status_id = db.Column(db.ForeignKey('status.status_id'))
    release_items = db.relationship(
        'ReleaseItemModel', backref='release_version', lazy=True)

    def json(self, release=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        release_version_json = {
            "release_version_id": self.release_version_id,
            "release_version_name": self.release_version_name,
            "creation_date": self.creation_date,
            "target_release_date": self.target_release_date,
            "remarks": self.remarks,
            "release_version_status": self.status.json(),
            "release_items": list(map(lambda x: x.json(), self.release_items))
        }
        if release:
            release_version_json["release"] = self.release.json()
        return release_version_json

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup release_version from database, based on provided release_version_id
        '''
        release_version = cls.query.filter_by(release_version_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            release_version, "Release", _id)
        return release_version

    @classmethod
    def check_if_release_exist(cls, release_id, name):
        '''
        This method is if release_version already exist in the DB
        '''
        release_version = cls.query.filter_by(
            release_id=release_id, release_version_name=name).first()
        return True if release_version is not None else False

    @classmethod
    def get_identifier(cls):
        return cls.release_version_id

    def save_to_db(self):
        '''
        This method save Instance record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.release_version_id
