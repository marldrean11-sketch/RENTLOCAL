from datetime import date, timedelta

from listing.listing import create_listing, create_rental_request


def test_renter_can_create_rental_request(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Rental Test Projector",
        description="Projector for rental testing.",
        category="Presentation & Events",
        price_per_day=500,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    start = date.today() + timedelta(days=5)
    end = start + timedelta(days=2)

    success, request_id = create_rental_request(
        listing_id=listing_id,
        renter_id=2,
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        message="I would like to rent this equipment."
    )

    assert success is True
    assert isinstance(request_id, int)
    assert request_id > 0


def test_renter_cannot_request_own_listing(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Owner Equipment",
        description="Owner equipment.",
        category="Test",
        price_per_day=100,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    start = date.today() + timedelta(days=5)
    end = start + timedelta(days=6)

    success, message = create_rental_request(
        listing_id=listing_id,
        renter_id=1,
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        message="Invalid request."
    )

    assert success is False
    assert message == "Only active renters can submit rental requests."