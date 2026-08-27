from fastapi import APIRouter, Depends, HTTPException
from asgiref.sync import sync_to_async
from app.core.dependencies import get_current_user, require_role
from app.core.cache import invalidate_listings_cache
from app.schemas.deal import DealCreate, DealStatusUpdate, DealOut

router = APIRouter(prefix="/deals", tags=["deals"])

ALLOWED_TRANSITIONS = {
    "pending": {"negotiating", "cancelled"},
    "negotiating": {"confirmed", "cancelled"},
    "confirmed": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}

@router.post("/", response_model=DealOut, status_code=201)
async def create_deal(
    data: DealCreate,
    current_user: dict = Depends(require_role("buyer")),
):
    from listings.models import Listing
    from deals.models import Deal

    def create():
        listing = Listing.objects.filter(id=data.listing_id, status="active").first()
        if listing is None:
            return None
        deal = Deal.objects.create(listing=listing, buyer_id=current_user["user_id"])
        listing.status = "reserved"
        listing.save(update_fields=["status"])
        return deal

    deal = await sync_to_async(create)()
    if deal is None:
        raise HTTPException(status_code=404, detail="Listing not found or not active")

    await invalidate_listings_cache()
    return DealOut.model_validate(deal)

@router.patch("/{deal_id}/status", response_model=DealOut)
async def update_deal_status(
    deal_id: int,
    data: DealStatusUpdate,
    current_user: dict = Depends(get_current_user),
):
    from deals.models import Deal

    def get_deal():
        return Deal.objects.select_related("listing").filter(id=deal_id).first()

    deal = await sync_to_async(get_deal)()
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")

    is_buyer = current_user["role"] == "buyer" and deal.buyer_id == current_user["user_id"]
    is_seller = current_user["role"] == "seller" and deal.listing.seller_id == current_user["user_id"]
    is_admin = current_user["role"] == "admin"
    if not (is_buyer or is_seller or is_admin):
        raise HTTPException(status_code=403, detail="Not your deal")

    if data.status not in ALLOWED_TRANSITIONS.get(deal.status, set()):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from {deal.status} to {data.status}",
        )

    def apply_transition():
        deal.status = data.status
        deal.save(update_fields=["status", "updated_at"])
        if data.status in ("completed",):
            deal.listing.status = "sold"
            deal.listing.save(update_fields=["status"])
        elif data.status == "cancelled":
            deal.listing.status = "active"
            deal.listing.save(update_fields=["status"])
        return deal

    updated = await sync_to_async(apply_transition)()
    await invalidate_listings_cache()

    # TODO день 12: Celery-таск на email при смене статуса

    return DealOut.model_validate(updated)