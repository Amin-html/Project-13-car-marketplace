import pytest
from app.routers.deals import ALLOWED_TRANSITIONS


@pytest.mark.parametrize("from_status,to_status,expected", [
    ("pending", "negotiating", True),
    ("pending", "completed", False),      # нельзя перепрыгнуть сразу
    ("negotiating", "confirmed", True),
    ("confirmed", "completed", True),
    ("completed", "cancelled", False),    # терминальный статус
    ("cancelled", "pending", False),      # терминальный статус
])
def test_allowed_transitions(from_status, to_status, expected):
    allowed = to_status in ALLOWED_TRANSITIONS.get(from_status, set())
    assert allowed == expected


def test_create_deal_on_inactive_listing_fails(client, auth_headers):
    from listings.models import Listing

    headers, buyer = auth_headers(role="buyer")

    seller_headers, seller = auth_headers(role="seller", username="seller1")
    listing = Listing.objects.create(
        seller=seller, brand="Toyota", model="Camry", year=2020,
        mileage=50000, price=15000, condition="used", city="Bishkek",
        status="sold",  # уже не активно
    )

    response = client.post("/deals/", json={"listing_id": listing.id}, headers=headers)
    assert response.status_code == 404