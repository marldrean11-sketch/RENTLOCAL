from listing.listing import get_available_listings


listings = get_available_listings()

print("Available listings:")
print("Count:", len(listings))

for listing in listings:
    print(
        listing["id"],
        listing["title"],
        listing["category"],
        listing["price_per_day"],
        listing["location"],
        listing["owner_name"],
        listing["status"]
    )