from hashlib import md5
from urlparse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models

from sorl.thumbnail import ImageField

from helpers import urlparams


class DuzzUser(AbstractUser):
    full_name = models.CharField(max_length=70)
    avatar = ImageField(upload_to='avatars', null=True, blank=True)


class Topic(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(DuzzUser)
    subject = models.CharField(max_length=40)

    class Meta:
        ordering = ['-updated']

    def get_absolute_url(self):
        return reverse('topic', kwargs={'topic_id': self.pk})
    

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(DuzzUser)
    topic = models.ForeignKey(Topic, related_name='comments')
    text = models.TextField(verbose_name='body')
    
    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        # Update topic's 'updated'
        Topic.objects.filter(pk=self.topic.pk).update(updated=self.created)

    def __unicode__(self):
        return unicode(self.pk)


class Attachment(models.Model):
    content = ImageField(upload_to='attachments')
    comment = models.ForeignKey(Comment, related_name='attachments')
