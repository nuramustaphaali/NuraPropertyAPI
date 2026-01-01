# apps/users/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.users.managers import CustomUserManager # We will create this next

class User(AbstractUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = None # We verify via email
    email = models.EmailField(_('email address'), unique=True)
    
    # Specific fields you requested
    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_default.png')
    city = models.CharField(_('city'), max_length=100, blank=True)
    address = models.TextField(_('address'), blank=True)
    
    # Role flags
    is_agent = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email
