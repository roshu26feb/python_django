"""
Author: Yogaraja Gopal
This module takes care of AJAX API requests from Front End
"""
import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from .abstract import get_request, trigger_jenkins_job, put_request,get_request_secure ,post_request_secure, put_request_secure
from .choice_list import ComponentTypeId, ComponentId, ComponentVersionId

class CompByCompTypeIdView(APIView):
    """
    This Class helps in retrieving  component By component type id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, component_type_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/component?component_type_id=" + component_type_id , request.COOKIES.get('access_token'))

        try:
            obj_list = []
            if resp.status_code == status.HTTP_200_OK:
                response_data = json.loads(resp.text)
                for data in response_data['components']:
                    obj = {}
                    obj['key'] = data['component_id']
                    obj['value'] = data['component_name']
                    obj_list.append(obj)
                return JsonResponse(obj_list, safe=False)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])

class SystemByIdView(APIView):
    """
    This Class helps in retrieving System By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system?system_id=" + system_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class SystemVersionByIdView(APIView):
    """
    This Class helps in retrieving System version By system id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_version?system_id=" + system_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])



class SystemEleCompByIdView(APIView):
    """
    This Class helps in retrieving System Element component By system version id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_version_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_element_component?system_version_id=" + system_version_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])

class SystemEleCompBySysVerIdSysEleIdView(APIView):
    """
    This Class helps in retrieving System Element component By system version id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_version_id, system_element_id, env_id, instance_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_element_component?system_version_id=" + system_version_id + '&system_element_id=' + system_element_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                obj = []
                resp_data = json.loads(resp.text)
                for data in resp_data['system_element_components']:
                    return_data = {}
                    return_data['system_element_components'] = data
                    return_data['system_element_components']['deployment_component'] = ''
                    if instance_id:
                        system_element_component_id = data['system_element_component_id']
                        resp2 = get_request_secure("/api/v1/deployment_component?system_element_component_id=" + str(system_element_component_id) , request.COOKIES.get('access_token'))
                        try:
                            if resp2.status_code == status.HTTP_200_OK:
                                resp_data2 = json.loads(resp2.text)
                                for deploy_data in resp_data2['deployment_components']:
                                    resp3 = get_request_secure("/api/v1/deployment?deployment_id=" + str(deploy_data['deployment_id']) , request.COOKIES.get('access_token'))
                                    try:
                                        if resp3.status_code == status.HTTP_200_OK:
                                            resp_data3 = json.loads(resp3.text)
                                            if int(env_id) == int(resp_data3["deployments"][0]["environment"]["environment_id"]) :
                                                if  'instance' in resp_data3["deployments"][0] and  int(instance_id) == int(resp_data3["deployments"][0]['instance']['instance_id']) :
                                                    return_data['system_element_components']['deployment_component'] = deploy_data['deployment_component_status']['status_description']
                                        elif resp3.status_code == status.HTTP_404_NOT_FOUND:
                                            return_data['system_element_components']['deployment_component'] = ''
                                    except:
                                        return JsonResponse({"error": "error"}, status=resp["status_code"])
                            elif resp2.status_code == status.HTTP_404_NOT_FOUND:
                                return_data['system_element_components']['deployment_component'] = ''
                        except:
                            return JsonResponse({"error": "error"}, status=resp["status_code"])
                    obj.append(return_data)
                return JsonResponse(obj, safe=False)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])

class SystemComponentbySysversionAndSyselemIDView(APIView):
    """
    This method handles the get request
    """
    @staticmethod
    def get(request, system_version_id, system_element_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_element_component?system_version_id=" + system_version_id +"&system_element_id=" + system_element_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                map_disable_flag = False
                # for data in resp_data["system_element_components"]:
                #     if data["component_version"]["component"]["deployment_type"]["deployment_type_id"] == 1 and data["component_version"]["component"]["component_type"]["component_type_id"] == 3:
                #         map_disable_flag = False
                #         break
                return JsonResponse({"map_disable_flag": map_disable_flag}, status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class SystemElementbyEnvIDView(APIView):
    """
    This Class helps in retrieving System Element By system id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_id, env_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_element_by_env?system_id=" + system_id + "&env_id=" + env_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                return JsonResponse(resp_data, safe=False)
        except:
            return JsonResponse({"error": "error"}, safe=False)

class SystemEleByIdView(APIView):
    """
    This Class helps in retrieving System Element By system id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_element?system_id=" + system_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class InfraById(APIView):
    """
    This Class helps in retrieving Infra Template By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, infra_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/infrastructure_template?infra_template_id=" + infra_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class ReleaseByIdView(APIView):
    """
    This Class helps in retrieving Release By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, release_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/release?release_id=" + release_id ,request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class ParameterByIdAPI(APIView):
    """
    This Class helps in retrieving Parameter By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, parameter_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/parameter?parameter_id=" + parameter_id,request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class DeploymentByEnvId(APIView):
    """
    This Class helps in retrieving Deployments By environment ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, env_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/deployment?environment_id=" + env_id, request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])

class SystemElementByEnvId(APIView):
    """
    This Class helps in retrieving Deployments By environment ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, env_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/environment?environment_id=" + env_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])

class GetLinkedItems(APIView):
    """
    This Class helps in retrieving Release By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, link_item):
        """
        This method handles the get request
        """
        if link_item == 'component_type_id':
            choices = ComponentTypeId(request.COOKIES['access_token']).get_choices()
        elif link_item == 'component_id':
            choices = ComponentId(request.COOKIES['access_token']).get_choices()
        elif link_item == 'component_version_id':
            choices = ComponentVersionId(request.COOKIES['access_token']).get_choices()
        else:
            choices = []
        return JsonResponse(choices, safe=False)


class InstanceFromEnv(APIView):
    """
    This Class helps in retrieving the list of instances related to the environment
    from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, env_id):
        """
        This method handles the get request
        """
        obj_list = []
        try:
            response = get_request_secure("/api/v1/environment?environment_id=" + env_id , request.COOKIES.get('access_token'))
            response_data = json.loads(response.text)
            if response.status_code == status.HTTP_200_OK:
                for data in response_data["environments"][0]["instances"]:
                    obj = dict()
                    obj['key'] = data["instance_id"]
                    obj['value'] = data["instance_name"]
                    obj['env_identifier'] = response_data["environments"][0]["environment_type"]["identifier"]
                    obj_list.append(obj)
        except:
            obj_list = [{'key': '', 'value': 'Error : Unable to get Instance Details'}]

        return JsonResponse(obj_list, safe=False)


class InstanceName(APIView):
    """
    This Class helps in retrieving the list of instances names from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request):
        """
        This method handles the get request
        """
        obj_list = []
        obj = dict()
        try:
            response = get_request_secure("/api/v1/instance" , request.COOKIES.get('access_token'))
            response_data = json.loads(response.text)
            if response.status_code == status.HTTP_200_OK:
                for data in response_data["instances"]:
                    obj_list.append(data["instance_name"])
            unique_obj_list = sorted(set(x.lower() for x in obj_list))
            obj["instance_names"] = unique_obj_list
        except:
            obj["Error"] = "Unable to get Instance Details"

        return JsonResponse(obj, safe=False)


class InfraFromInst(APIView):
    """
    This Class helps in retrieving the list of instances related to the environment
    from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, inst_id):
        """
        This method handles the get request
        """
        obj_list = []
        try:
            response = get_request_secure("/api/v1/instance?instance_id=" + inst_id ,request.COOKIES.get('access_token'))
            response_data = json.loads(response.text)
            if response.status_code == status.HTTP_200_OK:
                for data in response_data["instances"]:
                    obj = dict()
                    obj['key'] = data["infrastructure_template"]["infra_template_id"]
                    obj['value'] = data["infrastructure_template"]["host_template_description"]
                    obj['host'] = data["infrastructure_template"]["host_type"]["host_type_id"]
                    obj_list.append(obj)
        except:
            obj_list = [{'key': '-1', 'value': 'Error : Unable to get Instance Details'}]

        return JsonResponse(obj_list, safe=False)


class UserByIdView(APIView):
    """
    This Class helps in retrieving User By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, user_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/user?user_id=" + user_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text))
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text))
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class SystemElementDeployedVersion(APIView):
    """
    This Class helps in retrieving User By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, inst_id, se_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/system_element_deployment_version?system_element_id=" +
                           se_id + "&instance_id=" + inst_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                return JsonResponse(json.loads(resp.text))
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text))
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])

class InstanceAllocation(APIView):
    """
    This Class helps in retrieving User By ID from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, env_id, sys_id, sys_ele_id):
        """
        This method handles the get request
        """
        resp = get_request_secure("/api/v1/instance_allocation?environment_id=" +
                           env_id + "&system_id=" + sys_id + "&system_element_id=" + sys_ele_id , request.COOKIES.get('access_token'))
        #print ('====',resp.text)
        response_data = json.loads(resp.text)
        obj_list = []
        try:
            if resp.status_code == status.HTTP_200_OK:
                for data in response_data["instance_allocations"]:
                    obj = dict()
                    obj['key'] = data["instance"][0]["instance_id"]
                    obj['value'] = data["instance"][0]["instance_name"]
                    obj_list.append(obj)
                obj_list_data = list({v['key']:v for v in obj_list}.values())
                return JsonResponse(obj_list_data, safe=False)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text))
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class CallJenkinsJob(APIView):
    """
    This Class helps in Calling the jenkins job  and returns the response
    in JSON form
    """
    @staticmethod
    def get(request, mode, deployment_id, comp_id):
        """
        This method handles the get request
        """
        url = "/api/v1/deployment?deployment_id=" + deployment_id
        resp = get_request_secure(url , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                resp = json.loads(resp.text)
                deploy_params = get_deployment_parameters(request , mode, resp['deployments'][0], comp_id )
                env_type = resp["deployments"][0]["environment"]["environment_type"]["environment_type_id"]
                response = trigger_jenkins_job(deploy_params, env_type , request)
                if response == "Triggered":
                    update_status =\
                        update_deployment_status(request ,mode, deployment_id, comp_id, "approved",
                                                 "Triggered the jenkins Job",
                                                 deploy=resp['deployments'][0] )
                    if update_status == "Updated":
                        ret = {"resp": "Automated deployment has been initiated", "status":"success"}
                    else:
                        ret = {"resp": "Automated deployment has been initiated but Failed to update "
                                       "the status to In-Progress", "status":"failed"}
                elif response == "Deployment tag version missing":
                    ret = {"resp": "Failed due to deployment tag version missing" , "status":"failed"}
                else:
                    ret = {"resp": "Failed to Trigger the job" , "status":"failed"}
            else:
                ret = {"resp": "Failed to get deployment details" , "status":"failed"}
            return JsonResponse(ret, safe=False)
        except ConnectionError as e:
            return {"resp": e}


def get_deployment_parameters(request , mode, resp, comp_id=None ):
    """
    This function is used to get the deployment parameters for the deployment
    """
    deploy_params = dict()
    deploy_params["infra"] = {}
    deploy_params["infraConf"] = {}
    deploy_params["app"] = {}
    available_application, available_infra_config = [], []
    if mode == 'S':
        for deploy_comp in resp['deployment_components']:
            if deploy_comp['deployment_component_id'] == int(comp_id):
                component_id = deploy_comp["system_element_component"]["component_version"]["component"]["component_id"]
                comp_type_id = deploy_comp["system_element_component"]["component_version"]["component"]["component_type"]["component_type_id"]
                param_list = get_deployment_parameter_list(component_id, comp_type_id , request)
                comp_ver_id = deploy_comp["system_element_component"]["component_version"]["component_version_id"]
                if comp_type_id == 1:
                    available_application.append({'component_version':comp_ver_id})
                    resp['app_flag'] = True
                    resp['infra_code_flag'] = False
                    resp['infra_config_flag'] = False
                if comp_type_id == 2:
                    available_infra_config.append({'component_version':comp_ver_id})
                    resp['app_flag'] = False
                    resp['infra_code_flag'] = False
                    resp['infra_config_flag'] = True 
                if comp_type_id == 3:
                    resp['app_flag'] = False
                    resp['infra_code_flag'] = True
                    resp['infra_config_flag'] = False 
                for deploy_param in resp['deployment_parameters']:
                    if deploy_param["parameter"]["parameter_id"] in param_list:
                        if "component_type" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component_type"]["component_type_id"] == 3:
                            deploy_params['infra'][deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]
                        elif "component" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component"]["component_type"]["component_type_id"] == 3:
                            deploy_params['infra'][deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]
                        if "component_type" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component_type"]["component_type_id"] == 2:
                            deploy_params['infraConf'][deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]
                        elif "component" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component"]["component_type"]["component_type_id"] == 2:
                            if str(deploy_param["parameter"]["linked_element"]["component"]['component_id']) not in deploy_params['infraConf']:
                                deploy_params['infraConf'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])] = {}
                            deploy_params['infraConf'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])][deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]
                        if "component_type" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component_type"]["component_type_id"] == 1:
                            deploy_params['app'][deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]
                        elif "component" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component"]["component_type"]["component_type_id"] == 1:
                            if str(deploy_param["parameter"]["linked_element"]["component"]['component_id']) not in deploy_params['app']:
                                deploy_params['app'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])] = {}
                            deploy_params['app'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])][deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]
                        if "'deploymentTagVersion'" == deploy_param['parameter']['parameter_internal_name']:
                            deploy_params[deploy_param['parameter']['parameter_internal_name']] =\
                                deploy_param["deployment_parameter_value"]

    elif mode == "M":
        for deploy_param in resp['deployment_parameters']:
            if "component_type" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component_type"]["component_type_id"] == 3:
                deploy_params['infra'][deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
            elif "component" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component"]["component_type"]["component_type_id"] == 3:
                deploy_params['infra'][deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
            if "component_type" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component_type"]["component_type_id"] == 2:
                deploy_params['infraConf'][deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
            elif "component" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component"]["component_type"]["component_type_id"] == 2:
                if str(deploy_param["parameter"]["linked_element"]["component"]['component_id']) not in deploy_params['infraConf']:
                    deploy_params['infraConf'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])] = {}
                deploy_params['infraConf'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])][deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
            if "component_type" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component_type"]["component_type_id"] == 1:
                deploy_params['app'][deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
            elif "component" in deploy_param["parameter"]["linked_element"] and deploy_param["parameter"]["linked_element"]["component"]["component_type"]["component_type_id"] == 1:
                if str(deploy_param["parameter"]["linked_element"]["component"]['component_id']) not in deploy_params['app']:
                    deploy_params['app'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])] = {}
                deploy_params['app'][str(deploy_param["parameter"]["linked_element"]["component"]['component_id'])][deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
            if "'deploymentTagVersion'" == deploy_param['parameter']['parameter_internal_name']:
                deploy_params[deploy_param['parameter']['parameter_internal_name']] =\
                    deploy_param["deployment_parameter_value"]
        for deploy_comp in resp['deployment_components']:
            comp_type_id = deploy_comp["system_element_component"]["component_version"]["component"]["component_type"]["component_type_id"]
            comp_ver_id = deploy_comp["system_element_component"]["component_version"]["component_version_id"]
            if comp_type_id == 1:
                available_application.append({'component_version':comp_ver_id})
            if comp_type_id == 2:
                available_infra_config.append({'component_version':comp_ver_id})

    deploy_params["api_data_param"] = {}
    deploy_params["api_data_param"]["app"] = resp['app_flag']
    deploy_params["api_data_param"]["infra"] = resp['infra_code_flag']
    deploy_params["api_data_param"]["infraConf"] = resp['infra_config_flag']
    deploy_params["api_data_param"]["environment_id"] = str(resp['environment_id'])
    deploy_params["api_data_param"]["instance_id"] = str(resp['instance_id'])
    deploy_params["api_data_param"]["sys_elem_id"] = str(resp['system_element_id'])
    #deploy_params["api_data_param"]["system_version_id"] = str(resp['system_version_id'])
    deploy_params["api_data_param"]["available_application"] = available_application
    #deploy_params["api_data_param"]["available_infra"] = []
    deploy_params["api_data_param"]["available_infra_config"] = available_infra_config

    deploy_params["infra"]["'commonParams'.'deployment_id'"] = resp['deployment_id']

    if not resp['app_flag'] and not resp['infra_config_flag']:
        if "'commonParams'.'specs_ansible_version'" in deploy_params["infra"]: del deploy_params["infra"]["'commonParams'.'specs_ansible_version'"]

    if resp['infra_template_id'] is not None and resp['infra_code_flag']:
        url = "/api/v1/infrastructure_template?infra_template_id=" + str(resp['infra_template_id'])
        resp_data = get_request_secure(url , request.COOKIES.get('access_token'))
        try:
            if resp_data.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp_data.text)
                deploy_params["infra"]["'infrastructureEnvironmentParams'.'instance_type'"] =\
                        resp_data['infrastructure_templates'][0]['host_template_description']
        except ConnectionError as e:
            print (e)
    return deploy_params


def get_deployment_parameter_list(comp_id, comp_type_id ,request):
    """
    This method is used to get the list of deployment parameters
    """
    param_list = []
    get_parameter_list('component_id', comp_id, param_list ,request)
    get_parameter_list('component_type_id', comp_type_id, param_list , request)
    return param_list


def get_parameter_list(comp, obj_id, param_list , request):
    """
    This method is used to get the list of parameters for the object type
    """
    url = "/api/v1/parameter?" + comp + "=" + str(obj_id)
    resp = get_request_secure(url , request.COOKIES.get('access_token'))
    try:
        if resp.status_code == status.HTTP_200_OK:
            resp = json.loads(resp.text)
            for param in resp['parameters']:
                param_list.append(param['parameter_id'])
    except ConnectionError as e:
        print(e)


def update_deployment_status(request , mode, deployment_id, comp_id, dploy_status, comment, deploy=None ):
    """
    This function is used to update the deployment status and deployment component status to
    'In Progress'
    """
    try:
        resp = get_request_secure("/api/v1/status?status_type=Deployment&status_description=" +
                           dploy_status , request.COOKIES.get('access_token'))
        if resp.status_code == status.HTTP_200_OK:
            deploy_statuses = json.loads(resp.text)
            deploy_status = deploy_statuses["statuss"][0]
            data = {
                "deployment_id": deployment_id,
                "user_name": "admin",
                "deployment_remarks": comment,
                "deployment_status_id": deploy_status["status_id"]
            }

            deploy_comp_statuses = []
            if mode == "M":
                if deploy is None:
                    try:
                        resp = get_request_secure("/api/v1/deployment?deployment_id=" + str(deployment_id) , request.COOKIES.get('access_token'))
                        if resp.status_code == status.HTTP_200_OK:
                            deployment = json.loads(resp.text)
                            deploy = deployment["deployments"][0]
                    except ConnectionError:
                        deploy = dict()

                for deploy_comp in deploy['deployment_components']:
                    deploy_comp_status = dict()
                    deploy_comp_status["deployment_component_id"] =\
                        deploy_comp["deployment_component_id"]
                    deploy_comp_status["deployment_component_status_id"] = deploy_status["status_id"]
                    deploy_comp_statuses.append(deploy_comp_status)
            elif mode == "S":
                deploy_comp_statuses.append({"deployment_component_id": int(comp_id),
                                             "deployment_component_status_id":
                                                 deploy_status["status_id"]})
            if deploy_status["status_id"] == 4:
                try:
                    resp = get_request_secure("/api/v1/historic_deployment_status?deployment_id=" + str(deployment_id) + "&comp_id=" + str(comp_id) , request.COOKIES.get('access_token'))
                    print ('comp_id==', comp_id)
                    if resp.status_code == status.HTTP_200_OK:
                        pass
                except ConnectionError as e:
                    print({"error": e})
            data["deployment_component_changed_status"] = deploy_comp_statuses
            resp = put_request_secure("/api/v1/deployment", data=data , access_token=request.COOKIES.get('access_token') )
            if resp.status_code == status.HTTP_200_OK:
                return "Updated"
            else:
                return "Failed"
        else:
            return "Failed"
    except ConnectionError as e:
        print({"error": e})
        return "Failed"


class UpdateDeploymentComponentStatus(APIView):
    """
    This method is used to update the deployment component status to Complete or In-Progress
    """
    def get(self, request, mode, deployment_id, comp_id):
        """
        This method handles the get request
        """
        ret = update_deployment_status( request , mode, deployment_id, comp_id, "Completed",
                                       "Updated status from ESMT frontend" , None )
        if ret == "Updated":
            return Response({"resp": "Updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed"}, status=status.HTTP_404_NOT_FOUND)


class PerformApiCall(APIView):
    """
    This Class performs the Api call
    """
    url = None

    def get(self, request, api_object):
        """
        This method handles the get request
        """
        self.url = "/api/v1/" + api_object
        resp = get_request_secure(self.url ,  request.COOKIES.get('access_token'))
        #resp = get_request_secure(self.url)
        try:
            if resp.status_code == status.HTTP_200_OK:
                return Response(json.loads(resp.text))
            return Response({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return Response({"error": "error"}, status=resp["status_code"])


class InstanceList(APIView):
   
    """
    This Class helps in retrieving the list of instances names from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request):
        """
        This method handles the get request
        """
        response = get_request_secure("/api/v1/instance_list" , request.COOKIES.get('access_token'))
        
        resp_data = json.loads(response.text)
        return JsonResponse(resp_data, safe=False)

class InstanceListWithoutDestroyed(APIView):
   
    """
    This Class helps in retrieving the list of instances names from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request):
        """
        This method handles the get request
        """
        response = get_request_secure("/api/v1/instance_list_without_destroyed",request.COOKIES.get('access_token'))
        resp_data = json.loads(response.text)
        return JsonResponse(resp_data, safe=False)


class CompByCompTypeIdFAView(APIView):
    """
    # ESMT-922 This Class helps in retrieving  component By component type id  which are fully automated from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, component_type_id):
        """
        This method handles the get request 
        to load all components by compnent_type_id fully automated type id = 3
        """
        deployment_type_id = '3' 
        resp = get_request_secure("/api/v1/component?component_type_id=" + component_type_id + "&deployment_type_id="+deployment_type_id ,request.COOKIES.get('access_token'))

        try:
            obj_list = []
            if resp.status_code == status.HTTP_200_OK:
                response_data = json.loads(resp.text)
                for data in response_data['components']:
                    obj = {}
                    obj['key'] = data['component_id']
                    obj['value'] = data['component_name']
                    obj_list.append(obj)
                return JsonResponse(obj_list, safe=False)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])


class SystemEleCompBySysVerIdSysEleIdViewEnv(APIView):
    """
    This Class helps in retrieving System Element component By system version id from Delivery DB and returns in JSON form
    """
    @staticmethod
    def get(request, system_version_id, system_element_id, env_id, instance_id):
        """
        This method handles the get request ESMT-926
        shows elememt components by system_version_id,system_element_id,env_id,instance_id
        
        """
       
        resp = get_request_secure("/api/v1/system_element_component_env?system_version_id="+ system_version_id + '&system_element_id='+system_element_id+'&env_id='+env_id+'&instance_id='+instance_id , request.COOKIES.get('access_token'))
        try:
            if resp.status_code == status.HTTP_200_OK:
                obj = []
                resp_data = json.loads(resp.text)
                obj = resp_data
            
                return JsonResponse(obj, safe=False)
            elif resp.status_code == status.HTTP_404_NOT_FOUND:
                return JsonResponse(json.loads(resp.text), status=resp.status_code)
            return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
        except:
            return JsonResponse({"error": "error"}, status=resp["status_code"])
