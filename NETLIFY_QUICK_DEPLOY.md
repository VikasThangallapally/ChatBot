# 🚀 NETLIFY DEPLOYMENT - QUICK START

## OPTION 1: Upload Pre-built Files (Fastest)

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. This creates a "dist" folder
# 3. Go to https://app.netlify.com/drop
# 4. Drag & drop the "dist" folder
# 5. Done! 🎉
```

---

## OPTION 2: Connect GitHub (Recommended)

### Step 1: Prepare GitHub
```bash
# Push frontend-netlify-deploy folder to GitHub
git add frontend-netlify-deploy/
git commit -m "Add standalone frontend for Netlify deployment"
git push origin main
```

### Step 2: Connect to Netlify
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Select GitHub repo: `VikasThangallapally/neuroAssist`
4. Click "Deploy"

### Step 3: Configure Build Settings
- **Base directory:** `frontend-netlify-deploy` (or `frontend`)
- **Build command:** `npm run build`
- **Publish directory:** `dist`

### Step 4: Add Environment Variables
Click "Site settings" → "Build & deploy" → "Environment"
```
VITE_API_BASE_URL=https://brain-tumor-api.onrender.com
VITE_ENVIRONMENT=production
CI=true
```

### Step 5: Deploy
Click "Deploy site" and wait 2-3 minutes ✅

---

## ✅ AFTER DEPLOYMENT

### Test Your App
1. Visit your Netlify URL (e.g., `https://your-site.netlify.app`)
2. Upload an MRI image
3. Check predictions
4. Test chatbot

### If It Fails
- Check **Netlify logs**: Site settings → "Deploys" → view logs
- Verify `VITE_API_BASE_URL` is correct
- Ensure backend API is running

---

## 📋 FILES TO USE

### Standalone (No dependencies on backend folder):
```
frontend-netlify-deploy/
├── src/
├── package.json
├── netlify.toml
├── index.html
└── README.md
```

### Or use original:
```
frontend/
├── src/
├── package.json
├── netlify.toml
├── index.html
└── [other files]
```

Both work! Use whichever you prefer.

---

## 🔑 REQUIRED SETTINGS

| Setting | Value |
|---------|-------|
| Build Command | `npm run build` |
| Publish Directory | `dist` |
| Node Version | `18` |
| API URL | Your backend URL |

---

**That's it! Your app is now live on Netlify!** 🎊
