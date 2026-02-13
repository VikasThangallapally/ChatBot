# API Keys & Environment Variables Reference

Complete guide to obtaining and configuring all required API keys for NeuroAssist deployment.

---

## 📋 Quick Checklist

- [ ] MongoDB Atlas connection string
- [ ] JWT Secret Key
- [ ] SendGrid API Key (optional, for emails)
- [ ] Frontend and Backend URLs
- [ ] CORS Origins configured

---

## 🗄️ 1. MongoDB Atlas (Database)

### Why You Need It
Stores user accounts, MRI predictions, and chat history.

### Free Tier Details
- ✅ 5 GB storage
- ✅ 3 shared nodes
- ✅ 512 MB RAM per node
- Perfect for development/testing

### Step-by-Step Setup

#### 1. Create Account
- Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Click **"Sign Up"**
- Use your email to create account
- Verify email address

#### 2. Create Organization & Project
- Create new organization (name: "NeuroAssist")
- Create new project (name: "MRI-Detection")

#### 3. Create Database Cluster
- Click **"Create Deployment"**
- Choose **"Free"** tier
- Select **"Shared"**
- Choose **Region**: US East (us-east-1) or closest to you
- Click **"Create Deployment"**
- Wait 5-10 minutes for cluster to deploy

#### 4. Create Database User
- Go to **"Database Access"** (left menu)
- Click **"Add New Database User"**
- Username: `vikasthangallapally8380_db_user`
- Password: Generate secure password
- Permission: **"Read and write to any database"**
- Click **"Add User"**

#### 5. Create Database
- Go to **"Databases"** (left menu)
- Click **"Browse Collections"**
- Click **"Create Database"**
- Database name: `neuro_assist`
- Collection name: `users`
- Click **"Create"**

#### 6. Get Connection String
- Go to **"Database"** (left menu)
- Click **"Connect"** on your cluster
- Choose **"Drivers"**
- Language: **Python**
- Copy connection string
- Format: `mongodb+srv://username:password@cluster.mongodb.net/?appName=dbname`

**Your Connection String:**
```
mongodb+srv://vikasthangallapally8380_db_user:PASSWORD@vikas1.rapgqvu.mongodb.net/?appName=vikas1
```

Replace `PASSWORD` with your actual password.

#### 7. Network Access
- Go to **"Network Access"** (left menu)
- Click **"Add IP Address"**
- Choose **"Allow access from anywhere"** (for Render deployment)
- Click **"Confirm"**

---

## 🔐 2. JWT Secret Key

### What It Is
A secure random string used to sign JWT authentication tokens.

### Generate Your Own
Run in Python:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Output example: `ae9d1e30-5bf2-423a-954c-13c8c759452a`

### Recommended Value
You can use: `ae9d1e30-5bf2-423a-954c-13c8c759452a`

### Security Notes
- Keep it secret
- Don't commit to GitHub
- Use different keys for development and production
- Rotate periodically for security

---

## 📧 3. SendGrid API Key (Optional)

### Why You Need It
Sends password reset OTP emails to users.

### Free Tier Details
- ✅ 100 emails/day free
- Sufficient for testing

### Step-by-Step Setup

#### 1. Create Account
- Go to [sendgrid.com](https://sendgrid.com)
- Click **"Sign Up"**
- Create free account
- Verify email

#### 2. Create API Key
- Go to **Settings → API Keys** (left menu)
- Click **"Create API Key"**
- Name: "NeuroAssist"
- Permission Level: **"Restricted"**
- Select **"Mail Send"** permission
- Click **"Create & Close"**

#### 3. Copy API Key
- Copy the displayed API key
- Format: `SG.xxxxxxxxxxxxx`

**Example:**
```
SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 4. Configure Sender Email
- Go to **Settings → Sender Authentication**
- Click **"Create New Sender"**
- Enter email: `noreply@yourdomain.com` (or verify existing email)
- Click **"Create"**

---

## 🌐 4. Frontend & Backend URLs (For Production)

After deploying to Render, you'll have:

### Backend URL
```
https://neuroassist-backend.onrender.com
```

### Frontend URL
```
https://neuroassist-frontend.onrender.com
```

### Update CORS Origins
In backend environment variables, set:
```
CORS_ORIGINS=https://neuroassist-frontend.onrender.com,http://localhost:5174
```

### Update Frontend API URL
In frontend environment variables, set:
```
VITE_API_URL=https://neuroassist-backend.onrender.com
```

---

## 📊 Environment Variables by Service

### Backend (FastAPI)

```env
# Database
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=dbname
MONGO_DB_NAME=neuro_assist

# Authentication
SECRET_KEY=ae9d1e30-5bf2-423a-954c-13c8c759452a
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# URLs
BACKEND_URL=https://neuroassist-backend.onrender.com
CORS_ORIGINS=https://neuroassist-frontend.onrender.com,http://localhost:5174

# Email (Optional)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# Model Settings
IMAGE_SIZE=224
CONFIDENCE_THRESHOLD=0.5
MAX_UPLOAD_SIZE=10485760

# Logging
LOG_LEVEL=INFO
```

### Frontend (React/Vite)

```env
VITE_API_URL=https://neuroassist-backend.onrender.com
VITE_APP_TITLE=NeuroAssist - Brain Tumor Detection
```

---

## 🔄 Integration Points

### MongoDB ↔ Backend
```python
# config.py
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
```

### JWT ↔ Auth
```python
# core/auth.py
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
```

### SendGrid ↔ Email Service
```python
# services/email_service.py
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")
```

### CORS ↔ Frontend Connection
```python
# main.py
CORS_ORIGINS = settings.CORS_ORIGINS
```

---

## 🧪 Testing API Keys

### Test MongoDB Connection
```bash
# In Python environment
python -c "
from pymongo import MongoClient
uri = 'YOUR_MONGODB_URI'
client = MongoClient(uri)
print('✅ MongoDB connected!' if client.admin.command('ping') else '❌ Failed')
"
```

### Test JWT Key
```python
# In Python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "ae9d1e30-5bf2-423a-954c-13c8c759452a"
token = jwt.encode(
    {"sub": "test@example.com", "exp": datetime.utcnow() + timedelta(hours=1)},
    SECRET_KEY,
    algorithm="HS256"
)
print(f"✅ Token generated: {token}")
```

### Test SendGrid Key
```bash
curl --request POST \
  --url https://api.sendgrid.com/v3/mail/send \
  --header 'Authorization: Bearer YOUR_SENDGRID_KEY' \
  --header 'Content-Type: application/json' \
  --data '{}'
```

---

## 🔒 Security Checklist

- [ ] Never commit `.env` files to GitHub
- [ ] Use Render's environment variable dashboard (not hardcoded)
- [ ] Rotate API keys every 3-6 months
- [ ] Use different keys for dev/staging/production
- [ ] Monitor API usage for suspicious activity
- [ ] Enable IP whitelisting where possible
- [ ] Use HTTPS only (Render provides automatic SSL)
- [ ] Restrict MongoDB Atlas network access

---

## 📋 Deployment Checklist

| API Key | Obtained | Added to Render | Status |
|---------|----------|-----------------|--------|
| MongoDB URI | ☐ | ☐ | ? |
| JWT Secret | ☐ | ☐ | ? |
| SendGrid API | ☐ | ☐ | ? |
| Backend URL | ☐ | ☐ | ? |
| Frontend URL | ☐ | ☐ | ? |

---

## 🆘 Troubleshooting

### MongoDB Connection Fails
- [ ] Verify connection string is correct
- [ ] Check username and password
- [ ] Ensure network access is allowed (Add IP 0.0.0.0/0)
- [ ] Check database exists
- [ ] Verify user permissions

### Emails Not Sending
- [ ] Check SendGrid API key is correct
- [ ] Verify sender email is authenticated
- [ ] Check SendGrid account is active
- [ ] Monitor SendGrid dashboard for errors

### JWT Token Errors
- [ ] Ensure SECRET_KEY matches between services
- [ ] Check token expiry time
- [ ] Verify algorithm is "HS256"

### CORS Errors
- [ ] Update CORS_ORIGINS to include new frontend URL
- [ ] Restart backend after changing CORS
- [ ] Check frontend is accessing correct API URL

---

## 📚 Additional Resources

- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
- [SendGrid API Docs](https://docs.sendgrid.com/api-reference/)
- [JWT.io](https://jwt.io/)
- [Render Docs](https://render.com/docs)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## 🔗 Quick Links

- **MongoDB Atlas**: https://cloud.mongodb.com
- **SendGrid**: https://app.sendgrid.com
- **Render Dashboard**: https://dashboard.render.com
- **GitHub Repo**: https://github.com/VikasThangallapally/MRI-Application.git

---

**Last Updated**: February 13, 2026

**Questions or Issues?** Check the main DEPLOYMENT_GUIDE.md or BACKEND_DEPLOYMENT.md
