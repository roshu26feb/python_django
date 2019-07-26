'''
Created on 29 Aug 2017

@author: neeraj.mahajan
'''
from flask.app import Flask
from flask_restful import Api
from flask_cors import CORS
from delivery_db_api.app_config import AppConfig
from delivery_db_api.models.user_role import UserRoleModel
from delivery_db_api.resources.artefact_store_resource import ArtefactStoreType
from delivery_db_api.resources.component_resource import Component, \
    ComponentVersion
from delivery_db_api.resources.component_type_resource import ComponentType
from delivery_db_api.resources.deployment_resource import Deployment, UpdateDeploymentStatus, UpdateInstanceForDeployment, HistoricComponentStatus
from delivery_db_api.resources.deployment_type_resource import DeploymentType
from delivery_db_api.resources.disk_type_resource import DiskType
from delivery_db_api.resources.environment_data_type_resource import EnvironmentDataType
from delivery_db_api.resources.environment_resource import Environment, EnvironmentsList, EnvironmentSystemelementsList
from delivery_db_api.resources.environment_set_resource import EnvironmentSet
from delivery_db_api.resources.environment_subscription_type_resource import EnvironmentSubscriptionType
from delivery_db_api.resources.environment_type_resource import EnvironmentType
from delivery_db_api.resources.environment_use_resource import EnvironmentUse
from delivery_db_api.resources.host_region_resource import HostRegion
from delivery_db_api.resources.host_site_resource import HostSite
from delivery_db_api.resources.host_subscription_resource import HostSubscription
from delivery_db_api.resources.host_type_resource import HostType
from delivery_db_api.resources.infrastructure_template_resource import InfrastructureTemplate
from delivery_db_api.resources.infrastructure_type_resource import InfrastructureType
from delivery_db_api.resources.instance_resource import Instance, InstanceList, InstanceListWithoutDestroyed
from delivery_db_api.resources.method_creation_type_resource import MethodCreationType
from delivery_db_api.resources.network_set_resource import NetworkSet
from delivery_db_api.resources.parameter_resource import Parameter
from delivery_db_api.resources.parameter_type_resource import ParameterType
from delivery_db_api.resources.parameter_value_resource import ParameterValue
from delivery_db_api.resources.release_resource import Release
from delivery_db_api.resources.release_version_resource import ReleaseVersion
from delivery_db_api.resources.role_resource import Role
from delivery_db_api.resources.route_to_live_resource import RouteToLive
from delivery_db_api.resources.status_resource import Status
from delivery_db_api.resources.system_element_component_resource import SystemElementComponent, SystemElementComponentEnv
from delivery_db_api.resources.system_element_deployment_version_resource import SystemElementDeploymentVersion
from delivery_db_api.resources.system_element_resource import SystemElement, SystemElementDetailsByEnvID
from delivery_db_api.resources.system_element_type_resource import SystemElementType
from delivery_db_api.resources.system_network_set_resource import SystemNetworkSet
from delivery_db_api.resources.system_resource import System, SystemVersion
from delivery_db_api.resources.user_resource import User
from delivery_db_api.resources.instance_allocation_resource import InstanceAllocation, MapInstance
from delivery_db_api.resources.deployment_component_resource import DeploymentComponent
from delivery_db_api.resources.environment_booking_resource import EnvironmentBooking

def main(app_config):
    '''
    This method registers all the end points of the application
    '''
    app = Flask(__name__)
    for key in app_config:
        app.config[key] = app_config[key]
    api = Api(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
    api.add_resource(System, '/api/v1/system')
    api.add_resource(
        SystemVersion, '/api/v1/system_version')
    api.add_resource(
        Instance,
        '/api/v1/instance')
    api.add_resource(
        Component,
        '/api/v1/component')
    api.add_resource(
        ComponentVersion,
        '/api/v1/component_version')
    api.add_resource(
        InfrastructureTemplate,
        '/api/v1/infrastructure_template')
    api.add_resource(
        Deployment,
        '/api/v1/deployment')
    api.add_resource(
        Release,
        '/api/v1/release')
    api.add_resource(
        ReleaseVersion,
        '/api/v1/release_version')
    api.add_resource(
        ComponentType,
        '/api/v1/component_type')
    api.add_resource(
        ArtefactStoreType,
        '/api/v1/artefact_type')
    api.add_resource(
        HostType,
        '/api/v1/host_type')
    api.add_resource(
        NetworkSet,
        '/api/v1/network_set')
    api.add_resource(
        Environment,
        '/api/v1/environment')
    api.add_resource(
        EnvironmentType,
        '/api/v1/environment_type')
    api.add_resource(
        DiskType,
        '/api/v1/disk_type')
    api.add_resource(
        Status,
        '/api/v1/status')
    api.add_resource(
        SystemElement,
        '/api/v1/system_element')
    api.add_resource(
        SystemElementComponent,
        '/api/v1/system_element_component')
    api.add_resource(
        DeploymentType,
        '/api/v1/deployment_type')
    api.add_resource(
        EnvironmentSet,
        '/api/v1/environment_set')
    api.add_resource(
        MethodCreationType,
        '/api/v1/method_creation_type')
    api.add_resource(
        ParameterType,
        '/api/v1/parameter_type')
    api.add_resource(
        Parameter,
        '/api/v1/parameter')
    api.add_resource(
        ParameterValue,
        '/api/v1/parameter_value')
    api.add_resource(
        InfrastructureType,
        '/api/v1/infrastructure_type')
    api.add_resource(
        EnvironmentUse,
        '/api/v1/environment_use')
    api.add_resource(
        EnvironmentDataType,
        '/api/v1/environment_data_type')
    api.add_resource(
        RouteToLive,
        '/api/v1/route_to_live')
    api.add_resource(
        EnvironmentSubscriptionType,
        '/api/v1/environment_subscription_type')
    api.add_resource(
        User,
        '/api/v1/user')
    api.add_resource(
        Role,
        '/api/v1/role')
    api.add_resource(
        SystemElementType,
        '/api/v1/system_element_type')
    api.add_resource(
        SystemNetworkSet,
        '/api/v1/system_network_set')
    api.add_resource(
        HostRegion,
        '/api/v1/host_region')
    api.add_resource(
        HostSite,
        '/api/v1/host_site')
    api.add_resource(
        HostSubscription,
        '/api/v1/host_subscription')

    api.add_resource(
        SystemElementDeploymentVersion,
        '/api/v1/system_element_deployment_version')

    api.add_resource(
        InstanceAllocation,
        '/api/v1/instance_allocation')

    api.add_resource(
        MapInstance,
        '/api/v1/mapinstance')

    api.add_resource(
        DeploymentComponent,
        '/api/v1/deployment_component')

    api.add_resource(
        SystemElementDetailsByEnvID,
        '/api/v1/system_element_by_env')

    api.add_resource(
        UpdateDeploymentStatus,
        '/api/v1/update_deployment_status')

    api.add_resource(
        InstanceList,
        '/api/v1/instance_list')

    api.add_resource(
        InstanceListWithoutDestroyed,
        '/api/v1/instance_list_without_destroyed')


    api.add_resource(
        UpdateInstanceForDeployment,
        '/api/v1/update_instance_deployment')

    api.add_resource(
        SystemElementComponentEnv,
        '/api/v1/system_element_component_env')

    api.add_resource(
        HistoricComponentStatus,
        '/api/v1/historic_deployment_status')

    api.add_resource(
        EnvironmentsList,
        '/api/v2/ev_environments')

    api.add_resource(
        EnvironmentSystemelementsList,
        '/api/v2/ev_system_elements')

    api.add_resource(
        EnvironmentSystemelementComponentsList,
        '/api/v2/ev_components')

    api.add_resource(
        EnvironmentBooking,
        '/api/v2/environment_booking')

    return app


def run_main():
    ''' This method launches and run the REST API for delivery database'''
    from delivery_db_api.database.config import db
    app = main(AppConfig.get_prod_config().config)
    if app.config['TESTING']:
        @app.before_first_request
        def create_tables():
            ''' This method will create the database schema on first REST request'''
            db.create_all()
    db.init_app(app)
    app.run(debug=False)


if __name__ == '__main__':
    run_main()
