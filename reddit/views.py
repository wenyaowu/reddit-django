from django.contrib.auth.decorators import login_required
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
    posts = Post.objects.filter(subreddit=subreddit).order_by('-votes')[:25]

    context_dict['posts'] = posts

    return render(request, 'reddit/subreddit.html', context_dict)

@login_required
def add_post(request):
    # Check if it's a 'POST' request
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_name = request.user
            obj.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return redirect('home.html')
        else:
            print form.errors
    else: # Not a post request, just show/render the page
        form = PostForm()

    return render(request, 'reddit/add_post.html', {'form': form})
