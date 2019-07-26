'''
Created on 30 Mar 2019

@author: devendra.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils
from delivery_db_api.models.environment import EnvironmentModel

class EnvironmentBookingModel(db.Model, AbstractModel):
    '''
      This class defines the representation of EnvironmentBooking entity
    '''
    __tablename__ = 'environment_booking'
    environment_booking_id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(
        db.Integer, db.ForeignKey('environment.environment_id'))
    from_date = db.Column(db.DateTime)
    to_date = db.Column(db.DateTime)
    project = db.Column(db.String(255))
    contact_person = db.Column(db.String(255))
    purpose = db.Column(db.String(255))

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup environment_booking from database, based on provided environment_booking_id
        '''
        environment_booking = cls.query.filter_by(environment_booking=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            environment_booking, "environment_booking", _id)
        return environment_booking

    @classmethod
    def get_identifier(cls):
        return cls.environment_booking

    def save_to_db(self):
        '''
        This method saves environment_booking record to database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_eb_booking_clashes(environment_id, from_date, to_date):
        '''
        get list of environment bookings clashes
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute( 
            "select environment_booking_id, environment_id, from_date, to_date, project, contact_person, purpose from environment_booking where ((from_date >= '{}' AND from_date <= '{}') OR (to_date >= '{}' AND to_date <= '{}'))  and environment_id = {};".format(from_date, to_date, from_date, to_date, environment_id))
        for row in result:
            data.append(row)
        return data

    def json(self, relationship_details=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        environment_booking_dict = {
            "environmentBookingId": self.environment_booking_id,
            "environmentId": self.environment_id,
            "fromDate": self.from_date,
            "toDate": self.to_date,
            "project": self.project,
            "contactPerson": self.contact_person,
            "purpose": self.purpose
        }

        if relationship_details is False:
            return environment_booking_dict
        
        environment_booking_dict["environment"] = self.environment.json()
        return environment_booking_dict
