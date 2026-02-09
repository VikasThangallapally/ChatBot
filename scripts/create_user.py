import sys
sys.path.insert(0, 'c:/Users/vikas/Downloads/neuroAssist-main/neuroAssist-main')
from app.db import SessionLocal
from app.models.user import User
from app.core.auth import get_password_hash

try:
    db = SessionLocal()
    user = User(name='Script Test', email='script2@example.com', password_hash=get_password_hash('testpass'))
    db.add(user)
    db.commit()
    db.refresh(user)
    print('created', user.id)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        db.close()
    except:
        pass
