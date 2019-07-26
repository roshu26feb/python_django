"""
Author: Yogaraja Gopal
This module is used to handle execution of rundeck scripts
"""
import datetime
from django.http import HttpResponse, JsonResponse
from esmt.base.lib.rundeck import RunDeck
from esmt.env.common import process_command as proc_cmd
from esmt.env.models import Server, RundeckJobEntry


def execute_script(job_name, third_octet, env, action):
    """
    This function is used to call the rundeck job with the required parameters and update the
    job id in database, as well as get the rundeck log and return it to the frontend
    """
    node = proc_cmd.getip(third_octet, 'store', env.upper())
    server = Server.objects.filter(server_ip=node)
    job_details = RundeckJobEntry.objects.filter(server_id__server_ip=node, job_name=job_name)

    if action == "run":
        if proc_cmd.job_already_running(job_name) == '0':
            rundeck = RunDeck(job_name, node)
            rundeck.execute_job()
            execution_id = rundeck.get_job_execution_id()
            if execution_id:
                if job_details:
                    job_details.update(job_execution_id=execution_id,
                                       executed_datetime=datetime.datetime.now())
                else:
                    if not server:
                        server = Server.objects.create(server_ip=node)

                    job = RundeckJobEntry.objects.create(
                        server_id=(Server.objects.get(server_ip=node)),
                        job_name=job_name,
                        job_execution_id=execution_id,
                        executed_datetime=datetime.datetime.now())
                    job.save()
                output_response = "Rundeck Job Started.. Click on Get status " \
                                  "to view the status of the job"
            else:
                output_response = "Not able to Trigger Rundeck Job"
            return HttpResponse(output_response)
        else:
            return HttpResponse("Another job is already Running, "
                                "Please run once it is completed or"
                                " click on Get status to view the job status")
    elif action == "status":
        if job_details:
            prev_job_execution_id_js = job_details.values("job_execution_id")
            prev_job_execution_id = str(prev_job_execution_id_js[0]["job_execution_id"])
            if prev_job_execution_id:
                partial_log = proc_cmd.get_partial_log(job_name, prev_job_execution_id, node)
                kill_log = 'Please kill the job if running, as the process is complete'
                abort_status = proc_cmd.check_and_kill_job(job_name, prev_job_execution_id,
                                                           partial_log, kill_log)
                if abort_status != 'Completed':
                    partial_log.append(abort_status)
                return JsonResponse(partial_log, safe=False)
            else:
                return JsonResponse(["No previous rundeck execution found for this node"],
                                    safe=False)
        else:
            return JsonResponse(["No previous rundeck execution found", "Please Note: ",
                                 "Only Logs for the Jobs ran from ESMT can be viewed here "],
                                safe=False)
    return "invalid Action"
