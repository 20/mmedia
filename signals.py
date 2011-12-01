from django.dispatch import receiver
from django.core import serializers
from django.conf import settings

from gitannex.signals import filesync_done
from gitannex.models import GitAnnexRepository

import os
# Listen to signals /aka plugin to gitannex

@receiver(filesync_done, sender=GitAnnexRepository)
def syncGitAnnexRepository(sender, **kwargs):
    print ">>> DESERIALIZING"
    createObjectsFromFiles(os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR, sender.repositoryURLOrPath))

def createObjectsFromFiles(pathToFiles):
    for root, dirs, files in os.walk(pathToFiles):
        for file in files:
            if file.endswith('.xml'):
                xmlIn = open(os.path.join(root, file), "r")
                # XMLSerializer = serializers.get_serializer("xml")
                # xml_serializer = XMLSerializer()
                # for obj in xml_serializer.deserialize("xml", xmlIn):
                #     obj.id = None
                #     obj.pk = None
                #     obj.save()
                for obj in serializers.deserialize("xml", xmlIn):
                    obj.id = None
                    obj.pk = None
                    obj.save()
                os.remove(os.path.join(root, file))
