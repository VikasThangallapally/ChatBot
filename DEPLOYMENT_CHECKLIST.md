# Brain Tumor AI Deployment Checklist

Use this checklist to deploy your application step-by-step.

## Pre-Deployment Preparation (Do Before Starting)

### Code & Repository
- [ ] All code is committed to GitHub
- [ ] No uncommitted changes: `git status` shows clean
- [ ] README.md is updated with project info
- [ ] `.gitignore` includes `.env` and node_modules/

### Testing Locally
- [ ] Backend runs: `python app/main.py` or `uvicorn app.main:app --reload`
- [ ] Frontend runs: `cd frontend && npm run dev`
- [ ] Can upload MRI image on localhost
- [ ] Image appears with absolute URL in response
- [ ] No console errors in browser DevTools

### Environment Files
- [ ] `.env.backend.example` is complete and documented
- [ ] `frontend/.env.example` is complete and documented
- [ ] Created `.env` in root from `.env.backend.example`
- [ ] Created `frontend/.env.local` from `frontend/.env.example`
- [ ] Tested locally with these `.env` files

### Dependencies
- [ ] All Python packages in `requirements.txt`
- [ ] All Node packages in `frontend/package.json`
- [ ] Python 3.11 version check: `python --version`
- [ ] Node 18+ version check: `node --version`
- [ ] npm packages install locally: `npm install` in frontend/

---

## Step 1: MongoDB Atlas Setup

### Create MongoDB Account
- [ ] Sign up at https://www.mongodb.com/cloud/atlas
- [ ] Verify email
- [ ] Create organization/project

### Create Cluster
- [ ] Click "Create" → "Database"
- [ ] Choose "M0 Sandbox" (free tier)
- [ ] Select region (preferably near your users)
- [ ] Create cluster (wait 5-10 minutes)

### Create Database User
- [ ] Go to "Database Access"
- [ ] Click "Add New Database User"
- [ ] Username: `db_user` (or your choice)
- [ ] Password: Generate strong password (save it!)
- [ ] Permissions: "Atlas Admin"
- [ ] Click "Add User"

### Get Connection String
- [ ] Go to "Clusters" → Click "Connect"
- [ ] Choose "Connect your application"
- [ ] Copy connection string
- [ ] Replace `<username>` with your username
- [ ] Replace `<password>` with your password
- [ ] Example: `mongodb+srv://db_user:password@cluster.mongodb.net/?appName=neuro_assist`
- [ ] **Save this string!**

### Configure Network Access
- [ ] Go to "Network Access"
- [ ] Click "Add IP Address"
- [ ] For production: Select "ALLOW ACCESS FROM ANYWHERE" (0.0.0.0/0)
- [ ] Or: Add specific Render IP (more secure)
- [ ] Click "Confirm"

### Test Connection (Optional)
- [ ] Install mongosh locally (if available)
- [ ] Test: `mongosh "YOUR_CONNECTION_STRING"`
- [ ] Should connect successfully

---

## Step 2: Render Backend Deployment

### Create Render Account
- [ ] Sign up at https://render.com (free account)
- [ ] Verify email
- [ ] Complete profile setup

### Connect GitHub
- [ ] In Render dashboard, click "Connect" or "Authorize"
- [ ] Choose your brain-tumor-ai repository
- [ ] Authorize Render to access your repo

### Create Web Service
- [ ] Dashboard → "New +" → "Web Service"
- [ ] Select your GitHub repo
- [ ] Click "Connect"

### Configure Service
Service Name:
- [ ] Name: `brain-tumor-api`
- [ ] Branch: `main`

Build Command:
- [ ] Copy exactly: `pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt`

Start Command:
- [ ] Copy exactly: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Deployment Settings:
- [ ] Environment: `Python 3.11`
- [ ] Region: `Virginia` (or your choice)
- [ ] Plan: `Free` (or paid if needed)

### Set Environment Variables
In Render dashboard, go to "Environment" and add these variables:

**Required Variables**:
- [ ] `MONGO_URI` = `mongodb+srv://db_user:password@cluster.mongodb.net/?appName=neuro_assist` (from MongoDB Atlas)
- [ ] `SECRET_KEY` = Generate from: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] `BACKEND_URL` = (leave as placeholder, update after deployment)
- [ ] `CORS_ORIGINS` = `http://localhost:3000,http://localhost:5174`

**Optional Variables** (copy if you use these features):
- [ ] `SENDGRID_API_KEY` = Your SendGrid key (if using email)
- [ ] `SENDGRID_FROM_EMAIL` = Your email (if using email)
- [ ] `OPENAI_API_KEY` = Your OpenAI key (if using GPT features)

**Copy-Paste Values**:
```
MONGO_DB_NAME=neuro_assist
MODEL_NAME=brain_tumor_model.h5
IMAGE_SIZE=224
MAX_UPLOAD_SIZE=10485760
CONFIDENCE_THRESHOLD=0.5
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
LOG_LEVEL=INFO
```

- [ ] Add all of the above

### Deploy
- [ ] Click "Deploy"
- [ ] Wait for build to complete (screen shows build logs in real-time)
- [ ] Status should change from "Building" → "Running"
- [ ] Expected time: 5-10 minutes

### Get Backend URL
- [ ] Once deployed, copy the service URL
- [ ] Should look like: `https://brain-tumor-api.onrender.com/`
- [ ] **Save this URL!**

### Update Backend URL
- [ ] Go back to "Environment"
- [ ] Edit `BACKEND_URL` variable
- [ ] Set to your actual Render URL: `https://brain-tumor-api.onrender.com`
- [ ] Edit `CORS_ORIGINS` variable
- [ ] Add your Netlify domain (you'll get this later): `http://localhost:3000,http://localhost:5174,https://your-site.netlify.app`
- [ ] Click "Deploy" to apply changes

### Test Backend
- [ ] Test health endpoint: `curl https://brain-tumor-api.onrender.com/health`
- [ ] Should return: `{"status": "healthy", "service": "Brain Tumor Chatbot", "version": "1.0.0"}`
- [ ] Backend is working! ✅

---

## Step 3: Netlify Frontend Deployment

### Create Netlify Account
- [ ] Sign up at https://app.netlify.com (free account)
- [ ] Verify email
- [ ] Complete profile setup

### Connect GitHub
- [ ] Dashboard → "Add new site" → "Import an existing project"
- [ ] Click "GitHub"
- [ ] Authorize Netlify to access your repos
- [ ] Select your `brain-tumor-ai` repository

### Configure Build Settings
- [ ] Build command: `cd frontend && npm run build`
- [ ] Publish directory: `frontend/dist`
- [ ] Click "Deploy site"
- [ ] Wait for initial build (2-5 minutes)

### Get Frontend URL
- [ ] Once deployed, copy the site URL
- [ ] Should look like: `https://your-site-name.netlify.app/`
- [ ] **Save this URL!**

### Set Environment Variables
- [ ] Dashboard → Your site → "Site settings" → "Build & deploy" → "Environment"
- [ ] Click "Edit variables"
- [ ] Add:
  - [ ] `VITE_API_URL` = Your Render backend URL: `https://brain-tumor-api.onrender.com`
  - [ ] `NODE_VERSION` = `18`
- [ ] Click "Save"

### Trigger New Deploy
- [ ] Dashboard → "Deploys" → "Trigger deploy" → "Deploy site"
- [ ] Wait for build with new environment variables (1-3 minutes)
- [ ] Status should be "Published"

### Test Frontend
- [ ] Visit your Netlify URL in browser
- [ ] Should load the app (may show login screen)
- [ ] Open browser DevTools Console
- [ ] Should see: `[API Config] Using API_BASE_URL: https://brain-tumor-api.onrender.com`
- [ ] No CORS errors
- [ ] Frontend is working! ✅

### Update Backend CORS
- [ ] Go back to Render dashboard
- [ ] Your service → "Environment"
- [ ] Edit `CORS_ORIGINS`
- [ ] Add your Netlify domain: `http://localhost:3000,http://localhost:5174,https://your-site-name.netlify.app`
- [ ] Click "Deploy" to apply

---

## Step 4: End-to-End Testing

### Test Authentication
- [ ] Visit https://your-site-name.netlify.app
- [ ] Register new account
- [ ] Check that registration works (or login with existing account)
- [ ] Should not see CORS errors

### Test MRI Upload
- [ ] Click "Upload MRI Scan"
- [ ] Select a test MRI image (JPEG/PNG)
- [ ] Upload
- [ ] Wait for prediction (30-60 seconds)
- [ ] Should see results displayed

### Check Image URL
- [ ] Open browser DevTools → Network tab
- [ ] Upload another image
- [ ] Look for response in Network tab (POST to `/api/predict`)
- [ ] Check the response JSON
- [ ] `image_path` should be: `https://brain-tumor-api.onrender.com/static/uploads/filename.jpg`
- [ ] NOT `http://localhost:...` or relative path

### Verify API Communication
- [ ] Open DevTools → Console
- [ ] No red errors should appear
- [ ] No CORS errors like "Access to XMLHttpRequest blocked..."
- [ ] Check Network → API calls should show Status 200, 201, etc.

### Mobile Testing (Optional)
- [ ] Test on mobile device
- [ ] Visit frontend URL on phone
- [ ] Test upload
- [ ] Should work identically to desktop

---

## Final Verification Checklist

### Backend Endpoints Working
- [ ] `/health` returns 200 and healthy status
- [ ] `/api/predict` accepts POST with image file
- [ ] `/static/uploads/*` serves uploaded images
- [ ] No 500 errors in logs

### Frontend Working
- [ ] Loads without errors
- [ ] Shows login/register page
- [ ] Can authenticate
- [ ] Can upload images
- [ ] Shows predictions
- [ ] Image displays from Render backend

### Database Working
- [ ] User data saves to MongoDB Atlas
- [ ] Can login with saved credentials
- [ ] No database connection errors in logs

### Cross-Domain Communication
- [ ] Netlify frontend talks to Render backend
- [ ] CORS allows requests
- [ ] Image URLs point to correct domain
- [ ] No mixed content errors (https/http issues)

---

## Post-Deployment Tasks

### Documentation
- [ ] Document your Render backend URL
- [ ] Document your Netlify frontend URL
- [ ] Save MongoDB credentials in secure location
- [ ] Update README with deployment info

### Monitoring (Optional)
- [ ] Check Render logs periodically: Dashboard → Logs
- [ ] Check Netlify logs: Dashboard → Deploys → Deploy log
- [ ] Monitor MongoDB Atlas: Dashboard → Metrics

### Backups (Optional)
- [ ] Export MongoDB data regularly
- [ ] Backup source code to multiple places
- [ ] Keep .env files backed up securely

### Performance (Optional)
- [ ] Test with slow internet (Chrome DevTools → Throttling)
- [ ] Check page load time (should be <3s)
- [ ] Test image upload with different file sizes

---

## Troubleshooting During Deploy

### Build Fails on Render
- [ ] Check build logs in Render dashboard
- [ ] Verify `requirements.txt` is not corrupted
- [ ] Verify Python version in `runtime.txt`
- [ ] Try manual build: `pip install -r requirements.txt`

### Build Fails on Netlify
- [ ] Check Netlify deploy logs
- [ ] Verify `frontend/package.json` has all dependencies
- [ ] Try manually: `cd frontend && npm install && npm run build`
- [ ] Check Node version matches

### CORS Error
- [ ] Check Render `CORS_ORIGINS` includes Netlify domain
- [ ] Verify Netlify domain is spelled correctly (no typos)
- [ ] Redeploy Render after updating CORS

### Image URL is Wrong
- [ ] Check Render `BACKEND_URL` is correct
- [ ] Verify it includes protocol (https://)
- [ ] Check trailing slashes
- [ ] Redeploy Render after updating

### Can't Connect to MongoDB
- [ ] Verify connection string is correct
- [ ] Check username/password
- [ ] Check IP whitelist in MongoDB Atlas allows Render IPs
- [ ] Test connection locally first

---

## SUCCESS! 🎉

If you've checked everything above and all tests pass, your application is successfully deployed!

**Your URLs**:
- Frontend: https://your-site-name.netlify.app
- Backend: https://brain-tumor-api.onrender.com
- Database: MongoDB Atlas (accessed via connection string)

---

## Helpful Links

- Render Logs: https://dashboard.render.com
- Netlify Logs: https://app.netlify.com
- MongoDB Atlas: https://cloud.mongodb.com
- GitHub: https://github.com (your repo)

---

**Estimated Total Time**: 30-45 minutes
- MongoDB setup: 10 minutes
- Render deployment: 10 minutes
- Netlify deployment: 10 minutes
- Testing: 10-15 minutes

Good luck! 🚀
