from django.shortcuts import render, get_object_or_404

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
