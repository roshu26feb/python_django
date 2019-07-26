"""
Author: Yogaraja Gopal
Comment: This module is used to check whether a server is pingable using rundeck
"""
from esmt.base.lib.rundeck import RunDeck
from esmt.env_set.conf.properties import PING_ENV_LIST
from esmt.env_set.common.process_command import get_static_data_file_name, save_data_to_file

LIST_OF_NODES = ['rundeck', '10.243.96.12', '10.243.96.5', '10.243.96.7', '10.243.96.10',
                 '10.243.32.26', '10.243.96.14', '10.243.96.4']
NODES = ",".join(LIST_OF_NODES)
RUNDECK = RunDeck("ping_status", NODES)
RUNDECK.execute_job()
RUNDECK.get_output()
RESPONSE = RUNDECK.get_response()

FILE_NAME = get_static_data_file_name("ping")
PING_STATUS = {}
SERVER_LIST = []
for server_name, ip in PING_ENV_LIST.items():
    SERVER_LIST.append(server_name)
print(SERVER_LIST)
NODE_SERVICE_STATUS = [d for d in RESPONSE if d['node'] in LIST_OF_NODES]
if NODE_SERVICE_STATUS:
    for entry in NODE_SERVICE_STATUS:
        server_name = entry['log'].split(":")[0].strip()
        print(server_name, entry['log'].split(":")[1].strip())
        if server_name in SERVER_LIST:
            PING_STATUS[server_name] = entry['log'].split(":")[1].strip()
        else:
            PING_STATUS[server_name] = "down"

save_data_to_file(FILE_NAME, PING_STATUS)
