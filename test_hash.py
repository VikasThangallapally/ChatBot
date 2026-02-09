import sys
sys.path.insert(0, 'c:/Users/vikas/Downloads/neuroAssist-main/neuroAssist-main')

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    password = "admin123"
    print(f"Password: {password} (len={len(password)})")
    
    hash_result = pwd_context.hash(password)
    print(f"Hash succeeded: {hash_result}")
    print(f"Hash length: {len(hash_result)}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
