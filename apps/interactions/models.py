# apps/interactions/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from apps.properties.models import Property

User = get_user_model()

class PropertyInspection(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        CONFIRMED = "CONFIRMED", _("Confirmed")
        REJECTED = "REJECTED", _("Rejected")
        CANCELLED = "CANCELLED", _("Cancelled")
        COMPLETED = "COMPLETED", _("Completed")

    property = models.ForeignKey(Property, related_name="inspections", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="my_inspections", on_delete=models.CASCADE) # The person requesting
    agent = models.ForeignKey(User, related_name="scheduled_inspections", on_delete=models.CASCADE) # The agent
    
    inspection_date = models.DateField()
    inspection_time = models.TimeField()
    message = models.TextField(blank=True, default="I am interested in viewing this property.")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        verbose_name = "Property Inspection"
        verbose_name_plural = "Property Inspections"
        ordering = ["-inspection_date"]

    def __str__(self):
        return f"{self.user.full_name} visiting {self.property.title}"


# apps/interactions/models.py (Append this)

class Message(TimeStampedUUIDModel):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, blank=True)
    body = models.TextField()
    property = models.ForeignKey(Property, related_name="inquiries", on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"From {self.sender.full_name} to {self.recipient.full_name}"

class Announcement(TimeStampedUUIDModel):
    title = models.CharField(max_length=250)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title