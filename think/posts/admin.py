from django.contrib import admin, messages
from django.db.models import Count

from .models import Posts, Category, TagPost


# Register your models here.
class FilterTagsCategory(admin.SimpleListFilter):
    title = 'Наличие тегов или категории'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('hasnt_tags', 'Без тегов'),
            ('has_tags', 'Есть теги'),
            ('hasnt_category', 'Без категории'),
            ('has_category', 'Есть привязка к категории'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'hasnt_tags':
            return queryset.filter(tags__isnull=True)
        elif self.value() == 'has_tags':
            return queryset.filter(tags__isnull=False)
        if self.value() == 'hasnt_category':
            return queryset.filter(category__isnull=True)
        elif self.value() == 'has_category':
            return queryset.filter(category__isnull=False)


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'time_created', 'is_published', 'category', 'brief_info')
    list_display_links = ('user_id', 'title')
    ordering = ['-time_created']
    list_editable = ('is_published', 'category')
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'category__name']
    list_filter = [FilterTagsCategory, 'category__name', 'is_published']

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

