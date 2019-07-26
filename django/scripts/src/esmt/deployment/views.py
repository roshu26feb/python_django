"""
Author: Yogaraja Gopal
This module is used to handle view for Deployment app
"""
import json
import datetime
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import status
from esmt.api.abstract import post_request, get_request, get_yamldata , get_request_secure , post_request_secure 
from esmt.api.choice_list import get_value
from .forms import RequestDeploymentForm
from django.views.decorators.csrf import csrf_exempt

def deployment(request):
    """
    This function is used to render deployment view
    """
    return render(request, 'deployment/deployment.html', {})


def deployment_request_view(request, system_element_id, system_version_id):
    """
    This function is used to render Instance update view and handle instance update form submission
    """
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['request'] = request
        form = RequestDeploymentForm(request.POST)
        if form.is_valid():
            if request.is_ajax():
                post_data = dict(request.POST.items())
                resp = get_request_secure(
                    "/api/v1/system_element_component?system_element_id=" + system_element_id +
                    "&system_version_id=" + system_version_id ,  request.COOKIES.get('access_token'))
                if resp.status_code == status.HTTP_200_OK:
                    resp_data = json.loads(resp.text)
                    sys_ele_comp_resp_data = resp_data["system_element_components"]

                    deployment_status_id = get_value("status?status_type=Deployment&"
                                                     "status_description=Awaiting%20Approval",
                                                     "statuss", "status_id" , request)
                    data = {
                        "deployment_name": form.cleaned_data["deployment_name"],
                        "system_element_id": system_element_id,
                        "system_version_id": system_version_id,
                        "planned_deployment_date": form.cleaned_data["planned_deployment_date"],
                        "requested_date": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                        "user_name": form.cleaned_data["user_name"],
                        "deployment_remarks": form.cleaned_data["deployment_remarks"],
                        "environment_id": form.cleaned_data["environment_id"],
                        "deployment_status_id": deployment_status_id,
                        "infra_code_flag": form.cleaned_data["infra_code_flag"],
                        "infra_config_flag": form.cleaned_data["infra_config_flag"],
                        "app_flag": form.cleaned_data["app_flag"],
                        "instance_name": form.cleaned_data["instance_name"]
                    }
                    data["infra_template_id"] = None
                    if form.cleaned_data["infra_template_id"]:
                        data["infra_template_id"] = form.cleaned_data["infra_template_id"]
                    deployment_components = []
                    # if form.cleaned_data["infra_code_flag"]:
                    #     infra_code_comp = get_component_by_type(sys_ele_comp_resp_data, 3)
                    #     for comp in infra_code_comp:
                    #         deploy_components = dict()
                    #         deploy_components["system_element_component_id"] = comp
                    #         deploy_components["deployment_component_status_id"] =\
                    #             deployment_status_id
                    #         deployment_components.append(deploy_components)

                    if form.cleaned_data["infra_config_flag"]:
                        #infra_config_comp = get_component_by_type(sys_ele_comp_resp_data, 2)
                        for comp in request.POST.getlist('available_infra_config'):
                            deploy_components = dict()
                            deploy_components["system_element_component_id"] = \
                                comp
                            deploy_components["deployment_component_status_id"] =\
                                deployment_status_id
                            deployment_components.append(deploy_components)

                    if form.cleaned_data["app_flag"]:
                        for comp in request.POST.getlist('available_application'):
                            deploy_components = dict()
                            deploy_components["system_element_component_id"] = \
                                comp
                            deploy_components["deployment_component_status_id"] = \
                                deployment_status_id
                            deployment_components.append(deploy_components)

                    if deployment_components:
                        data["deployment_components"] = deployment_components

                    if post_data["instance_id"] != '':
                        data["instance_id"] = post_data["instance_id"]
                    deployment_parameter = []
                    for key, value in request.POST.items():
                        param_dict = dict()
                        if len(key.split('-')) == 3:
                            value_data = request.POST.getlist(key)
                            if len(value_data) == 1:
                                string = ''.join(value_data)
                                value = string + ','
                            else:
                                value = ','.join(value_data)
                        if key.split('-')[0] == 'parameter' and value != '':
                            param_dict["parameter_id"] = key.split('-')[1]
                            param_dict["deployment_parameter_value"] = value
                            deployment_parameter.append(param_dict)

                    #if deployment_parameter:
                    data["deployment_parameters"] = deployment_parameter
                    resp = post_request_secure("/api/v1/deployment", data ,  request.COOKIES.get('access_token'))
                    if resp.status_code == status.HTTP_200_OK:
                        resp_data = json.loads(resp.text)
                        resp_data["url"] = reverse_lazy('deployment:deployment')
                        return JsonResponse(resp_data, status=resp.status_code, safe=False)
                    return JsonResponse(resp.text, status=resp.status_code, safe=False)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        resp = get_request_secure("/api/v1/system_element?system_element_id=" + system_element_id ,  request.COOKIES.get('access_token'))
        form_data = {}
        system_id = ''
        component_ids = []
        component_type_ids = []
        app_components = []
        infra_conf_components = []
        infra_components = []
        component_info = {}
        sys_element_short_name = ''
        app_comp_map = dict() 
        if resp.status_code == status.HTTP_200_OK:
            resp_data = json.loads(resp.text)
            sys_elem_resp_data = resp_data["system_elements"][0]
            form_data["system"] = sys_elem_resp_data["system"]["system_name"]
            form_data["system_id"] = sys_elem_resp_data["system"]["system_id"]
            form_data["system_element_id"] = sys_elem_resp_data["system_element_name"]
            form_data["system_version_id"] = system_version_id
            form_data["system_element_id2"] = system_element_id
            sys_element_short_name = sys_elem_resp_data["system_element_short_name"]

            system_id = sys_elem_resp_data["system"]["system_id"]

            resp = get_request_secure(
                "/api/v1/system_element_component?system_element_id=" + system_element_id +
                "&system_version_id=" + system_version_id ,  request.COOKIES.get('access_token'))
            if resp.status_code == status.HTTP_200_OK:
                resp_data = json.loads(resp.text)
                sys_ele_comp_resp_data = resp_data["system_element_components"]
                resp = get_request_secure("/api/v1/system_version?system_version_id=" +
                                   str(system_version_id) ,  request.COOKIES.get('access_token'))
                if resp.status_code == status.HTTP_200_OK:
                    resp_data = json.loads(resp.text)
                    sys_ver_resp_data = resp_data["system_versions"][0]
                    form_data["system_version"] = sys_ver_resp_data["system_version_name"]
                    sys_ele_comp = sorted(sys_ele_comp_resp_data, key = lambda i: i['install_order'])
                    component_type_ids.append(3)
                    for sys_element in sys_ele_comp:
                        component_type_ids.append(sys_element["component_version"]["component"]
                                                  ["component_type"]["component_type_id"])
                        component_ids.append(sys_element["component_version"]["component"]["component_id"])

                        if sys_element["component_version"]["component"]["component_type"]["component_type_id"] == 1:
                            app_comp = (sys_element["system_element_component_id"],
                                        sys_element["component_version"]["component"]["component_name"] )
                            app_comp_map[sys_element["component_version"]["component"]["component_id"]]= sys_element["system_element_component_id"]
                            app_components.append(app_comp)

                        if sys_element["component_version"]["component"]["component_type"]["component_type_id"] == 2:
                            app_comp = (sys_element["system_element_component_id"],
                                        sys_element["component_version"]["component"]["component_name"] )
                            app_comp_map[sys_element["component_version"]["component"]["component_id"]]= sys_element["system_element_component_id"]
                            infra_conf_components.append(app_comp)

                        if sys_element["component_version"]["component"]["component_type"]["component_type_id"] == 3:
                            app_comp = (sys_element["system_element_component_id"],
                                        sys_element["component_version"]["component"]["component_name"] )
                            app_comp_map[sys_element["component_version"]["component"]["component_id"]]= sys_element["system_element_component_id"]
                            infra_components.append(app_comp)

                        comp_id = sys_element["system_element_component_id"]
                        component_info[comp_id] = {}
                        component_info[comp_id]['deployment_type_description'] = sys_element["component_version"]["component"]["deployment_type"]["deployment_type_description"]
                        component_info[comp_id]['component_id'] = sys_element["system_element_component_id"]
                        component_info[comp_id]['component_name'] = sys_element["component_version"]["component"]["component_name"]
                        component_info[comp_id]['component_type'] = sys_element["component_version"]["component"]["component_type"]["component_type_description"]
                        component_info[comp_id]['component_version'] = sys_element["component_version"]["component_version_id"]
                        component_info[comp_id]['comp_id'] = sys_element["component_version"]["component"]["component_id"]
                        #component_type_ids.append(3)
        form = RequestDeploymentForm(initial=form_data, system_id=str(system_id),
                                     component_ids=component_ids, app_comp_map=app_comp_map,
                                     component_type_ids=set(component_type_ids), app_components=app_components,
                                     sys_element_short_name=sys_element_short_name, infra_conf_components=infra_conf_components,infra_components=infra_components,component_info=component_info , request=request)
    return render(request, 'deployment/deployment_request.html', {'form': form,'component_info':json.dumps(component_info)})


def get_component_by_type(sys_element_components, type_id):
    """
    This function is used to return the list of component by type
    """
    component_list = []
    for sys_comp in sys_element_components:
        if sys_comp["component_version"]["component"]["component_type"]["component_type_id"] ==\
                type_id:
            component_list.append(sys_comp["system_element_component_id"])
    return component_list


@csrf_exempt
def yamlgeneration(request):
    """
    yaml generation function
    """
    json_data = request.body
    resp_data = json.loads(json_data.decode('UTF-8'))
    yaml_content = get_yamldata(resp_data , request)
    return HttpResponse(yaml_content, content_type="text/plain")
