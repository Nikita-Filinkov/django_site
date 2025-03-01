from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .forms import AddPostForm
from .models import Posts, Category, TagPost
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', {})


class PostsHome(TemplateView):
    template_name = 'posts/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Posts.published.all()
        return context


class ShowPost(DetailView):
    template_name = 'posts/one_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context[self.context_object_name].title

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, post_slug=self.kwargs[self.slug_url_kwarg])


class Show_on_Category(ListView):
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Posts.published.filter(category__slug=self.kwargs['category_slug'])


class Show_on_Tag(ListView):
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Posts.published.filter(tags__slug=self.kwargs['tag_slug'])


class AddPost(CreateView):
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('posts')
    extra_context = {
        'title': 'Добавление поста',
        'message': 'Не валидный ввод',
    }
