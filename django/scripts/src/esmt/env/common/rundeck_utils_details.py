"""
Author: Yogaraja Gopal
This module is used to get List of utils installed using rundeck
"""
import re
import esmt.env.common.process_command as proc_cmd
from esmt.base.lib.rundeck import RunDeck


def parse_utils_list(response, node):
    """
    This function is used to parse utils list
    """
    node_utils_list = [d for d in response if d['node'] == node]
    if node_utils_list:
        utils = []
        for entry in node_utils_list:
            if re.search(r"Authentication failure", entry['log'], re.I) or \
                    re.search(r"No route to host", entry['log'], re.I):
                return ["Failed to connect to the server"]
            else:
                utils.append(entry['log'].strip("\n"))
        return utils
    return "Server not found in log"


def get_installed_utils_details(third_octet):
    """
    This function is used to get installed utils details form store server using rundeck
    """
    node = proc_cmd.getip(third_octet, 'store', 'r3'.upper())
    arg_string = '-facts utils'
    rundeck = RunDeck("facts", node, arg_string)
    rundeck.execute_job()
    execution_id = rundeck.get_job_execution_id()
    print(execution_id)
    if execution_id:
        rundeck.get_output()
        utils_list = parse_utils_list(rundeck.get_response(), node)
        return utils_list
    return '[]'


if __name__ == '__main__':
    print(get_installed_utils_details('16'))
