from fastapi import APIRouter, Depends, HTTPException, Query
from asgiref.sync import sync_to_async
from app.core.dependencies import get_current_user, require_role
from app.schemas.listing import ListingCreate, ListingOut, ListingListResponse

router = APIRouter(prefix="/listings", tags=["listings"])

@router.get("/", response_model=ListingListResponse)
async def list_listings(
    brand: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    mileage_max: int | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    from listings.models import Listing
    from django.db.models import Q

    def build_queryset():
        qs = Listing.objects.filter(status="active")
        if brand:
            qs = qs.filter(brand__iexact=brand)
        if year_min:
            qs = qs.filter(year__gte=year_min)
        if year_max:
            qs = qs.filter(year__lte=year_max)
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if mileage_max:
            qs = qs.filter(mileage__lte=mileage_max)
        if search:
            qs = qs.filter(Q(brand__icontains=search) | Q(model__icontains=search))
        return qs.order_by("-created_at")

    def paginate(qs):
        total = qs.count()
        offset = (page - 1) * page_size
        items = list(qs[offset : offset + page_size])
        return total, items

    qs = await sync_to_async(build_queryset)()
    total, items = await sync_to_async(paginate)(qs)

    return ListingListResponse(
        total=total,
        page=page,
        page_size=page_size,
        results=[ListingOut.model_validate(i) for i in items],
    )

@router.post("/", response_model=ListingOut, status_code=201)
async def create_listing(
    data: ListingCreate,
    current_user: dict = Depends(require_role("seller", "admin")),
):
    from listings.models import Listing

    def create():
        return Listing.objects.create(seller_id=current_user["user_id"], **data.model_dump())

    listing = await sync_to_async(create)()
    return ListingOut.model_validate(listing)

@router.get("/{listing_id}", response_model=ListingOut)
async def get_listing(listing_id: int):
    from listings.models import Listing

    def fetch():
        return Listing.objects.filter(id=listing_id).first()

    listing = await sync_to_async(fetch)()
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return ListingOut.model_validate(listing)

@router.get("/me")
async def whoami(current_user: dict = Depends(get_current_user)):
    return current_user