from listing.listing import create_listing


def test_owner_can_create_listing(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Test Projector",
        description="Portable projector for testing.",
        category="Presentation & Events",
        price_per_day=500,
        location="Taguig",
        condition="Good"
    )

    assert success is True
    assert isinstance(listing_id, int)
    assert listing_id > 0


def test_renter_cannot_create_listing(test_db):
    success, message = create_listing(
        owner_id=2,
        title="Invalid Listing",
        description="This should not be created.",
        category="Test",
        price_per_day=100,
        location="Quezon City",
        condition="Good"
    )

    assert success is False
    assert message == "Only active owners can create listings."


def test_listing_rejects_invalid_price(test_db):
    success, message = create_listing(
        owner_id=1,
        title="Invalid Price",
        description="Testing invalid price.",
        category="Test",
        price_per_day=0,
        location="Quezon City",
        condition="Good"
    )

    assert success is False
    assert message == "Price must be greater than zero."