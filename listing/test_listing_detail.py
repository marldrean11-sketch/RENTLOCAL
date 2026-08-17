from listing.listing import get_listing_by_id


listing = get_listing_by_id(1)

print("Listing detail test:")

if listing:
    print("Found:", True)
    print("ID:", listing["id"])
    print("Title:", listing["title"])
    print("Owner:", listing["owner_name"])
    print("Status:", listing["status"])
else:
    print("Found:", False)