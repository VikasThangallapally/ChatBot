# Deploy Brain Tumor Detection AI on Render.com

Deploy your complete full-stack application (React Frontend + FastAPI Backend) on **Render.com** with a single click!

## 📋 Prerequisites

- GitHub account (already set up ✅)
- Render.com account (free)
- Your project pushed to GitHub ✅

---

## 🚀 Step-by-Step Deployment Guide

### Step 1: Sign Up for Render.com

1. Go to [render.com](https://render.com)
2. Click **"Sign Up"** → Choose **"Sign up with GitHub"**
3. Authorize Render to access your GitHub account
4. Complete your profile setup

![Render Sign Up](/docs/render-signup.png)

---

### Step 2: Create a New Service from render.yaml

1. From your Render dashboard, click **"New +"** → **"Blueprint"**
2. Search and select your GitHub repository: **`VikasThangallapally/ChatBot`**
3. Render will automatically detect and parse **`render.yaml`**
4. You should see TWO services listed:
   - ✅ **brain-tumor-api** (Python Backend)
   - ✅ **brain-tumor-frontend** (React Frontend)

![Render Blueprint](/docs/render-blueprint.png)

---

### Step 3: Configure Environment Variables

#### For Backend (brain-tumor-api):

1. Click on **"brain-tumor-api"** service
2. Go to **"Environment"** tab
3. Add these environment variables:

| Variable | Value |
|----------|-------|
| `OPENAI_API_KEY` | Leave blank (GPT optional) |
| `PORT` | 8000 |
| `DEBUG` | false |

#### For Frontend (brain-tumor-frontend):

1. Click on **"brain-tumor-frontend"** service
2. Go to **"Environment"** tab
3. Add this variable:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://brain-tumor-api.onrender.com` |

> **Note:** Replace `brain-tumor-api` with your actual backend service name from Render

---

### Step 4: Deploy

1. Click **"Deploy"** button
2. Wait for both services to build and deploy (5-10 minutes)
3. You'll see deployment logs in real-time

### What's Happening:

```
✅ Backend Service:
   - Installing Python 3.11
   - Installing requirements.txt
   - Starting Uvicorn server
   - API running at: https://brain-tumor-api.onrender.com

✅ Frontend Service:
   - Installing Node.js dependencies
   - Building React app with Vite
   - Deploying to CDN
   - Site running at: https://brain-tumor-frontend.onrender.com
```

---

### Step 5: Get Your Live URLs

Once deployment completes:

🌐 **Frontend URL:** `https://brain-tumor-frontend.onrender.com`
🔌 **API URL:** `https://brain-tumor-api.onrender.com`

---

## ✨ What Happens After Deployment

### Automatic Features:
- ✅ SSL/TLS encryption (HTTPS enabled)
- ✅ Global CDN for frontend
- ✅ Health checks every 30 seconds
- ✅ Automatic restart if service crashes
- ✅ Environment variables are secure
- ✅ Logs accessible in dashboard

### Manual Updates:
Every time you push to GitHub:
1. Render detects the change
2. Automatically redeploys both services
3. Zero downtime deployments

---

## 🧪 Testing Your Deployment

### Test Backend API:
```bash
curl -X GET https://brain-tumor-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Brain Tumor Chatbot",
  "version": "1.0.0"
}
```

### Test API Docs:
Visit in browser:
```
https://brain-tumor-api.onrender.com/docs
```

### Test Frontend:
1. Open: `https://brain-tumor-frontend.onrender.com`
2. Upload a brain MRI image
3. See predictions instantly!

---

## 🔧 Common Issues & Solutions

### Issue: "503 Service Unavailable"
**Solution:** Wait 5 minutes for first startup. Render free tier starts services on demand.

### Issue: "Connection refused to backend"
**Solution:** Ensure `VITE_API_URL` is set correctly in frontend environment variables.

### Issue: "Build failed: npm install"
**Solution:** Check `frontend/package.json` has all dependencies listed correctly.

### Issue: "Build failed: pip install"
**Solution:** Check `requirements.txt` has all Python dependencies.

---

## 📊 Monitoring & Logs

In Render Dashboard:

1. **Logs Tab:** View real-time logs
   ```
   2026-02-07 14:32:51 - app.services.gpt_service - WARNING - OPENAI_API_KEY not found
   2026-02-07 14:33:01 - app.main - INFO - Python version: 3.11.9
   INFO:     Application startup complete.
   ```

2. **Metrics Tab:** View CPU, Memory, Requests
3. **Events Tab:** Track deployments and restarts

---

## 🚀 Performance Tips

### Frontend Optimization:
- ✅ Code splitting already enabled in vite.config.js
- ✅ Images are lazy-loaded
- ✅ Tailwind CSS is purged for production
- ✅ React components are optimized

### Backend Optimization:
- ✅ FastAPI is lightweight and fast
- ✅ Model is cached after first load
- ✅ Image validation is efficient
- ✅ CORS is enabled for cross-origin requests

---

## 💰 Pricing

### Render.com Free Tier:
- ✅ 1 free web service (Python backend) = **$0**
- ✅ 1 free static site (React frontend) = **$0**
- ✅ 512MB RAM per service = **Sufficient**
- ✅ Unlimited bandwidth = **Perfect**

### Optional Paid Upgrades:
- Pro plan: $7/month per service (if you need more resources)
- Pay-as-you-go database services available

---

## 📝 Custom Domain (Optional)

To use a custom domain like `yourdomain.com`:

1. Go to **Render Dashboard** → **Your Service**
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain
4. Update DNS settings (Render provides instructions)
5. SSL certificate auto-generates with Let's Encrypt

---

## 🔄 Continuous Deployment

Your project is now **Automatically Deployed** when you:

```bash
# Make changes locally
git add .
git commit -m "Fix bug or add feature"
git push origin main

# Render automatically detects changes and redeploys both services!
```

No manual deployments needed!

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** https://github.com/VikasThangallapally/ChatBot/issues
- **API Docs:** Visit `https://brain-tumor-api.onrender.com/docs`

---

## ✅ Deployment Checklist

- [ ] Created Render.com account
- [ ] Connected GitHub repository
- [ ] Deployed using render.yaml/Blueprint
- [ ] Configured backend environment variables
- [ ] Configured frontend API URL
- [ ] Both services deployed successfully
- [ ] Tested health endpoint
- [ ] Uploaded test MRI image
- [ ] Got predictions successfully
- [ ] Custom domain configured (optional)

---

## 🎉 Congratulations!

Your Brain Tumor Detection AI is now **LIVE** and accessible worldwide! 🧠

**Share your deployment:**
- Frontend: `https://brain-tumor-frontend.onrender.com`
- API: `https://brain-tumor-api.onrender.com`
- GitHub: `https://github.com/VikasThangallapally/ChatBot`

