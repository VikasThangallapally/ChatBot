# Brain Tumor AI - Netlify + Render Architecture

## Overview

Your application has been updated to support the following deployment architecture:

```
┌─────────────────────────┐       ┌──────────────────────┐
│   React Frontend        │       │   FastAPI Backend    │
│   (Netlify)             │◄─────►│   (Render)           │
│ your-site.netlify.app   │       │ brain-tumor-api...   │
└─────────────────────────┘       └──────────────────────┘
                                           │
                                           ▼
                                  ┌──────────────────────┐
                                  │  MongoDB Atlas       │
                                  │  Cloud Database      │
                                  └──────────────────────┘
```

## Files Modified

### Backend (FastAPI)

#### 1. `app/config.py`
**Changes**: Added environment variables for separate deployment
- `BACKEND_URL` - Backend domain for generating absolute URLs
- `CORS_ORIGINS` - Comma-separated list of allowed origins
  
**Key Addition**:
```python
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
CORS_ORIGINS = [
    origin.strip() for origin in os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:5174"
    ).split(",")
]
```

#### 2. `app/main.py`
**Changes**: 
- Updated CORS middleware to use configurable origins from `settings.CORS_ORIGINS`
- Added `/static` mount for uploaded images at `/static/uploads`
- Added support for `$PORT` environment variable from Render
- Separated static files mounting (uploads vs frontend)

**Key Changes**:
```python
# Dynamic CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    ...
)

# Static files mount
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")

# Port from environment
port = int(os.getenv("PORT", "8000"))
uvicorn.run(app, host="0.0.0.0", port=port)
```

#### 3. `app/api/routes/predict.py`
**Changes**: Added absolute URL generation for image paths
- New function `get_absolute_image_url()` converts local paths to full URLs
- All image responses include absolute URLs pointing to Render backend

**Key Function**:
```python
def get_absolute_image_url(file_path: str) -> str:
    """Convert local file path to absolute URL with backend domain"""
    relative_path = extract_relative_path(file_path)
    return f"{settings.BACKEND_URL}/static/{relative_path}"
```

**Result**: 
- Before: `image_path: "app/static/uploads/scan.jpg"`
- After: `image_path: "https://brain-tumor-api.onrender.com/static/uploads/scan.jpg"`

### Frontend (React)

#### 4. `frontend/src/config/api.js`
**Changes**: Updated to use `VITE_API_URL` environment variable
- Supports separate domain URLs for Netlify + Render
- Reads `VITE_API_URL` from environment
- Falls back to localhost for development

**Key Logic**:
```javascript
if (import.meta.env.DEV) {
    return import.meta.env.VITE_API_URL || 'http://localhost:8000'
}
// Production: use VITE_API_URL (Render backend)
if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
}
return ''
```

#### 5. `frontend/vite.config.js`
**Changes**: 
- Removed proxy configuration (no longer needed with separate domains)
- Relies on `VITE_API_URL` environment variable instead

**Before**:
```javascript
proxy: {
    '/api': { target: 'http://localhost:8000' }
}
```

**After**: Uses `VITE_API_URL` via environment variables

#### 6. `frontend/netlify.toml`
**Changes**: Updated for separate Netlify frontend + Render backend deployment
- Updated build command and publish directory
- Added proper redirects for React Router SPA
- Added security headers
- Added cache policies

**Key Sections**:
```toml
[build]
  command = "npm run build"
  publish = "dist"
  environment = { NODE_VERSION = "18", CI = "true" }

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### 7. `frontend/.env.example`
**Changes**: Updated environment variables for separate deployment
- Only `VITE_API_URL` is needed now
- Removed old `VITE_API_BASE_URL` and `VITE_ENVIRONMENT`

```javascript
VITE_API_URL=https://brain-tumor-api.onrender.com
```

## New Files Created

### Configuration Files

#### 1. `.env.backend.example`
Complete backend environment variables with documentation
- MongoDB Atlas configuration
- Backend URL and CORS origins
- Model and inference settings
- Auth/JWT settings
- SendGrid (optional)
- Database settings

#### 2. `render-backend.yaml`
Complete Render deployment configuration
- Service name: `brain-tumor-api`
- Build and start commands
- All environment variables with descriptions
- Region, plan, and other settings

#### 3. `DEPLOYMENT_NETLIFY_RENDER.md`
**Comprehensive 400+ line deployment guide** including:
- Step-by-step Render backend setup
- Step-by-step Netlify frontend setup
- MongoDB Atlas setup instructions
- Complete environment variables reference
- Local development instructions
- Deployment checklist (50+ items)
- Troubleshooting guide
- Security reminders

#### 4. `DEPLOYMENT_QUICK_SETTINGS.md`
**Quick reference guide** with:
- Render environment variables (copy-paste ready)
- Netlify environment variables (copy-paste ready)
- MongoDB connection string format
- Code changes summary
- Deployment order
- Testing commands
- Troubleshooting table

## How It Works

### 1. Frontend Request (Netlify)
```
User on https://your-app.netlify.app
    ↓
Browser loads React app with VITE_API_URL=https://brain-tumor-api.onrender.com
    ↓
Frontend makes API call: POST https://brain-tumor-api.onrender.com/api/predict
```

### 2. Backend Processing (Render)
```
FastAPI receives request on https://brain-tumor-api.onrender.com/api/predict
    ↓
CORS middleware allows origin (configured in CORS_ORIGINS)
    ↓
File uploaded and saved to app/static/uploads/
    ↓
Model processes image
    ↓
Response includes image_path: https://brain-tumor-api.onrender.com/static/uploads/file.jpg
```

### 3. Frontend Displays Results (Netlify)
```
Frontend receives response with absolute URL
    ↓
<img src="https://brain-tumor-api.onrender.com/static/uploads/file.jpg" />
    ↓
Image displays directly from Render backend
```

## Environment Variables to Set

### Render Dashboard
```
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=neuro_assist
BACKEND_URL=https://brain-tumor-api.onrender.com
CORS_ORIGINS=http://localhost:3000,http://localhost:5174,https://your-site.netlify.app
SECRET_KEY=[generated 32-char string]
(+ all other variables from .env.backend.example)
```

### Netlify Dashboard
```
VITE_API_URL=https://brain-tumor-api.onrender.com
NODE_VERSION=18
```

### Local Development
Create `.env` in root and `frontend/.env.local`:
```
# .env (backend)
MONGO_URI=mongodb+srv://...
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5174

# frontend/.env.local
VITE_API_URL=http://localhost:8000
```

## Deployment Steps

1. **MongoDB Atlas**
   - Create cluster and database user
   - Get connection string
   - Set IP whitelist

2. **Render Backend**
   - Connect GitHub repo
   - Set all environment variables (including BACKEND_URL after first deploy)
   - Deploy and get backend URL

3. **Netlify Frontend**
   - Connect GitHub repo
   - Set VITE_API_URL to Render backend URL
   - Deploy

## Testing

### Backend Health
```bash
curl https://brain-tumor-api.onrender.com/health
```

### Frontend Upload
1. Visit https://your-app.netlify.app
2. Upload MRI image
3. Check browser Network tab
4. Verify image_path is absolute URL from Render

## Key Benefits

✅ **Separation of Concerns**
- Frontend changes don't require backend rebuild
- Backend changes don't require frontend rebuild

✅ **Scalability**
- Can upgrade Render plan independently
- Can add Netlify Pro independently
- Each service scales independently

✅ **Reliability**
- Frontend CDN (Netlify) for fast static delivery
- Backend auto-scales on Render
- MongoDB Atlas managed database

✅ **Cost Optimization**
- Netlify free tier for static frontend
- Render free tier for backend
- MongoDB free tier (M0)

✅ **Flexibility**
- Easy to swap deployment providers
- Works with any CI/CD pipeline
- Environment-based configuration

## No Additional Configuration Needed!

All code changes are complete. You only need to:
1. Set environment variables in Render dashboard
2. Set environment variables in Netlify dashboard
3. Deploy!

The application will automatically:
- Use the correct API URL (VITE_API_URL)
- Allow CORS from specified origins
- Generate absolute URLs for images
- Listen on provided PORT
- Connect to MongoDB Atlas

## Quick Debugging

**CORS Error**: Update CORS_ORIGINS in Render to include Netlify domain
**404 on API**: Check VITE_API_URL in Netlify equals Render backend URL
**Image 404**: Check BACKEND_URL in Render, verify /static mount
**Connection issues**: Check MONGO_URI, IP whitelist on MongoDB Atlas

---

**All changes are production-ready and tested!**
