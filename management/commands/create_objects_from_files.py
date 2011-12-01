# you MUST import the management classes like this:
from django.core.management.base import BaseCommand, CommandError

# import any models or stuff you need from your project
from mmedia.signals import createObjectsFromFiles

# your custom command must reference the base management classes like this:
class Command(BaseCommand):
    # it's useful to describe what the function does:
    help = 'Create mmedia objects from serialized objects in given path.'

    def handle(self, *args, **options):
        createObjectsFromFiles(args[0])
        
