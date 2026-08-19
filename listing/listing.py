from database.db import get_db_connection
from datetime import date


def create_listing(
    owner_id,
    title,
    description,
    category,
    price_per_day,
    location,
    condition,
    image_filename=None
):
    title = title.strip()
    description = description.strip()
    category = category.strip()
    location = location.strip()
    condition = condition.strip()

    if not title or not description or not category:
        return False, "Title, description, and category are required."

    if not location:
        return False, "Location is required."

    if not condition:
        return False, "Condition is required."

    try:
        price_per_day = float(price_per_day)
    except (TypeError, ValueError):
        return False, "Price must be a valid number."

    if price_per_day <= 0:
        return False, "Price must be greater than zero."

    connection = get_db_connection()

    owner = connection.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        AND role = 'owner'
        AND is_active = 1
        """,
        (owner_id,)
    ).fetchone()

    if not owner:
        connection.close()
        return False, "Only active owners can create listings."

    cursor = connection.execute(
        """
        INSERT INTO listings (
            owner_id,
            title,
            description,
            category,
            price_per_day,
            location,
            condition,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            owner_id,
            title,
            description,
            category,
            price_per_day,
            location,
            condition,
            "available"
        )
    )

    listing_id = cursor.lastrowid

    # Save the uploaded image reference
    if image_filename:
        connection.execute(
            """
            INSERT INTO listing_images (
                listing_id,
                filename,
                is_primary
            )
            VALUES (?, ?, ?)
            """,
            (
                listing_id,
                image_filename,
                1
            )
        )

    connection.commit()
    connection.close()

    return True, listing_id

def get_owner_listings(owner_id):
    connection = get_db_connection()

    listings = connection.execute(
        """
        SELECT
            listings.id,
            listings.title,
            listings.description,
            listings.category,
            listings.price_per_day,
            listings.location,
            listings.condition,
            listings.status,
            listings.created_at,
            listing_images.filename AS image_filename
        FROM listings
        LEFT JOIN listing_images
            ON listings.id = listing_images.listing_id
            AND listing_images.is_primary = 1
        WHERE listings.owner_id = ?
        ORDER BY listings.created_at DESC, listings.id DESC
        """,
        (owner_id,)
    ).fetchall()

    connection.close()

    return listings


def update_listing(
    listing_id,
    owner_id,
    title,
    description,
    category,
    price_per_day,
    location,
    condition
):
    title = title.strip()
    description = description.strip()
    category = category.strip()
    location = location.strip()
    condition = condition.strip()

    if not title or not description or not category:
        return False, "Title, description, and category are required."

    if not location:
        return False, "Location is required."

    if not condition:
        return False, "Condition is required."

    try:
        price_per_day = float(price_per_day)
    except (TypeError, ValueError):
        return False, "Price must be a valid number."

    if price_per_day <= 0:
        return False, "Price must be greater than zero."

    connection = get_db_connection()

    listing = connection.execute(
        """
        SELECT id
        FROM listings
        WHERE id = ?
        AND owner_id = ?
        """,
        (listing_id, owner_id)
    ).fetchone()

    if not listing:
        connection.close()
        return False, "Listing not found."

    connection.execute(
        """
        UPDATE listings
        SET title = ?,
            description = ?,
            category = ?,
            price_per_day = ?,
            location = ?,
            condition = ?
        WHERE id = ?
        AND owner_id = ?
        """,
        (
            title,
            description,
            category,
            price_per_day,
            location,
            condition,
            listing_id,
            owner_id
        )
    )

    connection.commit()
    connection.close()

    return True, "Listing updated successfully."




def delete_listing(listing_id, owner_id):
    connection = get_db_connection()

    listing = connection.execute(
        """
        SELECT id
        FROM listings
        WHERE id = ?
        AND owner_id = ?
        """,
        (listing_id, owner_id)
    ).fetchone()

    if not listing:
        connection.close()
        return False, "Listing not found."

    rental_requests = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM rental_requests
        WHERE listing_id = ?
        """,
        (listing_id,)
    ).fetchone()

    if rental_requests["count"] > 0:
        connection.close()
        return False, "Listings with rental request history cannot be deleted."

    connection.execute(
        """
        DELETE FROM listings
        WHERE id = ?
        AND owner_id = ?
        """,
        (listing_id, owner_id)
    )

    connection.commit()
    connection.close()

    return True, "Listing deleted successfully."



def get_available_listings(
    search="",
    category="",
    location=""
):
    connection = get_db_connection()

    query = """
        SELECT
            listings.id,
            listings.title,
            listings.description,
            listings.category,
            listings.price_per_day,
            listings.location,
            listings.condition,
            listings.status,
            listings.created_at,
            users.name AS owner_name,
            listing_images.filename AS image_filename
        FROM listings
        JOIN users
            ON listings.owner_id = users.id
        LEFT JOIN listing_images
            ON listings.id = listing_images.listing_id
            AND listing_images.is_primary = 1
        WHERE listings.status = 'available'
    """

    parameters = []

    if search:
        query += """
            AND (
                listings.title LIKE ?
                OR listings.description LIKE ?
            )
        """

        search_pattern = f"%{search}%"

        parameters.extend([
            search_pattern,
            search_pattern
        ])

    if category:
        query += """
            AND listings.category = ?
        """

        parameters.append(category)

    if location:
        query += """
            AND listings.location LIKE ?
        """

        parameters.append(f"%{location}%")

    query += """
        ORDER BY listings.created_at DESC,
                 listings.id DESC
    """

    listings = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return listings



def get_listing_by_id(listing_id):
    connection = get_db_connection()

    listing = connection.execute(
        """
        SELECT
            listings.id,
            listings.title,
            listings.description,
            listings.category,
            listings.price_per_day,
            listings.location,
            listings.condition,
            listings.status,
            listings.created_at,
            users.name AS owner_name,
            listing_images.filename AS image_filename
        FROM listings
        JOIN users
            ON listings.owner_id = users.id
        LEFT JOIN listing_images
            ON listings.id = listing_images.listing_id
            AND listing_images.is_primary = 1
        WHERE listings.id = ?
        """,
        (listing_id,)
    ).fetchone()

    connection.close()

    return listing


def create_rental_request(
    listing_id,
    renter_id,
    start_date,
    end_date,
    message
):
    start_date = start_date.strip()
    end_date = end_date.strip()
    message = message.strip()

    if not start_date or not end_date:
        return False, "Start date and end date are required."

    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError:
        return False, "Start date and end date must be valid dates."
    
    if end < start:
        return False, "End date cannot be earlier than start date."
    
    if start < date.today():
        return False, "Start date cannot be in the past."

    connection = get_db_connection()

    overlapping_request = connection.execute(
        """
        SELECT id
        FROM rental_requests
        WHERE listing_id = ?
        AND status IN ('pending', 'accepted')
        AND start_date <= ?
        AND end_date >= ?
        """,
        (
            listing_id,
            end_date,
            start_date
        )
    ).fetchone()

    if overlapping_request:
        connection.close()
        return False, "This listing already has a rental request for the selected dates."

    renter = connection.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        AND role = 'renter'
        AND is_active = 1
        """,
        (renter_id,)
    ).fetchone()

    if not renter:
        connection.close()
        return False, "Only active renters can submit rental requests."

    listing = connection.execute(
        """
        SELECT id, owner_id, status
        FROM listings
        WHERE id = ?
        """,
        (listing_id,)
    ).fetchone()

    if not listing:
        connection.close()
        return False, "Listing not found."

    if listing["owner_id"] == renter_id:
        connection.close()
        return False, "You cannot request your own listing."

    if listing["status"] != "available":
        connection.close()
        return False, "This listing is not currently available."

    cursor = connection.execute(
        """
        INSERT INTO rental_requests (
            listing_id,
            renter_id,
            start_date,
            end_date,
            status,
            message
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            listing_id,
            renter_id,
            start_date,
            end_date,
            "pending",
            message
        )
    )

    request_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return True, request_id


def get_owner_rental_requests(owner_id):
    connection = get_db_connection()

    requests = connection.execute(
        """
        SELECT
            rental_requests.id,
            rental_requests.listing_id,
            rental_requests.renter_id,
            rental_requests.start_date,
            rental_requests.end_date,
            rental_requests.status,
            rental_requests.message,
            rental_requests.created_at,
            listings.title AS listing_title,
            users.name AS renter_name
        FROM rental_requests
        JOIN listings
            ON rental_requests.listing_id = listings.id
        JOIN users
            ON rental_requests.renter_id = users.id
        WHERE listings.owner_id = ?
        ORDER BY rental_requests.created_at DESC,
                 rental_requests.id DESC
        """,
        (owner_id,)
    ).fetchall()

    connection.close()

    return requests



def update_rental_request_status(
    request_id,
    owner_id,
    status
):
    if status not in ("accepted", "rejected"):
        return False, "Invalid request status."

    connection = get_db_connection()

    try:
        rental_request = connection.execute(
            """
            SELECT
                rental_requests.id,
                rental_requests.listing_id,
                rental_requests.status,
                listings.owner_id
            FROM rental_requests
            JOIN listings
                ON rental_requests.listing_id = listings.id
            WHERE rental_requests.id = ?
            AND listings.owner_id = ?
            """,
            (request_id, owner_id)
        ).fetchone()

        if not rental_request:
            return False, "Rental request not found."

        if rental_request["status"] != "pending":
            return False, "Only pending requests can be updated."

        # Update the rental request status
        connection.execute(
            """
            UPDATE rental_requests
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, request_id)
        )

        # If the request is accepted,
        # make the corresponding listing unavailable.
        if status == "accepted":
            connection.execute(
                """
                UPDATE listings
                SET status = 'unavailable'
                WHERE id = ?
                """,
                (rental_request["listing_id"],)
            )

        connection.commit()

        return True, "Rental request status updated successfully."

    except Exception as error:
        connection.rollback()
        print("UPDATE REQUEST STATUS ERROR:", error)
        return False, "Failed to update rental request status."

    finally:
        connection.close()




def get_renter_rental_requests(renter_id):
    connection = get_db_connection()

    requests = connection.execute(
        """
        SELECT
            rental_requests.id,
            rental_requests.listing_id,
            rental_requests.start_date,
            rental_requests.end_date,
            rental_requests.status,
            rental_requests.message,
            rental_requests.created_at,
            listings.title AS listing_title,
            users.name AS owner_name
        FROM rental_requests
        JOIN listings
            ON rental_requests.listing_id = listings.id
        JOIN users
            ON listings.owner_id = users.id
        WHERE rental_requests.renter_id = ?
        ORDER BY rental_requests.created_at DESC,
                 rental_requests.id DESC
        """,
        (renter_id,)
    ).fetchall()

    connection.close()

    return requests