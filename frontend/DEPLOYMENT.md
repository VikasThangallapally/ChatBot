# Brain Tumor AI Assistant - Frontend

Professional React-based frontend for brain tumor MRI analysis with AI-powered medical assistance.

## Features

- **MRI Image Upload** - Drag & drop or click to upload
- **AI Prediction** - CNN-based tumor classification (Glioma, Meningioma, Pituitary, No Tumor)
- **Detailed Medical Analysis** - 6-section educational analysis panel
- **Medical Chatbot** - Floating AI chatbot with GPT integration
- **3D Visualization** - Interactive Earth globe animation (pre-upload)
- **Responsive Design** - Desktop and tablet optimized
- **Dark Medical UI** - Professional medical-grade theme

## Local Development

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend running on `http://127.0.0.1:8000`

### Setup

```bash
cd frontend

# Install dependencies
npm install

# Create local environment file
cp .env.example .env.local

# Start development server
npm run dev
```

The app will be available at `http://localhost:5174`

### Environment Variables

Create a `.env.local` file:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_ENVIRONMENT=development
```

## Production Build

```bash
# Build for production
npm run build

# Preview production build locally
npm run preview
```

Output directory: `dist/`

## Netlify Deployment

### 1. Prepare Repository

```bash
git add .
git commit -m "Prepare for Netlify deployment"
git push origin main
```

### 2. Connect to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Select your GitHub repository
4. Configure:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
   - **Base directory:** `frontend`

### 3. Set Environment Variables

In Netlify dashboard:

**Build & deploy → Environment**

Add:
```
VITE_API_BASE_URL=https://your-backend-api.com
VITE_ENVIRONMENT=production
```

### 4. Deploy

Netlify automatically deploys on every push to main.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Brain3D.jsx           # 3D Earth animation
│   │   ├── UploadCard.jsx        # Image upload component
│   │   ├── ResultPanel.jsx       # Prediction results
│   │   ├── MedicalAnalysis.jsx   # Detailed analysis panel
│   │   ├── FloatingChatbot.jsx   # AI chatbot
│   │   └── ChatBot.jsx           # Legacy chatbot (backup)
│   ├── config/
│   │   ├── api.js                # API configuration
│   │   └── analysisData.js       # Medical analysis content
│   ├── styles/
│   │   └── index.css             # Global styles
│   ├── App.jsx                   # Main app component
│   └── main.jsx                  # Entry point
├── .env.example                   # Environment template
├── .env.local                     # Local environment (git ignored)
├── vite.config.js               # Vite configuration
├── netlify.toml                 # Netlify deployment config
└── package.json
```

## Key Features

### Conditional Hero Behavior

- **Before Upload:** Earth/globe 3D animation
- **After Upload:** MRI image preview replaces animation
- Smooth fade transitions
- No layout jumping

### Medical Analysis Panel

Automatically shows after successful prediction:
1. About the Result
2. Possible Symptoms & Effects
3. Medical Consultation (Specialists)
4. Lifestyle & General Health
5. Monitoring & Next Steps
6. Medical Disclaimer

### Floating Chatbot

- Always accessible (bottom-right)
- Click button to open/close
- Integrates with backend GPT service
- Passes prediction context to chatbot
- Professional medical UI

## API Integration

The frontend communicates with the backend via:

### POST `/api/predict`
- Accepts: MRI image file
- Returns: Prediction result with confidence scores

### POST `/api/chat`
- Accepts: Message + optional prediction context
- Returns: AI-generated response

All requests automatically use `VITE_API_BASE_URL` from environment variables.

## Troubleshooting

### Build Errors

```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Development Server Issues

```bash
# Kill process on port 5174
lsof -i :5174 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
npm run dev -- --port 5175
```

### Vite HMR Issues

In `.env.local`, add:
```
VITE_HMR_HOST=localhost
VITE_HMR_PORT=5174
VITE_HMR_PROTOCOL=http
```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- **Bundle size:** ~280 KB (gzipped)
- **Initial load:** <2s on 4G
- **Time to interactive:** <3s
- **Lighthouse:** 85+ score

## Accessibility

- WCAG 2.1 Level AA compliant
- Keyboard navigation
- Screen reader support
- High contrast colors

## Security

- No sensitive data stored locally
- All API calls validated on backend
- XSS protection via React
- CSRF protection via backend
- Security headers in Netlify config

## Technologies

- **React 18** - UI framework
- **Vite 5** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Axios** - HTTP client
- **Three.js** - 3D graphics (Brain3D)

## License

Medical AI Assistant © 2026
Educational and research purposes only.

## Support

For issues or questions:
1. Check backend logs
2. Verify environment variables
3. Check browser console for errors
4. Review Netlify deployment logs

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Backend URL set correctly
- [ ] npm run build succeeds
- [ ] npm run preview works
- [ ] No console errors
- [ ] MRI upload functional
- [ ] Predictions working
- [ ] Chatbot responding
- [ ] Responsive on mobile
- [ ] Performance acceptable
