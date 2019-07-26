"""
Author: Yogaraja Gopal
Comment: This module is used to handle AJAX calls from frontend for env_set app
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import login_required
from esmt.base.lib.rundeck import RunDeck
from .conf import properties as env_prop
from .common import process_command as proc_cmd


def get_ping_data(request):
    """
    This function returns the server ping status
    """
    if request.method == 'GET':
        data = proc_cmd.get_data_from_file('ping')
        return JsonResponse(data)
    return "Method not supported"


def get_server_data_file(request, file_name):
    """
    This function returns the server data
    """
    if request.method == 'GET':
        data = proc_cmd.get_data_from_file(file_name)
        return JsonResponse(data)
    return "Method not supported"


@csrf_exempt
@login_required
def process_soc_requests(request, env_region, service_name, action, client):
    """ This function handles the Socrates service start stop request """
    if request.method == 'GET':
        #domain = "soc"
        node = proc_cmd.getip(client, env_region)
        win_client = proc_cmd.check_win_client(env_region)
        file = env_region
        if client in win_client:
            # Handle windows specific commands
            proc_cmd.execute_win_command(env_region, node,
                                         env_prop.SERVICE_NAME_MAPPING[service_name], action)
            proc_cmd.updatejson(service_name, action, file, client)
        else:
            # Execute the Rundeck job to start/stop the service
            argstring = '-domain ' + env_region + ' -action ' + action + ' -service ' + \
                        env_prop.SERVICE_NAME_MAPPING[service_name]
            rundeck = RunDeck('start_stop', node, argstring)
            rundeck.execute_job()
            rundeck.get_output()
            status = rundeck.get_service_status()
            proc_cmd.updatejson(service_name, status, file, client)
        return HttpResponse("completed")
    return "Method not supported"


@csrf_exempt
@login_required
def process_plato_requests(request, plato_region, service_name, action):
    """ This function handles the Plato service start stop request """
    if request.method == 'GET':
        node = ""
        for key in env_prop.ENV[plato_region].keys():
            node = key

        if node != "":
            file = plato_region
            # Execute the Rundeck job to start/stop the service
            arg_string = '-domain ' + plato_region + ' -action ' + action + ' -service ' + \
                         env_prop.SERVICE_NAME_MAPPING[service_name]
            rundeck = RunDeck('start_stop', node, arg_string)
            rundeck.execute_job()
            rundeck.get_output()
            status = rundeck.get_service_status()
            proc_cmd.updatejson(service_name, status, file, "server")
            return HttpResponse("completed")
        return HttpResponse("Invalid Node/Node not found")
    return "Method not supported"


@csrf_exempt
@login_required
def process_aristo_requests(request, service_name, action):
    """ This function handles the Aristotle service start stop request """
    if request.method == 'GET':
        node = proc_cmd.getip('activemq', 'aristotle')
        file = 'aristotle'

        # Execute the Rundeck job to start/stop the service
        argstring = '-domain aristotle ' + '-action ' + action + ' -service ' + \
                    env_prop.SERVICE_NAME_MAPPING[service_name]
        rundeck = RunDeck('start_stop', node, argstring)
        rundeck.execute_job()
        rundeck.get_output()
        status = rundeck.get_service_status()
        proc_cmd.updatejson(service_name, status, file, "activemq")
        return HttpResponse("completed")
    return "Method not supported"


@csrf_exempt
@login_required
def process_solar7_requests(request, solar7_region, service_name, action):
    """ This function handles the Plato service start stop request """
    if request.method == 'GET':
        region = solar7_region.split("-")[1]
        node = ""
        for ip_address, regions in env_prop.ENV['solar7'].items():
            if regions[0] == region:
                node = ip_address

        if node != "":
            file = solar7_region
            # Execute the Rundeck job to start/stop the service
            arg_string = '-domain ' + solar7_region + ' -action ' + action + ' -service ' + \
                         env_prop.SERVICE_NAME_MAPPING[service_name]
            rundeck = RunDeck('start_stop', node, arg_string)
            rundeck.execute_job()
            rundeck.get_output()
            status = rundeck.get_service_status()
            proc_cmd.updatejson(service_name, status, file, region)
            return HttpResponse("completed")
        return HttpResponse("Invalid Node/Node not found")
    return "Method not supported"


@csrf_exempt
def get_interface_status(request):
    """ This function responds back with the interface json file """
    if request.method == 'GET':
        plato_aus_fin_services = ['platoContainer', 'platoBroker', 'plato-broker']
        data = proc_cmd.get_data_from_file('aristotle')
        service_return = data["activemq"]

        data = proc_cmd.get_data_from_file('plato-fin')
        plato_fin_service = data["server"]

        data = proc_cmd.get_data_from_file('plato-aus')
        plato_aus_service = data["server"]

        int_return = proc_cmd.get_data_from_file('interface')

        for service, status in service_return.items():
            int_return["aristotle"][service] = status

        if "plato-fin" not in int_return:
            int_return["plato-fin"] = {}
            for service, status in plato_fin_service.items():
                if service in plato_aus_fin_services:
                    int_return["plato-fin"][service] = status

        if "plato-aus" not in int_return:
            int_return["plato-aus"] = {}
            for service, status in plato_aus_service.items():
                if service in plato_aus_fin_services:
                    int_return["plato-aus"][service] = status

        return JsonResponse(int_return)
    return "Method not supported"
