import re

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.deconstruct import deconstructible


# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.Status.PUBLISHED)


@deconstructible
class RussianValidator:
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны быть латинские буквы'

    def __call__(self, value):
        if has_cyrillic(value):
            raise ValidationError(self.message, code=self.code, params={'value': value})


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class Posts(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    user_id = models.IntegerField(verbose_name="Id создателя поста", default=0)
    title = models.CharField(max_length=200, verbose_name="Заголовок поста")
    description = models.TextField(blank=True, verbose_name="Текст поста")
    images = models.ImageField(upload_to='posts/images/', verbose_name="Картинки",
                               default='Снимок экрана 2023-12-20 194130.png')
    post_slug = models.SlugField(max_length=20, unique=True, verbose_name="Slug_id", db_index=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    count_views = models.IntegerField(blank=True, default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(choices=map(lambda x: (bool(x[0]), x[1]), Status.choices),
                                       default=Status.PUBLISHED, verbose_name="Статус")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, related_name='posts',
                                 verbose_name='Категория', blank=True)
    tags = models.ManyToManyField('TagPost', blank=True, null=True, related_name='post')

    def save(self, *args, **kwargs):
        if not self.post_slug or not translit_to_eng(self.post_slug):
            self.post_slug = translit_to_eng(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post_slug', kwargs={'post_slug': self.post_slug})

    class Meta:
        verbose_name = 'Лента постов'
        verbose_name_plural = 'Лента постов'
        ordering = ['-time_created']

        indexes = [
            models.Index(fields=['-time_created']),
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=20, unique=True, verbose_name="slug_category", db_index=True)

    def get_absolute_url(self):
        return reverse('post_category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="slug_category", db_index=True)

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('posts_tags', kwargs={'tag_slug': self.slug})

