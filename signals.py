from django.dispatch import receiver
from django.core import serializers
from django.conf import settings

from gitannex.signals import filesync_done
from gitannex.models import GitAnnexRepository

# Listen to signals /aka plugin to gitannex


@receiver(filesync_done, sender=GitAnnexRepository)
def syncGitAnnexRepository(sender, **kwargs):
    print ">>> DESERIALIZING"
    for root, dirs, files in os.walk(\
        os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR, sender.repositoryURLOrPath)):
        for file in files:
            if file.endswith('.xml'):
                xmlIn = open(file, "r")
                XMLSerializer = serializers.get_serializer("xml")
                xml_serializer = XMLSerializer()
                for obj in xml_serializer.deserialize("xml", xmlIn):
                    obj.id = None
                    obj.pk = None
                    obj.save()
                os.remove(file)
