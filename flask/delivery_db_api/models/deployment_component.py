'''
Created on 29 May 2018

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class DeploymentComponentModel(db.Model, AbstractModel):
    '''
    This model class defines the database mapping for deployment_component table and\
     methods for retrieving and saving the records into deployment_component table.

    '''
    __tablename__ = 'deployment_component'

    deployment_component_id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey(
        'deployment.deployment_id'))
    system_element_component_id = db.Column(db.Integer, db.ForeignKey(
        'system_element_component.system_element_component_id'))
    deployment_component_status_id = db.Column(
        db.Integer, db.ForeignKey('status.status_id'))

    def save_to_db(self):
        '''
        This method saves system_element_component record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.deployment_component_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        release_dict = {
            "deployment_component_id": self.deployment_component_id,
            "deployment_id": self.deployment_id,
            "system_element_component": self.system_element_component.json(),
            "deployment_component_status": self.status.json()
        }
        return release_dict
