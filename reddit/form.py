__author__ = 'evanwu'
from datetime import datetime
from django import forms
from models import Post, Comment, Subreddit


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=256, help_text='Title')
    url = forms.URLField(max_length=200, help_text='URL', initial='http://')
    subreddit = forms.ModelChoiceField(queryset=Subreddit.objects.all(), help_text='Subreddit')
    votes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    pub_datetime = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:  # Things that is not included in the field
        # Provide an association between the ModelForm and a model
        model = Post
        exclude = ('user', 'comment_count', 'slug')


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='')
    parent = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'parent'}), required=False)

    class Meta:
        model = Comment
        exclude = ('parent', 'pub_datetime', 'user', 'post', 'votes', 'comment', 'depth')