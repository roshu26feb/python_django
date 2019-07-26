'''
Created on 16 Oct 2017

@author: neeraj.mahajan
'''

from delivery_db_api.database.config import db
from delivery_db_api.models.abstract_model import AbstractModel
from delivery_db_api.utils import ExceptionUtils


class InfrastructureTemplateModel(db.Model, AbstractModel):
    '''
      This class defines the representation of Infrastructure template entity
    '''
    __tablename__ = 'infrastructure_template'
    infra_template_id = db.Column(db.Integer, primary_key=True)
    infra_template_name = db.Column(db.String(255))
    host_template_description = db.Column(db.String(255))
    memory_size = db.Column(db.Float)
    cpu = db.Column(db.Integer)
    max_no_disk = db.Column(db.Integer)
    host_type_id = db.Column(db.Integer,
                             db.ForeignKey('host_type.host_type_id'))
    infrastructure_type_id = db.Column(db.Integer, db.ForeignKey(
        'infrastructure_type.infrastructure_type_id'))

    instances = db.relationship(
        'InstanceModel',
        backref='infrastructure_template',
        lazy=True)

    def __init__(
            self,
            infra_template_name,
            host_template_description,
            memory_size,
            cpu,
            max_no_disk,
            host_type_id,
            infrastructure_type_id):
        self.infra_template_name = infra_template_name
        self.host_template_description = host_template_description
        self.memory_size = memory_size
        self.cpu = cpu
        self.max_no_disk = max_no_disk
        self.host_type_id = host_type_id
        self.infrastructure_type_id = infrastructure_type_id

    @classmethod
    def find_by_id(cls, _id):
        '''
        This method is used to lookup InfrastructureTemplate from \
        database, based on provided infra_template_id
        '''
        infra_template = cls.query.filter_by(infra_template_id=_id).first()
        ExceptionUtils.raise_exception_if_object_not_found(
            infra_template, "Infrastructure Template", _id)
        return infra_template

    @classmethod
    def get_identifier(cls):
        return cls.infra_template_id

    @classmethod
    def find_by_name(cls, name):
        '''
        This method is used to lookup InfrastructureTemplate from database, based on provided infra_template_id
        '''
        return cls.query.filter_by(infra_template_name=name).first()

    def save_to_db(self):
        '''
        This method save InfrastructureTemplate record to the database
        '''
        db.session.add(self)
        db.session.commit()
        return self.infra_template_id

    @staticmethod
    def get_itv_infrastructure_templates():
        '''
        get list of infrastructure templates 
        '''
        data = []
        sql_connection = db.engine.connect()
        result = sql_connection.execute(
            "select infra_template_id, infra_template_name, ityp.infrastructure_type_id, infrastructure_type_name, host_template_description, memory_size, `cpu`, max_no_disk, ht.host_type_id, ht.host_name from infrastructure_template it join host_type ht on it.host_type_id = ht.host_type_id join infrastructure_type ityp on it.infrastructure_type_id = ityp.infrastructure_type_id order by infra_template_id desc;")
        for row in result:
            data.append(row)
        return data

    def json(self, detail_required=True):
        '''
          Convenience method to retrieve Json representation of this model class
        '''
        infra_temp = {
            "infra_template_id": self.infra_template_id,
            "infra_template_name": self.infra_template_name,
            "host_template_description": self.host_template_description,
            "memory_size": self.memory_size,
            "cpu": self.cpu,
            "max_no_disk": self.max_no_disk,
            "infrastructure_type": self.infrastructure_type.json(),
        }
        if detail_required is True:
            infra_temp["host_type"] = self.host_type.json(
                details_required=False)
        return infra_temp
