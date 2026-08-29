import threading
from django.db import connections


def test_concurrent_deal_creation_only_one_wins(client, auth_headers):
    from listings.models import Listing

    seller_headers, seller = auth_headers(role="seller", username="seller2")
    listing = Listing.objects.create(
        seller=seller, brand="BMW", model="X5", year=2021,
        mileage=10000, price=30000, condition="used", city="Bishkek",
        status="active",
    )

    results = []

    def try_book(username):
        connections.close_all()  # каждый поток — новое соединение к БД
        headers, _ = auth_headers(role="buyer", username=username)
        response = client.post("/deals/", json={"listing_id": listing.id}, headers=headers)
        results.append(response.status_code)

    threads = [threading.Thread(target=try_book, args=(f"buyer_{i}",)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    success_count = results.count(201)
    assert success_count == 1, f"Expected exactly 1 success, got {success_count}: {results}"