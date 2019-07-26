'''
Created on 15 May 2018

@author: neeraj.mahajan
'''
from flask.globals import request
from delivery_db_api.models.system_element_type import SystemElementTypeModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class SystemElementType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to system element type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('system_element_type_id', type=int, required=False)
        parser.add_argument(
            'system_element_type_name',
            type=str,
            required=False)
        parser.add_argument(
            'system_element_type_short_name',
            type=str,
            required=False)

    def get_model(self):
        return SystemElementTypeModel

    @authenticate
    def post(self):
        '''
        This method creates system_element_type store type in the delivery database
        '''
        request_data = request.get_json()
        system_element_type_name = request_data["system_element_type_name"]
        system_element_type_short_name = request_data["system_element_type_short_name"]
        if SystemElementTypeModel.find_by_name(
                system_element_type_name) is not None:
            return return_object_already_exist_errr(
                "system_element_type",
                "system_element_type_name:",
                system_element_type_name)
        system_element_type = SystemElementTypeModel(
            system_element_type_name=system_element_type_name,
            system_element_type_short_name=system_element_type_short_name)
        return {"system_element_type_id": system_element_type.save_to_db(
        ).system_element_type_id}
