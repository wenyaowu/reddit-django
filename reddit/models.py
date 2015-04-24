from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Subreddit(models.Model):

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subreddit, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=1024, unique=False)
    pub_datetime = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User)
    url = models.URLField()
    votes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    subreddit = models.ForeignKey(Subreddit)

    def __unicode__(self):
        return self.title


