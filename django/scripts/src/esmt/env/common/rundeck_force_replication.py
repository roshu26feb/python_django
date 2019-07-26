"""
Author: Yogaraja Gopal
This module is used to run force replication using rundeck
"""
import os
import json
from django.http import HttpResponse, JsonResponse
import esmt.env.conf.properties as env_prop
from esmt.base.lib.rundeck import RunDeck
from esmt.env.common.process_command import get_job_execution_id, get_job_status, \
    job_already_running, update_job_execution_id, get_rundeck_log, get_static_data_file_name, \
    save_data_to_file, get_data_from_file


def handle_force_replication_request(third_octet, action):
    """
    This function is used to handle run/status of force replication status
    """
    node = env_prop.CORE_OCTET + "." + third_octet + ".1"
    file = 'replication_status'

    file_name = get_static_data_file_name(file)
    if os.path.exists(file_name):
        data = get_data_from_file(file_name, True)
    else:
        data = {}
        save_data_to_file(file_name, data)
        data = get_data_from_file(file_name, True)

    data = (json.dumps('{}') if data == "" else data)

    if third_octet not in data:
        data[third_octet] = {}

    job_execution_id = get_job_execution_id(file, third_octet)
    prev_job_status = True
    if job_execution_id:
        prev_job_status = get_job_status('replication', job_execution_id)

    if prev_job_status and action == "run":
        if job_already_running('replication') == "0":
            # Execute the Rundeck job to start/stop the service
            rundeck = RunDeck('replication', node)
            rundeck.execute_job()
            execution_id = rundeck.get_job_execution_id()
            if execution_id:
                update_job_execution_id(file, third_octet, execution_id)
            return HttpResponse("Rundeck Job Started")
        else:
            return HttpResponse("Another Force Replication job is already Running,"
                                " Please run once it is completed")
    elif action == "status":
        if prev_job_status:
            if job_execution_id:
                return JsonResponse(get_rundeck_log('replication', job_execution_id, node),
                                    safe=False)
            return JsonResponse(["No previous rundeck execution found", "Please Note: ",
                                 "Only Logs for the Jobs ran from ESMT can be viewed here "],
                                safe=False)
        return JsonResponse(["Job is currently running"], safe=False)
    else:
        return HttpResponse("Force Replication already running")
