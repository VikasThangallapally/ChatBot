"""
MongoDB database client and initialization.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

_mongo_client = None
_mongo_db = None


def get_mongo_client():
    """Get or create MongoDB client."""
    global _mongo_client
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            _mongo_client.admin.command('ping')
            logger.info("✅ MongoDB client connected successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected MongoDB error: {e}")
            raise
    return _mongo_client


def get_mongo_db():
    """Get MongoDB database instance."""
    global _mongo_db
    if _mongo_db is None:
        client = get_mongo_client()
        _mongo_db = client[settings.MONGO_DB_NAME]
        logger.info(f"✅ Using MongoDB database: {settings.MONGO_DB_NAME}")
    return _mongo_db


def close_mongo_connection():
    """Close MongoDB connection."""
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None
        logger.info("MongoDB connection closed")


# Convenience function to get users collection
def get_users_collection():
    """Get users collection."""
    db = get_mongo_db()
    return db["users"]


def get_password_reset_otps_collection():
    """Get password reset OTPs collection."""
    db = get_mongo_db()
    return db["password_reset_otps"]


# Initialize collections with indexes on startup
def init_collections():
    """Initialize MongoDB collections with required indexes."""
    try:
        users = get_users_collection()
        # Create unique index on email
        users.create_index("email", unique=True)
        logger.info("✅ Users collection initialized with indexes")
        
        otps = get_password_reset_otps_collection()
        # Create index for automatic expiration of OTPs
        otps.create_index("expires_at", expireAfterSeconds=0)
        logger.info("✅ Password reset OTPs collection initialized with TTL index")
    except Exception as e:
        logger.error(f"❌ Error initializing collections: {e}")
        raise
