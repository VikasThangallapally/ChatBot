from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

_supabase_client: Client = None


def get_supabase_client() -> Client:
    """Get or create Supabase client (lazy initialization)."""
    global _supabase_client
    if _supabase_client is None:
        try:
            # Create client without any extra parameters
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logger.info("✅ Supabase client initialized successfully")
        except TypeError as e:
            # Handle proxy parameter error from newer supabase versions
            if "proxy" in str(e):
                logger.error(f"❌ Supabase proxy parameter error: {e}")
                logger.error("⚠️  Try updating supabase package: pip install --upgrade supabase")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase client: {e}")
            logger.error("⚠️  Backend will run but database operations may fail.")
            raise
    return _supabase_client


class SupabaseProxy:
    """Proxy to get supabase client on demand."""
    def __getattr__(self, name):
        return getattr(get_supabase_client(), name)


# Create singleton instance for global use
supabase = SupabaseProxy()
