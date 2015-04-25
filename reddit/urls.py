from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reddit-django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^subreddit/(?P<subreddit_slug>[\w\-]+)/$', views.subreddit, name='subreddit'),
    url(r'^add_post/$', views.add_post, name='add_post'),

)
