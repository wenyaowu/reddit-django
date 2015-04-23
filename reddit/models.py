from datetime import datetime
from django.db import models

# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=1024, unique=False)
    pub_datetime = models.DateTimeField(default=datetime.now, blank=True)
    # user = models.ForeignKey(user)
    url = models.URLField()
    votes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    # tag = models.ManyToManyField(tag)

    def __unicode__(self):
        return self.title


