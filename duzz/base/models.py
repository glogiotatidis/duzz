from hashlib import md5
from urlparse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from helpers import urlparams


class DuzzUser(AbstractUser):
    full_name = models.CharField(max_length=70)

    def get_avatar_url(self, size=48):
        digest = md5(self.email).hexdigest()
        return urlparams(urljoin(settings.GRAVATAR_URL, digest), size=size)


class Topic(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(DuzzUser)
    subject = models.CharField(max_length=40)

    class Meta:
        ordering = ['-updated']


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(DuzzUser)
    topic = models.ForeignKey(Topic, related_name='comments')
    text = models.TextField()
