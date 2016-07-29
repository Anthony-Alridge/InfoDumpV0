from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class KeyWords(models.Model):
    keywords = models.CharField(max_length=256)

    def __str__(self):
        return self.keywords


class Links(models.Model):
    links = models.CharField(max_length=256)

    def __str__(self):
        return self.links


class FileModel(models.Model):
    file_field = models.FileField(upload_to = 'media/files')

    def __str__(self):
        return self.file_field.url


class Focus(models.Model):
    focus = models.CharField(max_length=256)
    keywords = models.ManyToManyField('Keywords')
    links = models.ManyToManyField('Links')
    files = models.ManyToManyField('FileModel')

    def __str__(self):
        return self.focus
