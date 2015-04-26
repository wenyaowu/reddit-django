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


def post(request, post_slug):

    post = Post.objects.get(slug=post_slug)
    user = request.user

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            temp.post = post
            temp.user = user
            parent = form['parent'].value()
            print parent
            if parent == '':
                # Set a blank path then save it to get an ID
                temp.path = []
                temp.save()
                temp.path = [temp.id]
            else:
                # Get the parent node
                node = Comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path

                # Store parents path then apply comment ID
                temp.save()
                temp.path.append(temp.id)

            # Final save for parents and children
            temp.save()

    # Retrieve all comments and sort them by path
    comment_tree = Comment.objects.filter(post=post).order_by('path')

    return render(request, 'reddit/post.html', locals())


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

