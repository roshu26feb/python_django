'''
Created on 12 Sep 2017

@author: neeraj.mahajan
'''


class ObjectNotFound(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''
        Exception.__init__(self)
        self.message = message
        self.status_code = 404


class ObjectAlreadyExists(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''
        Exception.__init__(self)
        self.message = message
        self.status_code = 400
