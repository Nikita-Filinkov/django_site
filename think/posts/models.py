from django.db import models

# Create your models here.


class Posts(models.Model):
    user_id = models.IntegerField(verbose_name="Id создателя поста")
    title = models.CharField(max_length=200, verbose_name="Заголовок поста")
    description = models.TextField(blank=True, verbose_name="Текст поста")
    images = models.ImageField(verbose_name="Картинки")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True)

