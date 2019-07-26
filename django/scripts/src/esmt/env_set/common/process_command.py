"""
It is a support file which handling some common functions
"""
import json
import subprocess
import re
import inspect
import os
from esmt.env_set.conf.properties import STORE_NUM, CLIENT_IP_MAPPING, ENV


def check_stopped_running(line):
    """This function is used to check whether running or stop word is present in the line provided
    """
    search_run = re.search(r"running", line, re.I)
    search_stop = re.search(r"stop", line, re.I)
    status = ""
    if search_run:
        status = "running"
    if search_stop:
        status = "stopped"
    return status


def execute_win_command(env_region, ipaddress, service_name, action, return_status=False):
    """This is function is used to execute windows related command - net rpc
       Example : net rpc service start mysql -I 10.34.23.69 -U client69%8022
    """
    try:
        for env_ip, clients in ENV[env_region].items():
            store_num = STORE_NUM[env_ip]
        cred = 'client69%' + store_num
        sub_process_response = subprocess.Popen(['net', 'rpc', 'service', action, service_name,
                                                 '-I', ipaddress, '-U', cred],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = sub_process_response.communicate()
        std_out_value, std_err_value = output
        if return_status:
            std_out = std_out_value.decode().split("\n")
            for out_put in std_out:
                status = check_stopped_running(out_put)
                if status == "running" or status == "stopped":
                    break
            return status
    except:
        if return_status:
            return ''


def getip(client, env_region):
    """This function is used to form IP address based on the input provided """
    for env_ip, clients in ENV[env_region].items():
        ip_address = env_ip + '.' + CLIENT_IP_MAPPING[env_region][client]
    return ip_address


def updatejson(service_name, action, file_name, env):
    """This Function is used to update the json file provided as input parameter with the
    supplied values"""
    if action == "stop":
        value = "stopping"
    elif action == "start":
        value = "starting"
    else:
        value = action

    if value != "":
        # Open the json file
        abs_file_name = get_static_data_file_name(file_name)
        data = get_data_from_file(abs_file_name, True)
        # Update the JSON value
        data[env][service_name] = value
        # Write to the file
        save_data_to_file(abs_file_name, data)


def check_win_client(env_region):
    """This function is used to provide the list of windows client based on the region provided"""
    soc_r3 = ['soc-uk']
    soc_r2 = ['soc-roi', 'soc-nl', 'soc-esp']
    if env_region in soc_r3:
        win_client = ['lop']
    elif env_region in soc_r2:
        win_client = ['dispense', 'dispense13', 'dispense1', 'dispense2', 'dispense3', 'dispense4',
                      'till', 'till1', 'lop', 'lop56']
    else:
        win_client = []

    return win_client


def get_static_data_file_path():
    """
    This function is used to get static data file path
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe()))))
    return os.path.join(base_dir, 'static', 'env_set', 'data')


def get_static_data_file_name(file_name, ext='.json'):
    """
    This function is used to get static data from file
    """
    file_name_with_ext = file_name + ext
    return os.path.join(get_static_data_file_path(), file_name_with_ext)


def get_data_from_file(file_name, full_file_path=False):
    """
    This function is used to get data from file
    """
    abs_file_name = (file_name if full_file_path else get_static_data_file_name(file_name))
    with open(abs_file_name, "r") as json_file:
        data = ({} if os.stat(abs_file_name).st_size == 0 else json.load(json_file))
    return data


def save_data_to_file(file_name, data):
    """
    This function is used to save data to file
    """
    with open(file_name, "w") as json_file:
        json_file.write(json.dumps(data))
