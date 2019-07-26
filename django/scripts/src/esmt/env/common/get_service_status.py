"""
This moudule calls the rundeck job with the list server and client list
to get the status of the services running on them
"""
import sys
from django.db import transaction
from esmt.base.lib.rundeck import RunDeck
from esmt.env.common.process_command import check_win_client, execute_win_command,\
    check_rundeck_auth_connetion_error
from esmt.env.models import Server, ServiceInstance


def get_win_client_status(win_client_list):
    """This function get the status of the services running in windows client"""

    for win_client in win_client_list:
        services_list = ServiceInstance.objects.filter(server_id__server_ip=win_client)
        with transaction.atomic():
            for service in services_list:
                service_instance = \
                    ServiceInstance.objects.get(server_id__server_ip=win_client,
                                                service_name__service_name=
                                                service.service_name.service_name)
                status = execute_win_command(win_client.split(".")[2], win_client,
                                             service.service_name.alias_name, "status", True)
                if status == "running" or status == "stopped":
                    service_status = status
                else:
                    service_status = "NA"
                service_instance.service_status = service_status
            service_instance.save()


def parse_status_output(response, env_region):
    """This function parses the rundeck output and creates a json file for each store/server"""
    store_servers = Server.objects.filter(env_type="socrates", app="env", sub_app=env_region,
                                          service_group__client_name="store")
    win_client = check_win_client("soc-" + env_region)
    for store in store_servers:
        client_list = Server.objects.filter(env_type="socrates", app="env", sub_app=env_region,
                                            store_server=store)
        nodes = [store.server_ip]
        win_client_list = []
        for client in client_list:
            if client.service_group.client_name not in win_client:
                nodes.append(client.server_ip)
            elif client.service_group.client_name in win_client:
                win_client_list.append(client.server_ip)

        for node in nodes:
            # From the rundeck response, filter only the output for the nodes
            node_service_status = [d for d in response if d['node'] == node]
            services = []
            services_list = ServiceInstance.objects.filter(server_id__server_ip=node)
            for service in services_list:
                services.append(service.service_name.service_name)
            #ping = "down"

            if node_service_status:
                for entry in node_service_status:
                    if check_rundeck_auth_connetion_error(entry):
                        ServiceInstance.objects.filter(server_id__server_ip=node,
                                                       service_name__service_name__in=services)\
                            .update(service_status="NA")
                        #ping = "down"
                    else:
                        #ping = "up"
                        service = entry['log'].split(":")[0].strip()
                        if service in services:
                            ServiceInstance.objects.filter(server_id__server_ip=node,
                                                           service_name__service_name=service)\
                                .update(service_status=entry['log'].split(":")[1].strip())
            else:
                # If no response is found for the client then populate the service details for the
                # clients with NA
                ServiceInstance.objects.filter(server_id__server_ip=node,
                                               service_name__service_name__in=services)\
                    .update(service_status="NA")
                #ServiceInstance.objects.filter(server_id__server_ip=node,
                #                               service_name__service_name="ping").update(
                 #   service_status=ping)

        # Get the lop service status using windows command
        get_win_client_status(win_client_list)


def get_service_status(env_region):
    """
    This Function generates a list of Server/Client IP address based on the properties file
    calls the rundeck job with the list nodes and after the job completes,
    it call the parse_status_output function to create the json file for each store/servers
    """
    nodes = []
    win_client = check_win_client("soc-" + env_region)
    servers = Server.objects.filter(env_type="socrates", app="env",
                                    sub_app=env_region).prefetch_related("service_group")
    for store in servers:
        if store.service_group.client_name not in win_client:
            nodes.append(store.server_ip)
    nodes = ",".join(nodes)
    # Execute the rundeck job to get the service status by providing the list of nodes
    rundeck = RunDeck("status_env", nodes)
    rundeck.execute_job()
    rundeck.get_output()
    # Parse the output and generate the output json file
    parse_status_output(rundeck.get_response(), env_region)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "r3":
            get_service_status('r3')
        elif sys.argv[1] == "r2":
            get_service_status('r2')
        else:
            print("Please enter r3 or r2 as argument")
    else:
        print("Please enter r3 or r2 as argument")
