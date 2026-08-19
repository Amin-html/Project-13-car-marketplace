from django.db import models
from django.conf import settings


class Listing(models.Model):
    class Condition(models.TextChoices):
        NEW = "new", "New"
        USED = "used", "Used"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        RESERVED = "reserved", "Reserved"
        SOLD = "sold", "Sold"

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(help_text="km")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=10, choices=Condition.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    vin = models.CharField(max_length=17, blank=True, null=True)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["brand", "year"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"