from django.shortcuts import render, get_object_or_404

from .models import Posts
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', {})


def posts(request):
    all_posts = {1: {'title': 'Здание из будущего',
                     'image': 'Снимок экрана 2023-12-20 194130.png',
                     'description': '''Описание варианта развития будущего
                                        в котором возможно возникновения подобных строений'''},
                 2: {'title': 'Преодоление',
                     'image': 'Снимок экрана 2023-10-17 223729.png',
                     'description': 'Если идти до конца, можно до него дойти'},
                 3: {'title': 'Прост прикольно)',
                     'image': '00009-813486580.png',
                     'description': 'Без комментариев'}
                 }

    return render(request, 'posts/posts.html', {'posts': all_posts})


def show_post(request, post_slug):
    post = get_object_or_404(Posts, post_slug=post_slug)
    print(post.title)
    date = {'title': post.title,
            'image': post.images,
            'MEDIA_URL': settings.MEDIA_URL,
            'user_id': post.user_id,
            'description': post.description}
    return render(request, 'posts/one_post.html', date)
