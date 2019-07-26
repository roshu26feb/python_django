'''
Created on 08 Feb 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel


class DeploymentParameterModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for deployment_parameter table and\
     methods for retrieving and saving the records into deployment_parameter table.

    '''
    __tablename__ = 'deployment_parameter'

    deployment_parameter_id = db.Column(db.Integer, primary_key=True)
    deployment_parameter_value = db.Column(db.Text(65000))
    parameter_id = db.Column(db.Integer, db.ForeignKey(
        'parameter.parameter_id'))
    deployment_id = db.Column(db.Integer, db.ForeignKey(
        'deployment.deployment_id'))

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        return{
            "deployment_parameter_id": self.deployment_parameter_id,
            "deployment_parameter_value": self.deployment_parameter_value,
            "parameter": self.parameter.json()
        }
