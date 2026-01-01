# apps/properties/models.py
import random
import string
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "FOR_SALE", _("For Sale")
        FOR_RENT = "FOR_RENT", _("For Rent")
        AUCTION = "AUCTION", _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "HOUSE", _("House")
        APARTMENT = "APARTMENT", _("Apartment")
        OFFICE = "OFFICE", _("Office")
        WAREHOUSE = "WAREHOUSE", _("Warehouse")
        COMMERCIAL = "COMMERCIAL", _("Commercial")
        OTHER = "OTHER", _("Other")

    user = models.ForeignKey(User, related_name="agent_buyer", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    ref_code = models.CharField(max_length=255, unique=True, blank=True)
    description = models.TextField(default="Default description...update me please user")
    country = models.CharField(max_length=50, default="Nigeria")
    city = models.CharField(max_length=180, default="Lagos")
    postal_code = models.CharField(max_length=100, default="100001")
    street_address = models.CharField(max_length=150, default="Ikeja Avenue")
    property_number = models.IntegerField(default=112)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.15, help_text="15% trade tax")
    plot_area = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_floors = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    
    advert_type = models.CharField(max_length=50, choices=AdvertType.choices, default=AdvertType.FOR_SALE)
    property_type = models.CharField(max_length=50, choices=PropertyType.choices, default=PropertyType.HOUSE)
    
    cover_photo = models.ImageField(upload_to="property_cover_photos/", default="property_cover.jpg")
    published_status = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str(self.title).title()
        if not self.slug:
            slug = slugify(self.title)
            while Property.objects.filter(slug=slug).exists():
                slug = f"{slug}-{random.randint(1, 1000)}"
            self.slug = slug
        if not self.ref_code:
            self.ref_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_amount = self.price * self.tax
        final_price = self.price + tax_amount
        return final_price

    def __str__(self):
        return self.title
# apps/properties/models.py

class PropertyImage(TimeStampedUUIDModel):
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images/", default="property_sample.jpg")

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"

    def __str__(self):
        return f"Image for {self.property.title}"

# apps/properties/models.py (add at the bottom)

class PropertySearch(TimeStampedUUIDModel):
    user = models.ForeignKey(User, related_name="saved_searches", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text="e.g. 3 Bedroom in Lekki")
    criteria = models.JSONField(help_text="JSON of search params, e.g. {'city': 'Lagos', 'price_max': 1000000}")

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"