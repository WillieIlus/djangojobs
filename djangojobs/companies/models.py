from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from categories.models import Category
from locations.models import Location


class Company(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to="logos/company", blank=True, null=True)
    image = models.ImageField(upload_to="image/company", blank=True, null=True)
    description = models.TextField(max_length=1024)
    category = models.ForeignKey(Category, related_name="company", blank=True, null=True, on_delete=models.PROTECT)
    website = models.URLField(blank=True, null=True, help_text="Please leave empty if none")
    location = models.ForeignKey(Location, related_name='company', blank=True, null=True,
                                 help_text="Please leave empty if 100% virtual",
                                 on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'slug': self.slug})
