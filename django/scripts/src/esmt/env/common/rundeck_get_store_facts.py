"""
Author: Yogaraja Gopal
This module is used to Get Store Facts using rundeck
"""
import sys
from esmt.env.conf import properties as env_prop
from esmt.env.conf import properties_r2 as r2_env_prop
from esmt.env.conf.properties import STORE_FACTS
import esmt.env.common.process_command as proc_cmd
from esmt.base.lib.rundeck import RunDeck


def region_name(region_code):
    """
    This function returns the region name based on region code
    """
    region_code_name = {
        '020304': 'UK',
        '020321': 'scottish',
        '020322': 'Nothern Ireland',
        '020323': 'Guernsey & Jersey',
        '1315': 'Spain',
        '0218': 'ROI',
        '0708': 'NL'
    }
    try:
        region = region_code_name[region_code]
    except KeyError:
        region = "Unknown Region"
    return region


def get_filename(r2_r3):
    """
    This function returns the file name based on env
    """
    file = ("facts" if r2_r3 == "r3" else "facts_r2")
    file_name = proc_cmd.get_static_data_file_name(file)
    return file_name


def parse_fact_details(response, node):
    """
    This function returns the parsed fact details
    """
    node_mount_detail = [d for d in response if d['node'] == node]
    facts = []
    for fact in STORE_FACTS.keys():
        facts.append(fact)
    fact_dict = {}
    if node_mount_detail:
        for entry in node_mount_detail:
            if proc_cmd.check_rundeck_auth_connetion_error(entry):
                for fact in facts:
                    fact_dict[fact] = "NA"
                return fact_dict
            else:
                fact = entry['log'].split(":")[0].strip()
                if fact in facts:
                    if fact == 'regioncode':
                        fact_dict[fact] = region_name(entry['log'].split(":")[1].strip())
                    else:
                        fact_dict[fact] = entry['log'].split(":")[1].strip()

        return fact_dict
    return "No matching node found in response"


def get_current_store_facts(r2_r3, third_octet, file_name, data):
    """
    This function returns current store facts
    """
    node = proc_cmd.getip(third_octet, 'store', r2_r3.upper())
    arg_string = '-facts facts ' + ' -region ' + r2_r3
    rundeck = RunDeck("facts", node, arg_string)
    rundeck.execute_job()
    execution_id = rundeck.get_job_execution_id()
    if execution_id:
        rundeck.get_output()
        store_facts = parse_fact_details(rundeck.get_response(), node)
        data[third_octet]['timestamp'] = proc_cmd.get_current_datetime()
        data[third_octet]["facts"] = store_facts
        proc_cmd.save_data_to_file(file_name, data)
        return store_facts
    return '[]'


def get_store_facts(r2_r3, third_octet):
    """
    This function returns the store facts
    """
    file_name = get_filename(r2_r3)
    data = proc_cmd.get_data_from_json_file(file_name)

    if third_octet not in data:
        data[third_octet] = {}

    if "timestamp" in data[third_octet] and data[third_octet]["facts"]:
        updated_timestamp = data[third_octet]["timestamp"]
        hours = proc_cmd.get_time_diff_in_hrs(updated_timestamp)
        if hours >= 5:
            return get_current_store_facts(r2_r3, third_octet, file_name, data)
        return data[third_octet]["facts"]
    return get_current_store_facts(r2_r3, third_octet, file_name, data)


def get_list_of_store(r2_r3):
    """
    This function returns the list of stores based on the region
    """
    soc_stores = (env_prop.SOC_STORES if r2_r3 == "r3" else r2_env_prop.SOC_STORES)
    final_octet = (env_prop.FINAL_OCTET if r2_r3 == "r3" else r2_env_prop.FINAL_OCTET)
    nodes = []
    for store, clients in soc_stores.items():
        for client in clients:
            if client == "store":
                nodes.append(store + "." + final_octet[client])
    return nodes


def get_server_group_facts(r2_r3):
    """
    This Function generates a list of Server/Client IP address based on the properties file
    calls the rundeck job with the list nodes and after the job completes,
    it call the parse_status_output function to create the json file for each store/servers
    """
    store_list = get_list_of_store(r2_r3)
    nodes = ",".join(store_list)
    # Execute the rundeck job to get the service status by providing the list of nodes
    arg_string = '-facts facts ' + ' -region ' + r2_r3
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
        store_facts = parse_fact_details(rundeck.get_response(), store)
        data[third_octet]['timestamp'] = proc_cmd.get_current_datetime()
        data[third_octet]["facts"] = store_facts
        proc_cmd.save_data_to_file(file_name, data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "r3":
            get_server_group_facts('r3')
        elif sys.argv[1] == "r2":
            get_server_group_facts('r2')
        else:
            print("Please enter r3 or r2 as argument")
    else:
        print("Please enter r3 or r2 as argument")
