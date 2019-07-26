'''
Created on 18 Sept 2018

@author: bharat.rathod
'''
from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils
from delivery_db_api.models.instance import InstanceModel

class InstanceAllocationModel(db.Model, AbstractModel):
    '''
      This model class defines the database mapping for Instance and Enviornment table and\
      methods for retrieving and saving the records into InstanceAllocation table.
    '''
    __tablename__ = 'instance_allocation'

    instance_allocation_id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(db.Integer,
                               db.ForeignKey('environment.environment_id'))
    system_id = db.Column(db.Integer, db.ForeignKey(
        'system.system_id'))
    system_element_id = db.Column(
        db.Integer, db.ForeignKey('system_element.system_element_id'))
    #system_version_id = db.Column(db.Integer,
    #                           db.ForeignKey('system_version.system_version_id'))
    instance_id = db.Column(db.Integer,
                            db.ForeignKey('instance.instance_id'))

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup Instance Allocation id from database,
        based on provided instance_allocation_id
        '''
        instance_allocation = cls.query.filter_by(instance_allocation_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            instance_allocation, "InstanceAllocation", _id)
        return instance_allocation

    def save_to_db(self):
        '''
        This method  save Instance Allocation details to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_identifier(cls):
        return cls.instance_allocation_id

    def json(self):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        instance_allocation_dict = {
            "instance_allocation_id": self.instance_allocation_id
        }
        # instance_allocation_dict["system"] = self.system_id.json(system_version_required=False)
        # instance_allocation_dict["system_element"] = self.system_element_id.json(
        #     instances_detail_required=False)
        # instance_allocation_dict["environment"] = self.environment.json(
        #     instance_required=False, system_required=False)
        instance_allocation_dict["instance"] = list(map(lambda x: x.json(),InstanceModel.query.filter_by(instance_id=self.instance_id)))
        
        
        return instance_allocation_dict
