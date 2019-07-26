'''
Created on 1 Nov 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class ReleaseModel(db.Model, AbstractModel):
    '''
        This model class defines the database mapping for release table and\
        methods for retrieving and saving the records into host table.

    '''
    __tablename__ = 'release'

    release_id = db.Column(db.Integer, primary_key=True)
    release_name = db.Column(db.String(250))
    release_owner = db.Column(db.String(250))
    release_summary = db.Column(db.String(5000))
    release_versions = db.relationship(
        'ReleaseVersionModel', backref='release', lazy=True)
    routes_to_live = db.relationship(
        'RouteToLiveModel', backref='release', lazy=True)

    def __init__(
            self,
            release_name,
            release_owner,
            release_summary):
        self.release_name = release_name
        self.release_owner = release_owner
        self.release_summary = release_summary

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "release_id": self.release_id,
            "release_name": self.release_name,
            "release_owner": self.release_owner,
            "release_summary": self.release_summary,
            "release_versions": list(map(lambda x: x.json(release=False), self.release_versions)),
            "route_to_live": list(map(lambda x: x.json(), self.routes_to_live))
        }

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup release from database, based on provided release_id
        '''
        release = cls.query.filter_by(release_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            release, "Release", _id)
        return release

    @classmethod
    def check_if_release_exist(cls, name):
        '''
        This method check if release already exist in the DB
        '''
        release = cls.query.filter_by(release_name=name).first()
        return True if release is not None else False

    @classmethod
    def get_identifier(cls):
        return cls.release_id

    def save_to_db(self):
        '''
        This method save Release record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.release_id
