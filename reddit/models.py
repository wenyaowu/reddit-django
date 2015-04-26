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

    title = models.CharField(max_length=256, unique=False)
    pub_datetime = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)
    url = models.URLField()
    votes = models.IntegerField(default=0)
    subreddit = models.ForeignKey(Subreddit)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-pub_datetime"]


class Comment(models.Model):

    text = models.TextField(max_length=1024, blank=False)
    pub_datetime = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User)
    votes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, null=True, blank=True)
    comment = models.ForeignKey("self", related_name="children_comment", null=True, blank=True)

    def __unicode__(self):
        return self.text