'''
Created on 10 April 2018

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.models.parameter_type import ParameterTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class ParameterType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to parameter type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('parameter_type_id', type=int, required=False)
        parser.add_argument('parameter_type', type=str, required=False)

    def get_model(self):
        return ParameterTypeModel

    @authenticate
    def post(self):
        '''
        This method creates parameter_type store type in the delivery database
        '''
        request_data = request.get_json()
        parameter_type = request_data["parameter_type"]
        if ParameterTypeModel.find_by_name(parameter_type) is not None:
            return return_object_already_exist_errr(
                "parameter_type ", "", parameter_type)
        parameter_type = ParameterTypeModel(
            parameter_type=parameter_type)
        return {"parameter_type_id": parameter_type.save_to_db()}
