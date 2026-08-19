from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "price", "status", "seller", "city")
    list_filter = ("brand", "status", "condition", "city")
    search_fields = ("brand", "model", "vin")