from django.db import models
from django.utils.text import slugify


class Phone(models.Model):

    id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена')

    image = models.URLField(max_length=500, verbose_name='Ссылка на изображение')

    release_date = models.DateField(verbose_name='Дата релиза')
    lte_exists = models.BooleanField(default=False, verbose_name='Есть LTE')

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.price} ₽)'

    def save(self, *args, **kwargs):

        base_slug = slugify(self.name)
        if not base_slug:
            base_slug = str(self.id)

        slug_candidate = base_slug
        counter = 2
        while Phone.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
            slug_candidate = f'{base_slug}-{counter}'
            counter += 1

        self.slug = slug_candidate
        return super().save(*args, **kwargs)
