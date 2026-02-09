import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import { motion, AnimatePresence } from 'framer-motion'
import Brain3D from './components/Brain3D'
import UploadCard from './components/UploadCard'
import ResultPanel from './components/ResultPanel'
import MedicalAnalysis from './components/MedicalAnalysis'
import FloatingChatbot from './components/FloatingChatbot'

function PredictionPage(){
  const [predictionResult, setPredictionResult] = useState(null)
  const [uploadedImage, setUploadedImage] = useState(null)

  useEffect(() => {
    // Listen for prediction updates from UploadCard
    const handlePredictionUpdate = (e) => {
      setPredictionResult(e.detail)
    }

    // Listen for MRI upload
    const handleMriUploaded = (e) => {
      setUploadedImage(e.detail)
    }

    window.addEventListener('predictionUpdated', handlePredictionUpdate)
    window.addEventListener('mriUploaded', handleMriUploaded)
    
    return () => {
      window.removeEventListener('predictionUpdated', handlePredictionUpdate)
      window.removeEventListener('mriUploaded', handleMriUploaded)
    }
  }, [])

  return (
    <div className="min-h-screen bg-[#061018] text-white antialiased">
      <header className="container mx-auto p-6 flex items-center justify-between sticky top-0 z-30 bg-[#061018]/80 backdrop-blur-sm">
        <div>
          <h1 className="text-2xl font-semibold">Brain Tumor AI Assistant</h1>
          <p className="text-sm text-slate-300">AI-assisted MRI analysis & medical guidance</p>
        </div>
        <nav className="flex items-center gap-4">
          <button className="px-4 py-2 bg-neon/10 border border-neon text-neon rounded-lg hover:bg-neon/20 transition-colors">Upload MRI Scan</button>
          <button onClick={()=> { localStorage.removeItem('token'); window.location.href='/login' }} className="px-4 py-2 bg-red-600/20 border border-red-600 text-red-300 rounded-lg hover:bg-red-600/30 transition-colors text-sm">Logout</button>
        </nav>
      </header>

      {/* Hero Section - Conditional Content */}
      <section className="container mx-auto px-6 py-12 grid grid-cols-2 gap-8 items-center min-h-[600px]">
        {/* Left Column - Upload Card (Always Visible) */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6"
        >
          <h2 className="text-4xl font-bold leading-tight">Brain Tumor AI Assistant</h2>
          <p className="text-lg text-slate-300 leading-relaxed">Upload your MRI scan for AI-assisted analysis and personalized medical guidance.</p>
          <UploadCard />
        </motion.div>

        {/* Right Column - Conditional: Earth or MRI Preview */}
        <AnimatePresence mode="wait">
          {!uploadedImage ? (
            // Before Upload: Show Earth Animation
            <motion.div
              key="earth-animation"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.8 }}
              className="w-full h-[520px] rounded-xl bg-gradient-to-br from-[#071021] to-[#091428] p-4 shadow-lg"
              style={{
                boxShadow: '0 0 30px rgba(0, 230, 255, 0.1)'
              }}
            >
              <Brain3D />
            </motion.div>
          ) : (
            // After Upload: Show MRI Preview
            <motion.div
              key="mri-preview"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.5 }}
              className="w-full h-[520px] rounded-xl bg-gradient-to-br from-[#071021] to-[#091428] p-4 shadow-lg flex items-center justify-center overflow-hidden"
              style={{
                boxShadow: '0 0 30px rgba(0, 230, 255, 0.15)'
              }}
            >
              <div className="w-full h-full flex items-center justify-center bg-black/20 rounded-lg">
                <img
                  src={uploadedImage.url}
                  alt="Uploaded MRI"
                  className="max-w-full max-h-full object-contain rounded-lg"
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </section>

      {/* Results Section - Only shows after valid prediction */}
      {predictionResult && (
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="container mx-auto px-6 py-8 grid grid-cols-3 gap-6"
        >
          <ResultPanel result={predictionResult} />
          <MedicalAnalysis result={predictionResult} />
        </motion.section>
      )}

      <FloatingChatbot />

      <footer className="text-center py-8 text-sm text-slate-400">
        For educational and research purposes only. Not a medical diagnosis.
      </footer>
    </div>
  )
}

function ProtectedRoute({ element }) {
  const token = localStorage.getItem('token')
  return token ? element : <Navigate to="/login" replace />
}

export default function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/prediction" element={<ProtectedRoute element={<PredictionPage />} />} />
        <Route path="/" element={<Navigate to={localStorage.getItem('token') ? '/prediction' : '/login'} replace />} />
      </Routes>
    </BrowserRouter>
  )
}

