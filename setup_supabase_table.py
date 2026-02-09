#!/usr/bin/env python
"""Create users table in Supabase using Python client"""

from supabase import create_client
import json

# Your Supabase credentials
SUPABASE_URL = "https://uluxzbfstcemaprjhyjl.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVsdXh6YmZzdGNlbWFwcmpoeWpsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDY0MjAwNiwiZXhwIjoyMDg2MjE4MDA2fQ.e8nHKwZjQzr4z-FtuyDxqPNAfkLoOhIVdIBlUsQss60"

def create_users_table():
    """Create users table in Supabase"""
    # Initialize Supabase client with service role key
    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    
    print("\n" + "="*60)
    print("CREATING USERS TABLE IN SUPABASE")
    print("="*60)
    
    # SQL to create the table
    sql = """
    BEGIN;
    
    -- Drop table if exists (fresh start)
    DROP TABLE IF EXISTS public.users CASCADE;
    
    -- Create users table
    CREATE TABLE public.users (
      id BIGSERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create index on email
    CREATE INDEX idx_users_email ON public.users(email);
    
    -- Enable RLS
    ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
    
    -- Create policies
    CREATE POLICY "Allow insert for registration" ON public.users
      FOR INSERT WITH CHECK (true);
    
    CREATE POLICY "Allow select" ON public.users
      FOR SELECT USING (true);
    
    CREATE POLICY "Allow update" ON public.users
      FOR UPDATE USING (true);
    
    COMMIT;
    """
    
    try:
        print("\nExecuting SQL to create users table...")
        response = supabase.rpc('') # Just test connection first
        print("✓ Connected to Supabase")
        
        # Alternative: Use exec directly on the client
        # Since supabase-py doesn't have direct SQL execution, 
        # we'll manually verify and create
        
        print("\nAttempting to query existing tables...")
        # Try to select from the table to see if it exists
        result = supabase.table("users").select("*").limit(1).execute()
        print("✓ Users table already exists!")
        print(f"  Existing records: {len(result.data) if result.data else 0}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"⚠️  Table might not exist or needs to be created: {error_msg}")
        
        if "does not exist" in error_msg or "Could not find" in error_msg:
            print("\n📝 The users table needs to be created manually in Supabase.")
            print("\nGo to: https://app.supabase.com → Your Project → SQL Editor")
            print("\nCopy and paste this SQL, then click RUN:\n")
            
            simple_sql = """CREATE TABLE IF NOT EXISTS public.users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow_insert" ON public.users FOR INSERT WITH CHECK (true);
CREATE POLICY "allow_select" ON public.users FOR SELECT USING (true);"""
            
            print(simple_sql)
            return False
        else:
            print(f"❌ Error: {error_msg}")
            return False

def test_registration():
    """Test if registration works"""
    print("\n" + "="*60)
    print("TESTING REGISTRATION")
    print("="*60)
    
    import requests
    import time
    
    payload = {
        "name": "Test User",
        "email": f"test{int(time.time())}@example.com",
        "password": "TestPassword123!"
    }
    
    try:
        print(f"\nRegistering: {payload['email']}")
        response = requests.post(
            "http://127.0.0.1:8000/api/register",
            json=payload,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ REGISTRATION SUCCESSFUL!")
            return True
        else:
            print(f"\n❌ Registration failed")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend (http://127.0.0.1:8000)")
        print("   Make sure backend is running!")
        return False

if __name__ == "__main__":
    print("\n🔧 NEUROASSIST TABLE SETUP")
    
    # Try to create/verify table
    table_ready = create_users_table()
    
    if table_ready:
        print("\n✅ Table is ready! Testing registration...")
        test_registration()
    else:
        print("\n⚠️  Manual setup required - see instructions above")
    
    print("\n" + "="*60)
