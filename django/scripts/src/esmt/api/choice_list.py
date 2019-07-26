"""
Author: Yogaraja Gopal
This module contains the Class and function which is used to call the delivery_db api and return the
list of dropdown list choices
"""
import json
from rest_framework import status
from .abstract import get_request , get_request_secure
from .mixins import GetChoiceListMixin, GetChoiceDictMixin


class Systems(GetChoiceListMixin):
    """
    This method is used to get list of Systems from Delivery DB API
    """
    url_param = "system"
    choice_key = "system_id"
    choice_value = "system_name"
    parent_element = "systems"

    def __init__(self, access_token):
        self.access_token = access_token


class Components(GetChoiceListMixin):
    """
    This method is used to get list of Components from Delivery DB API
    """
    url_param = "component"
    choice_key = "component_name"
    choice_value = "component_name"
    parent_element = "components"

    def __init__(self, access_token):
        self.access_token = access_token


class ComponentId(GetChoiceDictMixin):
    """
    This method is used to get list of Component with key as ids from Delivery DB API
    """
    url_param = "component"
    choice_key = "component_id"
    choice_value = "component_name"
    parent_element = "components"

    def __init__(self, access_token):
        self.access_token = access_token


class ComponentType(GetChoiceListMixin):
    """
    This method is used to get list of Component Types from Delivery DB API
    """
    url_param = "component_type"
    choice_key = "component_type_description"
    choice_value = "component_type_description"
    parent_element = "component_types" 

    def __init__(self, access_token):
        self.access_token = access_token


class ComponentTypeId(GetChoiceDictMixin):
    """
    This method is used to get list of Component Types with key as id from Delivery DB API
    """
    url_param = "component_type"
    choice_key = "component_type_id"
    choice_value = "component_type_description"
    parent_element = "component_types" 

    def __init__(self, access_token):
        self.access_token = access_token


class ComponentVersionId(GetChoiceDictMixin):
    """
    This method is used to get list of Component Version with key as id from Delivery DB API
    """
    url_param = "component_version"
    choice_key = "component_version_id"
    choice_value = "component_version_name"
    parent_element = "component_versions"

    def __init__(self, access_token):
        self.access_token = access_token


class ArtefactStoreType(GetChoiceListMixin):
    """
    This method is used to get list of Artefact Store Types from Delivery DB API
    """
    url_param = "artefact_type"
    choice_key = "artefact_store_type_desc"
    choice_value = "artefact_store_type_desc"
    parent_element = "artefact_store_types" 

    def __init__(self, access_token):
        self.access_token = access_token


class HostType(GetChoiceListMixin ):
    """
    This method is used to get list of Host Types from Delivery DB API
    """
    url_param = "host_type"
    choice_key = "host_type_id"
    choice_value = "host_name"
    parent_element = "host_types"
    def __init__(self, access_token):
        self.access_token = access_token


class DeploymentType(GetChoiceListMixin):
    """
    This method is used to get list of Deployment Type from Delivery DB API
    """
    url_param = "deployment_type"
    choice_key = "deployment_type_id"
    choice_value = "deployment_type_description"
    parent_element = "deployment_types"

    def __init__(self, access_token):
        self.access_token = access_token


class InfraTemplate(GetChoiceListMixin):
    """
    This method is used to get list of Infrastructure Template from Delivery DB API
    """
    url_param = "infrastructure_template"
    choice_key = "infra_template_id"
    choice_value = "host_template_description"
    parent_element = "infrastructure_templates"
    def __init__(self, access_token):
        self.access_token = access_token


class MethodCreation(GetChoiceListMixin):
    """
    This method is used to get list of Method Creation from Delivery DB API
    """
    url_param = "method_creation_type"
    choice_key = "method_creation_type_id"
    choice_value = "description"
    parent_element = "method_creation_types"

    def __init__(self, access_token):
        self.access_token = access_token


class NetworkSet(GetChoiceListMixin):
    """
    This method is used to get list of Network Set from Delivery DB API
    """
    url_param = "network_set"
    choice_key = "network_set_id"
    choice_value = "network_set_name"
    parent_element = "network_sets"

    def __init__(self, access_token):
        self.access_token = access_token


class Releases(GetChoiceListMixin):
    """
    This method is used to get list of Network Set from Delivery DB API
    """
    url_param = "release"
    choice_key = "release_id"
    choice_value = "release_name"
    parent_element = "releases" 

    def __init__(self, access_token):
        self.access_token = access_token


class EnvDataType(GetChoiceListMixin):
    """
    This method is used to get list of Environment Data type from Delivery DB API
    """
    url_param = "environment_data_type"
    choice_key = "environment_data_type_id"
    choice_value = "environment_data_type_name"
    parent_element = "environment_data_types" 

    def __init__(self, access_token):
        self.access_token = access_token


class ParameterType(GetChoiceListMixin):
    """
    This method is used to get list of Parameter type from Delivery DB API
    """
    url_param = "parameter_type"
    choice_key = "parameter_type_id"
    choice_value = "parameter_type"
    parent_element = "parameter_types"

    def __init__(self, access_token):
        self.access_token = access_token


class InfraType(GetChoiceListMixin):
    """
    This method is used to get list of Infrastructure type from Delivery DB API
    """
    url_param = "infrastructure_type"
    choice_key = "infrastructure_type_id"
    choice_value = "infrastructure_type_name"
    parent_element = "infrastructure_types"

    def __init__(self, access_token):
        self.access_token = access_token


class DeploymentStatus(GetChoiceListMixin):
    """
    This method is used to get list of Statuses for Deployment  from Delivery DB API
    """
    url_param = "status?status_type=Deployment"
    choice_key = "status_id"
    choice_value = "status_description"
    parent_element = "statuss"

    def __init__(self, access_token):
        self.access_token = access_token


class Users(GetChoiceListMixin):
    """
    This method is used to get list of Users from Delivery DB API
    """
    url_param = "user"
    choice_key = "user_id"
    choice_value = "user_name"
    parent_element = "users"

    def __init__(self, access_token):
        self.access_token = access_token


class SystemNetworkSet(GetChoiceListMixin):
    """
    This method is used to get list of  System Network sets from Delivery DB API
    """
    url_param = "system_network_set"
    choice_key = "system_network_set_id"
    choice_value = "system_network_set_name"
    parent_element = "system_network_sets"

    def __init__(self, access_token):
        self.access_token = access_token



class UserRole(GetChoiceListMixin):
    """
    This method is used to get list of User Roles from Delivery DB API
    """
    url_param = "role"
    choice_key = "role_id"
    choice_value = "role_name"
    parent_element = "roles"
    include_select = False

    def __init__(self, access_token):
        self.access_token = access_token



class HostRegion(GetChoiceListMixin):
    """
    This method is used to get list of System Element Type from Delivery DB API
    """
    url_param = "host_region"
    choice_key = "host_region_id"
    choice_value = "host_region_name"
    parent_element = "host_regions"

    def __init__(self, access_token):
        self.access_token = access_token


class instances(GetChoiceListMixin):
    """
    This method is used to get list of System Element Type from Delivery DB API
    """
    url_param = "instance"
    choice_key = "instance_id"
    choice_value = "instance_name"
    parent_element = "instances"

    def __init__(self, access_token):
        self.access_token = access_token


def get_release_status(request):
    """
    This method is used to get list of Status from Delivery DB API for Release
    """
    release_status = get_request_secure("/api/v1/status?status_type=Release" , request.COOKIES.get('access_token'))
    release_status_data = json.loads(release_status.text)
    release_status_list = [('', '--Select--')]
    if release_status.status_code == status.HTTP_200_OK:
        for state in release_status_data["statuss"]:
            status_list = (state["status_id"],
                           state["status_description"])
            release_status_list.append(status_list)
    else:
        release_status_list = [('-1', 'Error : Unable to get Release status')]
    return release_status_list


def get_parameter_type_name(parameter_type_id , request):
    """
    This method is used to get parameter_type_name from parameter_type_id from Delivery DB API
    """
    response = get_request_secure("/api/v1/parameter_type?parameter_type_id=" + str(parameter_type_id) ,  request.COOKIES.get('access_token'))
    response_data = json.loads(response.text)
    parameter_type_name = ''
    if response.status_code == status.HTTP_200_OK:
        for data in response_data["parameter_types"]:
            parameter_type_name = data["parameter_type"]
    return parameter_type_name


def get_environment_by_system_id(system_id , access_token):
    """
    This method is used to get list of Environments by System ID from Delivery DB API
    """
    env_response = get_request_secure("/api/v1/environment?system_id=" + system_id , access_token)
    env_response_data = json.loads(env_response.text)
    env_lists = [('', '--Select--')]
    if env_response.status_code == status.HTTP_200_OK:
        for env in env_response_data["environments"]:
            env_list = (env["environment_id"], env["environment_name"])
            env_lists.append(env_list)
    else:
        env_lists = [('', 'No Environments found for this system')]
    return env_lists


def getSysElement(system_id):
    """
    This method is used to get required value based on the supplied url from Delivery DB API
    not used any where
    """
    ele_response = get_request_secure("/api/v1/system_elements?system_id=" + system_id)
    ele_response_data = json.loads(ele_response.text)
    ele_lists = []
    if ele_response.status_code == status.HTTP_200_OK:
        for sysEle in ele_response_data["system_elements"]:
                ele_list = (sysEle["system_element_id"], sysEle["system_element_short_name"])
                ele_lists.append(ele_list)
                
    else:
        ele_lists = [('','No elements')]
    return ele_lists


def get_value(url, parent_key, key , request ):
    """
    This method is used to get required value based on the supplied url from Delivery DB API
    """
    response = get_request_secure("/api/v1/" + url ,   request.COOKIES.get('access_token'))
    response_data = json.loads(response.text)
    if response.status_code == status.HTTP_200_OK:
        for env in response_data[parent_key]:
            return env[key]
    else:
        return -1


def application_components(component_ids):
    """
    This method is used to get list of parameter linked to comp/comp_type from Delivery DB API
    not used any where
    """
    app_comp_list = []
    for comp in component_ids:
        response = get_request_secure("/api/v1/component?component_id=" + str(comp) +
                               "&component_type_id=1")
        if response.status_code == status.HTTP_200_OK:
            response = json.loads(response.text)
            for component in response["components"]:
                app_comp = (comp, component['component_name'])
                app_comp_list.append(app_comp)
    return app_comp_list


def get_parameters(link, list_ids ,cookeis):
    """
    This method is used to get list of parameter linked to comp/comp_type from Delivery DB API
    """
    parameter_field_list = []
    for list_id in list_ids:
        response = get_request_secure("/api/v1/parameter?" + link + "_id=" + str(list_id) , cookeis )
        if response.status_code == status.HTTP_200_OK:
            response = json.loads(response.text)
            for param in response["parameters"]:
                parameter = dict()
                if (param["active"] and (link == "component")  ):
                    if ("component" in param["linked_element"]) and (param["linked_element"]["component"]["component_type"]["component_type_id"] == 1):
                        parameter["comp_id"] = list_id
                        get_param_details(param, parameter)
                        parameter_field_list.append(parameter)
                    if ("component" in param["linked_element"]) and (param["linked_element"]["component"]["component_type"]["component_type_id"] == 2):
                        parameter["infraConf_comp_id"] = list_id
                        get_param_details(param, parameter)
                        parameter_field_list.append(parameter)
                    if ("component" in param["linked_element"]) and (param["linked_element"]["component"]["component_type"]["component_type_id"] == 3):
                        parameter["infra_comp_id"] = list_id
                        get_param_details(param, parameter)
                        parameter_field_list.append(parameter)

                elif (link == "component_type" and param["active"]):
                    if "component_type" in param["linked_element"] and param["linked_element"]["component_type"]["component_type_id"] == 3:
                        parameter["comp_type"] = 'infra'
                        get_param_details(param, parameter)
                        parameter_field_list.append(parameter)
                    elif "component_type" in param["linked_element"] and param["linked_element"]["component_type"]["component_type_id"] == 2:
                        parameter["comp_type"] = 'infraConf'
                        get_param_details(param, parameter)
                        parameter_field_list.append(parameter)
                    elif "component_type" in param["linked_element"] and param["linked_element"]["component_type"]["component_type_id"] == 1:
                        parameter["comp_type"] = 'app'
                        get_param_details(param, parameter)
                        parameter_field_list.append(parameter)
               
    return parameter_field_list


def get_param_details(param, parameter):
    """
    Get the parameter details for active para 
    """
    if param["active"]:
        parameter["name"] = "parameter-" + str(param["parameter_id"])
        label = param["parameter_name"]
        parameter["parameter_internal_name"] = param["parameter_internal_name"]
        parameter["label"] = label.replace('_', ' ').title()
        parameter["mandatory"] = param["mandatory"]
        parameter_type = param["parameter_type"]["parameter_type"]
        parameter["type"] = parameter_type
        if "LIST" in parameter_type.upper():
            if "MULTI" not in parameter_type.upper():
                parameter_values = [('', '--Select--')]
            else:
                parameter_values = []
                parameter["name"] = "parameter-" + str(param["parameter_id"]) + "-MULTI"
            for param_value in param["parameter_values"]:
                obj = (param_value["parameter_value"],
                       param_value["parameter_value"].strip())
                parameter_values.append(obj)
            parameter["choices"] = parameter_values
        elif "BOOLEAN" in parameter_type.upper():
            parameter["choices"] = [('', '--Select--'), (True, 'True'),
                                    (False, 'False')]
        elif "FREE" in parameter_type.upper():
            for value in param["parameter_values"]:
                val = value["parameter_value"]
                #parameter["size"] = val[val.find("(")+1:val.find(")")]
                parameter["size"] = val
        elif "NUMBER" in parameter_type.upper():
            for value in param["parameter_values"]:
                val = value["parameter_value"]
                min_max = val[val.find("(") + 1:val.find(")")].split(',')
                parameter["min"] = min_max[0]
                parameter["max"] = min_max[1]
        return parameter