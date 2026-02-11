# Brain Tumor AI - Netlify + Render Deployment Guide

This guide provides step-by-step instructions to deploy your Brain Tumor AI application with:
- **Frontend**: React on Netlify
- **Backend**: FastAPI on Render  
- **Database**: MongoDB Atlas

## Table of Contents
1. [Backend Setup (Render)](#backend-setup-render)
2. [Frontend Setup (Netlify)](#frontend-setup-netlify)
3. [Database Setup (MongoDB Atlas)](#database-setup-mongodb-atlas)
4. [Environment Variables](#environment-variables)
5. [Local Development](#local-development)
6. [Deployment Checklist](#deployment-checklist)

---

## Backend Setup (Render)

### Prerequisites
- GitHub account with your repository
- Render account (free tier available)
- MongoDB Atlas cluster

### Step 1: Push Code to GitHub
```bash
cd neuroAssist-main
git init
git add .
git commit -m "Initial commit for Render + Netlify deployment"
git remote add origin https://github.com/YOUR_USERNAME/brain-tumor-ai.git
git push -u origin main
```

### Step 2: Create Web Service on Render

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in the configuration:
   - **Name**: `brain-tumor-api`
   - **Branch**: `main`
   - **Build Command**: 
     ```
     pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt
     ```
   - **Start Command**: 
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Environment**: `Python 3.11`
   - **Region**: `Virginia`
   - **Plan**: `Free` (or paid as needed)

### Step 3: Set Environment Variables

In Render dashboard, navigate to your service's "Environment" tab and add:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=neuro_assist
MONGO_DB_NAME=neuro_assist
BACKEND_URL=https://brain-tumor-api.onrender.com
CORS_ORIGINS=http://localhost:3000,http://localhost:5174,https://your-netlify-app.netlify.app
SECRET_KEY=your-secret-key-here
SENDGRID_API_KEY=your-sendgrid-key (optional)
SENDGRID_FROM_EMAIL=noreply@yourapp.com (optional)
OPENAI_API_KEY=your-openai-key (optional)
```

> **Important**: Replace `brain-tumor-api.onrender.com` with your actual Render service URL (available after first deployment)

### Step 4: Initial Deployment

1. Click "Deploy"
2. Wait for build to complete (5-10 minutes)
3. Copy the backend URL: `https://brain-tumor-api.onrender.com`
4. Update `BACKEND_URL` and `CORS_ORIGINS` environment variables with the correct domain
5. Trigger a redeploy if needed

### Verifying Backend

Test your backend with:
```bash
curl https://brain-tumor-api.onrender.com/health
# Expected response: {"status": "healthy", "service": "Brain Tumor Chatbot", "version": "1.0.0"}
```

---

## Frontend Setup (Netlify)

### Prerequisites
- GitHub repository with frontend code
- Netlify account (free tier available)

### Step 1: Connect Repository to Netlify

1. Log in to [Netlify Dashboard](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Select GitHub and authorize Netlify
4. Choose your repository
5. Fill in the configuration:
   - **Owner**: Your team/account
   - **Branch to deploy**: `main`
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/dist`

### Step 2: Set Environment Variables

In Netlify dashboard, navigate to "Site settings" → "Build & deploy" → "Environment":

Add the environment variables:
```
VITE_API_URL=https://brain-tumor-api.onrender.com
NODE_VERSION=18
```

> **Replace** `https://brain-tumor-api.onrender.com` with your actual Render backend URL

### Step 3: Configure Build Settings

1. Go to "Site settings" → "Build & deploy" → "Build settings"
2. Verify:
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/dist`

### Step 4: Deploy

1. Netlify will automatically deploy on every push to `main` branch
2. Or manually trigger a deploy from "Deploys" tab
3. Wait for build to complete (2-5 minutes)

### Verifying Frontend

Your frontend will be available at: `https://your-site-name.netlify.app`

---

## Database Setup (MongoDB Atlas)

### Prerequisites
- MongoDB Atlas account (free tier available)

### Step 1: Create a Cluster

1. Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new project or use existing
3. Click "Create" → "Database"
4. Choose "M0 Sandbox" (free tier)
5. Select your region
6. Click "Create Deployment"

### Step 2: Create Database User

1. In Atlas dashboard, go to "Database Access"
2. Click "Add New Database User"
3. Create username and strong password (save this!)
4. Set permissions to "Atlas Admin"
5. Click "Add User"

### Step 3: Get Connection String

1. Go back to "Clusters"
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<username>` and `<password>` with your database credentials

Example:
```
mongodb+srv://username:password@cluster.mongodb.net/?appName=neuro_assist
```

### Step 4: Whitelist IPs

1. Go to "Network Access"
2. Click "Add IP Address"
3. For development: Add your IP
4. For production: Allow `0.0.0.0/0` (or specific IPs)

### Verify Connection

Test from your backend or local machine:
```bash
mongosh "mongodb+srv://username:password@cluster.mongodb.net"
```

---

## Environment Variables

### Backend Environment Variables (.env or Render dashboard)

```dotenv
# MongoDB
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=neuro_assist
MONGO_DB_NAME=neuro_assist

# Backend URL (for generating absolute image URLs)
BACKEND_URL=https://brain-tumor-api.onrender.com

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:5174,https://your-site.netlify.app

# Model/Image settings
MODEL_NAME=brain_tumor_model.h5
IMAGE_SIZE=224
MAX_UPLOAD_SIZE=10485760
CONFIDENCE_THRESHOLD=0.5

# Auth
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Email (optional)
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_FROM_EMAIL=noreply@yourapp.com

# Logging
LOG_LEVEL=INFO
```

### Frontend Environment Variables (Netlify dashboard)

```
VITE_API_URL=https://brain-tumor-api.onrender.com
NODE_VERSION=18
```

---

## Local Development

### Backend Setup

1. Copy `.env.backend.example` to `.env`:
   ```bash
   cp .env.backend.example .env
   ```

2. Update `.env` with your local/development values:
   ```dotenv
   MONGO_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net
   BACKEND_URL=http://localhost:8000
   CORS_ORIGINS=http://localhost:3000,http://localhost:5174
   SECRET_KEY=your-secret-key
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python app/main.py
   # or
   uvicorn app.main:app --reload --port 8000
   ```

Server runs at: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

3. Update `.env.local`:
   ```
   VITE_API_URL=http://localhost:8000
   ```

4. Install dependencies:
   ```bash
   npm install
   ```

5. Start development server:
   ```bash
   npm run dev
   ```

Frontend runs at: `http://localhost:5174`

### Testing Locally

1. **Backend health check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Upload an MRI image**:
   - Open `http://localhost:5174`
   - Login/Register
   - Upload an MRI image
   - Check browser console for API calls
   - Verify `image_path` has absolute URL format

---

## Deployment Checklist

### Before Deploying

- [ ] MongoDB Atlas cluster created and user credentials saved
- [ ] GitHub repository is private and code is pushed
- [ ] `.env.backend.example` updated with all required variables
- [ ] `.env.frontend.example` updated with `VITE_API_URL` 
- [ ] Local development tested and working
- [ ] All dependencies in `requirements.txt` 
- [ ] `frontend/package.json` has all required dependencies
- [ ] Build commands tested locally:
  - Backend: `pip install -r requirements.txt && uvicorn app.main:app --port 8000`
  - Frontend: `npm run build`

### Render Backend Deployment

- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Web service created with correct build/start commands
- [ ] Environment variables set in Render dashboard
- [ ] Initial deployment successful
- [ ] Backend URL obtained (e.g., `https://brain-tumor-api.onrender.com`)
- [ ] Health endpoint responds: `/health`
- [ ] Static files endpoint works: `/static/test.txt`

### Netlify Frontend Deployment

- [ ] Netlify account created
- [ ] GitHub repository connected to Netlify
- [ ] Build settings correct:
  - Build command: `cd frontend && npm run build`
  - Publish: `frontend/dist`
- [ ] Environment variables set:
  - `VITE_API_URL=https://brain-tumor-api.onrender.com`
  - `NODE_VERSION=18`
- [ ] Site deployed successfully
- [ ] Frontend loads with correct API URL
- [ ] API calls reach Render backend successfully

### Post-Deployment Testing

- [ ] Visit `https://your-site.netlify.app`
- [ ] Login/Register works
- [ ] Upload MRI image works
- [ ] Prediction response shows absolute URLs in `image_path`
- [ ] Check browser console for no CORS errors
- [ ] Test on mobile device
- [ ] Verify `/health` endpoint works
- [ ] Check Render/Netlify logs for errors

### Troubleshooting

#### CORS Errors
- Check `CORS_ORIGINS` in Render includes your Netlify domain
- Verify frontend calls correct `VITE_API_URL`

#### Image paths not working
- Verify `BACKEND_URL` is set correctly in Render
- Check `/static/uploads` directory exists on Render
- Test: `curl https://brain-tumor-api.onrender.com/static/test.txt`

#### Build failures
- Check Render/Netlify logs
- Verify Python/Node versions match `runtime.txt`/`NODE_VERSION`
- Ensure all dependencies are in requirements.txt/package.json

#### Slow performance
- Upgrade Render plan from Free
- Enable caching on Netlify
- Optimize images in frontend

---

## File Structure

```
neuroAssist-main/
├── app/
│   ├── main.py                 (updated for CORS + PORT)
│   ├── config.py               (updated for BACKEND_URL + CORS_ORIGINS)
│   ├── api/routes/
│   │   └── predict.py          (updated for absolute URLs)
│   └── ... (other files)
├── frontend/
│   ├── src/config/
│   │   └── api.js              (updated for VITE_API_URL)
│   ├── vite.config.js          (updated - no proxy)
│   ├── netlify.toml            (updated for separate deployment)
│   ├── .env.example            (updated)
│   └── package.json
├── .env.backend.example        (created)
├── render-backend.yaml         (created)
├── requirements.txt
└── README.md
```

---

## Quick Reference

### Important URLs After Deployment

- **Frontend**: `https://your-site-name.netlify.app`
- **Backend**: `https://brain-tumor-api.onrender.com`
- **Backend Health**: `https://brain-tumor-api.onrender.com/health`
- **Render Dashboard**: `https://dashboard.render.com`
- **Netlify Dashboard**: `https://app.netlify.com`
- **MongoDB Atlas**: `https://cloud.mongodb.com`

### Environment Variables Summary

| Variable | Backend | Frontend | Example |
|----------|---------|----------|---------|
| `VITE_API_URL` | ✗ | ✓ | `https://brain-tumor-api.onrender.com` |
| `MONGO_URI` | ✓ | ✗ | `mongodb+srv://...` |
| `BACKEND_URL` | ✓ | ✗ | `https://brain-tumor-api.onrender.com` |
| `CORS_ORIGINS` | ✓ | ✗ | `https://app.netlify.app` |
| `SECRET_KEY` | ✓ | ✗ | random 32-char string |

### Common Commands

**Generate Secret Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Test Backend Locally**:
```bash
uvicorn app.main:app --reload --port 8000
```

**Build Frontend Locally**:
```bash
cd frontend && npm run build
```

**Check Render Logs**:
```
Render Dashboard → Your Service → Logs
```

**Check Netlify Logs**:
```
Netlify Dashboard → Your Site → Deploys → Build log
```

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Netlify Docs**: https://docs.netlify.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **MongoDB Atlas Docs**: https://docs.mongodb.com/atlas
- **Vite Docs**: https://vitejs.dev

---

## Security Reminders

✅ **DO**:
- Use environment variables for all secrets
- Keep MongoDB credentials safe
- Enable IP whitelisting in MongoDB Atlas
- Use strong `SECRET_KEY` for JWT
- Set `CORS_ORIGINS` to specific domains in production

❌ **DON'T**:
- Commit `.env` files
- Use `allow_origins=["*"]` in production
- Share API keys or passwords
- Store secrets in code
- Use weak passwords for MongoDB

---

Last Updated: February 11, 2025
