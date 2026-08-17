from listing.listing import create_listing, get_owner_listings


def test_get_owner_listings(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Owner Test Listing",
        description="Listing owned by the test owner.",
        category="Test",
        price_per_day=200,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    listings = get_owner_listings(1)

    assert len(listings) == 1
    assert listings[0]["id"] == listing_id
    assert listings[0]["title"] == "Owner Test Listing"


def test_owner_does_not_see_other_owner_listings(test_db):
    listings = get_owner_listings(2)

    assert len(listings) == 0