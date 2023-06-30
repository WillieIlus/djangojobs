from datetime import timedelta, date
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from categories.models import Category
from companies.models import Company
from locations.models import Location
from plans.models import Plan


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    )

    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=50, unique=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, verbose_name='Job Type')

    user = models.ForeignKey(User, related_name='jobs', on_delete=models.PROTECT)
    company = models.ForeignKey(Company, related_name='jobs', on_delete=models.PROTECT)
    location = models.ForeignKey(Location, related_name='jobs', on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='jobs', on_delete=models.PROTECT, null=True, blank=True)
    plan = models.ForeignKey(Plan, verbose_name='plan', on_delete=models.CASCADE)

    poster = models.ImageField(upload_to='poster', null=True, blank=True)
    description = models.TextField()
    requirements = models.TextField(help_text='application_info')
    salary = models.CharField(max_length=128, blank=True)
    work_hours = models.CharField(max_length=80, blank=True)
    contact_email = models.EmailField(max_length=254, null=True, blank=True)
    on_site = models.BooleanField(default=False)

    duration_days = models.PositiveSmallIntegerField()
    openings = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    url = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0, editable=False)
    click_count = models.PositiveIntegerField(default=0, editable=False)
    amount = models.DecimalField('amount', max_digits=10, decimal_places=2, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    payment_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-created_on',)
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        get_latest_by = 'created_on'

    def __str__(self):
        return f"{self.user} [{self.plan}] ({self.title})"

    def save(self, *args, **kwargs):
        slug = slugify(f"{self.title} {self.user.username} {self.company.name}")
        self.slug = slug
        self.amount = self.get_price()
        super().save(*args, **kwargs)

    @staticmethod
    def get_sorted_jobs():
        return Job.objects.filter(active=True).order_by('-plan__weight')

    def is_expired(self):
        return timezone.now() >= self.updated_on + timedelta(days=self.duration_days)

    def time_since(self):
        return (date.today() - self.created_on.date()).days

    def get_price(self):
        if self.plan and self.duration_days is not None:
            price_per_day = self.plan.price_per_day
            total_price = Decimal(price_per_day) * self.duration_days
            return total_price
        return None

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'slug': self.slug})

    def is_active(self):
        now = timezone.now()
        return self.created_on <= now < self.updated_on + timedelta(days=self.duration_days)

    @property
    def days_left(self):
        remaining_days = (self.updated_on + timedelta(days=self.duration_days) - timezone.now()).days
        return max(remaining_days, 0)

    def expires_soon(self):
        days_left = self.days_left
        return days_left is not None and days_left <= 7

    def get_extended_until(self, plan):
        return self.updated_on + timedelta(days=plan.trial_duration)


class JobSortedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True).order_by('-plan__weight')


class Impression(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Job', related_name='impressions')
    impression_date = models.DateTimeField(verbose_name='When', auto_now_add=True)
    source_ip = models.GenericIPAddressField(verbose_name='Source IP Address', null=True, blank=True)
    session_id = models.CharField(verbose_name='Source Session ID', max_length=40, null=True, blank=True)

    class Meta:
        verbose_name = 'Job Impression'
        verbose_name_plural = 'Job Impressions'
        index_together = ('job', 'session_id',)

    def __str__(self):
        return str(self.job)


class Click(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Job', related_name='clicks')
    click_date = models.DateTimeField(verbose_name='When', auto_now_add=True)
    source_ip = models.GenericIPAddressField(verbose_name='Source IP Address', null=True, blank=True)
    session_id = models.CharField(verbose_name='Source Session ID', max_length=40, null=True, blank=True)

    class Meta:
        verbose_name = 'Job Click'
        verbose_name_plural = 'Job Clicks'
        index_together = ('job', 'session_id',)

    def __str__(self):
        return str(self.job)
