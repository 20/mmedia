from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

#import os

def path(instance, filename):
    return settings.MEDIA_ROOT + instance.user.username + '/' + filename

def path_relative(instance, filename):
        return instance.author.username + '/' + instance.mediatype + '/' + filename


class MMedia(models.Model):

    def __init__(self, *args, **kwargs):
        super(MMedia, self).__init__(*args, **kwargs)

    title = models.CharField(_('title'), max_length=120)
    description = models.TextField(_('description'), blank=True)
    author = models.ForeignKey(User)
    date = models.DateTimeField(_('release date'), blank=True, null=True)
    filename = models.FileField(upload_to=path_relative)
#    tags = TagField(verbose_name=_('tags'), help_text=tagfield_help_text)

    def __unicode__(self):
        return self.title


class Audio(MMedia):
    mediatype = "audio"
#    media = models.ForeignKey(MMedia, related_name='audio_mmedia')
    
class Image(MMedia):
    mediatype = "image"
#    media = models.ForeignKey(MMedia, related_name='image_mmedia')
    height = models.IntegerField(max_length=4)
    width = models.IntegerField(max_length=4)

    def get_tiny_object(self):
        return self.mediatype

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

class Video(MMedia):
    mediatype = "video"
#    media = models.ForeignKey(MMedia, related_name='video_mmedia')
    preview = models.ImageField(upload_to="video_thumbnails")

    def get_tiny_object(self):
        return self.mediatype

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')



# picture = Picture.objects.create(foo='some picture')
# video = Video.objects.create(bar='some video')
# something1 = Something.objects.create(media=picture)
# something2 = Something.objects.create(media=video)
# print something1.media.get_tiny_object() # this is a picture remember?
# print something2.media.get_tiny_object() # and lo, here is a video



# Forse da mettere in un package separato  
# class MultimediaFile(models.Model):
#     user = models.ForeignKey(User) 
#     name = models.TextField()
#     filename = models.FileField(upload_to=_pathToSave())
    
#     def __unicode__(self):
#         return u"%s" % self.id

#     def _pathToSave():
#         return User.username
    
#     def save():
#         super()
#         gitAnnex.gitAdd(filename, _pathToSave())

# gitAdd('exampleFile.txt', '/usr/local/example_git_repo_dir')

    
