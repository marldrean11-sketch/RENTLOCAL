from datetime import date, timedelta

from listing.listing import (
    create_listing,
    create_rental_request,
    get_renter_rental_requests
)


def test_renter_can_view_rental_requests(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Renter Request Equipment",
        description="Equipment for renter request testing.",
        category="Test",
        price_per_day=150,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    start = date.today() + timedelta(days=7)
    end = start + timedelta(days=2)

    success, request_id = create_rental_request(
        listing_id,
        2,
        start.isoformat(),
        end.isoformat(),
        "Renter request test."
    )

    assert success is True

    requests = get_renter_rental_requests(2)

    assert len(requests) == 1
    assert requests[0]["id"] == request_id
    assert requests[0]["listing_title"] == "Renter Request Equipment"
    assert requests[0]["owner_name"] == "Test Owner"
    assert requests[0]["status"] == "pending"