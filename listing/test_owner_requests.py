from listing.listing import get_owner_rental_requests


requests = get_owner_rental_requests(owner_id=2)

print("Owner rental requests:")
print("Count:", len(requests))

for request in requests:
    print(dict(request))