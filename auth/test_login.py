from auth.auth import login_user


def test_login_with_correct_password(test_db):
    success, user, message = login_user(
        "owner@test.com",
        "TestPassword123"
    )

    assert success is True
    assert user is not None
    assert user["name"] == "Test Owner"
    assert user["role"] == "owner"
    assert message == "Login successful."


def test_login_with_wrong_password(test_db):
    success, user, message = login_user(
        "owner@test.com",
        "WrongPassword123"
    )

    assert success is False
    assert user is None
    assert message == "Invalid email or password."


def test_login_with_unknown_email(test_db):
    success, user, message = login_user(
        "doesnotexist@test.com",
        "TestPassword123"
    )

    assert success is False
    assert user is None
    assert message == "Invalid email or password."