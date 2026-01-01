# apps/finance/models.py
import random
import string
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from apps.properties.models import Property

User = get_user_model()

class Transaction(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending Verification")
        VERIFIED = "VERIFIED", _("Verified (Paid)")
        FAILED = "FAILED", _("Failed / Rejected")

    class PaymentMethod(models.TextChoices):
        BANK_TRANSFER = "BANK_TRANSFER", _("Bank Transfer")
        CASH = "CASH", _("Cash")
        CHEQUE = "CHEQUE", _("Cheque")
        POS = "POS", _("POS Terminal")

    user = models.ForeignKey(User, related_name="transactions", on_delete=models.DO_NOTHING)
    property = models.ForeignKey(Property, related_name="transactions", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10, default="NGN")
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    description = models.CharField(max_length=255, help_text="e.g. Booking Fee for Duplex")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    note = models.TextField(blank=True, help_text="Agent notes on verification")

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            # Generate a unique receipt ID like TX-ABC12345
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=9))
            self.transaction_id = f"TX-{code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.amount} {self.currency}"


# apps/finance/models.py (Append this)

class Deal(TimeStampedUUIDModel):
    property = models.OneToOneField(Property, related_name="deal", on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name="deals_brokered", on_delete=models.DO_NOTHING)
    client = models.ForeignKey(User, related_name="deals_closed", on_delete=models.DO_NOTHING)
    
    final_price = models.DecimalField(max_digits=20, decimal_places=2, help_text="The actual price it was sold/rented for")
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, help_text="Agent commission %")
    commission_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    
    date_closed = models.DateField(auto_now_add=True)
    deal_description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate commission based on percentage
        if not self.commission_amount:
            self.commission_amount = (float(self.final_price) * float(self.commission_percentage)) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Deal for {self.property.title} - {self.final_price}"