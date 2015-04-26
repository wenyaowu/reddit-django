import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from models import Post, Subreddit, Comment
from form import PostForm, CommentForm
# Create your views here.


def index(request):
    context_dict = {}
    posts = Post.objects.all().order_by('-votes')[:25]
    context_dict['posts'] = posts

    return render(request, 'reddit/index.html', context_dict)


def subreddit(request, subreddit_slug):
    context_dict = {}
    subreddit = get_object_or_404(Subreddit, slug=subreddit_slug)
    if subreddit:
        context_dict['subreddit'] = subreddit
        posts = Post.objects.filter(subreddit=subreddit).order_by('-votes')[:25]
        context_dict['posts'] = posts

    return render(request, 'reddit/subreddit.html', context_dict)

@login_required
def add_post(request):
    # Check if it's a 'POST' request
    if request.method == 'POST':
        form = PostForm(request.POST)
        user = request.user
        if form.is_valid():
            if user:
                post = form.save(commit=False)
                post.user = user
                post.save()
            # Now call the index() view.
            # The user will be shown the homepage.
            return redirect('/reddit/')
        else:
            print form.errors
    else:  # Not a post request, just show/render the page
        form = PostForm()
    context_dict = {'form': form}

    return render(request, 'reddit/add_post.html', context_dict)

@login_required
def vote_post(request):

    post_id = None
    if request.method=='GET':
        post_id = request.GET['post_id']

    votes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            votes = post.votes+1
            post.votes = votes
            post.save()
    return HttpResponse(votes)

@login_required
def downvote_post(request):

    post_id = None
    if request.method=='GET':
        post_id = request.GET['post_id']

    votes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            votes = post.votes-1
            post.votes = votes
            post.save()
    return HttpResponse(votes)