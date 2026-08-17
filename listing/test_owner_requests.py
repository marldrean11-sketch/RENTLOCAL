from datetime import date, timedelta

from listing.listing import (
    create_listing,
    create_rental_request,
    get_owner_rental_requests
)


def test_owner_can_view_rental_requests(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Request Test Equipment",
        description="Equipment for request testing.",
        category="Test",
        price_per_day=200,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    start = date.today() + timedelta(days=5)
    end = start + timedelta(days=6)

    success, request_id = create_rental_request(
        listing_id,
        2,
        start.isoformat(),
        end.isoformat(),
        "Test rental request."
    )

    assert success is True

    requests = get_owner_rental_requests(1)

    assert len(requests) == 1
    assert requests[0]["id"] == request_id
    assert requests[0]["listing_title"] == "Request Test Equipment"
    assert requests[0]["renter_name"] == "Test Renter"
    assert requests[0]["status"] == "pending"