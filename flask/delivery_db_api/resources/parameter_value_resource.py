'''
Created on 10 April 2018

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.parameter_value import ParameterValueModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class ParameterValue(AbstractResource):
    '''
    This class defines the handler for handing the requests related to parameter_value
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('parameter_value_id', type=int, required=False)
        parser.add_argument('parameter_value', type=str, required=False)
        parser.add_argument('parameter_id', type=int, required=False)

    def get_model(self):
        return ParameterValueModel

    @authenticate
    def post(self):
        '''
        This method creates parameter_value store type in the delivery database
        '''
        request_data = request.get_json()
        parameter_value = request_data["parameter_value"]
        parameter_id = request_data["parameter_id"]
        kwargs = {
            'parameter_value': parameter_value,
            'parameter_id': parameter_id}

        try:
            if ParameterValueModel.find_generic(**kwargs):
                return return_object_already_exist_errr(
                    "parameter_value", "same class", "")
        except ObjectNotFound as exception:
            paramater_class = ParameterValueModel(
                parameter_value=parameter_value,
                parameter_id=parameter_id,
            )
            return {
                "parameter_value_id": paramater_class.save_to_db().parameter_value_id}
