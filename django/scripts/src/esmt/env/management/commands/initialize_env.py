"""
Author: Yogaraja Gopal
This module contains the management command to initialize the env app
"""
from django.core.management.base import BaseCommand
from esmt.env.common.initialize_env import env_initialize


class Command(BaseCommand):
    """
    This class is used to initialize the env app database
    """
    help = 'Initializes the Env app database'

    def handle(self, *args, **options):
        env_initialize()
        self.stdout.write(self.style.SUCCESS('Successfully initialized the env'))
