"""
Author : Yogaraja Gopal
Comment: This module is used to create/update cron jobs related to ESMT Application
"""
from crontab import CronTab

CRON_JOBS = {
    'env_uk_r3_service_status': {
        'cmd': '/usr/bin/python3 -m esmt.env.common.rundeck_get_service_status soc-r3',
        'schedule': ['*/15', '4-18', '*', '*', '1-5']
    },
    'env_uk_r2_service_status': {
        'cmd': '/usr/bin/python3 -m esmt.env.common.rundeck_get_service_status soc-r2',
        'schedule': ['*/15', '4-18', '*', '*', '1-5']
    },
    'env_uk_r3_store_facts': {
        'cmd': '/usr/bin/python3 -m esmt.env.common.rundeck_get_store_facts r3',
        'schedule': ['0', '4-18/5', '*', '*', '1-5']
    },
    'env_uk_r2_store_facts': {
        'cmd': '/usr/bin/python3 -m esmt.env.common.rundeck_get_store_facts r2',
        'schedule': ['0', '4-18/5', '*', '*', '1-5']
    },
    'env_uk_r3_mount': {
        'cmd': '/usr/bin/python3 -m esmt.env.common.rundeck_get_mount_details r3',
        'schedule': ['0', '4-18/5', '*', '*', '1-5']
    },
    'env_uk_r2_mount': {
        'cmd': '/usr/bin/python3 -m esmt.env.common.rundeck_get_mount_details r2',
        'schedule': ['0', '4-18/5', '*', '*', '1-5']
    },
}


def install_cron():
    """
    This function is used to delete the cron if present and create it
    """
    my_cron = CronTab(user='root')
    for comment, job_details in CRON_JOBS.items():
        for cron in my_cron:
            if cron.comment == comment:
                my_cron.remove(cron)
                my_cron.write()
                break
        job = my_cron.new(command=job_details['cmd'], comment=comment)
        job.setall(*job_details['schedule'])
        my_cron.write()


if __name__ == '__main__':
    install_cron()
