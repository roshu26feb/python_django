'''
Created on 4 Oct 2017

@author: neeraj.mahajan
'''
from functools import wraps
import os

from flask.globals import request


class User(object):
    '''
    This class is used to represent user entity
    '''

    def __init__(self, username, password):
        self.username = username
        self.password = password


users = []


def populate_users():
    '''
    This method reads environment variable and initialisee \
    the users in memory which will be used for authentication
    '''
    authorized_users = os.getenv('DELIVERY_DB_API_USERS', 'jenkins_master:passwd')
    if authorized_users is not None and authorized_users.strip() != '':
        authorized_users = authorized_users.split(",")
        for user in authorized_users:
            api_user = user.split(":")
            users.append(User(api_user[0], api_user[1]))


def validate_user(username, password):
    '''
      This method validates the endpoint caller user \
      information against the defined list of users
    '''
    if len(users) is 0:
        populate_users()
    for user in users:
        if user.username == username and user.password == password:
            return True
    return False


def authenticate(func):
    '''
      This is an authentication decorator that \
      would be used for authenticating endpoint callers
    '''
    @wraps(func)
    def any_name(*args, **kwargs):
        '''
          This method authenticates the endpoint caller
        '''
        auth = request.authorization
        custom_headers = {'Content-Type': 'application/json',
                          'WWW-Authenticate': 'Basic realm="Login Required"'}
        if not auth or not auth.username or not auth.password:
            return {
                "message": "Missing user authentication information"}, 400, custom_headers
        elif not validate_user(auth.username, auth.password):
            return {"message": "Invalid user credentials"}, 401, custom_headers
        return func(*args, **kwargs)
    return any_name
