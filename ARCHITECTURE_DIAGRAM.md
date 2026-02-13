# Architecture Diagram - Netlify + Render Deployment

## System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                     INTERNET / USERS                            │
└────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴──────────────┐
                │                            │
                ▼                            ▼
        ┌──────────────────┐        ┌──────────────────┐
        │  NETLIFY CDN     │        │  RENDER CLOUD    │
        │  (Frontend)      │        │  (Backend)       │
        │                  │        │                  │
        │  React App       │        │  FastAPI App     │
        │  VITE Build      │        │  Python 3.11     │
        │  HTML/CSS/JS     │        │                  │
        │                  │        │  Port: $PORT     │
        │  Domain:         │        │                  │
        │  app.netlify.app │◄──────►│  Domain:         │
        │                  │   API  │  api.onrender.com│
        │  VITE_API_URL    │ Calls  │                  │
        │  =               │        │  Routes:         │
        │  api.onrender.com│        │  /api/predict    │
        │                  │        │  /api/auth       │
        │  Assets:         │        │  /api/chat       │
        │  - JS chunks     │        │  /static/*       │
        │  - CSS           │        │                  │
        │  - Images        │        │  Uploads:        │
        │  - Fonts         │        │  /static/uploads/│
        │                  │        │                  │
        └──────────────────┘        └──────────────────┘
                │                              │
                │                              │
                │          ┌──────────────────┘
                │          │
                │          ▼
                │    ┌──────────────────┐
                │    │  MONGODB ATLAS   │
                │    │  Cloud Database  │
                │    │                  │
                │    │  Connection:     │
                │    │  MONGO_URI       │
                │    │  mongodb+srv://  │
                │    │                  │
                │    │  Collections:    │
                │    │  - users         │
                │    │  - predictions   │
                │    │  - chats         │
                │    │  - sessions      │
                │    └──────────────────┘
                │
                └──────────────────────────┘
                      Store & Retrieve Data
```

---

## Request Flow Diagram

### 1. User Opens Frontend

```
┌─────────────┐
│   Browser   │
│             │
│ User types  │
└──────┬──────┘
       │ https://app.netlify.app
       │
       ▼
┌──────────────────────────────┐
│  Netlify CDN                 │
│  - Serves React HTML/CSS/JS  │
│  - Injects VITE_API_URL env  │
│  - Returns index.html + app  │
└──────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Browser JavaScript          │
│  - Loads React components    │
│  - Reads VITE_API_URL        │
│  - = "https://api.onrender" │
└──────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  App Ready! User can interact│
└──────────────────────────────┘
```

### 2. User Uploads MRI Image

```
┌──────────────────────────────┐
│   Browser                    │
│   <input type="file" />      │
│   User selects image         │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  frontend/src/components/    │
│  UploadCard.jsx              │
│  - Reads file                │
│  - Uses API_BASE_URL config  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Make API Request            │
│  POST /api/predict           │
│  Host: api.onrender.com      │
│  With CORS headers           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Render Backend              │
│  app/main.py                 │
│  - Check CORS_ORIGINS        │
│  - Allow origin              │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  app/api/routes/predict.py   │
│  - Validate file             │
│  - Validate MRI              │
│  - Save to uploads/          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  app/services/inference.py   │
│  - Load model                │
│  - Run prediction            │
│  - Generate results          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Generate Absolute URL       │
│  get_absolute_image_url()    │
│  - Take: "uploads/img.jpg"   │
│  - Return: "https://api...   │
│    /static/uploads/img.jpg"  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Return JSON Response        │
│  {                           │
│    "image_path": "https://..." │
│    "predictions": [...],     │
│    "top_prediction": {...}   │
│  }                           │
└──────────┬───────────────────┘
           │
           │ CORS allows response
           │
           ▼
┌──────────────────────────────┐
│  Browser receives response   │
│  axios/fetch parses JSON     │
│  getPrediction event emitted │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Display Results             │
│  - Show predictions          │
│  - Display image from URL    │
│    <img src="https://api.../>
└──────────────────────────────┘
```

### 3. Static File Access (Images)

```
Frontend displays image:
<img src="https://api.onrender.com/static/uploads/scan.jpg" />
         │
         │
         ▼
    Browser makes GET request
         │
         ▼
Render backend receives:
GET /static/uploads/scan.jpg
         │
         ▼
app/main.py routes to StaticFiles handler
app.mount("/static", StaticFiles(...))
         │
         ▼
Returns file from UPLOAD_DIR
app/static/uploads/scan.jpg
         │
         ▼
Browser receives image file
<img> tag loads and displays
```

---

## Environment Variable Flow

```
┌─────────────────────────────────────────┐
│  When you push to GitHub                │
└────┬────────────────────────────────────┘
     │
     ├─────────────────────────────────────────┐
     │                                         │
     ▼                                         ▼
Netlify Detects Change                  Render Detects Change
     │                                         │
     │ Reads Netlify dashboard env vars        │ Reads Render dashboard env vars
     ▼                                         ▼
  Builds with:                            Builds with:
  - NODE_VERSION=18                       - Python 3.11
  - VITE_API_URL=https://api...          - pip install -r requirements.txt
                                          
  Runs build command:                     Runs start command:
  cd frontend && npm run build             uvicorn app.main:app --port $PORT

  Output: frontend/dist/                  OutputRegister app.config + app.main
  - index.html                            with CORS from env
  - JS bundles
  - CSS
     │                                         │
     ▼                                         ▼
Frontend gets VITE_API_URL              Backend gets CORS_ORIGINS
Hardcoded in build                      Hardcoded in app startup
     │                                         │
     ▼                                         ▼
Deployed on Netlify                     Deployed on Render
All requests go to:                     Handles requests from:
https://api.onrender.com                - https://app.netlify.app
                                        - http://localhost:3000
                                        - http://localhost:5174
```

---

## Configuration Files Relationship

```
┌─────────────────────────┐
│  GitHub Repository      │
└────┬────────────────────┘
     │
     ├──────────────────────┬────────────────────┐
     │                      │                    │
     ▼                      ▼                    ▼
┌─────────────┐      ┌────────────┐      ┌──────────────┐
│  render-    │      │  Netlify   │      │ Source Code  │
│  backend.   │      │  Config    │      │              │
│  yaml       │      │ netlify.   │      │ Backend:     │
│             │      │ toml       │      │ - main.py    │
│             │      │            │      │ - config.py  │
│ Defines:    │      │ Defines:   │      │ - predict.py │
│ - Service   │      │ - Build    │      │              │
│ - Commands  │      │   command  │      │ Frontend:    │
│ - Env vars  │      │ - Publish  │      │ - api.js     │
│   template  │      │   dir      │      │ - vite.js    │
│             │      │ - Redirects│      │              │
└──────┬──────┘      └────┬───────┘      └──────┬───────┘
       │                  │                     │
       │ (reference)      │ (deployed)          │ (pushed)
       │                  │                     │
       ▼                  ▼                     ▼
   Render           Netlify          GitHub Webhooks
   Dashboard        Dashboard              │
       │                │                  │
       │ Set env        │ Set env        Auto-redeploy
       │ manually       │ manually        when code
       │                │               changes
       ▼                ▼
   Render Auth     Netlify Auth
   - CORS_ORIGINS  - VITE_API_URL
   - MONGO_URI     - NODE_VERSION
   - BACKEND_URL
   - SECRET_KEY
       │                │
       ▼                ▼
   Backend App    Frontend App
   Uses env vars  Uses env vars
   for config     in build
```

---

## Data Flow Diagram

```
External API/LLM (Optional)
│
├─ OpenAI API (Chat)
├─ SendGrid API (Emails)
│
└──────────┐
           │
           ▼
    Render Backend
    app/main.py
           │
      ┌────┴────┬──────────┬──────────┐
      │          │          │          │
      ▼          ▼          ▼          ▼
   Auth API  Predict API  Chat API  Status API
   /api/     /api/        /api/      /health
   auth/*    predict      chat/*
      │          │          │
      │          ▼          │
      │    Image Upload     │
      │    Save to disk     │
      │    Run model        │
      │          │          │
      └─────┬────┴────┬─────┘
            │         │
            ▼         ▼
         MongoDB Atlas
         Database
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
    users  predictions  chats
    table  table       table
      │     │         │
      └─────┴─────────┘
            │
            ▼
        Response JSON
            │
       ┌────┴────┐
       │          │
       ▼          ▼
   Image URL    Data
   (absolute)   (predictions)
       │          │
       └────┬─────┘
            │
       CORS Allowed
            │
            ▼
    Netlify Frontend
    React Component
            │
       ┌────┴─────┐
       │           │
       ▼           ▼
   Display Image  Show Results
   from absolute  to User
   URL
```

---

## Security Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              PUBLIC INTERNET (HTTPS)                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         NETLIFY CDN (Everything is public)          │  │
│  │                                                     │  │
│  │  frontend/dist (built React app, no secrets)       │  │
│  └────────────────────────────────┬────────────────────┘  │
│                                    │                       │
│  ┌────────────────────────────────┴────────────────────┐  │
│  │         RENDER BACKEND (Protected)                 │  │
│  │                                                     │  │
│  │  Environment Variables (NOT in code):              │  │
│  │  MONGO_URI ..................... PROTECTED          │  │
│  │  SECRET_KEY .................... PROTECTED          │  │
│  │  CORS_ORIGINS .................. PUBLIC             │  │
│  │  BACKEND_URL ................... PUBLIC             │  │
│  │                                                     │  │
│  │  API Endpoints:                                     │  │
│  │  /api/auth            - Auth check                │  │
│  │  /api/predict         - Requires Token             │  │
│  │  /api/chat            - Requires Token             │  │
│  │  /static/*            - Static files               │  │
│  └────────────────────────────────┬────────────────────┘  │
│                                    │                       │
│  ┌────────────────────────────────┴────────────────────┐  │
│  │    MONGODB ATLAS (Private Network)                 │  │
│  │                                                     │  │
│  │  Users/Predictions/Chats (All private)             │  │
│  │  IP Whitelist: Only Render IP allowed              │  │
│  │  Auth: Username/Password from env var              │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Timeline

```
T=0min   ┌──────────────────────────────────────┐
         │  MongoDB Atlas Setup (10 min)         │
         │  - Create cluster                     │
         │  - Create user                        │
         │  - Get connection string              │
         └──────────────────────────────────────┘
                          │
T=10min  ┌────────────────┴──────────────────────┐
         │  Render Deployment (10 min)            │
         │  - Set environment variables          │
         │  - Deploy application                 │
         │  - Get backend URL                    │
         │  - Update CORS_ORIGINS                │
         └──────────────────────────────────────┘
                          │
T=20min  ┌────────────────┴──────────────────────┐
         │  Netlify Deployment (10 min)           │
         │  - Set VITE_API_URL                   │
         │  - Deploy application                 │
         │  - Redeploy with env vars             │
         └──────────────────────────────────────┘
                          │
T=30min  ┌────────────────┴──────────────────────┐
         │  Testing (10-15 min)                   │
         │  - Test login/register                │
         │  - Test MRI upload                    │
         │  - Check image URLs                   │
         │  - Verify CORS works                  │
         └──────────────────────────────────────┘
                          │
T=45min  ✅ DEPLOYED & READY!
```

---

## Summary

The architecture ensures:
- ✅ **Frontend** served globally via Netlify CDN (fast)
- ✅ **Backend** running on Render with auto-scaling
- ✅ **Database** secure on MongoDB Atlas
- ✅ **Communication** cross-domain with CORS headers
- ✅ **Images** stored on Render, referenced with absolute URLs
- ✅ **Security** secrets in environment, not in code
- ✅ **Scalability** each service scales independently
