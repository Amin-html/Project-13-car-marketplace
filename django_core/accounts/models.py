from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Seller"
        BUYER = "buyer", "Buyer"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"