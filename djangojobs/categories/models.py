from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to="category/photos", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category_order = models.PositiveIntegerField('Category order', unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={"slug": self.slug})

    def get_total_jobs(self):
        pass
