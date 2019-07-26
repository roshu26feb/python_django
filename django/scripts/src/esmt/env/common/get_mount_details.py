import pytz
import datetime
import re
import env.common.process_command as proc_cmd
from esmt_base.lib.rundeck import RunDeck
from env.models import Server, MountTimeStamp, Mount
from django.db import transaction
from django.db.models.base import ObjectDoesNotExist


def parse_mount_details(response, node):
    node_mount_detail = [d for d in response if d['node'] == node]
    if node_mount_detail:
        mount = []
        for entry in node_mount_detail:
            if re.search(r"Authentication failure", entry['log'], re.I) or \
                    re.search(r"No route to host", entry['log'], re.I) or \
                    re.search(r"Connection timed out", entry['log'], re.I):
                return mount
            else:
                entry = entry['log'].strip()
                mount.append(entry.split())
        return mount


def get_current_mount_details(node, server, mount_ts):
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
            mount_ts = MountTimeStamp.objects.create(server_id=server, timestamp=datetime.datetime.now(pytz.utc))
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
    if r2_r3 == "r3":
        file = "mount"
    elif r2_r3 == "r2":
        file = "mount_r2"
    elif r2_r3 == "solar7":
        file = "solar7"
    elif r2_r3 == "plato":
        file = "plato_mount"

    env_type = ("socrates" if r2_r3 == 'r3' or r2_r3 == 'r2' else r2_r3)
    node = proc_cmd.getip(third_octet, 'store', r2_r3.upper())
    try:
        server = Server.objects.get(server_ip=node)
    except ObjectDoesNotExist:
        server = Server.objects.create(server_ip=node)
        server.save()
    try:
        mount_ts = MountTimeStamp.objects.get(server_id=server)
        updated_timestamp = mount_ts.timestamp.strftime('%Y/%m/%d %H:%M:%S')
        last_update_timestamp = datetime.datetime.strptime(updated_timestamp, '%Y/%m/%d %H:%M:%S')
        current_timestamp = proc_cmd.formatted_datetime()
        diff = current_timestamp - last_update_timestamp
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        if hours >= 5:
            return get_current_mount_details(node, server, mount_ts)
        else:
            mount_list = Mount.objects.filter(mount_ts=mount_ts)
            mounts = []
            for mount in mount_list:
                mount_detail = [mount.filesystem, mount.size, mount.used, mount.avail, mount.used_percent, mount.mounted_on]
                mounts.append(mount_detail)

            return mounts
    except ObjectDoesNotExist:
        return get_current_mount_details(node, server, mount_ts=None)


if __name__ == '__main__':
    print(get_mount_details('r3', '125'))

