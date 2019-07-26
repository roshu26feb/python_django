"""
Author: Yogaraja Gopal
This module contains the management command to install cron jobs
"""
from django.core.management.base import BaseCommand
from esmt.env.common.manage_crontab import install_cron


class Command(BaseCommand):
    """
    This class is used to create cron jobs
    """
    help = 'Create cron jobs'

    def handle(self, *args, **options):
        install_cron()
        self.stdout.write(self.style.SUCCESS('Successfully created cron job'))
