'''
Created on 21 May 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class HostSiteModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for host_site table and\
     methods for retrieving and saving the records into host_site table.

    '''
    __tablename__ = 'host_site'

    host_site_id = db.Column(db.Integer, primary_key=True)
    host_site_name = db.Column(db.String(255))
    host_site_description = db.Column(db.String(255))
    host_region_id = db.Column(db.Integer, db.ForeignKey(
        'host_region.host_region_id'))
    network_sets = db.relationship(
        'NetworkSetModel',
        backref='host_site',
        lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup host_site from database, based on provided host_site_id
        '''
        host_site = cls.query.filter_by(host_site_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            host_site, "HostSite", _id)
        return host_site

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup host_site from database, based on provided host_site
        '''
        host_site = cls.query.filter_by(host_site_name=name).first()
        return host_site

    def save_to_db(self):
        '''
        This method save HostSite record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self
    
    @staticmethod
    def get_hsv_host_sites():
        '''
        get list of host sites to show on list of host sites screen 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select hs.host_site_id, hs.host_site_name, hs.host_site_description, hs.host_region_id, hr.host_region_name, hr.host_region_description from host_site hs join host_region hr on hs.host_region_id = hr.host_region_id order by hs.host_site_id desc;")
        for row in result:
            data.append(row)
        return data

    def json(self, detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        host_site_json = {
            "host_site_id": self.host_site_id,
            "host_site_name": self.host_site_name,
            "host_site_description": self.host_site_description,
        }
        if detail_required:
            host_site_json["host_region"] = self.host_region.json(
                host_site=False, host_subscriptions=False)
        return host_site_json
