'''
Created on 15 Aug 2017

@author: neeraj.mahajan
'''
import datetime
import re

from flask import jsonify
from flask_restful import Resource, reqparse

from delivery_db_api.exception import ObjectNotFound


def return_object_already_exist_errr(
        entity_type,
        entity_attributes,
        attributes_value):
    '''
    This method raises the Object Already exception when called
    '''
    return {'message': "Invalid Request : {} with {} {} already exist.".format(
        entity_type, entity_attributes, attributes_value)}, 400


class AbstractResource(Resource):
    '''
    This class for abstractions  '''

    def camel_to_snake(self, string_value):
        """
        Method to convert camelCase string to snake_case
        """
        _underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
        _underscorer2 = re.compile('([a-z0-9])([A-Z])')
        subbed = _underscorer1.sub(r'\1_\2', string_value)
        return _underscorer2.sub(r'\1_\2', subbed).lower()

    def get_model(self):
        ''' Abstract method to be implemented by sub class'''
        raise NotImplementedError()

    def get_resource_name(self):
        ''' Abstract method to be implemented by sub class'''
        return self.__class__.__name__

    def convert_to_date_time_type(self):
        ''' Convert string to datetime type'''
        return lambda x: datetime.datetime.strptime(
            x,
            '%Y-%m-%dT%H:%M:%S')

    def add_date_to_parser(self, parser, field_name='creation_date'):
        ''' Adding creating date to parser'''
        return parser.add_argument(
            field_name,
            type=self.convert_to_date_time_type(),
            required=False)

    def get(self):
        '''
        This method retrieves the host type from delivery database
        and returns the output in JSON format
        '''
        parser = reqparse.RequestParser()
        self.add_argument_for_parsing(parser)
        args = parser.parse_args(strict=True)
        request_parameters = {k: v for k, v in args.items() if v is not None}
        try:
            return jsonify({self.camel_to_snake(self.get_resource_name() + 's'): list(
                map(lambda x: x.json(), self.get_model().find_generic(**request_parameters)))})
        except ObjectNotFound as exception:
            return exception.message, exception.status_code
