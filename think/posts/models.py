from django.db import models


# Create your models here.


class Posts(models.Model):
    user_id = models.IntegerField(verbose_name="Id создателя поста")
    title = models.CharField(max_length=200, verbose_name="Заголовок поста")
    description = models.TextField(blank=True, verbose_name="Текст поста")
    images = models.ImageField(upload_to='posts/images/', verbose_name="Картинки")
    post_slug = models.SlugField(max_length=20, unique=True, verbose_name="Slug_id", db_index=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_created']

        indexes = [
            models.Index(fields=['-time_created']),
        ]
