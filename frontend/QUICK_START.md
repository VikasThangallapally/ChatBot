# 🚀 QUICK START - Brain Tumor AI Assistant

## Local Development (5 minutes)

```bash
# Terminal 1: Backend
cd /path/to/brain-tumor-chatbot
$env:PYTHONPATH="$(Get-Location)"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

**Access:**
- Frontend: `http://localhost:5174`
- Backend: `http://127.0.0.1:8000`
- API Docs: `http://127.0.0.1:8000/docs`

---

## Features Overview

### 1. Upload MRI
- Drag & drop or click to upload
- Supports JPEG, PNG, DICOM
- Real-time validation
- Upload progress bar

### 2. See Prediction
- Real-time CNN prediction
- Confidence score (0-100%)
- Severity level
- Prediction timing

### 3. Read Analysis
- Dynamic content based on tumor type
- 6 detailed sections
- Non-diagnostic language
- Medical disclaimers

### 4. Chat with Bot
- Floating button (bottom-right)
- Click to open/close
- Ask medical questions
- Context-aware responses

### 5. Share Results
- Screenshot friendly
- Professional appearance
- Educational content only

---

## Hero Section Behavior

**Before Upload:**
```
┌─────────────────────────────┐
│  Upload Card  │  🌍 Earth  │
│               │  Animation │
└─────────────────────────────┘
```

**After Upload:**
```
┌─────────────────────────────┐
│  Upload Card  │   📸 MRI    │
│               │  Preview    │
└─────────────────────────────┘
```

---

## Production Build

```bash
cd frontend

# Build (creates dist/ folder)
npm run build

# Preview production build locally
npm run preview

# Deploy to Netlify (after build)
netlify deploy --prod --dir=dist
```

**Build Stats:**
- Bundle: ~1.1 MB
- Gzipped: ~322 KB
- Build time: <6s
- Chunks: 6 (optimized)

---

## Environment Setup

### Development (.env.local)
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_ENVIRONMENT=development
```

### Production (Netlify)
```env
VITE_API_BASE_URL=https://your-backend-api.com
VITE_ENVIRONMENT=production
```

---

## Netlify Deployment (3 steps)

1. **Connect GitHub**
   - Push code to GitHub
   - Go to netlify.com
   - Click "New site from Git"
   - Select your repo

2. **Configure**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Set Variables**
   - Add `VITE_API_BASE_URL` → Your backend URL
   - Add `VITE_ENVIRONMENT` → `production`
   - Deploy!

---

## File Structure

```
brain-tumor-chatbot/
├── app/                           # Backend (FastAPI)
│   ├── main.py
│   ├── api/routes/
│   ├── core/
│   └── services/
├── frontend/                      # React Frontend
│   ├── src/
│   │   ├── App.jsx               # Main app (conditional hero)
│   │   ├── components/           # UI components
│   │   ├── config/               # API & analysis data
│   │   └── styles/
│   ├── .env.example              # Environment template
│   ├── .env.local                # Local env (git ignored)
│   ├── vite.config.js            # Vite config (optimized)
│   ├── netlify.toml              # Netlify deployment
│   └── package.json
└── README.md
```

---

## Component Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| **App.jsx** | Main component, conditional hero | `src/App.jsx` |
| **UploadCard** | MRI upload | `src/components/UploadCard.jsx` |
| **ResultPanel** | Prediction results | `src/components/ResultPanel.jsx` |
| **MedicalAnalysis** | Detailed analysis panel | `src/components/MedicalAnalysis.jsx` |
| **FloatingChatbot** | AI chatbot | `src/components/FloatingChatbot.jsx` |
| **Brain3D** | Earth animation | `src/components/Brain3D.jsx` |

---

## API Endpoints

```javascript
// Predict MRI
POST /api/predict
Content-Type: multipart/form-data
Body: { file: MRI_image }
Response: { 
  status: 'success',
  top_prediction: { label, confidence },
  medical_analysis: {...}
}

// Chat
POST /api/chat
Content-Type: application/json
Body: { 
  message: 'question',
  prediction_label?: 'Glioma',
  confidence_score?: 0.89
}
Response: { response: 'bot answer' }
```

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Upload MRI | Click upload card |
| Open Chat | Click floating button |
| Send Message | Enter (in chat input) |
| Close Chat | Click ✕ button |
| Copy Analysis | Select + Ctrl+C |

---

## Performance Tips

- **Build:** npm run build (creates optimized dist/)
- **Gzip:** Already enabled (322 KB)
- **Caching:** netlify.toml configured
- **Code split:** Chunks separated by library
- **Images:** Use WebP for smaller size

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5174 in use | `npm run dev -- --port 5175` |
| Build fails | `rm -rf node_modules && npm install` |
| API not responding | Check VITE_API_BASE_URL |
| No prediction | Verify MRI format (JPEG/PNG) |
| Chat not working | Check backend /api/chat endpoint |

---

## Security Checklist

- ✅ Environment variables for URLs
- ✅ Security headers in netlify.toml
- ✅ XSS protection (React)
- ✅ No hardcoded secrets
- ✅ CORS configured on backend
- ✅ Content Security Policy ready

---

## Monitoring

**Netlify Dashboard:**
- Build logs
- Performance metrics
- Error tracking
- Environment variables

**Browser DevTools:**
- Network tab (API calls)
- Console (errors)
- Performance tab (load time)

---

## Support

1. Check logs: Backend console + Browser console
2. Verify: API URL, environment variables
3. Test: Manual API call with curl/Postman
4. Review: Code in src/ directory

---

## Next Deployment

When ready to deploy:

```bash
# Local verification
npm run build
npm run preview

# Push to GitHub
git add .
git commit -m "Production ready"
git push origin main

# Netlify auto-deploys!
# Check deployment at netlify.com
```

---

**Last Updated:** February 3, 2026  
**Status:** ✅ Ready for Production  
**Next:** Deploy to Netlify! 🚀
