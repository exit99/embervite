import os

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    unique_hash = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.unique_hash:
            self.unique_hash = self._create_hash()
        super(UserProfile, self).save(*args, **kwargs)

    def _create_hash(self):
        new_hash = os.urandom(4).encode('hex')
        if UserProfile.objects.filter(unique_hash=new_hash):
            return self._create_hash()
        return new_hash
