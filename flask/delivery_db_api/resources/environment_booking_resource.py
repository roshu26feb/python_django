'''
Created on 02 Apr 2019

@author: devendra.mahajan
'''
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, AbstractResource
from delivery_db_api.models.environment_booking import EnvironmentBookingModel
from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.security import authenticate
from delivery_db_api.utils import ExceptionUtils, DateUtils
from flask import jsonify
from flask.globals import request
from flask_restful import reqparse, Resource

class EnvironmentBooking(AbstractResource):
    '''
    This method creates a new EnvironmentBooking entry in the delivery database
    '''

    def add_argument_for_parsing(self, parser):
        '''Method to add arguments for validating the request'''
        parser.add_argument('environmentBookingId', type=int, required=False)
        parser.add_argument('environmentId', type=int, required=False)
        parser.add_argument('fromDate', type=self.convert_to_date_time_type(), required=False)
        parser.add_argument('toDate', type=self.convert_to_date_time_type(), required=False)
        parser.add_argument('project', type=str, required=False)
        parser.add_argument('contactPerson', type=str, required=False)
        parser.add_argument('purpose', type=str, required=False)
        self.add_date_to_parser(parser)

    def get_model(self):
        return EnvironmentBookingModel
    
    @authenticate
    def post(self):
        '''
        This post methos will get details in Json format and creates a new
        environment_booking entry in the delivery database
        '''
        request_data = request.get_json()
        #environment_booking_id = request_data["environmentBookingId"]
        environment_id = request_data["environmentId"]
        from_date = DateUtils.create_date_from_input_string(request_data.get("fromDate", None))
        to_date = DateUtils.create_date_from_input_string(request_data.get("toDate", None))
        project = request_data["project"]
        contact_person = request_data["contactPerson"]
        purpose = request_data["purpose"]

        environment_booking = EnvironmentBookingModel(
            #environment_booking_id=environment_booking_id,
            environment_id=environment_id,
            from_date=from_date,
            to_date=to_date,
            project=project,
            contact_person=contact_person,
            purpose=purpose
        )

        return {"environmentBookingId": environment_booking.save_to_db().environment_booking_id}

    @authenticate
    def put(self):
        '''
        This method updates the details of environment_booking for the changed state
        '''
        request_data = request.get_json()
        environment_booking_id = request_data["environment_booking_id"]

        try:
            environment_booking = EnvironmentBookingModel.find_by_id(environment_booking_id)

            from_date = request_data.get("from_date", None)
            if from_date is not None:
                environment_booking.from_date = from_date

            to_date = request_data.get("to_date", None)
            if to_date is not None:
                environment_booking.to_date = to_date
            
            return jsonify(environment_booking.save_to_db().json())
        except ObjectNotFound as exception:
            return exception.message, exception.status_code

class EnvironmentBookingClashes(AbstractResource):
    
    def add_argument_for_parsing(self, parser):
        parser.add_argument('environmentId', type=int, required=True)
        parser.add_argument('fromDate', type=self.convert_to_date_time_type(), required=True)
        parser.add_argument('toDate', type=self.convert_to_date_time_type(), required=True)

    def get(self):
        '''
        This method used to get the list of all environment booking clashes
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        environment_id = args['environmentId']
        from_date = args['fromDate']
        to_date = args['toDate']

        booking_clashes = EnvironmentBookingModel.get_eb_booking_clashes(environment_id, from_date, to_date)
        return_data = []
        for data in booking_clashes:
            json_data = {
                'environmentBookingId' : data[0], 
                'environmentId' : data[1],
                'fromDate' : data[2],
                'toDate' : data[3],
                'project' : data[4],
                'contactPerson' : data[5],
                'purpose' : data[6]
            }
            return_data.append(json_data)
        return jsonify(return_data)
