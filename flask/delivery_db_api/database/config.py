'''
Created on 9 Oct 2017

@author: neeraj.mahajan
'''

from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_test_app():
    '''
      Convenience method to create test app for test cases
    '''
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()  # this does the binding
    return app

# you can create another app context here, say for production
