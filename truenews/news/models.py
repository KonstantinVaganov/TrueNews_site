from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class PublishedManager(models.Manager): # Менеджер возвращающий только опубликованные посты
    def get_queryset(self):
        return super().get_queryset().filter(is_published=News.Status.PUBLISHED)


class News(models.Model):   # Виджет, для лучшего понимания, заместо 0 и 1(False, True) DRAFT и PUBLISHED
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик-DRAFT'
        PUBLISHED = 1, 'Опубликовано-PUBLISHED'

    title = models.CharField(max_length=250, unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    categ = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='categ')
    # Формирует связи многие к одному, с моделью category

    objects = models.Manager() # Чтобы objects можно было испозьзовать как и раньше
    published = PublishedManager()

    def save(self, *args, **kwargs):
        if not self.slug:  # Если слаг не указан вручную
            # Транслитерируем кириллицу в латиницу
            transliterated_title = translit(self.title, 'ru', reversed=True)
            # Генерируем слаг (заменяет пробелы на дефисы и приводит к нижнему регистру)
            self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create'] # Порядок сортировки
        indexes = [
            models.Index(fields=['-time_create']) # Для ускарения поиска по индексу
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=250, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Если слаг не указан вручную
            # Транслитерируем кириллицу в латиницу
            transliterated_name = translit(self.name, 'ru', reversed=True)
            # Генерируем слаг (заменяет пробелы на дефисы и приводит к нижнему регистру)
            self.slug = slugify(transliterated_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('categories', kwargs={'categories_slug': self.slug})
