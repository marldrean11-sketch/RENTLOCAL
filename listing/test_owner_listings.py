from listing.listing import get_owner_listings


listings = get_owner_listings(2)

print("Owner listings:")
print("Count:", len(listings))

for listing in listings:
    print(
        listing["id"],
        listing["title"],
        listing["category"],
        listing["price_per_day"],
        listing["location"],
        listing["status"]
    )