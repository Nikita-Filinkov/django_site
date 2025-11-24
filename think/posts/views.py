from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .forms import AddPostForm
from .models import Posts, Category, TagPost
from django.conf import settings

from .utils import DataMixin


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', {})


class PostsHome(DataMixin, ListView):
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    title_page = 'Посты'

    def get_queryset(self):
        return Posts.published.all()


class ShowPost(DataMixin, DetailView):
    template_name = 'posts/one_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title_page = context[self.context_object_name].title

        return self.get_mixin_context(context=context, title=title_page)

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, post_slug=self.kwargs[self.slug_url_kwarg])


class Show_on_Category(DataMixin, ListView):
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title_page = context[self.context_object_name][0].category.name

        return self.get_mixin_context(context=context, title=title_page)

    def get_queryset(self):
        return Posts.published.filter(category__slug=self.kwargs['category_slug'])


class Show_on_Tag(DataMixin, ListView):
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title_page = TagPost.objects.filter(slug=self.kwargs['tag_slug'])[0].tag

        return self.get_mixin_context(context=context, title=title_page)

    def get_queryset(self):
        return Posts.published.filter(tags__slug=self.kwargs['tag_slug'])


class AddPost(LoginRequiredMixin, DataMixin, FormView):
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('posts')
    title_page = 'Добавление поста'

    login_url = '/users/login'

    def form_valid(self, form):
        data = form.cleaned_data
        new_post = form.save(commit=False)
        new_post.user_name = self.request.user
        new_post.save()
        new_post.tags.set(data['tags'])
        form.save_m2m()
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, DataMixin, UpdateView):
    model = Posts
    fields = ['title', 'description', 'images', 'is_published', 'category', 'tags']
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('posts')
    slug_url_kwarg = 'post_slug'
    title_page = 'Редактирование поста'

    login_url = '/users/login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['forms'] = context.pop('form')

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, post_slug=self.kwargs[self.slug_url_kwarg])


class DeletePost(LoginRequiredMixin, DataMixin, DeleteView):
    model = Posts
    fields = ['title']
    template_name = 'posts/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts')
    slug_url_kwarg = 'post_slug'
    title_page = 'Удаление поста'

    login_url = '/users/login'

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, post_slug=self.kwargs[self.slug_url_kwarg])
