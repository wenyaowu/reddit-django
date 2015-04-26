from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db.models import signals
from dbarray import IntegerArrayField

class Subreddit(models.Model):

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subreddit, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)
    pub_datetime = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)
    url = models.URLField()
    votes = models.IntegerField(default=0)
    subreddit = models.ForeignKey(Subreddit)
    comment_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

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

    # For threaded comments
    path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:  # On creation
            if self.post:  # comment->post
                self.post.comment_count += 1
                self.post.save()
        super(Comment, self).save(*args, **kwargs)

def decrement_comment_count(sender, instance, **kwargs):  # Use signal to handle the deletion event of comment
    instance.post.comment_count -= 1
    instance.post.save()
signals.post_delete.connect(decrement_comment_count, sender=Comment)