'''
Created on 24 Jan 2018

@author: neeraj.mahajan

Entry point module for flask api to be use by app server
'''

from delivery_db_api.app_config import AppConfig
from delivery_db_api.database.config import db
from delivery_db_api.delivery_db_rest_api_app import main


delivery_db_api_app = main(AppConfig.get_prod_config().config)
db.init_app(delivery_db_api_app)
