from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', {})


def posts(request):
    return render(request, 'posts/posts.html', {})