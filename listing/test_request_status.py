from datetime import date, timedelta

from listing.listing import (
    create_listing,
    create_rental_request,
    update_rental_request_status,
    get_renter_rental_requests
)


def test_owner_can_accept_pending_request(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Accept Test Equipment",
        description="Equipment for accept testing.",
        category="Test",
        price_per_day=200,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    start = date.today() + timedelta(days=10)
    end = start + timedelta(days=2)

    success, request_id = create_rental_request(
        listing_id,
        2,
        start.isoformat(),
        end.isoformat(),
        "Accept this request."
    )

    assert success is True

    success, message = update_rental_request_status(
        request_id,
        1,
        "accepted"
    )

    assert success is True
    assert message == "Rental request status updated successfully."

    requests = get_renter_rental_requests(2)

    assert requests[0]["status"] == "accepted"


def test_owner_can_reject_pending_request(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Reject Test Equipment",
        description="Equipment for reject testing.",
        category="Test",
        price_per_day=200,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    start = date.today() + timedelta(days=15)
    end = start + timedelta(days=2)

    success, request_id = create_rental_request(
        listing_id,
        2,
        start.isoformat(),
        end.isoformat(),
        "Reject this request."
    )

    assert success is True

    success, message = update_rental_request_status(
        request_id,
        1,
        "rejected"
    )

    assert success is True
    assert message == "Rental request status updated successfully."

    requests = get_renter_rental_requests(2)

    assert requests[0]["status"] == "rejected"


def test_invalid_request_status_is_rejected(test_db):
    success, message = update_rental_request_status(
        999,
        1,
        "invalid"
    )

    assert success is False
    assert message == "Invalid request status."