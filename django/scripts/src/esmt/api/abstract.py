"""
This module hold common methods used in Delivery DB App
"""
import base64
import json
import requests
import jenkins
from django.conf import settings
import yaml
import sys
import ruamel.yaml
from functools import reduce
from rest_framework import status
from collections import OrderedDict, Counter
from django.http import JsonResponse
DELIVERY_API_URL = settings.DELIVERY_DB_API_URL
DELIVERY_API_USER = settings.DELIVERY_DB_API_USER
JENKINS_URI = settings.JENKINS_URI
JENKINS_API_ACCESS_USER = settings.JENKINS_API_ACCESS_USER
JENKINS_API_ACCESS_PSW = settings.JENKINS_API_ACCESS_PSW
from django.shortcuts import render, redirect

def post_request(api_url, data):
    """
    This method is used to handle post requests to Delivery DB API
    """
    user_pass = base64.b64encode(bytes(DELIVERY_API_USER, "utf-8")).decode("ascii")
    url = DELIVERY_API_URL + api_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
               'Authorization': 'Basic %s' % user_pass}
    response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    return response


def put_request(api_url, data):
    """
    This method is used to handle post requests to Delivery DB API
    """
    user_pass = base64.b64encode(bytes(DELIVERY_API_USER, "utf-8")).decode("ascii")
    url = DELIVERY_API_URL + api_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
               'Authorization': 'Basic %s' % user_pass}
    response = requests.put(url, data=json.dumps(data), headers=headers, verify=False)
    return response


def get_request(api_url):
    """
    This method is used to handle Get requests from Delivery DB API
    """
    url = DELIVERY_API_URL + api_url
    try:
        response = requests.get(url, verify=False)
        return response

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        response = {'status_code': '500',
                    'error': 'Error Conneting to Delivery DB'
                   }
        return response
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def get_request_secure(api_url, access_token):
    """
    This method is used to handle Get requests from Delivery DB API
    """
    url = DELIVERY_API_URL + api_url
    try:
        headers = {'Authorization': 'Bearer %s' % access_token}
   
        response = requests.get(url,headers=headers, verify=False )
        return response

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        response = {'status_code': '500',
                    'error': 'Error Conneting to Delivery DB'
                   }
       
        return response
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def post_request_secure(api_url, data , access_token):
    """
    This method is used to handle post requests to Delivery DB API
    """
    user_pass = base64.b64encode(bytes(DELIVERY_API_USER, "utf-8")).decode("ascii")
    url = DELIVERY_API_URL + api_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer %s' % access_token }
    response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    return response



def put_request_secure(api_url, data , access_token):
    """
    This method is used to handle post requests to Delivery DB API
    """
    user_pass = base64.b64encode(bytes(DELIVERY_API_USER, "utf-8")).decode("ascii")
    url = DELIVERY_API_URL + api_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer %s' % access_token }
    response = requests.put(url, data=json.dumps(data), headers=headers, verify=False)
    return response


def trigger_jenkins_job(parameters, env_type , request):
    """
    Send yaml data to jenkins uri 
    """
    try:
        yaml_data = get_yamldata(parameters , request )

        if "'deploymentTagVersion'" not in parameters  :
            return "Deployment tag version missing"

        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        headers = dict()
        user_pass = base64.b64encode(
            bytes(JENKINS_API_ACCESS_USER + ":" + JENKINS_API_ACCESS_PSW, "utf-8")).decode("ascii")
        headers['Authorization'] = 'Basic %s' % user_pass

        # Get a CRUMB from Jenkins
        url = "{0}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)".\
            format(JENKINS_URI)
        crumb = requests.get(url, headers=headers, verify=False).content
        # Convert bytes to Strings
        crumb = crumb.decode("utf-8")

        DEPLOYMENT_PIPELINE_TYPE = settings.JENKINS_DEPLOYMENT_PIPELINE_NONPROD
        JENKINS_JOB = settings.JENKINS_JOB_NAME
        if env_type == 5:
            DEPLOYMENT_PIPELINE_TYPE = settings.JENKINS_DEPLOYMENT_PIPELINE_PROD
            JENKINS_JOB = settings.JENKINS_JOB_NAME_PROD
        

        build_tag = parameters["'deploymentTagVersion'"]

        #url = "{}/view/{}/job/{}/view/tags/job/{}/build".format(JENKINS_URI, DEPLOYMENT_PIPELINE_TYPE, settings.JENKINS_JOB_NAME, build_tag) 
        url = "{}/view/{}/job/{}/view/tags/job/{}/build".format(JENKINS_URI, JENKINS_JOB, DEPLOYMENT_PIPELINE_TYPE, build_tag)        

        request_payload = {"parameter": [{"name":settings.JENKINS_PARAMETER_NAME, "value":yaml_data}]}
        payload = 'json={}'.format(json.dumps(request_payload))
        
        headers = {
            crumb.split(":")[0]: crumb.split(":")[1],
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization' : 'Basic %s' % user_pass
            }
        payload_removing_unsafe_ascii = payload.replace("%","%25").replace("&","%26")
        response = requests.request("POST", url, data=payload_removing_unsafe_ascii, headers=headers, verify=False)

        if response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_201_CREATED:
            return "Triggered"
        else:
            return "Failed"
    except Exception as e :
        print (e)
        return "Failed"


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def get_yamldata(resp_data , request ): 
    """
    Prepare yaml data
    """
    data, dict_data = {}, {}
    reduce(merge_dict, [dict_data, resp_data['infra'], resp_data['infraConf'], resp_data['app']])
    for para_internal_name, value in dict_data.items():
        if para_internal_name !=  "'deploymentTagVersion'" and value != "" and type(para_internal_name) != int and not para_internal_name.isdigit():
            para_internal_name = para_internal_name.strip("'")
            if type(value) is str and ',' in value:
                list_data = value.split(',')
                list_data_without_empty = [x for x in list_data if x]
                value = list_data_without_empty
            elif type(value) is str and (value == 'True' or value == 'False'):
                value = (value == 'True')
            elif type(value) is str and value.isdigit():
                value = int(value)
            resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(para_internal_name.split("'.'")),value)
            merge_dict(data, resp_data_output)
    if 'api_data_param' in resp_data:
        deploy_params = get_yaml_other_data(resp_data ,request )
        merge_dict(data, deploy_params)
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
    
    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '')

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return collections.OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(collections.OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)
    yaml.add_representer(type(None), represent_none)

    yaml_str = yaml.dump(data, Dumper=MyDumper, default_flow_style=False)
    return yaml_str


def get_yaml_other_data(api_data_req , request):
    """
    Get other yaml data from database
    """
    deploy_params = {}
    data = {}
    componentDeploy = False
    api_data = api_data_req['api_data_param']
    if (api_data['infraConf'] or api_data['app']) :
        componentDeploy = True
    deploy_params['booleanParams'] = {}
    deploy_params['booleanParams']['infrastructureBuild'] = api_data['infra']        
    deploy_params['booleanParams']['componentDeploy'] = componentDeploy       
    #deploy_params['booleanParams']['auto_teardown'] = False

    deploy_params['environmentAppParams'] = {}
    # REMOVE below if condition(line:178- 203) with api call once jenkins will be updated to handle instance username and password
    if  not api_data['infra'] and (api_data['infraConf'] or api_data['app']) :
        #+ "&system_version_id=" + str(api_data['system_version_id'])       
        url = "/api/v1/deployment?environment_id=" + str(api_data['environment_id'] + "&instance_id=" + str(api_data['instance_id']) + "&system_element_id=" + str(api_data['sys_elem_id']))
        resp_data = get_request_secure(url , request.COOKIES.get('access_token'))
        try:
            if resp_data.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp_data.text)
                deploy_params['commonParams'] = {}
                for deploy_param in resp_data['deployments'][0]['deployment_parameters']:
                    # if deploy_param['parameter']['parameter_internal_name'] == "'commonParams'.'specs_terraform_version'" and api_data['infra']:
                    #     deploy_params['commonParams']['specs_terraform_version'] =\
                    #             deploy_param["deployment_parameter_value"]
                    # if deploy_param['parameter']['parameter_internal_name'] == "'commonParams'.'specs_ansible_version'" and (api_data['infraConf'] or api_data['app']):
                    #     deploy_params['commonParams']['specs_ansible_version'] =\
                    #             deploy_param["deployment_parameter_value"]
                    # if deploy_param['parameter']['parameter_internal_name'] == "'commonParams'.'infrastructurecheck_version'" and (api_data['infra']):
                    #     deploy_params['commonParams']['infrastructurecheck_version'] =\
                    #             deploy_param["deployment_parameter_value"]
                    if deploy_param['parameter']['parameter_internal_name'] == "'infrastructureBuildParams'.'primary_user'" and (not api_data['infra']):
                        deploy_params['environmentAppParams']['instance_user'] =\
                                deploy_param["deployment_parameter_value"]
                    if deploy_param['parameter']['parameter_internal_name'] == "'infrastructureBuildParams'.'primary_password'" and (not api_data['infra']):
                        deploy_params['environmentAppParams']['instance_password'] =\
                                deploy_param["deployment_parameter_value"]
        except ConnectionError as e:
            print (e)
    if  api_data['instance_id'] and not api_data['infra']:
        url = "/api/v1/instance?instance_id=" + str(api_data['instance_id'])
        resp_data_inst = get_request_secure(url , request.COOKIES.get('access_token')) 
        try:
            if resp_data_inst.status_code == status.HTTP_200_OK:
                resp_data_inst = json.loads(resp_data_inst.text)
                deploy_params['environmentAppParams']['azure_ip'] = resp_data_inst['instances'][0]['assigned_ip']
        except ConnectionError as e:
            print (e)
    deploy_uri_data = []
    if  len(api_data['available_infra_config']) > 0 and api_data['infraConf']:
        for available_infra_config in api_data['available_infra_config']:
            url = "/api/v1/component_version?component_version_id=" + str(available_infra_config['component_version'])
            resp_data_comp_ver = get_request_secure(url , request.COOKIES.get('access_token'))
            try:
                if resp_data_comp_ver.status_code == status.HTTP_200_OK:
                    resp_data_comp_ver = json.loads(resp_data_comp_ver.text)
                    if resp_data_comp_ver['component_versions'][0]['component']['deployment_type']['deployment_type_id'] == 3:
                        comp_infra_deploy_params, comp_infra_deploy_params['result_para'], comp_infra_deploy_params['result_override'], comp_infra_deploy_params['result_data']= {}, {}, {}, {}
                        if str(resp_data_comp_ver['component_versions'][0]['component']['component_id']) in api_data_req['infraConf']:
                            comp_infra_deploy_params = searchforsubstr(api_data_req['infraConf'][str(resp_data_comp_ver['component_versions'][0]['component']['component_id'])], 'deploy_params_list', 'deploy_override')
                        infra_deploy_params = searchforsubstr(api_data_req['infraConf'], 'deploy_params_list', 'deploy_override')
                        infraConf_data_dict = OrderedDict()
                        infraConf_data_dict['deploy_uri'] = resp_data_comp_ver['component_versions'][0]['artefact_store_url']
                        infraConf_data_dict['component_id'] = resp_data_comp_ver['component_versions'][0]['component']['component_id']   
                        if len(infra_deploy_params['result_override']) > 0 or len(comp_infra_deploy_params['result_override']) > 0:
                            infra_temp_result_override = infra_deploy_params['result_override']
                            infra_deploy_params['result_override'] = {}
                            infra_deploy_param_dict = {}
                            for result_override_data in comp_infra_deploy_params['result_override'] :
                                if 'deploy_override' in str(result_override_data):
                                    result_override_data_array = result_override_data[0].split('deploy_override\'.\'')
                                    result_override_data_list = list(result_override_data)
                                    result_override_data_list[0] = result_override_data_array[1]
                                    result_override_data = tuple(result_override_data_list)
                                    infra_conf_list_of_key = result_override_data_array[1]
                                    resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(infra_conf_list_of_key.split("'.'")),result_override_data[1])
                                    nested_dict = merge_nested_dict(infra_deploy_param_dict,resp_data_output)
                                    if nested_dict not in infra_deploy_params['result_override'].values():
                                        infra_deploy_params['result_override'] = dict(infra_deploy_params['result_override'])
                                        infra_deploy_params['result_override'].update(nested_dict)                                 
                            for result_override_data in infra_temp_result_override :
                                if 'deploy_override' in str(result_override_data):
                                    result_override_data_array = result_override_data[0].split('deploy_override\'.\'')
                                    result_override_data_list = list(result_override_data)
                                    result_override_data_list[0] = result_override_data_array[1]
                                    result_override_data = tuple(result_override_data_list)
                                    infra_conf_list_of_key = result_override_data_array[1]
                                    resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(infra_conf_list_of_key.split("'.'")),result_override_data[1])
                                    nested_dict = merge_nested_dict(infra_deploy_param_dict,resp_data_output)
                                    if nested_dict not in infra_deploy_params['result_override'].values():
                                        infra_deploy_params['result_override'] = dict(infra_deploy_params['result_override'])
                                        infra_deploy_params['result_override'].update(nested_dict)
                            infraConf_data_dict['deploy_override'] = infra_deploy_params['result_override']
                        infraConf_data_dict['test_uri'] = resp_data_comp_ver['component_versions'][0]['test_set_url']
                        if len(infra_deploy_params['result_para']) > 0 or len(comp_infra_deploy_params['result_para']) > 0:
                            for result_para_data in comp_infra_deploy_params['result_para']:
                                infra_deploy_params['result_para'].append(result_para_data)
                            infraConf_data_dict.update(infra_deploy_params['result_para'])

                        deploy_uri_data.append(infraConf_data_dict)
                        if len(infra_deploy_params['result_data']) > 0 or len(comp_infra_deploy_params['result_data']) > 0:
                            for result_para_data in comp_infra_deploy_params['result_data']:
                                list_of_key = result_para_data[0]
                                resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(list_of_key.split("'.'")),result_para_data[1])
                                merge_dict(data,resp_data_output)                               
                        
            except ConnectionError as e:
                print (e)
    if  len(api_data['available_application']) > 0 and api_data['app']:
        for available_application in api_data['available_application']:
            url = "/api/v1/component_version?component_version_id=" + str(available_application['component_version'])
            resp_data_comp_ver = get_request_secure(url ,  request.COOKIES.get('access_token'))
            try:
                if resp_data_comp_ver.status_code == status.HTTP_200_OK:
                    resp_data_comp_ver = json.loads(resp_data_comp_ver.text)
                    if resp_data_comp_ver['component_versions'][0]['component']['deployment_type']['deployment_type_id'] == 3:
                        comp_deploy_param_data, comp_deploy_param_data['result_para'], comp_deploy_param_data['result_override'], comp_deploy_param_data['result_data'] = {}, {}, {}, {}
                        if str(resp_data_comp_ver['component_versions'][0]['component']['component_id']) in api_data_req['app']:
                            comp_deploy_param_data = searchforsubstr(api_data_req['app'][str(resp_data_comp_ver['component_versions'][0]['component']['component_id'])], 'deploy_params_list', 'deploy_override')
                        deploy_params_data = searchforsubstr(api_data_req['app'], 'deploy_params_list', 'deploy_override')
                        app_data_dict = OrderedDict()
                        app_data_dict['deploy_uri'] = resp_data_comp_ver['component_versions'][0]['artefact_store_url']
                        app_data_dict['component_id'] = resp_data_comp_ver['component_versions'][0]['component']['component_id']
                        if len(deploy_params_data['result_override']) > 0 or len(comp_deploy_param_data['result_override']) > 0:
                            temp_result_override = deploy_params_data['result_override']
                            deploy_params_data['result_override'] = {}
                            app_deploy_param_dict = {}
                            for result_override_data in comp_deploy_param_data['result_override'] :
                                if 'deploy_override' in str(result_override_data):
                                    result_override_data_array = result_override_data[0].split('deploy_override\'.\'')
                                    result_override_data_list = list(result_override_data)
                                    result_override_data_list[0] = result_override_data_array[1]
                                    result_override_data = tuple(result_override_data_list)
                                    application_list_of_key = result_override_data_array[1]
                                    resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(application_list_of_key.split("'.'")),result_override_data[1])
                                    nested_dict = merge_nested_dict(app_deploy_param_dict,resp_data_output)
                                    if nested_dict not in deploy_params_data['result_override'].values():
                                        deploy_params_data['result_override'] = dict(deploy_params_data['result_override'])
                                        deploy_params_data['result_override'].update(nested_dict)
                            for result_override_data in temp_result_override :
                                if 'deploy_override' in str(result_override_data):
                                    result_override_data_array = result_override_data[0].split('deploy_override\'.\'')
                                    result_override_data_list = list(result_override_data)
                                    result_override_data_list[0] = result_override_data_array[1]
                                    result_override_data = tuple(result_override_data_list)
                                    application_list_of_key = result_override_data_array[1]
                                    resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(application_list_of_key.split("'.'")),result_override_data[1])
                                    nested_dict = merge_nested_dict(app_deploy_param_dict,resp_data_output)
                                    if nested_dict not in deploy_params_data['result_override'].values():
                                        deploy_params_data['result_override'] = dict(deploy_params_data['result_override'])
                                        deploy_params_data['result_override'].update(nested_dict)
                            app_data_dict['deploy_override'] = deploy_params_data['result_override']
                        app_data_dict['test_uri'] = resp_data_comp_ver['component_versions'][0]['test_set_url']
                        if len(deploy_params_data['result_para']) > 0 or len(comp_deploy_param_data['result_para']) > 0:
                            for result_para_data in comp_deploy_param_data['result_para']:
                                deploy_params_data['result_para'].append(result_para_data)
                            app_data_dict.update(deploy_params_data['result_para'])
                        deploy_uri_data.append(app_data_dict)
                        if len(deploy_params_data['result_data']) > 0 or len(comp_deploy_param_data['result_data']) > 0:
                            for result_para_data in comp_deploy_param_data['result_data']:
                                list_of_key = result_para_data[0]
                                resp_data_output = reduce(lambda res, cur: {cur: res}, reversed(list_of_key.split("'.'")),result_para_data[1])
                                merge_dict(data,resp_data_output)    
                        
                       
                        
            except ConnectionError as e:
                print (e)
    if len(deploy_uri_data) > 0:
        deploy_params['environmentAppParams']['deploy_params_list'] = deploy_uri_data 
    if len(deploy_params['environmentAppParams']) == 0: del deploy_params['environmentAppParams']
    #if len(deploy_params['commonParams']) == 0: del deploy_params['commonParams']
    merge_dict(deploy_params,data)
    
    return deploy_params


import collections
def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k,v2 in d2.items():
        v1 = d1.get(k)
        if ( isinstance(v1, collections.Mapping) and
             isinstance(v2, collections.Mapping) ):
            merge_dict(v1, v2)
        else:
            d1[k] = v2
    return d1

def merge_nested_dict(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_nested_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def searchforsubstr(dictionary, substrone, substrtwo):
    result_para, result_override , result_data = [], [] , []
    for key in dictionary:
        if type(key) != int:
            if substrtwo in key:
                key_data = key.strip("'")
                list_of_key = key_data.split("'.'")
                value = dictionary[key]
                if type(value) is str and ',' in value:
                    list_data = value.split(',')
                    list_data_without_empty = [x for x in list_data if x]
                    value = list_data_without_empty
                elif type(value) is str and (value == 'True' or value == 'False'):
                    value = (value == 'True')
                elif type(value) == str and value.isdigit():
                    value = int(value)
                result_override.append((key_data, value))
            if substrone in key and substrtwo not in key:
                key_data = key.strip("'")
                list_of_key = key_data.split("'.'")
                value = dictionary[key]
                if type(value) is str and ',' in value:
                    list_data = value.split(',')
                    list_data_without_empty = [x for x in list_data if x]
                    value = list_data_without_empty
                elif type(value) is str and (value == 'True' or value == 'False'):
                    value = (value == 'True')
                elif type(value) == str and value.isdigit():
                    value = int(value)
                result_para.append((key_data, value)) 
            if substrone  not in key and substrtwo not in key:
                key_data = key.strip("'")
                list_of_key = key_data.split("'.'")
                value = dictionary[key]
                if type(value) is str and ',' in value:
                    list_data = value.split(',')
                    list_data_without_empty = [x for x in list_data if x]
                    value = list_data_without_empty
                elif type(value) is str and (value == 'True' or value == 'False'):
                    value = (value == 'True')
                elif type(value) == str and value.isdigit():
                    value = int(value)
                result_data.append((key_data, value))
    return {'result_override':result_override,'result_para':result_para , 'result_data':result_data}

'''
def call_jenkins_job():
    """
    This function is used to call the jenkins job with required parameters
    """

    headers = dict()
    user_pass = base64.b64encode(
        bytes(JENKINS_API_ACCESS_USER + ":" + JENKINS_API_ACCESS_PSW, "utf-8")).decode("ascii")
    headers['Authorization'] = 'Basic %s' % user_pass

    # Get a CRUMB from Jenkins
    url = "https://{0}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)".\
        format(JENKINS_HOST)
    crumb = requests.get(url, headers=headers, verify=False).content
    # Convert bytes to Strings
    crumb = crumb.decode("utf-8")

    action = 'build'
    jenkins_job = 'esmt_test'

    # Form the jenkins job URL
    job_url = "https://{0}/job/{1}/{2}".format(JENKINS_HOST, jenkins_job, action)
    # Add the crumb to the header
    headers[crumb.split(":")[0]] = crumb.split(":")[1]

    print("{0}ing job {1} at jenkins server {2}".format(action[0:-1], jenkins_job, JENKINS_HOST))
    response = requests.post(job_url, headers=headers, verify=False)

    print(response.content)
    if response.status_code == 200:
        resp = {"resp": "Job {0} {1}ed successfully on the server {2}".format(jenkins_job, action,
                                                                              JENKINS_HOST)}
    else:
        resp = {"resp": "Something went wrong. Check out the response while {0}ing the job {1}:"
                        "\nResponse:{2}".format(action, jenkins_job, response.content)}
    return resp
'''
