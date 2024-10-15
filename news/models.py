from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='news/', verbose_name='Фото')
    text = models.TextField(verbose_name='Текст')
    number_views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = verbose_name
