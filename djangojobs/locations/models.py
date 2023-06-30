from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "locations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("locations:detail", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
