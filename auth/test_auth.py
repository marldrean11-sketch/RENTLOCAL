from auth.auth import register_user


def test_register_user_success(test_db):
    success, message = register_user(
        "New User",
        "newuser@test.com",
        "TestPassword123"
    )

    assert success is True
    assert message == "Account created successfully."


def test_register_user_rejects_duplicate_email(test_db):
    success, message = register_user(
        "Another User",
        "owner@test.com",
        "TestPassword123"
    )

    assert success is False
    assert message == "An account with this email already exists."


def test_register_user_rejects_short_password(test_db):
    success, message = register_user(
        "Short Password",
        "short@test.com",
        "123"
    )

    assert success is False
    assert message == "Password must be at least 8 characters."