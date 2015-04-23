from django.shortcuts import render
from models import Post

# Create your views here.
def index(request):
    context_dict = {}
    posts = Post.objects.all()
    context_dict['posts'] = posts

    return render(request, 'reddit/index.html', context_dict)