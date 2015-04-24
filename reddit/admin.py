from django.contrib import admin
from models import Post, Subreddit, Comment
# Register your models here.

class SubredditAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Post)
# Update the registeration to include this customised interface
admin.site.register(Subreddit, SubredditAdmin)
admin.site.register(Comment)