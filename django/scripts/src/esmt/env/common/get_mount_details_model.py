"""
Author: Yogaraja Gopl
Comment: This Module is used to get the store server mount details and insert it to database
"""
import datetime
import pytz
from django.db import transaction
from django.db.models.base import ObjectDoesNotExist
import esmt.env.common.process_command as proc_cmd
from esmt.base.lib.rundeck import RunDeck
from esmt.env.models import Server, MountTimeStamp, Mount


def parse_mount_details(response, node):
    """
    This function is parses the mount details from the response xml
    """
    node_mount_detail = [d for d in response if d['node'] == node]
    if node_mount_detail:
        mount = []
        for entry in node_mount_detail:
            if proc_cmd.check_rundeck_auth_connetion_error(entry):
                return mount
            else:
                entry = entry['log'].strip()
                mount.append(entry.split())
        return mount
    return "No matching node found in response"


def get_current_mount_details(node, server, mount_ts):
    """
    This function is used to get the current mount details from the store server using rundeck
    """
    arg_string = '-facts mount'
    rundeck = RunDeck("facts", node, arg_string)
    rundeck.execute_job()
    execution_id = rundeck.get_job_execution_id()
    if execution_id:
        rundeck.get_output()
        mount_data = parse_mount_details(rundeck.get_response(), node)
        if mount_ts:
            mount_ts.timestamp = datetime.datetime.now(pytz.utc)
            Mount.objects.filter(mount_ts=mount_ts).delete()
        else:
            mount_ts = MountTimeStamp.objects.create(server_id=server,
                                                     timestamp=datetime.datetime.now(pytz.utc))
        with transaction.atomic():
            for mnt in mount_data:
                mount = Mount.objects.create(
                    mount_ts=mount_ts,
                    filesystem=mnt[0],
                    size=mnt[1],
                    used=mnt[2],
                    avail=mnt[3],
                    used_percent=mnt[4],
                    mounted_on=mnt[5]
                )
                mount.save()
        mount_ts.save()
        return mount_data
    else:
        return '[]'


def get_mount_details(r2_r3, third_octet):
    """
    This function is used to get the mount details
    """
    node = proc_cmd.getip(third_octet, 'store', r2_r3.upper())
    try:
        server = Server.objects.get(server_ip=node)
    except ObjectDoesNotExist:
        server = Server.objects.create(server_ip=node)
        server.save()
    try:
        mount_ts = MountTimeStamp.objects.get(server_id=server)
        updated_timestamp = mount_ts.timestamp.strftime('%Y/%m/%d %H:%M:%S')
        hours = proc_cmd.get_time_diff_in_hrs(updated_timestamp)
        if hours >= 5:
            return get_current_mount_details(node, server, mount_ts)
        mount_list = Mount.objects.filter(mount_ts=mount_ts)
        mounts = []
        for mount in mount_list:
            mount_detail = [mount.filesystem, mount.size, mount.used, mount.avail,
                            mount.used_percent, mount.mounted_on]
            mounts.append(mount_detail)

        return mounts
    except ObjectDoesNotExist:
        return get_current_mount_details(node, server, mount_ts=None)


if __name__ == '__main__':
    print(get_mount_details('r3', '125'))
