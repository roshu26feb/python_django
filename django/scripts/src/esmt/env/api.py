"""
Author : Yogaraja Gopal
THis module is used to handle api requests from frontend for env App
"""
import os
import time
import re
import json
#from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from esmt.base.lib.rundeck import RunDeck
from esmt.api.abstract import get_request
from .conf import properties as env_prop
from .common import process_command as proc_cmd
from .common.rundeck_get_mount_details import get_mount_details
from .common.rundeck_utils_details import get_installed_utils_details
from .common.rundeck_get_store_facts import get_store_facts
from .common.rundeck_get_eod_log import get_eod_logs
from .common.rundeck_exec_script import execute_script
#from .models import Server, ServiceInstance


@csrf_exempt
def server_status(request, third_octet):
    """
    This api is to handle server ping status
    """
    if request.method == 'GET':
        hostname = env_prop.CORE_OCTET + "." + third_octet + ".1"
        response = os.system("ping -c 1 " + hostname)
        css_class = "btn-danger"
        if response == 0:
            css_class = "btn-success"
        return HttpResponse(css_class)
    return "Un-supported Method"


@csrf_exempt
def get_service_status(request, third_octet):
    """
    This api is to handle server/client service status
    """
    if request.method == 'GET':
        data = proc_cmd.get_data_from_file(third_octet)
        return JsonResponse(data)
    return "Un-supported Method"


@csrf_exempt
def mount_detail_request(request, r2_r3, third_octet):
    """
    This api is to handle Store server mount detail request
    """
    if request.method == 'GET':
        return JsonResponse(get_mount_details(r2_r3, third_octet), safe=False)
    return "Un-supported Method"


def rundeck_repl_detail_request(request, third_octet, r2_r3):
    """
    This api is to handle replication detail request
    """
    if request.method == 'GET':
        file_name = ('replication' if r2_r3 == 'r3' else 'replication_r2')
        file_name = proc_cmd.get_static_data_file_name(file_name)
        soc_node = env_prop.CORE_OCTET + "." + third_octet + ".1"
        nodes = ["10.2.166.23", soc_node]
        arg_string = '-facts replication' + ' -store_num ' + env_prop.STORE_NUM[third_octet]
        rundeck = RunDeck('facts', ",".join(nodes), arg_string)
        rundeck.execute_job()
        execution_id = rundeck.get_job_execution_id()
        if execution_id:
            rundeck.get_output()
            response = rundeck.get_response()
            rep_log_dict = {}
            for node in nodes:
                node_repl_log = [d for d in response if d['node'] == node]

                if node_repl_log:
                    for entry in node_repl_log:
                        if re.search(r"Authentication failure", entry['log'], re.I) or \
                                re.search(r"No route to host", entry['log'], re.I):
                            rep_log = "Failed to connect to server"
                        elif re.search(r"tail: cannot open input", entry['log'], re.I):
                            rep_log = ""
                        else:
                            rep_log = entry['log'].strip()

                    if node == '10.2.166.23':
                        if rep_log == "":
                            rep_log = "File for the store " + env_prop.STORE_NUM[third_octet] + \
                                      " Not found in plato "
                        rep_log_dict["plato_log"] = rep_log
                    elif node == soc_node:
                        rep_log_dict["soc_log"] = rep_log

        data = proc_cmd.get_data_from_file(file_name, True)
        if third_octet in data:
            data[third_octet] = rep_log_dict
        else:
            data[third_octet] = {}
            data[third_octet] = rep_log_dict
        proc_cmd.save_data_to_file(file_name, data)
        return JsonResponse(rep_log_dict)
    return "Un-supported Method"


def process_replication_requests(request, third_octet, action):
    """
    This function handles the running/getting status of Force Replication using Rundeck
    """
    if request.method == 'GET':
        return execute_script('replication', third_octet, "R3", action)
    return "Un-supported Method"


def process_eod_log_requests(request, third_octet):
    """
    This function handles request to get the EOD logs using Rundeck
    """
    if request.method == 'GET':
        return JsonResponse(get_eod_logs(third_octet), safe=False)
    return "Un-supported Method"


def utils_detail_request(request, third_octet):
    """
    This api is to handle Utils installed on store server
    """
    if request.method == 'GET':
        return JsonResponse(get_installed_utils_details(third_octet), safe=False)
    return "Un-supported Method"


def fact_detail_request(request, third_octet, r2_r3):
    """
    This function handles the get Store facts request
    """
    if request.method == 'GET':
        return JsonResponse(get_store_facts(r2_r3, third_octet), safe=False)
    return "Un-supported Method"


@csrf_exempt
@login_required
def process_service_action(request, env_region, service_name, action, third_octet, client):
    """
    This function handles the Socrates service start stop request
    """
    if request.method == 'GET':
        print(request.user.username)
        filename = proc_cmd.get_static_data_file_name('audit', '.log')
        file = open(filename, "w")
        file.write(time.strftime("%c") + " service : " + service_name + " > " + action + " by " +
                   request.user.username + " On Store Server " + third_octet)
        file.close()

        node = proc_cmd.getip(third_octet, client, env_region.upper())
        win_client = proc_cmd.check_win_client("soc-" + env_region)
        file = third_octet
        service_status = ""
        if client in win_client:
            # Handle windows specific commands
            proc_cmd.execute_win_command(third_octet, node, env_prop.SERVICE_MAPPING[service_name],
                                         action)
            proc_cmd.updatejson(service_name, action, file, client, third_octet)
            action = 'status'
            service_status = proc_cmd.execute_win_command(third_octet, node,
                                                          env_prop.SERVICE_MAPPING[service_name],
                                                          action, True)
            proc_cmd.updatejson(service_name, action, file, client, third_octet, service_status)
        else:
            # Execute the Rundeck job to start/stop the service
            argstring = '-domain soc-' + env_region + ' -action ' + action + ' -service ' + \
                        env_prop.SERVICE_MAPPING[service_name]
            rundeck = RunDeck('start_stop', node, argstring)

            rundeck.execute_job()
            proc_cmd.updatejson(service_name, action, file, client, third_octet)
            rundeck.get_output()
            service_status = rundeck.get_service_status()
            action = 'status'
            proc_cmd.updatejson(service_name, action, file, client, third_octet, service_status)
        return HttpResponse(service_name + " is " + service_status)
    return "Un-supported Method"


@login_required
def restart_store_comms(request, third_octet, action):
    """
    This function is used to handle store comms restart request
    """
    if request.method == 'GET':
        return execute_script("lop_store_comms_fix", third_octet, "R3", action)
    return "Un-supported Method"


class EnvironmentView(APIView):
    """
    This Class is used to handle Environment View
    """
    def get(self, request):
        """
        This function is used to handle get request
        """
        resp = get_request_secure("/api/v1/environment" , request.COOKIES.get('access_token'))
        if resp.status_code == status.HTTP_200_OK:
            return JsonResponse(json.loads(resp.text))
        return JsonResponse({"error": "Failed to get response"}, status=resp.status_code)
