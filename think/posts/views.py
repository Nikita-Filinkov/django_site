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
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.save()
            print(data['images'])
            # new_post.images = data['images']
            new_post.tags.set(data['tags'])
            form.save_m2m()
            return redirect('posts')
        else:
            form = AddPostForm()
            return render(request, 'posts/add_post.html',
                          {'title': 'Добавление поста', 'form': form, 'message': 'Не валидный ввод'})
    form = AddPostForm()
    return render(request, 'posts/add_post.html', {'title': 'Добавление поста', 'form': form})
