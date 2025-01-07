import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Generate hash for 'admin123'
hashed_password = hash_password("admin123")
print(f"Hashed password for 'admin123': {hashed_password}")
