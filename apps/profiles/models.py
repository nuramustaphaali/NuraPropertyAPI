# apps/profiles/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel # We need to create this first!

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25, default="+234")
    about_me = models.TextField(default="Say something about yourself", blank=True)
    license_number = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="profile_default.png", default="profile_default.png")
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default="Other")
    country = models.CharField(max_length=100, default="Nigeria", blank=False, null=False)
    city = models.CharField(max_length=180, default="Lagos", blank=False, null=False)
    is_buyer = models.BooleanField(default=False, help_text="Looking to buy?")
    is_seller = models.BooleanField(default=False, help_text="Looking to sell?")
    is_agent = models.BooleanField(default=False, help_text="Are you an agent?")
    top_agent = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    num_reviews = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"