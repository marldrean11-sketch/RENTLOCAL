from listing.listing import create_listing, get_available_listings


def test_browse_available_listings(test_db):
    success, listing_id = create_listing(
        owner_id=1,
        title="Test Projector",
        description="Portable projector for presentations.",
        category="Presentation & Events",
        price_per_day=500,
        location="Taguig",
        condition="Good"
    )

    assert success is True

    listings = get_available_listings()

    assert len(listings) == 1
    assert listings[0]["id"] == listing_id
    assert listings[0]["title"] == "Test Projector"
    assert listings[0]["owner_name"] == "Test Owner"


def test_browse_search_filter(test_db):
    create_listing(
        owner_id=1,
        title="Portable Projector",
        description="Projector for presentations.",
        category="Presentation & Events",
        price_per_day=500,
        location="Taguig",
        condition="Good"
    )

    create_listing(
        owner_id=1,
        title="Badminton Racket",
        description="Racket for recreation.",
        category="Sports & Recreation",
        price_per_day=100,
        location="Quezon City",
        condition="Good"
    )

    results = get_available_listings(search="Projector")

    assert len(results) == 1
    assert results[0]["title"] == "Portable Projector"

    results = get_available_listings(category="Sports & Recreation")

    assert len(results) == 1
    assert results[0]["title"] == "Badminton Racket"

    results = get_available_listings(location="Taguig")

    assert len(results) == 1
    assert results[0]["title"] == "Portable Projector"