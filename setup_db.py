"""
Setup script to create initial Supabase tables.
Run this once to initialize your database schema.
"""

import sys
sys.path.insert(0, '.')

from app.db import supabase
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_users_table():
    """Create users table in Supabase via direct SQL."""
    try:
        # Try to get the schema by querying the table
        response = supabase.table("users").select("count", count="exact").execute()
        logger.info("✅ Users table already exists!")
        return True
    except Exception as e:
        logger.warning(f"Users table does not exist or error checking: {e}")
        logger.info("⚠️  You need to create the users table manually in Supabase.")
        logger.info("""
        
        SQL to run in Supabase (SQL Editor):
        
        CREATE TABLE users (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX idx_users_email ON users(email);
        
        """)
        return False

if __name__ == "__main__":
    logger.info("🔧 Initializing Supabase tables...")
    if create_users_table():
        logger.info("✅ Database setup complete!")
    else:
        logger.info("⚠️  Please run the SQL above in your Supabase dashboard SQL Editor.")
