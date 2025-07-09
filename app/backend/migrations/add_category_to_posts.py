"""
Migration to add category field to posts table
"""
from extensions import db

def upgrade():
    """Add category column to posts table"""
    try:
        # Add category column with default value
        db.engine.execute("""
            ALTER TABLE posts 
            ADD COLUMN category VARCHAR(50) DEFAULT 'general'
        """)
        
        # Create index on category column for better performance
        db.engine.execute("""
            CREATE INDEX idx_posts_category ON posts(category)
        """)
        
        print("Successfully added category column to posts table")
        
    except Exception as e:
        print(f"Error adding category column: {e}")
        raise

def downgrade():
    """Remove category column from posts table"""
    try:
        # Drop the index first
        db.engine.execute("DROP INDEX IF EXISTS idx_posts_category")
        
        # Remove the column
        db.engine.execute("ALTER TABLE posts DROP COLUMN IF EXISTS category")
        
        print("Successfully removed category column from posts table")
        
    except Exception as e:
        print(f"Error removing category column: {e}")
        raise

if __name__ == "__main__":
    upgrade() 