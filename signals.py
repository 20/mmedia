from django.db.models.signals import pre_save
from django.dispatch import receiver

from gitannex.signals import filesync_done

from gitannex.models import GitAnnexRepository
from mmedia.models import createObjectFromFiles

from django.core import serializers

from django.conf import settings

# Listen to signals /aka plugin to gitannex

@receiver(filesync_done, instance=GitAnnexRepository)
def syncGitAnnexRepository(instance, **kwargs):
    # Fai il sync.. ri
    for root, dirs, files in os.walk(\
        os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR, instance.repositoryURLOrPath)):
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
