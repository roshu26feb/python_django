'''
Created on 21 May 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class HostRegionModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for host_region table and\
     methods for retrieving and saving the records into host_region table.

    '''
    __tablename__ = 'host_region'

    host_region_id = db.Column(db.Integer, primary_key=True)
    host_region_name = db.Column(db.String(255))
    host_region_description = db.Column(db.String(255))
    host_type_id = db.Column(db.Integer, db.ForeignKey(
        'host_type.host_type_id'))
    host_subscriptions = db.relationship(
        'HostSubscriptionModel',
        backref='host_region',
        lazy=True)
    host_sites = db.relationship(
        'HostSiteModel',
        backref='host_region',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup host_region from database, based on provided host_region_id
        '''
        host_region = cls.query.filter_by(host_region_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            host_region, "HostRegion", _id)
        return host_region

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup host_region from database, based on provided host_region
        '''
        host_region = cls.query.filter_by(host_region_name=name).first()
        return host_region

    @staticmethod
    def get_hrv_host_regions():
        '''
        get list of host rergions to show on list of host regions screen 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select hr.host_region_id, hr.host_region_name, hr.host_region_description, hr.host_type_id, ht.host_name from host_region hr join host_type ht on hr.host_type_id = ht.host_type_id order by hr.host_region_id desc;")
        for row in result:
            data.append(row)
        return data

    def save_to_db(self):
        '''
        This method save HostRegion record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def json(
            self,
            detail_required=True,
            host_type=True,
            host_site=True,
            host_subscriptions=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        host_region_json = {
            "host_region_id": self.host_region_id,
            "host_region_name": self.host_region_name,
            "host_region_description": self.host_region_description,
        }
        if detail_required:
            if host_type:
                host_region_json["host_type"] = self.host_type.json(
                    details_required=False)
            if host_site:
                host_region_json["sites"] = list(
                    map(lambda x: x.json(detail_required=False), self.host_sites))
            if host_subscriptions:
                host_region_json["host_subscriptions"] = list(
                    map(lambda x: x.json(host_region=False), self.host_subscriptions))
        return host_region_json
