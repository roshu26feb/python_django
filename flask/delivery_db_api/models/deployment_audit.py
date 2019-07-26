'''
Created on 21 Nov 2017

@author: neeraj.mahajan
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel


class DeploymentAuditModel(db.Model, AbstractModel):
    '''
      This model class defines the database mapping for DeploymentAudit table and\
      methods for retrieving and saving the records into deployment_audit table.
    '''
    __tablename__ = 'deployment_audit'
    deployment_audit_id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer,
                              db.ForeignKey('deployment.deployment_id'))
    deployment_status_id = db.Column(
        db.Integer, db.ForeignKey('status.status_id'))
    deployment_remarks = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    audit_date = db.Column(db.DateTime)

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        deployment_dict = {
            "deployment_audit_id": self.deployment_audit_id,
            "deployment_status": self.deployment_status.json(),
            "deployment_remarks": self.deployment_remarks,
            "user_name": self.user_name,
            "audit_date": self.audit_date
        }
        return deployment_dict
