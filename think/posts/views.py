from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View

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


class AddPost(View):
    def get(self, request):
        form = AddPostForm()
        return render(request, 'posts/add_post.html', {'title': 'Добавление поста', 'form': form})

    def post(self, request):
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

        return render(request, 'posts/add_post.html',
                      {'title': 'Добавление поста', 'form': form, 'message': 'Не валидный ввод'})
