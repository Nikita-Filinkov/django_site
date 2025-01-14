from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', {})


def posts(request):
    all_posts = {1: {'title': 'Здание из будущего',
                     'image': 'Снимок экрана 2023-12-20 194130.png',
                     'description': '''Описание варианта развития будующего
                                        в котором возможно вознкновения подобных строений'''},
                 2: {'title': 'Преодоление',
                     'image': 'Снимок экрана 2023-10-17 223729.png',
                     'description': 'Если идти до конца, можно до него дойти'},
                 3: {'title': 'Прост прикольно)',
                     'image': '00009-813486580.png',
                     'description': 'Без комментариев'}
                 }
    return render(request, 'posts/posts.html', {'posts': all_posts})
