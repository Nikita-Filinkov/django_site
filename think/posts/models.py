from django.db import models
from django.urls import reverse

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.Status.PUBLISHED)


class Posts(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    user_id = models.IntegerField(verbose_name="Id создателя поста")
    title = models.CharField(max_length=200, verbose_name="Заголовок поста")
    description = models.TextField(blank=True, verbose_name="Текст поста")
    images = models.ImageField(upload_to='posts/images/', verbose_name="Картинки")
    post_slug = models.SlugField(max_length=20, unique=True, verbose_name="Slug_id", db_index=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post_slug', kwargs={'post_slug': self.post_slug})

    class Meta:
        ordering = ['-time_created']

        indexes = [
            models.Index(fields=['-time_created']),
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=20, unique=True, verbose_name="slug_cat", db_index=True)

    def __str__(self):
        return self.name
