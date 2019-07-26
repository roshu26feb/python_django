'''
Created on 04 April 2018

@author: neeraj.mahajan
'''
from flask.globals import request

from delivery_db_api.exception import ObjectNotFound
from delivery_db_api.models.route_to_live import RouteToLiveModel
from delivery_db_api.resources.abstract_resource import return_object_already_exist_errr, \
    AbstractResource
from delivery_db_api.security import authenticate


class RouteToLive(AbstractResource):
    '''
    This class defines the handler for handing the requests related to route to live
    '''

    def add_argument_for_parsing(self, parser):
        parser.add_argument('route_to_live_id', type=int, required=False)
        parser.add_argument('route_to_live_order', type=int, required=False)
        parser.add_argument('critical', type=bool, required=False)
        parser.add_argument('release_id', type=str, required=False)
        parser.add_argument('system_id', type=str, required=False)
        parser.add_argument('environment_use_id', type=str, required=False)
        parser.add_argument('environment_id', type=str, required=False)

    def get_model(self):
        return RouteToLiveModel

    @authenticate
    def post(self):
        '''
        This method creates route_to_live store type in the delivery database
        '''
        request_data = request.get_json()
        route_to_live_order = request_data["route_to_live_order"]
        critical = request_data["critical"]
        release_id = request_data["release_id"]
        system_id = request_data["system_id"]
        environment_use_id = request_data["environment_use_id"]
        environment_id = request_data["environment_id"]
        kwargs = {
            'release_id': release_id,
            'system_id': system_id,
            'environment_use_id': environment_use_id,
            'environment_id': environment_id}

        try:
            if RouteToLiveModel.find_generic(**kwargs):
                return return_object_already_exist_errr(
                    "route_to_live", "same parameters value", "")
        except ObjectNotFound as exception:
            route_to_live = RouteToLiveModel(
                route_to_live_order=route_to_live_order,
                critical=critical,
                release_id=release_id,
                system_id=system_id,
                environment_use_id=environment_use_id,
                environment_id=environment_id
            )
            return {"route_to_live_id": route_to_live.save_to_db()}
