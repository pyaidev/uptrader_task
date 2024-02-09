from django.db import models
from django.urls import reverse


class Page(models.Model):
    title = models.CharField(max_length=300,
                             verbose_name='Название страницы')
    title_in_menu = models.CharField(max_length=300,
                                     verbose_name='Название пункта меню')

    def get_absolute_url(self):
        return reverse('page', kwargs={'page_id': self.id})

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(max_length=300,
                             verbose_name='Название меню')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    pages = models.ManyToManyField(Page,
                                   through='MenuPage',
                                   through_fields=('menu', 'page'))

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


    def __str__(self):
        return self.title


class MenuPage(models.Model):
    menu = models.ForeignKey(Menu,
                             verbose_name='Меню',
                             on_delete=models.CASCADE,
                             to_field='slug')
    page = models.ForeignKey(Page,
                             verbose_name='Cтраница',
                             related_name='menus',
                             on_delete=models.CASCADE)
    parent = models.ForeignKey(Page,
                               verbose_name='Родитель',
                               null=True,
                               blank=True,
                               related_name='children',
                               on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Порядок в уровне меню',
                                null=True)

    class Meta:
        verbose_name = 'Страница меню'
        verbose_name_plural = 'Страницы меню'
        unique_together = ('menu', 'page', 'parent')
        ordering = ['order']


    def __str__(self):
        return self.page.title
