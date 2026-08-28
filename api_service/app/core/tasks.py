import os
from celery import Celery

celery_app = Celery("car_marketplace_producer", broker=os.environ.get("REDIS_URL"))


def enqueue_deal_status_email(deal_id: int, old_status: str, new_status: str):
    celery_app.send_task(
        "deals.tasks.send_deal_status_email",
        args=[deal_id, old_status, new_status],
    )