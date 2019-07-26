"""
This module calls the Rundeck job to get the status of the interface services
generates a json file with the interface service status
"""
import re
from esmt.env_set.conf.properties import INTERFACE_LIST
from esmt.env_set.common.process_command import get_static_data_file_name, save_data_to_file
from esmt.base.lib.rundeck import RunDeck


def parse_status_output(response):
    """This function parses the rundeck output and creates a json file """
    file_path = get_static_data_file_name('interface')
    json_dict = {}
    for domain, clients in INTERFACE_LIST.items():
        for node, service in clients.items():
            #if domain == "soc":
            #    key = node.split(".")[2]
            #else:
            #    key = node.split(".")[3]

            # From the rundeck response, filter only the output for the nodes
            node_service_status = [d for d in response if d['node'] == node]
            client = domain
            temp_dict = {}
            if client not in json_dict:
                json_dict.update(temp_dict)
                temp_dict[client] = {}
            print(node_service_status)

            if node_service_status:
                for entry in node_service_status:
                    if re.search(r"Authentication failure", entry['log'], re.I) or \
                            re.search(r"No route to host", entry['log'], re.I) or \
                            re.search(r"Connection timed out", entry['log'], re.I):
                        for na_service in INTERFACE_LIST[domain][node]:
                            temp_dict[client][na_service] = "NA"
                    else:
                        service = entry['log'].split(":")[0].strip()
                        if service in INTERFACE_LIST[domain][node]:
                            temp_dict[client][service] = entry['log'].split(":")[1].strip()
            else:
                # If no response is found for the client then populate the service details for the
                # clients with NA
                for service_name in INTERFACE_LIST[domain][node]:
                    temp_dict[client][service_name] = "NA"
            json_dict.update(temp_dict)
    save_data_to_file(file_path, json_dict)


def get_service_status():
    """
    This Function generates a list of Interface IP address based on the properties file
    calls the rundeck job with the list nodes and after the job completes,
    it call the parse_status_output function to create the json file
    """
    nodes = []
    for env_region, values in INTERFACE_LIST.items():
        for store, clients in values.items():
            nodes.append(store)
    nodes = ",".join(nodes)
    # Execute the rundeck job to get the service status by providing the list of nodes
    rundeck = RunDeck("interface_status", nodes)
    rundeck.execute_job()
    rundeck.get_output()
    # Parse the output and generate the output json file
    #for env_region, values in ENV.items():
    parse_status_output(rundeck.get_response())

if __name__ == '__main__':
    get_service_status()




