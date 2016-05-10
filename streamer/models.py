from django.db import models

# Create your models here.
class KeyWords(models.Model):
    keywords = models.CharField(max_length=256)

    def __str__(self):
        return self.keywords


class Links(models.Model):
    links = models.CharField(max_length=256)

    def __str__(self):
        return self.links


class Focus(models.Model):
    focus = models.CharField(max_length=256)
    keywords = models.ManyToManyField('Keywords')
    links = models.ManyToManyField('Links')

    def __str__(self):
        return self.focus
//unstable branch change
