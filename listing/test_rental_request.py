from listing.listing import create_rental_request


success, result = create_rental_request(
    listing_id=1,
    renter_id=1,
    start_date="2026-08-15",
    end_date="2026-08-17",
    message="I would like to rent this drill for a home repair project."
)

print("Rental request test:")
print("Success:", success)
print("Result:", result)