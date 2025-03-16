from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView

register = template.Library()


@register.inclusion_tag('users/logout_tag.html')
def logout_link():
    logout_form = LogoutView()
    return {'logout_form': logout_form}