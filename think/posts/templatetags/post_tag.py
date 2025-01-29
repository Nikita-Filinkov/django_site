from django import template
from posts.models import Category

register = template.Library()


@register.inclusion_tag('posts/list_categories.html')
def get_tags():
    tag = Category.objects.all()
    return {'categories': categories}