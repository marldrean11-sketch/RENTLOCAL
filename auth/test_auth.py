from auth.auth import register_user


success, message = register_user(
    "Test User",
    "test@rentlocal.com",
    "TestPassword123"
)

print("Registration result:", success)
print("Message:", message)