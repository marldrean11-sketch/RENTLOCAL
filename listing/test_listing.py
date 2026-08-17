from listing.listing import create_listing


success, result = create_listing(
    owner_id=1,
    title="Renter Test Listing",
    description="This listing should not be created.",
    category="Test",
    price_per_day=100,
    location="Quezon City",
    condition="Good"
)

print("Renter listing test:")
print("Success:", success)
print("Result:", result)

