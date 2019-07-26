'''
Created on 05 April 2018

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class RouteToLiveModel(db.Model, AbstractModel):
    ''' This class defines the data model for route_to_live and provides method to store and retrieve data from database'''

    __tablename__ = 'route_to_live'

    route_to_live_id = db.Column(db.Integer, primary_key=True)
    route_to_live_order = db.Column(db.Integer)
    critical = db.Column(db.Boolean)
    release_id = db.Column(db.Integer, db.ForeignKey('release.release_id'))
    system_id = db.Column(db.Integer, db.ForeignKey('system.system_id'))
    environment_use_id = db.Column(
        db.Integer, db.ForeignKey('environment_use.environment_use_id'))
    environment_id = db.Column(db.Integer,
                               db.ForeignKey('environment.environment_id'))

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup route_to_live from database, based on provided route_to_live_id
        '''
        route_to_live = cls.query.filter_by(route_to_live_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            route_to_live, "RouteToLive", _id)
        return route_to_live

    @classmethod
    def get_identifier(cls):
        return cls.route_to_live_id

    def save_to_db(self):
        '''
        This method save Environment record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.route_to_live_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        route_to_live_json = {
            "route_to_live_id": self.route_to_live_id,
            "route_to_live_order": self.route_to_live_order,
            "critical": self.critical,
            "release_id": self.release_id,
            "system": self.system.json(),
            "environment_use": self.environment_use.json(),
            "environment": self.environment.json(
                system_version_required=False),
        }
        return route_to_live_json
