"""
Author: Yogaraja Gopal
This module is contains common functions used by env app
"""
import datetime
import json
import subprocess
import re
import os
import inspect
#from django.conf import settings
import esmt.env.conf.properties as env_prop
import esmt.env.conf.properties_r2 as r2_env_prop
from esmt.env.conf.solar7_properties import SOLAR7_ENV
from esmt.env.conf.plato_properties import PLATO_ENV
from esmt.base.lib.rundeck import RunDeck


class ProcessHandler:
    """
    This class takes care of forming the command and parsing the output for start/stop status
    """
    @staticmethod
    def form_command(service_name, action):
        """
        This function is used to form the command
        """
        return 'service ' + service_name + ' ' + action

    @staticmethod
    def check_stopped_running(line):
        """
        This function is used to parse the output for start/stop status
        """
        search_run = re.search(r"running", line, re.I)
        search_stop = re.search(r"stop", line, re.I)
        status = ""
        if search_run:
            status = "running"
        if search_stop:
            status = "stopped"
        return status


def execute_win_command(server_octet, ip_addr, service_name, action, return_status=False):
    """
    This function is used to execute the windows command
    """
    # net rpc service start mysql -I 10.34.23.69 -U client69%8022
    try:
        cred = 'client69%' + env_prop.STORE_NUM[server_octet]
        process_output = subprocess.Popen(['net', 'rpc', 'service', action, service_name, '-I',
                                           ip_addr, '-U', cred], stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        resp_output = process_output.communicate()
        std_out_value, std_err_value = resp_output
        if return_status:
            std_out = std_out_value.decode().split("\n")
            for output in std_out:
                print(output)
                status = ProcessHandler.check_stopped_running(output)
                if status == "running" or status == "stopped":
                    break
            return status
    except:
        if return_status:
            return ''


def getip(thirdoctet, env, r2_r3="R3"):
    """
    This function is used to form the ip address
    """
    if r2_r3 == "R3":
        final_octet = env_prop.FINAL_OCTET[env]
    elif r2_r3 == "R2":
        final_octet = r2_env_prop.FINAL_OCTET[env]
    elif r2_r3 == "SOLAR7":
        for server, details in SOLAR7_ENV.items():
            for key, value in details.items():
                if key == 'name' and value == thirdoctet:
                    return server
    elif r2_r3 == "PLATO":
        for server, details in PLATO_ENV.items():
            for key, value in details.items():
                if key == 'name' and value == thirdoctet:
                    return server

    ip_addr = env_prop.CORE_OCTET + "." + thirdoctet + '.' + final_octet
    return ip_addr


def check_rundeck_auth_connetion_error(entry):
    """
    This function is used to check for auth error in rundeck logs
    """
    return (re.search(r"Authentication failure", entry['log'], re.I) or
            re.search(r"No route to host", entry['log'], re.I) or
            re.search(r"Connection timed out", entry['log'], re.I) or
            re.search(r"No space left on device", entry['log'], re.I))


def updatejson(service_name, action, file, client, third_octet, value=""):
    """
    This function is used to update the json file
    """
    if action == "stop":
        value = "stopping"
    elif action == "start":
        value = "starting"
    if value != "":
        # Open the json file
        file_name = get_static_data_file_name(file)
        data = get_data_from_file(file_name, True)
        # Update the JSON value
        data[client][service_name] = value
        # Write to the file
        save_data_to_file(file_name, data)


def check_win_client(env_region):
    """This function is used to provide the list of windows client based on the region provided"""
    if env_region == 'soc-r3':
        win_client = ['lop']
    elif env_region == 'soc-r2':
        win_client = ['dispense', 'dispense13', 'dispense1', 'dispense2', 'dispense3', 'dispense4',
                      'till', 'till1', 'lop', 'lop56']
    else:
        win_client = []

    return win_client


def get_current_datetime():
    """
    This function is used to get the current date and time
    """
    curr_date = datetime.datetime.now()
    return curr_date.strftime('%Y/%m/%d %H:%M:%S')


def formatted_datetime():
    """
    This function returns the formatted date and time
    """
    return datetime.datetime.strptime(get_current_datetime(), '%Y/%m/%d %H:%M:%S')


def get_time_diff_in_hrs(updated_timestamp):
    """
    This function is used to get the time difference in hours
    """
    last_update_timestamp = datetime.datetime.strptime(updated_timestamp, '%Y/%m/%d %H:%M:%S')
    current_timestamp = formatted_datetime()
    diff = current_timestamp - last_update_timestamp
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours


def get_static_data_file_path():
    """
    This function is used to get the static data file path
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe()))))
    return os.path.join(base_dir, 'static', 'env', 'data')


def get_static_data_file_name(file, ext='.json'):
    """
    This function is used to get the static data file name
    """
    file_name = file + ext
    return os.path.join(get_static_data_file_path(), file_name)


def get_data_from_file(file, full_file_path=False):
    """
    This function is used to get the data from the file
    """
    file_name = (file if full_file_path else get_static_data_file_name(file))
    with open(file_name, "r") as json_file:
        data = ({} if os.stat(file_name).st_size == 0 else json.load(json_file))
    return data


def get_data_from_json_file(file_name):
    """
    This function is used to get data from json file
    """
    if os.path.exists(file_name):
        data = get_data_from_file(file_name, True)
    else:
        data = {}
        save_data_to_file(file_name, data)
        data = get_data_from_file(file_name, True)

    data = (json.dumps('{}') if data == "" else data)
    return data


def save_data_to_file(file_name, data):
    """
    This function is used to save data to the file
    """
    static_data_file_path = get_static_data_file_path()
    if not os.path.exists(static_data_file_path):
        os.makedirs(static_data_file_path)

    with open(file_name, "w+") as json_file:
        json_file.write(json.dumps(data))


def get_job_execution_id(file, third_octet):
    """
    This function is used to get the rundeck job execution id
    """
    data = get_data_from_file(file)

    if third_octet not in data:
        data[third_octet] = {}
        data[third_octet]["execution_id"] = ""
    return data[third_octet]["execution_id"]


def update_job_execution_id(file, third_octet, job_execution_id):
    """
    This function is used to update the job execution id
    """
    file_name = get_static_data_file_name(file)
    data = get_data_from_file(file_name, True)
    if third_octet not in data:
        data[third_octet] = {}
        data[third_octet]["execution_id"] = job_execution_id
        data[third_octet]["status"] = "running"
    else:
        data[third_octet]["execution_id"] = job_execution_id
        data[third_octet]["status"] = "running"
    save_data_to_file(file_name, data)


def job_already_running(job_name):
    """
    This function is used to check if the rundeck job is already running
    """
    rundeck = RunDeck(job_name)
    return rundeck.check_job_status()


def get_job_status(job_name, job_execution_id):
    """
    This function is used to get the job status
    """
    rundeck = RunDeck(job_name, "", "", job_execution_id)
    return rundeck.get_completion_status()


def get_rundeck_log(job_name, job_execution_id, node):
    """
    This function is used to get the rundeck log
    """
    rundeck = RunDeck(job_name, "", "", job_execution_id)
    rundeck.get_output()
    entries = rundeck.get_response()
    rundeck_log = []
    for entry in entries:
        if entry['node'] == node:
            rundeck_log.append(entry['log'])
    return rundeck_log


def get_partial_log(job_name, job_execution_id, node):
    """
    This function is used to get the partial rundeck log
    """
    rundeck = RunDeck(job_name, "", "", job_execution_id)
    partial_log_entries = rundeck.get_partial_log()
    rundeck_partial_log = []
    for entry in partial_log_entries:
        if entry['node'] == node:
            rundeck_partial_log.append(entry['log'])
    return rundeck_partial_log


def check_and_kill_job(job_name, job_execution_id, log, kill_log):
    """
    This function is used to check and kill the rundeck job, if it keeps on running
    """
    rundeck = RunDeck(job_name, "", "", job_execution_id)
    status = rundeck.get_completion_status()
    if status:
        return "<b>Job Completed Successfully</b>"
    if kill_log in log:
        return "Job Abort Request Status : " + rundeck.kill_job()
    return "<b>Rundeck Job is Still Running</b>"
