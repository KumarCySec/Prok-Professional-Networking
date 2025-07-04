# Flask Application Setup

This is a Flask application with a User model, database integration, and proper application factory pattern.

## Features

- **User Model**: Complete user authentication with password hashing and validation
- **Database Integration**: SQLAlchemy with MySQL support
- **Migrations**: Flask-Migrate for database versioning
- **CORS Support**: Cross-origin resource sharing enabled
- **Application Factory**: Proper Flask application factory pattern
- **CLI Ready**: Ready for Flask CLI commands

## User Model Features

- **Password Complexity**: 8+ characters, uppercase, lowercase, digit, special character
- **Username Validation**: 3-80 characters, alphanumeric with underscores and hyphens
- **Email Validation**: Proper email format validation
- **Uniqueness**: Username and email uniqueness enforced
- **Security**: Password hashing with Werkzeug

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Database Configuration

The application is configured to use MySQL. Update the database URL in `config.py` if needed:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:Kumar@249@localhost/prok_db')
```

### 3. Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://root:Kumar@249@localhost/prok_db
JWT_SECRET_KEY=your-jwt-secret-key
```

### 4. Initialize Database

```bash
# Set Flask app
export FLASK_APP=app.py

# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Add User model"

# Apply migration
flask db upgrade
```

### 5. Run the Application

```bash
# Development mode
flask run

# Or with debug
flask run --debug
```

## File Structure

```
app/backend/
├── app.py              # Main Flask application factory
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions (db, migrate)
├── models/
│   ├── __init__.py     # Models package
│   └── user.py         # User model with validation
├── requirements.txt    # Python dependencies
└── test_setup.py      # Setup verification script
```

## User Model Usage

```python
from models.user import User

# Create a new user
user = User("john_doe", "john@example.com", "SecurePass123!")

# Save to database
user.save()

# Find user by username
user = User.find_by_username("john_doe")

# Check password
if user.check_password("SecurePass123!"):
    print("Password is correct!")

# Convert to dictionary
user_dict = user.to_dict()
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*(),.?":{}|<>)

## Testing

Run the test script to verify everything is working:

```bash
python test_setup.py
```

## CLI Commands

The application supports standard Flask CLI commands:

- `flask run` - Run the development server
- `flask db init` - Initialize database migrations
- `flask db migrate -m "message"` - Create a new migration
- `flask db upgrade` - Apply pending migrations
- `flask db downgrade` - Revert last migration

## Troubleshooting

### Import Errors
If you see import errors, make sure:
1. Virtual environment is activated
2. All dependencies are installed: `pip install -r requirements.txt`
3. You're in the correct directory (`app/backend`)

### Database Connection Issues
1. Check MySQL is running
2. Verify database credentials in `config.py`
3. Ensure database `prok_db` exists

### Migration Issues
1. Delete `migrations/` folder if corrupted
2. Run `flask db init` again
3. Check database connection before running migrations 