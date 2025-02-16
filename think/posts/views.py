from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddPostForm
from .models import Posts, Category, TagPost
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', {})


def posts(request):
    all_posts = Posts.published.all()
    return render(request, 'posts/posts.html', {'posts': all_posts, 'MEDIA_URL': settings.MEDIA_URL})


def show_post(request, post_slug):
    post = get_object_or_404(Posts, post_slug=post_slug)
    print(post.title)
    date = {'title': post.title,
            'image': post.images,
            'MEDIA_URL': settings.MEDIA_URL,
            'user_id': post.user_id,
            'description': post.description}
    return render(request, 'posts/one_post.html', date)


def show_category(request, category_slug):
    posts_on_category = Posts.objects.filter(category__slug=category_slug)
    # posts_on_category = Posts.objects.all()
    # posts_on_category = get_object_or_404(Category, cat_slug=cat_slug)
    return render(request, 'posts/posts.html',
                  {'posts': posts_on_category, 'MEDIA_URL': settings.MEDIA_URL})


def show_posts_tags(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts_on_tag = tag.post.filter(is_published=Posts.Status.PUBLISHED)
    return render(request, 'posts/posts.html',
                  {'posts': posts_on_tag, 'MEDIA_URL': settings.MEDIA_URL})


def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        # print(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            try:
                print(form.cleaned_data)
                data = form.cleaned_data
                post = Posts.objects.create(title=data['title'],
                                            description=data['description'],
                                            post_slug=data['post_slug'],
                                            category=data['category'],
                                            is_published=data['is_published'])
                post.tags.set(data['tags'])
            #               Posts.objects.create(**form.cleaned_data)
                return redirect('posts')
            except Exception as e:
                form.add_error(None, 'Ошибка добавления поста: {}'.format(str(e)))
                print('Error:', str(e))
                return render(request, 'posts/add_post.html',
                              {'title': 'Добавление поста', 'form': form, 'error_message': str(e)})
        else:
            form = AddPostForm()
            return render(request, 'posts/add_post.html',
                          {'title': 'Добавление поста', 'form': form, 'message': 'Не валидный ввод'})
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', {'title': 'Добавление поста', 'form': form})
