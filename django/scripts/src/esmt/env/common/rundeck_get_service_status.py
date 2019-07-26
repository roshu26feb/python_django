"""
This moudule calls the rundeck job with the list server and client list
to get the status of the services running on them
"""
import json
import os
import sys
from esmt.env.conf import properties as env_prop
from esmt.env.conf import properties_r2 as r2_env_prop
from esmt.base.lib.rundeck import RunDeck
from esmt.env.common.process_command import check_win_client, execute_win_command, \
    get_static_data_file_path, check_rundeck_auth_connetion_error

THIS = sys.modules[__name__]
THIS.soc_stores = ""
THIS.final_octet = ""
THIS.final_octet_mapping = ""
THIS.service_mapping = ""
THIS.services = ""
THIS.rundeck_job = ""


def set_env(env_region):
    """This function sets the environment details"""
    THIS.soc_stores = (env_prop.SOC_STORES if env_region == "soc-r3" else r2_env_prop.SOC_STORES)
    THIS.final_octet = (env_prop.FINAL_OCTET if env_region == "soc-r3" else r2_env_prop.FINAL_OCTET)
    THIS.final_octet_mapping = (env_prop.CLIENT_FINAL_OCTET_MAPPING if env_region == "soc-r3" else
                                r2_env_prop.CLIENT_FINAL_OCTET_MAPPING)
    THIS.service_mapping = (env_prop.SERVICE_MAPPING if env_region == "soc-r3" else
                            r2_env_prop.SERVICE_MAPPING)
    THIS.services = (env_prop.SERVICES if env_region == "soc-r3" else r2_env_prop.SERVICES)


def get_win_client_status(env_region, store, store_octet):
    """This function get the status of the services running in windows client"""
    win_clients = check_win_client(env_region)
    store_clients = THIS.soc_stores[store]
    temp_dict = {}
    for win_client in win_clients:
        if win_client in store_clients:
            ip_address = store + "." + THIS.final_octet[win_client]
            temp_dict[win_client] = {}
            for service in THIS.services[win_client]:
                status = execute_win_command(store_octet, ip_address,
                                             THIS.service_mapping[service], "status", True)
                if status == "running" or status == "stopped":
                    temp_dict[win_client][service] = status
                else:
                    temp_dict[win_client][service] = "NA"
            response = os.system("ping -c 1 " + ip_address)
            if response == 0:
                temp_dict[win_client]["ping"] = "up"
            else:
                temp_dict[win_client]["ping"] = "down"
    return temp_dict


def parse_status_output(response, env_region):
    """This function parses the rundeck output and creates a json file for each store/server"""
    win_client = check_win_client(env_region)
    for store, clients in THIS.soc_stores.items():
        file_path = get_static_data_file_path()
        third_octet = store.split(".")[2]

        file_name = third_octet + ".json"
        nodes = []

        # Get the list of server/client ip in order to filter the rundeck output
        for client in clients:
            if client not in win_client:
                nodes.append(store + "." + THIS.final_octet[client])

        json_dict = {}
        for node in nodes:
            # From the rundeck response, filter only the output for the nodes
            node_service_status = [d for d in response if d['node'] == node]
            client = THIS.final_octet_mapping[node.split(".")[3]]
            temp_dict = {}
            ping = "down"
            if client not in json_dict:
                json_dict.update(temp_dict)
                temp_dict[client] = {}

            if node_service_status:
                for entry in node_service_status:
                    if check_rundeck_auth_connetion_error(entry):
                        for service in THIS.services[client]:
                            temp_dict[client][service] = "NA"
                        ping = "down"
                    else:
                        ping = "up"
                        service = entry['log'].split(":")[0].strip()
                        if service in THIS.services[client]:
                            temp_dict[client][service] = entry['log'].split(":")[1].strip()
            else:
                # If no response is found for the client then populate the service details for the
                # clients with NA
                for service in THIS.services[client]:
                    temp_dict[client][service] = "NA"
            temp_dict[client]["ping"] = ping
            json_dict.update(temp_dict)

        # Get the lop service status using windows command
        if env_region.split("-")[0] == "soc":
            json_dict.update(get_win_client_status(env_region, store, third_octet))
        with open(os.path.join(file_path, file_name), "w") as json_file:
            json_file.write(json.dumps(json_dict))


def get_service_status(env_region):
    """
    This Function generates a list of Server/Client IP address based on the properties file
    calls the rundeck job with the list nodes and after the job completes,
    it call the parse_status_output function to create the json file for each store/servers
    """
    set_env(env_region)
    nodes = []
    win_client = check_win_client(env_region)
    for store, clients in THIS.soc_stores.items():
        for client in clients:
            if client not in win_client:
                nodes.append(store + "." + THIS.final_octet[client])
    nodes = ",".join(nodes)
    # Execute the rundeck job to get the service status by providing the list of nodes
    rundeck = RunDeck("status_env", nodes)
    rundeck.execute_job()
    rundeck.get_output()
    # Parse the output and generate the output json file
    parse_status_output(rundeck.get_response(), env_region)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "soc-r3":
            get_service_status('soc-r3')
        elif sys.argv[1] == "soc-r2":
            get_service_status('soc-r2')
        else:
            print("Please enter soc-r3 or soc-r2 as argument")
    else:
        print("Please enter soc-r3 or soc-r2 as argument")
