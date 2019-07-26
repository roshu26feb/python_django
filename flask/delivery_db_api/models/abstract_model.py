'''
Created on 25 Oct 2017

@author: neeraj.mahajan
'''
from delivery_db_api.exception import ObjectNotFound


class AbstractModel:
    '''
    Abstract model class for defining common methods
    '''
    @classmethod
    def find_generic(cls, **kwargs):
        '''
        This method is used to lookup component type from database, based on provided parameters
        '''
        model_type = cls.query.filter_by(**kwargs).all()
        if not model_type:
            raise ObjectNotFound(
                {'message': "No {} found.".format(cls.__name__).replace('Model', '')})
        return model_type
