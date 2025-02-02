from django.contrib import admin
from .models import Posts, Category


# Register your models here.

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'time_created', 'is_published', 'cat')
    list_display_links = ('user_id', 'title')
    ordering = ['-time_created']
    list_editable = ('is_published',)
    list_per_page = 5

# admin.site.register(Posts)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

