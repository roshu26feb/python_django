"""
Author: Yogaraja Gopal
This module is used to get mount details from each store server
"""
import sys
from esmt.env.conf import properties as env_prop
from esmt.env.conf import properties_r2 as r2_env_prop
from esmt.env.conf import plato_properties as plato_prop
from esmt.env.conf import solar7_properties as solar7_prop
import esmt.env.common.process_command as proc_cmd
from esmt.base.lib.rundeck import RunDeck


def get_list_of_store(r2_r3):
    """
    This function is used to get list of stores
    """
    nodes = []
    if r2_r3 == "plato":
        for ip_addr, value in plato_prop.PLATO_ENV.items():
            nodes.append(ip_addr)
    elif r2_r3 == "solar7":
        for ip_addr, value in solar7_prop.SOLAR7_ENV.items():
            nodes.append(ip_addr)
    elif r2_r3 == "r2" or r2_r3 == "r2":
        soc_stores = (env_prop.SOC_STORES if r2_r3 == "r3" else r2_env_prop.SOC_STORES)
        final_octet = (env_prop.FINAL_OCTET if r2_r3 == "r3" else r2_env_prop.FINAL_OCTET)
        for store, clients in soc_stores.items():
            for client in clients:
                if client == "store":
                    nodes.append(store + "." + final_octet[client])
    return nodes


def get_filename(r2_r3):
    """
    This function is used to get the file name
    """
    if r2_r3 == "r3":
        file = "mount"
    elif r2_r3 == "r2":
        file = "mount_r2"
    elif r2_r3 == "solar7":
        file = "solar7"
    elif r2_r3 == "plato":
        file = "plato_mount"

    file_name = proc_cmd.get_static_data_file_name(file)
    return file_name


def parse_mount_details(response, node):
    """
    This function is used to parse the mount details
    """
    node_mount_detail = [d for d in response if d['node'] == node]
    if node_mount_detail:
        mount = []
        for entry in node_mount_detail:
            if proc_cmd.check_rundeck_auth_connetion_error(entry):
                return mount
            else:
                entry = entry['log'].strip()
                mount.append(entry.split())
        return mount
    return "No Matching Node found in response"


def get_current_mount_details(r2_r3, third_octet, file_name, data):
    """
    This function is used to get the current mount details
    """
    node = proc_cmd.getip(third_octet, 'store', r2_r3.upper())
    print(node)
    arg_string = '-facts mount'
    rundeck = RunDeck("facts", node, arg_string)
    rundeck.execute_job()
    execution_id = rundeck.get_job_execution_id()
    if execution_id:
        rundeck.get_output()
        mount_data = parse_mount_details(rundeck.get_response(), node)
        data[third_octet]['timestamp'] = proc_cmd.get_current_datetime()
        data[third_octet]["mount"] = mount_data
        proc_cmd.save_data_to_file(file_name, data)
        return mount_data
    return '[]'


def get_mount_details(r2_r3, third_octet):
    """
    This function is used to get the mount details
    """
    file_name = get_filename(r2_r3)
    data = proc_cmd.get_data_from_json_file(file_name)

    if third_octet not in data:
        data[third_octet] = {}

    if "timestamp" in data[third_octet] and data[third_octet]["mount"]:
        updated_timestamp = data[third_octet]["timestamp"]
        hours = proc_cmd.get_time_diff_in_hrs(updated_timestamp)
        if hours >= 5:
            return get_current_mount_details(r2_r3, third_octet, file_name, data)
        return data[third_octet]["mount"]
    return get_current_mount_details(r2_r3, third_octet, file_name, data)


def get_server_mount_details(r2_r3):
    """
    This Function generates a list of Server/Client IP address based on the properties file
    calls the rundeck job with the list nodes and after the job completes,
    it call the parse_status_output function to create the json file for each store/servers
    """
    store_list = get_list_of_store(r2_r3)
    nodes = ",".join(store_list)
    # Execute the rundeck job to get the service status by providing the list of nodes
    arg_string = '-facts mount ' + ' -region ' + r2_r3
    rundeck = RunDeck("facts", nodes, arg_string)
    rundeck.execute_job()
    rundeck.get_output()
    # Parse the output and generate the output json file
    file_name = get_filename(r2_r3)
    data = proc_cmd.get_data_from_json_file(file_name)

    for store in store_list:
        third_octet = store.split(".")[2]
        if third_octet not in data:
            data[third_octet] = {}
        store_mount = parse_mount_details(rundeck.get_response(), store)
        data[third_octet]['timestamp'] = proc_cmd.get_current_datetime()
        data[third_octet]["mount"] = store_mount
        proc_cmd.save_data_to_file(file_name, data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "r3":
            get_server_mount_details('r3')
        elif sys.argv[1] == "r2":
            get_server_mount_details('r2')
        else:
            print("Please enter r3 or r2 as argument")
    else:
        print("Please enter r3 or r2 as argument")
