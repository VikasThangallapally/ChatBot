# 🚀 Quick Render.com Deployment (5 Minutes)

## What You'll Get
- ✅ Frontend running on `https://yourappdomain.onrender.com`
- ✅ Backend API on `https://api-yourappdomain.onrender.com`
- ✅ Auto-scaling & HTTPS included
- ✅ Free tier available
- ✅ Automatic redeploys on GitHub push

---

## 🎯 TL;DR - 3 Steps

### Step 1: Sign in to Render
```
https://render.com
Sign up with GitHub → Authorize
```

### Step 2: Connect Repository
```
Dashboard → New → Blueprint
Select: VikasThangallapally/ChatBot
Render auto-reads render.yaml ✅
```

### Step 3: Deploy
```
Click "Deploy"
Wait 5-10 minutes
Get URLs ✅
```

---

## 📞 Services Deployed

| Service | Type | URL Format | Status |
|---------|------|-----------|--------|
| **Backend** | Python API | `https://brain-tumor-api.onrender.com` | 🟢 Live |
| **Frontend** | React App | `https://brain-tumor-frontend.onrender.com` | 🟢 Live |

---

## 🧪 Test It Works

**Backend Health Check:**
```bash
curl https://brain-tumor-api.onrender.com/health
```

**API Docs:**
Open in browser:
```
https://brain-tumor-api.onrender.com/docs
```

**Upload & Predict:**
Open frontend and upload brain MRI image:
```
https://brain-tumor-frontend.onrender.com
```

---

## 📌 Environment Variables (Auto-Configured)

**Backend:**
- `PORT`: 8000
- `DEBUG`: false
- `OPENAI_API_KEY`: (optional - leave blank)

**Frontend:**
- `VITE_API_URL`: https://brain-tumor-api.onrender.com

✅ Already in `render.yaml` - no manual config needed!

---

## 🔄 Update Your Site

Every GitHub push auto-deploys:
```bash
git add .
git commit -m "Your changes"
git push origin main
# Render auto-redeploys ✅
```

---

## 💡 Next Steps

1. ✅ Go to https://render.com
2. ✅ Click "New" → "Blueprint"
3. ✅ Select your GitHub repo
4. ✅ Click "Deploy"
5. ✅ Share your live URL!

---

**Questions?** Read the full guide: `RENDER_DEPLOYMENT_GUIDE.md`
