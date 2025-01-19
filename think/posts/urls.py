from django.urls import path
from . import views


urlpatterns = [
    path('', views.posts, name='posts'),
    path('<slug:post_slug>', views.show_post, name='post_slug'),
]


