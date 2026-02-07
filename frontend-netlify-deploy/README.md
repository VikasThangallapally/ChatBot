# Brain Tumor AI Assistant - Frontend Deployment

This is the standalone frontend folder ready for **direct Netlify deployment**.

## 📁 Structure

```
frontend-netlify-deploy/
├── src/                    # React source code
│   ├── components/         # React components
│   ├── config/            # Configuration files
│   └── styles/            # CSS styles
├── package.json           # Dependencies
├── index.html             # HTML entry point
├── vite.config.js         # Vite build config
├── tailwind.config.cjs    # Tailwind CSS config
├── postcss.config.cjs     # PostCSS config
├── netlify.toml           # Netlify deployment config
└── .env.example           # Environment variables template
```

## 🚀 Deploy to Netlify

### Option 1: Drag & Drop (Easiest)
1. Build locally: `npm run build`
2. Go to [Netlify](https://app.netlify.com)
3. Drag `dist` folder to deploy

### Option 2: Git & Netlify CI/CD (Recommended)
1. Upload this folder to your GitHub repo
2. In Netlify Dashboard:
   - **Base directory:** (leave empty or set to folder path)
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
3. Add environment variable:
   - `VITE_API_BASE_URL=https://your-backend-api.com`
4. Deploy!

## 🔧 Configuration

### Environment Variables
Copy `.env.example` → `.env.local` and update:
```
VITE_API_BASE_URL=https://your-backend-api.com
VITE_ENVIRONMENT=production
```

### Netlify Configuration
File: `netlify.toml`
- Build: `npm run build`
- Publish: `dist`
- Node version: `18`

## 📦 Installation & Build

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview build
npm run preview
```

## ✅ Deployment Checklist

- [ ] Copy folder to GitHub
- [ ] Set backend API URL (VITE_API_BASE_URL)
- [ ] Connect GitHub to Netlify
- [ ] Set build settings
- [ ] Deploy

## 🔗 Backend Integration

Make sure your backend API is deployed and running:
- Render: https://brain-tumor-api.onrender.com
- Or your custom API URL

Update `VITE_API_BASE_URL` in Netlify environment variables.

## 📱 Features

- ✅ Brain MRI image upload
- ✅ Real-time predictions
- ✅ Medical analysis panel
- ✅ GPT-powered chatbot
- ✅ Responsive design
- ✅ Production optimized (322 KB gzipped)

## 📞 Support

For issues, check:
1. `VITE_API_BASE_URL` is set correctly
2. Backend API is running
3. Check browser console for errors
4. Netlify logs for build errors

---

**Ready to deploy? Push this folder to your GitHub repo and connect to Netlify!** 🎯
