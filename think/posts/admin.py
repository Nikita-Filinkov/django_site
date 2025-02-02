from django.contrib import admin, messages
from django.db.models import Count

from .models import Posts, Category, TagPost


# Register your models here.

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'time_created', 'is_published', 'category', 'brief_info')
    list_display_links = ('user_id', 'title')
    ordering = ['-time_created']
    list_editable = ('is_published', 'category')
    list_per_page = 5
    actions = ['set_published', 'set_draft']

    @admin.display(description="Количество тегов")
    def brief_info(self, posts: Posts):
        tags = posts.tags.aggregate(count_tags=Count('tag'))
        return f"Количество тегов у поста: {tags['count_tags']}."

    @admin.action(description='Опубликовать пост')
    def set_published(self, request, queryset):
        count_posts = queryset.update(is_published=Posts.Status.PUBLISHED)
        if count_posts > 1:
            message = f'Опубликовано {count_posts} поста'
        else:
            message = f'Опубликован {count_posts} пост'
        self.message_user(request, message)

    @admin.action(description='Снять пост с публикации')
    def set_draft(self, request, queryset):
        count_posts = queryset.update(is_published=Posts.Status.DRAFT)
        if count_posts > 1:
            message = f'Снято с публикации {count_posts} поста'
        else:
            message = f'Снят с публикации {count_posts} пост'
        self.message_user(request, message, messages.WARNING)

# admin.site.register(Posts)


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    list_display_links = ('id', 'tag')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

