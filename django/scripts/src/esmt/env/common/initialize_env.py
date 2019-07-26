"""
Author: Yogaraja Gopal
This module is used to initialize the env app - create table entries based on the properties file
"""
import os
from django.db import transaction
from esmt.env.models import Server, ServiceGroup, Services, ServiceInstance
from esmt.env.conf import properties as prop
from esmt.env.conf import properties_r2 as prop_r2
from esmt.env.common import process_command as proc_cmd


def create_service_group_entry(soc_clients, region, service_list, service_mapping):
    """
    This function is used to create service Group entry
    """
    with transaction.atomic():
        for soc_client in soc_clients:
            service_group, created_group = ServiceGroup.objects.get_or_create(
                client_name=soc_client,
                region=region
            )
            for service_name in service_list[soc_client]:
                services, created_service = Services.objects.get_or_create(
                    service_group=service_group,
                    service_name=service_name,
                    alias_name=service_mapping[service_name]
                )
        services.save()


def create_server_entry(sub_app, soc_stores, final_octect, service_list):
    """
    This function is used to create server entry
    """
    with transaction.atomic():
        for three_octet, soc_client in soc_stores.items():
            service_group = ServiceGroup.objects.get(client_name="store", region=sub_app)
            store_server, created_server = Server.objects.get_or_create(
                server_ip=three_octet + "." + final_octect["store"],
                env_type="socrates",
                app="env",
                sub_app=sub_app,
                service_group=service_group
            )
            for client in soc_client:
                if client != "store":
                    service_group = ServiceGroup.objects.get(client_name=client, region=sub_app)
                    server, created_server = Server.objects.get_or_create(
                        server_ip=three_octet + "." + final_octect[client],
                        env_type="socrates",
                        app="env",
                        sub_app=sub_app,
                        service_group=service_group,
                        store_server=store_server
                    )
                elif client == "store":
                    server = store_server

                for service in service_list[client]:
                    service_name = Services.objects.get(service_group=service_group,
                                                        service_name=service)
                    service_instance, created_service = ServiceInstance.objects.get_or_create(
                        server_id=server,
                        service_name=service_name,
                        service_status="stopped"
                    )
            service_instance.save()


def env_initialize():
    """
    This function is used to initialize env
    """
    soc_clients_r2 = ['store',
                      'testroom', 'testroom1', 'testroom2', 'testroom3', 'testroom4', 'testroom5',
                      'dispense', 'dispense1', 'dispense2', 'dispense3', 'dispense13',
                      'till', 'till1',
                      'lop', 'lop56']

    soc_clients_r3 = ['store',
                      'testroom', 'testroom1', 'testroom2', 'testroom3', 'testroom4', 'testroom5',
                      'dispense', 'dispense1', 'dispense2', 'dispense3',
                      'till', 'till1',
                      'lop']

    create_service_group_entry(soc_clients_r2, "r2", prop_r2.SERVICES, prop_r2.SERVICE_MAPPING)
    create_service_group_entry(soc_clients_r3, "r3", prop.SERVICES, prop.SERVICE_MAPPING)
    create_server_entry("r3", prop.SOC_STORES, prop.FINAL_OCTET, prop.SERVICES)
    create_server_entry("r2", prop_r2.SOC_STORES, prop_r2.FINAL_OCTET, prop_r2.SERVICES)

    required_files = ['mount', 'mount_r2', 'plato_mount', 'solar7', 'facts', 'facts_r2',
                      'replication', 'replication_r2']

    for file in required_files:
        file_name = proc_cmd.get_static_data_file_name(file)
        if os.path.exists(file_name):
            pass
        else:
            data = {}
            proc_cmd.save_data_to_file(file_name, data)
