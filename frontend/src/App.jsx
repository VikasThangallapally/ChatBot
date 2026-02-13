import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import Logout from './pages/Logout'
import { motion, AnimatePresence } from 'framer-motion'
import Brain3D from './components/Brain3D'
import UploadCard from './components/UploadCard'
import ResultPanel from './components/ResultPanel'
import MedicalAnalysis from './components/MedicalAnalysis'
import FloatingChatbot from './components/FloatingChatbot'

function PredictionPage(){
  const navigate = useNavigate()
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
    <div className="min-h-screen bg-[#061018] text-white antialiased relative overflow-hidden">
      {/* Animated background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        {/* Animated grid background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-purple-500/10 animate-gradient-shift"></div>
          <div className="absolute inset-0" style={{
            backgroundImage: 'linear-gradient(rgba(6, 182, 212, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(6, 182, 212, 0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px',
            animation: 'grid-flow 20s linear infinite'
          }}></div>
        </div>

        {/* Gradient orbs with smooth floating animation */}
        <div className="absolute top-0 left-0 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-float" style={{animationDuration: '8s', animationDelay: '0s'}}></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-float" style={{animationDuration: '10s', animationDelay: '2s'}}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-float" style={{animationDuration: '12s', animationDelay: '4s'}}></div>
        
        {/* Animated waves */}
        <div className="absolute bottom-0 left-0 right-0 h-64 opacity-30">
          <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-cyan-500/20 to-transparent animate-wave" style={{animationDelay: '0s'}}></div>
          <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-blue-500/20 to-transparent animate-wave" style={{animationDelay: '1s'}}></div>
        </div>

        {/* Floating particles with glow */}
        <div className="absolute top-20 left-20 w-3 h-3 bg-cyan-400 rounded-full animate-float-particle shadow-lg shadow-cyan-400/50" style={{animationDuration: '6s'}}></div>
        <div className="absolute top-40 right-32 w-4 h-4 bg-purple-400 rounded-full animate-float-particle shadow-lg shadow-purple-400/50" style={{animationDuration: '8s', animationDelay: '1s'}}></div>
        <div className="absolute bottom-32 left-40 w-3 h-3 bg-blue-400 rounded-full animate-float-particle shadow-lg shadow-blue-400/50" style={{animationDuration: '7s', animationDelay: '2s'}}></div>
        <div className="absolute top-60 left-1/3 w-2 h-2 bg-cyan-300 rounded-full animate-float-particle shadow-lg shadow-cyan-300/50" style={{animationDuration: '9s', animationDelay: '0.5s'}}></div>
        <div className="absolute top-1/3 right-1/4 w-3 h-3 bg-purple-300 rounded-full animate-float-particle shadow-lg shadow-purple-300/50" style={{animationDuration: '10s', animationDelay: '3s'}}></div>
        
        {/* Rotating rings */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 border border-cyan-500/10 rounded-full animate-spin-slow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 border border-purple-500/10 rounded-full animate-spin-reverse"></div>
      </div>

      <header className="container mx-auto p-6 flex items-center justify-between sticky top-0 z-30 bg-[#061018]/80 backdrop-blur-sm relative">
        <div>
          <h1 className="text-2xl font-semibold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Brain Tumor AI Assistant</h1>
          <p className="text-sm text-slate-300">AI-assisted MRI analysis & medical guidance</p>
        </div>
        <nav className="flex items-center gap-4">
          <button className="px-4 py-2 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/50 text-cyan-300 rounded-lg hover:bg-cyan-500/20 hover:border-cyan-400 transition-all duration-300 transform hover:scale-105">Upload MRI Scan</button>
          <button onClick={() => navigate('/logout')} className="px-4 py-2 bg-red-600/20 border border-red-600 text-red-300 rounded-lg hover:bg-red-600/30 transition-all duration-300 transform hover:scale-105 text-sm">Logout</button>
        </nav>
      </header>

      {/* Hero Section - Conditional Content */}
      <section className="container mx-auto px-6 py-12 grid grid-cols-2 gap-8 items-center min-h-[600px] relative z-10">
        {/* Left Column - Upload Card (Always Visible) */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6"
        >
          <div className="mb-8">
            <h2 className="text-5xl font-bold leading-tight mb-4 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent animate-gradient" style={{backgroundSize: '200% 200%'}}>Brain Tumor AI Assistant</h2>
            <p className="text-lg text-slate-300 leading-relaxed">Upload your MRI scan for AI-assisted analysis and personalized medical guidance.</p>
          </div>
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

      {/* Results Section - Shows for ALL predictions (valid or invalid) */}
      {predictionResult && (
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="container mx-auto px-6 py-8 grid grid-cols-3 gap-6 relative z-10"
        >
          <ResultPanel result={predictionResult} />
          {/* Only show medical analysis for valid, successful predictions */}
          {predictionResult?.status === 'success' && predictionResult?.is_valid_brain_image && predictionResult?.medical_analysis && (
            <MedicalAnalysis result={predictionResult} />
          )}
        </motion.section>
      )}

      <FloatingChatbot />

      <footer className="text-center py-8 text-sm text-slate-400 relative z-10">
        For educational and research purposes only. Not a medical diagnosis.
      </footer>

      {/* Background Animation Styles */}
      <style>{`
        @keyframes gradient {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        @keyframes float {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -30px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        @keyframes float-particle {
          0%, 100% { transform: translate(0, 0); opacity: 1; }
          25% { transform: translate(20px, -40px); opacity: 0.8; }
          50% { transform: translate(-30px, -80px); opacity: 0.6; }
          75% { transform: translate(40px, -40px); opacity: 0.8; }
        }
        @keyframes wave {
          0%, 100% { transform: translateX(0) translateY(0); }
          50% { transform: translateX(-25px) translateY(-10px); }
        }
        @keyframes grid-flow {
          0% { transform: translate(0, 0); }
          100% { transform: translate(50px, 50px); }
        }
        @keyframes gradient-shift {
          0%, 100% { transform: rotate(0deg) scale(1); opacity: 1; }
          50% { transform: rotate(180deg) scale(1.2); opacity: 0.8; }
        }
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes spin-reverse {
          from { transform: rotate(360deg); }
          to { transform: rotate(0deg); }
        }
        .animate-gradient {
          animation: gradient 3s ease infinite;
        }
        .animate-float {
          animation: float 8s ease-in-out infinite;
        }
        .animate-float-particle {
          animation: float-particle 6s ease-in-out infinite;
        }
        .animate-wave {
          animation: wave 8s ease-in-out infinite;
        }
        .animate-gradient-shift {
          animation: gradient-shift 15s ease-in-out infinite;
        }
        .animate-spin-slow {
          animation: spin-slow 30s linear infinite;
        }
        .animate-spin-reverse {
          animation: spin-reverse 25s linear infinite;
        }
      `}</style>
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
        <Route path="/logout" element={<Logout />} />
        <Route path="/prediction" element={<ProtectedRoute element={<PredictionPage />} />} />
        <Route path="/" element={<Navigate to={localStorage.getItem('token') ? '/prediction' : '/login'} replace />} />
      </Routes>
    </BrowserRouter>
  )
}

