from listing.listing import update_rental_request_status


success, message = update_rental_request_status(
    request_id=2,
    owner_id=2,
    status="rejected"
)

print("Reject request test:")
print("Success:", success)
print("Message:", message)