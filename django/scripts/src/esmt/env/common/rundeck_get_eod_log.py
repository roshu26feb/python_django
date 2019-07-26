"""
Author: Yogaraja Gopal
This module is used to Get EOD logs
"""
import re
import esmt.env.common.process_command as proc_cmd
from esmt.base.lib.rundeck import RunDeck


def parse_eod_log(response, node):
    """
    This function is used to parse the eod logs
    """
    node_utils_list = [d for d in response if d['node'] == node]
    if node_utils_list:
        utils = []
        for entry in node_utils_list:
            if proc_cmd.check_rundeck_auth_connetion_error(entry):
                return ["Failed to connect to the server"]
            else:
                utils.append(entry['log'].strip("\n"))
        return utils


def get_eod_logs(third_octet):
    """
    This function is used to handle eod logs request
    """
    node = proc_cmd.getip(third_octet, 'store', 'r3'.upper())
    rundeck = RunDeck("eod_log", node)
    rundeck.execute_job()
    execution_id = rundeck.get_job_execution_id()
    print(execution_id)
    if execution_id:
        rundeck.get_output()
        utils_list = parse_eod_log(rundeck.get_response(), node)
        return utils_list
    return '[]'
