# User Model Documentation

## Overview

The User model provides a complete user authentication and management system with the following features:

- **Secure password hashing** using Werkzeug's `generate_password_hash` and `check_password_hash`
- **Username and email uniqueness validation**
- **Password complexity requirements**
- **Input validation** for username and email formats
- **Database integration** with SQLAlchemy

## Model Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key, auto-incrementing |
| `username` | String(80) | Unique username, indexed |
| `email` | String(120) | Unique email address, indexed |
| `password_hash` | String(255) | Hashed password (never stored in plain text) |
| `created_at` | DateTime | User creation timestamp |
| `updated_at` | DateTime | Last update timestamp |
| `is_active` | Boolean | Account active status (default: True) |
| `is_verified` | Boolean | Email verification status (default: False) |

## Password Complexity Requirements

Passwords must meet the following criteria:
- **Minimum 8 characters** in length
- **At least one uppercase letter** (A-Z)
- **At least one lowercase letter** (a-z)
- **At least one digit** (0-9)
- **At least one special character** (!@#$%^&*(),.?":{}|<>)

## Username Validation

Usernames must:
- Be **3-20 characters** in length
- Contain only **alphanumeric characters and underscores**
- Be **unique** across all users

## Email Validation

Emails must:
- Follow standard email format (user@domain.com)
- Be **unique** across all users

## Usage Examples

### Creating a New User

```python
from models.user import User

# Create user with validation
try:
    user = User.create_user(
        username="john_doe",
        email="john@example.com",
        password="SecurePass123!"
    )
    db.session.add(user)
    db.session.commit()
    print("User created successfully!")
except ValueError as e:
    print(f"Validation error: {e}")
```

### Password Verification

```python
# Check if password is correct
user = User.find_by_username("john_doe")
if user and user.check_password("SecurePass123!"):
    print("Password is correct!")
else:
    print("Invalid password!")
```

### Finding Users

```python
# Find by username
user = User.find_by_username("john_doe")

# Find by email
user = User.find_by_email("john@example.com")

# Find by ID
user = User.find_by_id(1)
```

### User Data Serialization

```python
# Convert user to dictionary (excludes sensitive data)
user_dict = user.to_dict()
print(user_dict)
# Output: {
#     'id': 1,
#     'username': 'john_doe',
#     'email': 'john@example.com',
#     'created_at': '2024-01-01T12:00:00',
#     'updated_at': '2024-01-01T12:00:00',
#     'is_active': True,
#     'is_verified': False
# }
```

## Error Handling

The model provides clear error messages for validation failures:

- **Invalid username format**: "Invalid username format. Must be 3-20 characters, alphanumeric and underscores only."
- **Invalid email format**: "Invalid email format."
- **Username already exists**: "Username already exists."
- **Email already exists**: "Email already exists."
- **Password complexity**: "Password does not meet complexity requirements."

## Security Features

1. **Password Hashing**: All passwords are hashed using Werkzeug's secure hashing
2. **No Plain Text Storage**: Passwords are never stored in plain text
3. **Input Validation**: All user inputs are validated before processing
4. **Unique Constraints**: Database-level uniqueness constraints on username and email
5. **Indexed Fields**: Username and email are indexed for fast lookups

## Dependencies

Make sure to install the required dependencies:

```bash
pip install -r requirements.txt
```

The User model requires:
- `Flask-SQLAlchemy` for database integration
- `Werkzeug` for password hashing
- `SQLAlchemy` for database operations

## Testing

Run the test script to validate all functionality:

```bash
cd app/backend
python test_user_model.py
```

This will test:
- Password complexity validation
- Username format validation
- Email format validation
- Password hashing and verification
- User creation with validation
- Duplicate username/email handling 