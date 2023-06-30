from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('N', 'Not specified')), blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.pk})



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
