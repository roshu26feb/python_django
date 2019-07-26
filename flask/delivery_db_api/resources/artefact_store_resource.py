'''
Created on 11 Dec 2017

@author: anil.kumar
'''
from flask.globals import request
from delivery_db_api.models.artefact_store_type import ArtefactStoreTypeModel
from delivery_db_api.resources.abstract_resource \
    import return_object_already_exist_errr, AbstractResource
from delivery_db_api.security import authenticate


class ArtefactStoreType(AbstractResource):
    '''
    This class defines the handler for handing the requests related to artefact store type
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('artefact_store_type_id', type=int, required=False)
        parser.add_argument(
            'artefact_store_type_desc',
            type=str,
            required=False)

    def get_model(self):
        return ArtefactStoreTypeModel

    @authenticate
    def post(self):
        '''
        This method creates aartefact store type in the delivery database
        '''
        request_data = request.get_json()
        artefact_store_type_desc = request_data["artefact_store_type_desc"]
        if ArtefactStoreTypeModel.find_by_description(
                artefact_store_type_desc) is not None:
            return return_object_already_exist_errr(
                "Artefact", "artefact store type:", artefact_store_type_desc)
        artefact_store_type = ArtefactStoreTypeModel(
            artefact_store_type_desc=artefact_store_type_desc)
        return {"artefact_store_type_id": artefact_store_type.save_to_db()}
