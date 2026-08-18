import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from functools import wraps
from auth.auth import register_user, login_user
from listing.listing import (
    create_listing,
    create_rental_request,
    get_owner_listings,
    get_available_listings,
    get_listing_by_id,  
    get_owner_rental_requests,
    get_renter_rental_requests,
    update_listing,
    delete_listing,
    update_rental_request_status,
    get_db_connection
)


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.secret_key = "dev-secret-key"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to continue.", "error")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


def owner_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to continue.", "error")
            return redirect(url_for("login"))

        if session.get("user_role") != "owner":
            flash("Owner access required.", "error")
            return redirect(url_for("home"))

        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def home():
    listings = get_available_listings()

    return render_template(
        "index.html",
        listings=listings
    )


@app.route("/browse")
def browse():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    location = request.args.get("location", "").strip()

    listings = get_available_listings()

    if search:
        search_lower = search.lower()

        listings = [
            listing
            for listing in listings
            if search_lower in listing["title"].lower()
            or search_lower in listing["description"].lower()
            or search_lower in listing["category"].lower()
        ]

    if category:
        listings = [
            listing
            for listing in listings
            if listing["category"] == category
        ]

    if location:
        location_lower = location.lower()

        listings = [
            listing
            for listing in listings
            if location_lower in listing["location"].lower()
        ]

    return render_template(
        "browse.html",
        listings=listings,
        categories=RENTLOCAL_CATEGORIES,
        search=search,
        category=category,
        location=location
    )



@app.route("/listing/<int:listing_id>")
def listing_detail(listing_id):
    listing = get_listing_by_id(listing_id)

    if not listing:
        return "Listing not found", 404

    return render_template(
        "listing_detail.html",
        listing=listing
    )


@app.route("/listing/<int:listing_id>/request", methods=["POST"])
@login_required
def request_rental(listing_id):
    if session.get("user_role") != "renter":
        flash("Only renters can submit rental requests.", "error")
        return redirect(url_for("listing_detail", listing_id=listing_id))

    start_date = request.form.get("start_date", "")
    end_date = request.form.get("end_date", "")
    message = request.form.get("message", "")

    success, result = create_rental_request(
        listing_id=listing_id,
        renter_id=session["user_id"],
        start_date=start_date,
        end_date=end_date,
        message=message
    )

    if success:
        flash("Rental request submitted successfully.", "success")
    else:
        flash(result, "error")

    return redirect(url_for("listing_detail", listing_id=listing_id))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        role = request.form.get("role", "renter")

        success, message = register_user(
            name,
            email,
            password,
            role
        )

        if success:
            flash(message, "success")
        else:
            flash(message, "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        success, user, message = login_user(email, password)

        if success:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]

            flash(message, "success")
            return redirect(url_for("home"))

        flash(message, "error")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/owner-test")
@owner_required
def owner_test():
    return f"""
        <h1>Owner Area</h1>
        <p>Welcome, {session["user_name"]}</p>
        <p>Role: {session["user_role"]}</p>
    """


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("home"))


@app.route("/owner/listings/new", methods=["GET", "POST"])
@login_required
@owner_required
def create_listing_page():
    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        price_per_day = request.form.get("price_per_day", "")
        location = request.form.get("location", "")
        condition = request.form.get("condition", "")
        image = request.files.get("image")

        image_filename = None
        if image and image.filename:
            image_filename = image.filename
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
            image.save(image_path)

        success, result = create_listing(
            owner_id=session["user_id"],
            title=title,
            description=description,
            category=category,
            price_per_day=price_per_day,
            location=location,
            condition=condition,
            image_filename=image_filename
        )

        if success:
            flash("Listing created successfully.", "success")
            return redirect(url_for("dashboard"))

        flash(result, "error")

    return render_template(
    "create_listing.html",
    categories=RENTLOCAL_CATEGORIES
)


@app.route("/owner/listings")
@login_required
@owner_required
def owner_listings():
    listings = get_owner_listings(session["user_id"])

    return render_template(
        "owner_listings.html",
        listings=listings
    )


@app.route("/owner/listings/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
@owner_required
def edit_listing(listing_id):
    listing = get_listing_by_id(listing_id)

    if not listing:
        flash("Listing not found.", "error")
        return redirect(url_for("owner_listings"))

    connection = get_db_connection()

    owner_check = connection.execute(
        """
        SELECT id
        FROM listings
        WHERE id = ?
        AND owner_id = ?
        """,
        (listing_id, session["user_id"])
    ).fetchone()

    connection.close()

    if not owner_check:
        flash("You can only edit your own listings.", "error")
        return redirect(url_for("owner_listings"))

    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        price_per_day = request.form.get("price_per_day", "")
        location = request.form.get("location", "")
        condition = request.form.get("condition", "")

        success, message = update_listing(
            listing_id=listing_id,
            owner_id=session["user_id"],
            title=title,
            description=description,
            category=category,
            price_per_day=price_per_day,
            location=location,
            condition=condition
        )

        if success:
            flash(message, "success")
            return redirect(url_for("owner_listings"))

        flash(message, "error")

    return render_template(
    "edit_listing.html",
    listing=listing,
    categories=RENTLOCAL_CATEGORIES
)


@app.route("/owner/listings/<int:listing_id>/delete", methods=["POST"])
@login_required
@owner_required
def delete_listing_page(listing_id):
    success, message = delete_listing(
        listing_id=listing_id,
        owner_id=session["user_id"]
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("owner_listings"))


@app.route("/owner/requests")
@login_required
@owner_required
def owner_requests():
    requests = get_owner_rental_requests(session["user_id"])

    return render_template(
        "owner_requests.html",
        requests=requests
    )


@app.route("/renter/requests")
@login_required
def renter_requests():
    if session.get("user_role") != "renter":
        flash("Renter access required.", "error")
        return redirect(url_for("home"))

    requests = get_renter_rental_requests(
        session["user_id"]
    )

    return render_template(
        "renter_requests.html",
        requests=requests
    )


@app.route("/owner/requests/<int:request_id>/status", methods=["POST"])
@login_required
@owner_required
def update_request_status(request_id):
    status = request.form.get("status", "")

    success, message = update_rental_request_status(
        request_id=request_id,
        owner_id=session["user_id"],
        status=status
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

        print("STATUS FLASH:", message)

    return redirect(url_for("owner_requests"))


RENTLOCAL_CATEGORIES = [
    "Study & School",   
    "Presentation & Events",
    "Photography & Video",
    "Audio & Content Creation",
    "Tech & Gadgets",
    "Tools & DIY",
    "Sports & Recreation",
    "Other",
]

if __name__ == "__main__":
    app.run(debug=True)