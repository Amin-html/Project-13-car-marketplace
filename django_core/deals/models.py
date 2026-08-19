from django.db import models
from django.conf import settings
from listings.models import Listing


class Deal(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        NEGOTIATING = "negotiating", "Negotiating"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="deals")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deals")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Deal #{self.id} ({self.status})"