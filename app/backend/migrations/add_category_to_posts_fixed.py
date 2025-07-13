"""
Migration to add category field to posts table (Fixed version)
"""
from extensions import db
from sqlalchemy import text

def upgrade():
    """Add category column to posts table"""
    try:
        # Check if column already exists
        result = db.session.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name = 'posts' 
            AND column_name = 'category'
        """))
        
        if result.scalar() == 0:
            # Add category column with default value
            db.session.execute(text("""
                ALTER TABLE posts 
                ADD COLUMN category VARCHAR(50) DEFAULT 'general'
            """))
            
            # Create index on category column for better performance
            db.session.execute(text("""
                CREATE INDEX idx_posts_category ON posts(category)
            """))
            
            db.session.commit()
            print("✅ Successfully added category column to posts table")
        else:
            print("⏭️  Category column already exists, skipping...")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error adding category column: {e}")
        raise

def downgrade():
    """Remove category column from posts table"""
    try:
        # Drop the index first
        db.session.execute(text("DROP INDEX IF EXISTS idx_posts_category"))
        
        # Remove the column
        db.session.execute(text("ALTER TABLE posts DROP COLUMN IF EXISTS category"))
        
        db.session.commit()
        print("✅ Successfully removed category column from posts table")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error removing category column: {e}")
        raise

if __name__ == "__main__":
    from app import get_app
    app = get_app()
    with app.app_context():
        upgrade()
