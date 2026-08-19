from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "buyer", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("listing__brand", "listing__model", "buyer__username")