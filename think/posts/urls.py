from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostsHome.as_view(), name='posts'),
    path('add', views.AddPost.as_view(), name='add'),
    path('category/<slug:category_slug>', views.Show_on_Category.as_view(), name='post_category'),
    path('<slug:post_slug>', views.ShowPost.as_view(), name='post_slug'),
    path('tags/<slug:tag_slug>', views.Show_on_Tag.as_view(), name='posts_tags'),
    path('edit/<slug:post_slug>/', views.UpdatePost.as_view(), name='edit_post'),
    path('delete/<slug:post_slug>/', views.DeletePost.as_view(), name='delete_post'),
]


