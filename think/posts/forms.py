import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Posts, Category, TagPost


@deconstructible
class RussianValidator:
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны быть латинские буквы'

    @staticmethod
    def has_cyrillic(text):
        return bool(re.search('[а-яА-Я]', text))

    def __call__(self, value):
        if self.has_cyrillic(value):
            raise ValidationError(self.message, code=self.code, params={'value': value})


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=200, label="Заголовок поста:")

    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
                                  label="Введите описание поста:")
    #
    # images = forms.ImageField(label="Добавьте картинку к посту:")
    post_slug = forms.SlugField(max_length=20, label="URL:", validators=[RussianValidator(),])
    is_published = forms.BooleanField(label="Опубликовать:", initial=True, required=False)

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      to_field_name="name",
                                      required=False,
                                      label="Выберите категорию:",
                                      empty_label="Не выбрано")

    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(),
                                          widget=forms.CheckboxSelectMultiple(),
                                          required=False,
                                          to_field_name="tag",
                                          label='Выберите теги:')
