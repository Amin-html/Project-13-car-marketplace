from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_deal_status_email(deal_id: int, old_status: str, new_status: str):
    from deals.models import Deal

    try:
        deal = Deal.objects.select_related("listing", "buyer", "listing__seller").get(id=deal_id)
    except Deal.DoesNotExist:
        return

    subject = f"Сделка #{deal_id}: статус изменён на {new_status}"
    message = (
        f"Объявление: {deal.listing.brand} {deal.listing.model}\n"
        f"Статус: {old_status} → {new_status}"
    )
    recipients = [deal.buyer.email, deal.listing.seller.email]
    send_mail(subject, message, None, recipients, fail_silently=True)