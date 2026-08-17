from auth.auth import login_user


success, user, message = login_user(
    "owner-test@rentlocal.com",
    "TestPassword123"
)

print("Correct password test:")
print("Success:", success)
print("Message:", message)

if user:
    print("User:", user["name"])
    print("Role:", user["role"])


success, user, message = login_user(
    "owner-test@rentlocal.com",
    "WrongPassword123"
)

print("\nWrong password test:")
print("Success:", success)
print("Message:", message)