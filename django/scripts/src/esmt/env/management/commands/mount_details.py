from django.core.management.base import BaseCommand
from env.common.rundeck_get_mount_details import get_server_mount_details


class Command(BaseCommand):
    help = 'Get the mount details of the specified Group of Server'

    def add_arguments(self, parser):
        parser.add_argument('env', nargs='+')

    def handle(self, *args, **options):
        for env in options['env']:
            get_server_mount_details(env)
        self.stdout.write(self.style.SUCCESS('Successfully executed for "%s"' % env))
