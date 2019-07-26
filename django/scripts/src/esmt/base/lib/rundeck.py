"""
Author : Yogaraja Gopal
This module handles the Rundeck related activities
"""
import json
import re
import time
import xml.etree.ElementTree as ET
import requests
from esmt.base.lib.app_config import RUNDECK_URL, AUTH_TOKEN, RUNDECK_JOB_ID


class RunDeck:
    """ This class takes care of handling the Rundeck part"""
    def __init__(self, job_name, node="", arg_string="", job_execution_id=""):
        self.rundeck_url = RUNDECK_URL
        self.job_uuid = RUNDECK_JOB_ID[job_name]
        self.auth_token = AUTH_TOKEN
        self.node = node
        self.arg_string = arg_string
        self.job_execution_id = job_execution_id
        self.response = ""
        self.url_val = ""

    def node_filter(self, node_list):
        """ This method sets the node filter"""
        self.node = ",".join(node_list)

    def check_job_status(self):
        """This method performs the activity of checking the status of the Rundeck job"""
        request_url = self.rundeck_url + '1/job/' + self.job_uuid + '/executions?authtoken=' + \
                      self.auth_token + '&status=running&max=10&format=json'
        response = requests.get(request_url)
        print(response)
        elements = ET.fromstring(response.text)
        for element in elements.iter('executions'):
            return element.attrib.get('count')

    def set_arg_string(self, arg_list):
        """ This method sets the argument string"""
        self.arg_string = "&argString= "
        for param, value in arg_list.items():
            self.arg_string += " -" + param + " " + value

    def execute_job(self):
        """This method performs the activity of calling the Rundeck job"""
        if self.node == "":
            print("Please provide the Node Filter")
            return

        if self.arg_string != "":
            arg_string = '&argString= ' + self.arg_string
        else:
            arg_string = ""

        request_url = self.rundeck_url + '12/job/' + self.job_uuid + '/run?authtoken=' + \
                      self.auth_token + arg_string + '&filter=' + self.node
        response = requests.get(request_url)
        elements = ET.fromstring(response.text)
        for element in elements.iter('execution'):
            self.job_execution_id = element.attrib.get('id')
            return self.job_execution_id

    def kill_job(self):
        """This method performs the activity of Killing the Rundeck job"""
        if self.job_execution_id == "":
            print("Invalid Execution Id")
            return

        # Get the the output using the execution id:
        self.url_val = self.rundeck_url + '1/execution/' + self.job_execution_id +\
                       '/abort?authtoken=' + self.auth_token
        response = requests.get(self.url_val)
        elements = ET.fromstring(response.text)
        for element in elements.iter('execution'):
            return element.attrib.get('status')

    def get_partial_log(self):
        """
        This method retrieves the Partial Rundeck job output based on the
        execution id returned while triggering the job to run
        """
        if self.job_execution_id == "":
            print("Invalid Execution Id")
            return

        # Get the the output using the execution id:
        self.url_val = self.rundeck_url + '5/execution/' + self.job_execution_id +\
                       '/output?authtoken=' + self.auth_token + '&format=json'
        response = requests.get(self.url_val)
        response_json = json.loads(response.text)
        return response_json['entries']

    def get_completion_status(self):
        """
        This method retrieves the Rundeck job output based on the
        execution id returned while triggering the job to run
        """
        if self.job_execution_id == "":
            print("Invalid Execution Id")
            return

        # Get the the output using the execution id:
        self.url_val = self.rundeck_url + '5/execution/' + self.job_execution_id +\
                       '/output?authtoken=' + self.auth_token + '&format=json'
        response = requests.get(self.url_val)
        response_json = json.loads(response.text)
        status = response_json['completed']
        if status:
            self.response = response_json['entries']
        return status

    def get_output(self):
        """
        This method performs retrieves the Rundeck job output based on the
        execution id return while triggering the job to run
        """
        completed = self.get_completion_status()
        while not completed:
            time.sleep(1)
            response = requests.get(self.url_val)
            response_json = json.loads(response.text)
            # print(r.text)
            completed = response_json['completed']
            if completed:
                # print(response_json['entries'][0]['log'])
                self.response = response_json['entries']
                return self.response

    def get_job_execution_id(self):
        """This method is the getter for job_execution_id attribute"""
        return self.job_execution_id

    def get_response(self):
        """This method is the getter for response attribute"""
        return self.response

    def get_service_status(self):
        """This method parses the rundeck output and returns the status of the service"""
        if re.search(r"Authentication failure", self.response[0]['log'], re.I) or \
                re.search(r"No route to host", self.response[0]['log'], re.I):
            return "NA"
        return self.response[0]['log'].split(":")[1].strip()
