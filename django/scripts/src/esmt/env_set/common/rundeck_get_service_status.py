"""
This moudule calls the rundeck job with the list server and client list
to get the status of the services running on them
"""
import re
from esmt.env_set.conf.properties import CLIENT_IP_MAPPING, ENV, ENV_SERVICE_LIST, \
    SERVICE_NAME_MAPPING, CLIENT_FINAL_OCTET_MAPPING
from esmt.base.lib.rundeck import RunDeck
from esmt.env_set.common.process_command import check_win_client, execute_win_command, \
    get_static_data_file_name, save_data_to_file


def get_win_client_status(env_region, store, store_octet):
    """This function get the status of the services running in windows client"""
    win_clients = check_win_client(env_region)
    store_clients = ENV[env_region][store]
    temp_dict = {}
    for win_client in win_clients:
        if win_client in store_clients:
            ip_address = store + "." + CLIENT_IP_MAPPING[env_region][win_client]
            temp_dict[win_client] = {}
            for service in ENV_SERVICE_LIST[env_region][win_client]:
                status = execute_win_command(store_octet, ip_address,
                                             SERVICE_NAME_MAPPING[service], "status", True)
                if status == "running" or status == "stopped":
                    temp_dict[win_client][service] = status
                else:
                    temp_dict[win_client][service] = "NA"
    return temp_dict


def parse_status_output(response, env_region):
    """This function parses the rundeck output and creates a json file for each store/server"""
    win_client = check_win_client(env_region)
    for store, clients in ENV[env_region].items():
        env_platform = env_region.split("-")[0]
        third_octet = store.split(".")[2]
        if env_platform == 'soc':
            env = 'soc'
        elif env_platform == 'plato' or env_platform == 'solar7':
            env = env_region
            third_octet = ("-"+clients[0] if (env_platform == 'solar7') else "")
        else:
            env = env_region

        file_name = get_static_data_file_name(env_region)
        nodes = []

        # Get the list of server/client ip in order to filter the rundeck output
        for client in clients:
            if client not in win_client:
                if env_platform == 'plato' or env_platform == 'solar7':
                    nodes.append(store)
                else:
                    nodes.append(store + "." + CLIENT_IP_MAPPING[env_region][client])

        json_dict = {}
        print(response)
        for node in nodes:
            # From the rundeck response, filter only the output for the nodes
            node_service_status = [d for d in response if d['node'] == node]
            if env_platform != 'plato' and env_platform != 'solar7':
                client = CLIENT_FINAL_OCTET_MAPPING[env_region][node.split(".")[3]]
            temp_dict = {}
            if client not in json_dict:
                json_dict.update(temp_dict)
                temp_dict[client] = {}
            print(node_service_status)

            if node_service_status:
                for entry in node_service_status:
                    if re.search(r"Authentication failure", entry['log'], re.I) or \
                            re.search(r"No route to host", entry['log'], re.I):
                        for service in ENV_SERVICE_LIST[env_region][client]:
                            temp_dict[client][service] = "NA"
                    else:
                        service = entry['log'].split(":")[0].strip()
                        if service in ENV_SERVICE_LIST[env_region][client]:
                            temp_dict[client][service] = entry['log'].split(":")[1].strip()
            else:
                # If no response is found for the client then populate the service details for the
                # clients with NA
                for service in ENV_SERVICE_LIST[env_region][client]:
                    temp_dict[client][service] = "NA"
            json_dict.update(temp_dict)

        # Get the lop service status using windows command
        if env_region.split("-")[0] == "soc":
            json_dict.update(get_win_client_status(env_region, store, third_octet))

        save_data_to_file(file_name, json_dict)


def get_service_status():
    """
    This Function generates a list of Server/Client IP address based on the properties file
    calls the rundeck job with the list nodes and after the job completes,
    it call the parse_status_output function to create the json file for each store/servers
    """
    nodes = []
    for env_region, values in ENV.items():
        win_client = check_win_client(env_region)
        for store, clients in values.items():
            for client in clients:
                if client not in win_client:
                    if env_region.split("-")[0] == 'plato' or env_region.split("-")[0] == 'solar7':
                        nodes.append(store)
                    else:
                        nodes.append(store + "." + CLIENT_IP_MAPPING[env_region][client])
    nodes = ",".join(nodes)
    # Execute the rundeck job to get the service status by providing the list of nodes
    rundeck = RunDeck("status", nodes)
    rundeck.execute_job()
    rundeck.get_output()
    # response = handleProcess.execute_rundeck_job(nodes, "status")
    # Parse the output and generate the output json file
    for env_region, values in ENV.items():
        parse_status_output(rundeck.get_response(), env_region)


if __name__ == '__main__':
    get_service_status()
