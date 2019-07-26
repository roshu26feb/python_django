'''
Created on 19 Oct 2017

@author: neeraj.mahajan
'''
import os


def get_mysql_url():
    '''
    Builds the URL for the database
    '''
    delivery_db_user = os.getenv('DELIVERY_DB_USER', 'root')
    delivery_db_password = os.getenv('DELIVERY_DB_PASSWORD', 'welcome')
    delivery_db_connection_url = os.getenv(
        'DELIVERY_DB_CONNECTION_URL',
#        'mysql+mysqlconnector://{}:{}@localhost/delivery_db_qa'.format(
#        'mysql+mysqlconnector://{}:{}@localhost/delivery_db_090319'.format(
        'mysql+mysqlconnector://{}:{}@localhost/delivery_db'.format(
#        'mysql+mysqlconnector://{}:{}@localhost/delivery_db_qa_220319'.format(
            delivery_db_user,
            delivery_db_password))
    return delivery_db_connection_url


class AppConfig:
    '''
    Builds database config
    '''

    def __init__(self, testing, database_uri, check_modification):
        '''
        Constructor
        '''
        self.config = {
            "TESTING": os.getenv('DELIVERY_DB_TESTING_PROFILE', testing),
            "SQLALCHEMY_DATABASE_URI": database_uri,
            "SQLALCHEMY_TRACK_MODIFICATIONS": check_modification
        }

    @classmethod
    def get_test_config(cls):
        return cls(True, 'sqlite://', False)

    @classmethod
    def get_prod_config(cls):
        return cls(False, get_mysql_url(), False)
