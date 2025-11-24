from django import template
from posts.models import TagPost

register = template.Library()


@register.inclusion_tag('posts/list_tags.html')
def get_tags():
    tag = TagPost.objects.all()
    return {'tag': tag}
