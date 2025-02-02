from django.contrib import admin
from django.db.models import Count

from .models import Posts, Category, TagPost


# Register your models here.

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'time_created', 'is_published', 'cat', 'brief_info')
    list_display_links = ('user_id', 'title')
    ordering = ['-time_created']
    list_editable = ('is_published',)
    list_per_page = 5

    @admin.display(description="Количество тегов")
    def brief_info(self, posts: Posts):
        # count_tags = posts.objects.aggregate(Count('tags'))
        tags = posts.tags
        print(tags)
        return f"Количество тегов у поста {tags}."
# admin.site.register(Posts)


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    list_display_links = ('id', 'tag')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

