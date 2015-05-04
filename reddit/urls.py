from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reddit-django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^subreddit/(?P<subreddit_slug>[\w\-]+)/$', views.subreddit, name='subreddit'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^vote_post/$', views.vote_post, name='vote_post'),
    url(r'^downvote_post/$', views.downvote_post, name='downvote_post'),
    url(r'^comment/(?P<post_slug>[\w\-]+)/$', views.post, name='post'),
)
