from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

import os
import logging

logger = logging.getLogger(__name__)

def _path(instance):
    return os.path.join(settings.MEDIA_ROOT, instance.user.username, \
                            instance.filename)

def _path_to_upload(instance, filename):
    # TODO: Next release should manage gin annex directory dynamically
    return os.path.join(settings.GITANNEX_DIR, settings.PORTAL_NAME, instance.author.username, instance.mediatype, filename)

def createObjectFromFiles():
    pass


class MMedia(models.Model):

    def __init__(self, *args, **kwargs):
        super(MMedia, self).__init__(*args, **kwargs)

    title = models.CharField(_('title'), max_length=120)
    description = models.TextField(_('description'), blank=True)
    author = models.ForeignKey(User)
    date = models.DateTimeField(_('release date'), blank=True, null=True)
    fileref = models.FileField(upload_to=_path_to_upload)
    mediatype = "mmedia"
#    tags = TagField(verbose_name=_('tags'), help_text=tagfield_help_text)

    def path(self):
        return os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR, settings.PORTAL_NAME, self.author.username, self.mediatype, \
                                self.fileref.path)

    def path_relative(self):
        return os.path.join(settings.GITANNEX_DIR, settings.PORTAL_NAME, self.author.username, self.mediatype, \
                                self.fileref.path)

    def __unicode__(self):
        return self.title
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        logger.debug(type(self))
        serializeTo = os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR,\
                                       settings.PORTAL_NAME, settings.SERIALIZED_DIR,\
                                       os.path.basename(self.fileref.path) + '.xml')
        logger.info('>>>> Serialize to: ' + serializeTo)
        out = open(serializeTo, "w")
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        xml_serializer.serialize((self, ), stream=out)
        super(MMedia, self).save(*args, **kwargs)
        
class Audio(MMedia):
    mediatype = "audio"
    
class Image(MMedia):
    mediatype = "image"
    height = models.IntegerField(max_length=4)
    width = models.IntegerField(max_length=4)

    def get_tiny_object(self):
        return self.mediatype

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

class Video(MMedia):
    mediatype = "video"
    preview = models.ImageField(upload_to="video_thumbnails")

    def get_tiny_object(self):
        return self.mediatype

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')



