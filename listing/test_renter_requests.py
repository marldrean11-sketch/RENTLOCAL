from listing.listing import get_renter_rental_requests


requests = get_renter_rental_requests(1)

print("Renter rental requests:")
print("Count:", len(requests))

for request in requests:
    print(dict(request))