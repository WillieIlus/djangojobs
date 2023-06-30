from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone



class Plan(models.Model):
    title = models.CharField("title", unique=True, max_length=50)
    description = models.TextField("description", blank=True)
    price_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    trial_duration = models.PositiveSmallIntegerField(verbose_name="trial duration", help_text="In days", default=1)
    is_default = models.BooleanField("default",
                                     help_text="Default package for new purchaser (useful for trial packages). "
                                               "Only 1 default package at a time can be set.",
                                     default=False, db_index=True)
    is_fallback = models.BooleanField("fallback",
                                      help_text="Fallback package for purchaser when its subscription expires or trial "
                                                "ends (useful for freemium packages). Only 1 fallback package at a time"
                                                " can be set.",
                                      default=False, db_index=True)
    is_available = models.BooleanField("available", default=False, db_index=True,
                                       help_text="Is still available for purchase")
    is_visible = models.BooleanField("visible", default=True, db_index=True, help_text="Is visible in pricing page")
    is_trial = models.BooleanField('is trial', default=False)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    weight = models.IntegerField(verbose_name='Weight', default=1, validators=[MinValueValidator(1)],
                                 help_text='Weight of the job relative to other jobs. '
                                           'Ad with higher weight will be displayed more frequently.')

    class Meta:
        verbose_name = "subscription plan"
        verbose_name_plural = "subscription plans"

    def __str__(self):
        return f'{self.title}: Ksh {self.price_per_day} per day'



    def is_trial_expired(self):
        now = timezone.now()
        return self.trial_end_date <= now


# class PaymentMethod(models.Model):
#     method_name = models.CharField(max_length=100)
#     card_number = models.CharField(max_length=16)
#
#     def __str__(self):
#         return self.method_name


