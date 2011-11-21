from django.db.models.signals import pre_save
from django.dispatch import receiver

from gitannex.signals import filesync_done
#from gitannex.models import GitAnnexRepository

from gitannex.models import GitAnnexRepository
from mmedia.models import createObjectFromFiles

# Listen to signals /aka plugin to gitannex

@receiver(filesync_done, sender=GitAnnexRepository)
def syncGitAnnexRepository(sender, **kwargs):
    # Fai il sync.. ri
    createObjectFromFiles()
