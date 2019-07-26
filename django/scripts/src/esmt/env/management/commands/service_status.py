from django.core.management.base import BaseCommand
from env.common.rundeck_get_service_status import get_service_status


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('env', nargs='+')

    def handle(self, *args, **options):
        for env in options['env']:
            print("Test")
            #get_service_status(env)
        self.stdout.write(self.style.SUCCESS('Successfully executed for "%s"' % env))
