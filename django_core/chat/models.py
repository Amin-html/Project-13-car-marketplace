from django.db import models
from django.conf import settings
from listings.models import Listing

class ChatMessage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["listing", "created_at"])]

    def __str__(self):
        return f"msg#{self.id} on listing#{self.listing_id}"