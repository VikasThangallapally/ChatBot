"""
Diagnostic script to test Supabase connection and API key validity.
"""
import sys
sys.path.insert(0, '.')

from app.config import settings
import requests

print("=" * 70)
print("🔍 SUPABASE API KEY DIAGNOSTIC")
print("=" * 70)

print(f"\n✓ Project URL: {settings.SUPABASE_URL}")
print(f"✓ API Key: {settings.SUPABASE_KEY[:20]}...{settings.SUPABASE_KEY[-20:]}")

# Check key type
key = settings.SUPABASE_KEY
if key.startswith("sbprivate_"):
    print("\n✅ KEY TYPE: Service Role Secret (FULL ACCESS - Backend use)")
elif key.startswith("sb_anon_"):
    print("\n⚠️  KEY TYPE: Anon/Public Key (LIMITED ACCESS - Frontend only)")
elif key.startswith("sb_publishable_"):
    print("\n❌ KEY TYPE: Publishable Key (FRONTEND ONLY - No backend write access)")
else:
    print(f"\n❓ KEY TYPE: Unknown ({key[:20]}...)")

# Test connection
print("\n" + "=" * 70)
print("🧪 Testing Connection...")
print("=" * 70)

try:
    # Try to connect to Supabase
    resp = requests.get(
        f"{settings.SUPABASE_URL}/rest/v1/",
        headers={
            "apikey": settings.SUPABASE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_KEY}"
        },
        timeout=5
    )
    print(f"\n✓ Connection Response: {resp.status_code}")
    if resp.status_code == 401:
        print("❌ FAILED: Invalid API key or insufficient permissions")
    elif resp.status_code == 200 or resp.status_code == 404:
        print("✅ SUCCESS: Supabase is reachable and key is valid")
    else:
        print(f"Status: {resp.status_code}")
except Exception as e:
    print(f"\n❌ Connection Error: {e}")

print("\n" + "=" * 70)
print("📋 SOLUTION")
print("=" * 70)

if key.startswith("sb_publishable_"):
    print("""
The publishable key you're using is restricted to frontend read-only access.

FOR PRODUCTION/BACKEND: You need the Service Role Secret Key

Steps to get it:
1. Go to https://app.supabase.com
2. Select your project
3. Settings → API
4. Copy "service_role secret" key (starts with sbprivate_)
5. Update SUPABASE_KEY environment variable

FOR TESTING: You can switch back to SQLite temporarily:
- Revert requirements.txt to include sqlalchemy==2.0.20
- Revert db.py, models/user.py, auth.py to SQLite versions
- Delete supabase imports

""")
elif key.startswith("sbprivate_"):
    print("""
✅ You have a valid Service Role Secret Key!
The backend should work now.

If you're still getting errors:
1. Check that you created the 'users' table in Supabase
2. Run: python setup_db.py

""")
else:
    print("""
⚠️  Key type unknown. Please verify you copied the correct key from Supabase.
    """)

print("=" * 70)
