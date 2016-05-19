from django.db import models
from django.contrib.auth.models import User
from streamer.models import Focus
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    focus = models.ManyToManyField(Focus)
