from django.urls import path
from . import views


urlpatterns = [
    path('', views.posts, name='posts'),
    path('category/<slug:category_slug>', views.show_category, name='post_category'),
    path('<slug:post_slug>', views.show_post, name='post_slug'),
    path('tags/<slug:tag_slug>', views.show_posts_tags, name='posts_tags'),
]


