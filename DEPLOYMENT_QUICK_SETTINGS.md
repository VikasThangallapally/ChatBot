# Quick Deploy Settings - Netlify + Render

## Render Backend Configuration

**Service Name**: `brain-tumor-api`

### Build & Deployment
```
Build Command:   pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt
Start Command:   uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables (Set in Render Dashboard)
```
MONGO_URI                  = mongodb+srv://username:password@cluster.mongodb.net/?appName=neuro_assist
MONGO_DB_NAME              = neuro_assist
BACKEND_URL                = https://brain-tumor-api.onrender.com  (update after first deploy)
CORS_ORIGINS               = http://localhost:3000,http://localhost:5174,https://your-site.netlify.app
SECRET_KEY                 = [generate: python -c "import secrets; print(secrets.token_urlsafe(32))"]
JWT_ALGORITHM              = HS256
ACCESS_TOKEN_EXPIRE_MINUTES= 60
MODEL_NAME                 = brain_tumor_model.h5
IMAGE_SIZE                 = 224
MAX_UPLOAD_SIZE            = 10485760
CONFIDENCE_THRESHOLD       = 0.5
LOG_LEVEL                  = INFO
SENDGRID_API_KEY           = [optional - your SendGrid key]
SENDGRID_FROM_EMAIL        = [optional - noreply@yourapp.com]
OPENAI_API_KEY             = [optional - your OpenAI key]
```

---

## Netlify Frontend Configuration

**Site Name**: `your-brain-tumor-app` (customize)

### Build Settings
```
Build Command:     cd frontend && npm run build
Publish Directory: frontend/dist
```

### Environment Variables (Set in Netlify Dashboard)
```
VITE_API_URL = https://brain-tumor-api.onrender.com
NODE_VERSION = 18
```

### Redirects (Already in netlify.toml)
```
/* → /index.html  [200]  (for React Router SPA)
```

---

## MongoDB Atlas Configuration

### Connection String Format
```
mongodb+srv://username:password@cluster-name.mongodb.net/?appName=neuro_assist
```

### Required Settings
- **Cluster**: M0 Sandbox (free) or higher
- **Authentication**: Create database user with strong password
- **Network Access**: 
  - Dev: Add your IP
  - Production: 0.0.0.0/0 (allow all, or limit to Render IP)
- **Database Name**: `neuro_assist`

---

## Key Code Changes Made

### 1. Backend Config (`app/config.py`)
✅ Added `BACKEND_URL` - for absolute image URLs
✅ Added `CORS_ORIGINS` - comma-separated list from env

### 2. Backend Main (`app/main.py`)
✅ Dynamic CORS configuration from `settings.CORS_ORIGINS`
✅ $PORT environment variable support
✅ Separate /static mount for uploaded files

### 3. Backend Routes (`app/api/routes/predict.py`)
✅ `get_absolute_image_url()` function - converts local paths to full URLs
✅ All `image_path` responses now contain absolute URLs (e.g., `https://brain-tumor-api.onrender.com/static/uploads/file.jpg`)

### 4. Frontend API Config (`frontend/src/config/api.js`)
✅ Reads `VITE_API_URL` environment variable
✅ Supports dev (localhost:8000) and prod (Render backend) separately

### 5. Frontend Vite Config (`frontend/vite.config.js`)
✅ Removed proxy (no longer needed with separate domains)
✅ Uses `VITE_API_URL` environment variable

### 6. Frontend Netlify Config (`frontend/netlify.toml`)
✅ Updated for separate Netlify frontend + Render backend
✅ SPA redirects for React Router
✅ Security & caching headers

---

## Deployment Order

1. **MongoDB Atlas** - Set up database & get connection string
2. **Render Backend** - Deploy FastAPI service with env vars
3. **Netlify Frontend** - Deploy React frontend with API URL pointing to Render

---

## Testing After Deploy

### Backend
```bash
curl https://brain-tumor-api.onrender.com/health
# Response: {"status": "healthy", "service": "Brain Tumor Chatbot", "version": "1.0.0"}
```

### Frontend
- Visit: https://your-site.netlify.app
- Check Network tab for API calls → should show `https://brain-tumor-api.onrender.com/api/...`
- Check Console for errors (CORS, 404, etc.)

### Image URLs
- After uploading image, `image_path` should be: `https://brain-tumor-api.onrender.com/static/uploads/filename.jpg`
- NOT a relative path or localhost URL

---

## Troubleshooting Links

| Issue | Solution |
|-------|----------|
| CORS Error | Check `CORS_ORIGINS` in Render, includes your Netlify domain |
| 404 on API | Check `VITE_API_URL` in Netlify = Render backend URL |
| Image loads as 404 | Check `BACKEND_URL` in Render, `/static` mount exists |
| Build fails on Render | Check Python version, requirements.txt intact |
| Build fails on Netlify | Check Node version, frontend/package.json intact |
| Slow static files | Upgrade Render plan, enable Netlify caching |

---

## Important Notes

⚠️ **One-time Steps**:
- After Render deploys first time, copy the backend URL
- Add it to Render's `BACKEND_URL` env var
- Add it to Netlify's `VITE_API_URL` env var
- Trigger new deployments

📍 **Static Files Flow**:
1. User uploads image → saved to `app/static/uploads/filename.jpg`
2. Backend returns absolute URL: `https://brain-tumor-api.onrender.com/static/uploads/filename.jpg`
3. Frontend displays image from that full URL
4. Works across separate Netlify + Render domains

✅ **All Code Changes Included** - No additional configuration needed beyond env vars!
