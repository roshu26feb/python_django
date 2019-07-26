'''
Created on 5 Sep 2017

@author: neeraj.mahajan
'''
import datetime

from delivery_db_api.exception import ObjectAlreadyExists, ObjectNotFound


class DateUtils(object):
    '''
    The class is used to override the current time in test cases
    '''
    test_date = None

    def __init__(self):
        '''
        Constructor
        '''

    def get_current_date_time(self):
        '''
        This method returns the current system date
        '''
        if DateUtils.test_date is None:
            return datetime.datetime.now()
        return DateUtils.test_date

    @staticmethod
    def create_date_from_input_string(date_string):
        '''
        This method builds the date from current string or return current date if string is empty
        '''
        _date = None
        if date_string is not None:
            _date = datetime.datetime.strptime(
                date_string, "%d/%m/%y %H:%M:%S")
        else:
            _date = DateUtils().get_current_date_time()
        return _date


class ExceptionUtils:
    '''
    This class for exceptions utils
     '''
    @classmethod
    def raise_object_already_exist_exception(cls,
                                             entity_type,
                                             entity_attributes,
                                             attributes_value):
        '''
        This method raises the Object Already exception when called
        '''
        raise ObjectAlreadyExists(
            {
                'message': "Invalid Request : {} with {} {} already exist.".format(
                    entity_type,
                    entity_attributes,
                    attributes_value)})

    @classmethod
    def raise_object_not_found_exception(cls,
                                         entity_type,
                                         id):
        '''
        This method raises the Object Already exception when called
        '''
        raise ObjectNotFound(
            {'message': "{} with id {} does not exist.".format(entity_type, id)})

    @classmethod
    def raise_exception_if_object_not_found(cls, obj, entity, id):
        '''
        This method returns the current system date
        '''
        if obj is None:
            cls.raise_object_not_found_exception(entity, id)
