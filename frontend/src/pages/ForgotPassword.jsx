import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'
import { API_BASE_URL } from '../config/api'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [showOtpStep, setShowOtpStep] = useState(false)
  const navigate = useNavigate()

  const handleRequestOTP = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/forgot-password`, { email })
      setSuccess(response.data.message || 'OTP has been sent to your email')
      setShowOtpStep(true)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to request OTP')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#061018] text-white relative overflow-hidden">
      {/* Animated background effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Animated grid background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-transparent to-cyan-500/10 animate-gradient-shift"></div>
          <div className="absolute inset-0" style={{
            backgroundImage: 'linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px',
            animation: 'grid-flow 20s linear infinite'
          }}></div>
        </div>

        {/* Gradient orbs with smooth floating animation */}
        <div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-float" style={{animationDuration: '8s', animationDelay: '0s'}}></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-float" style={{animationDuration: '10s', animationDelay: '2s'}}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-float" style={{animationDuration: '12s', animationDelay: '4s'}}></div>
        
        {/* Floating particles with glow */}
        <div className="absolute top-20 left-20 w-3 h-3 bg-blue-400 rounded-full animate-float-particle shadow-lg shadow-blue-400/50" style={{animationDuration: '6s'}}></div>
        <div className="absolute top-40 right-32 w-4 h-4 bg-cyan-400 rounded-full animate-float-particle shadow-lg shadow-cyan-400/50" style={{animationDuration: '8s', animationDelay: '1s'}}></div>
        <div className="absolute bottom-32 left-40 w-3 h-3 bg-indigo-400 rounded-full animate-float-particle shadow-lg shadow-indigo-400/50" style={{animationDuration: '7s', animationDelay: '2s'}}></div>
        
        {/* Rotating rings */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 border border-blue-500/10 rounded-full animate-spin-slow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 border border-cyan-500/10 rounded-full animate-spin-reverse"></div>
      </div>

      <div className="w-full max-w-md p-8 rounded-xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg shadow-2xl border border-blue-500/20 hover:border-blue-500/40 transition-all duration-300 relative z-10">
        
        {!showOtpStep ? (
          <>
            <h2 className="text-3xl font-bold mb-2 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Forgot Password?</h2>
            <p className="text-slate-400 text-center mb-6 text-sm">Enter your email to receive a password reset OTP</p>

            {error && (
              <div className="mb-4 p-3 bg-red-600/20 border border-red-500/50 text-red-200 rounded-lg text-sm">
                {error}
              </div>
            )}

            {success && (
              <div className="mb-4 p-3 bg-green-600/20 border border-green-500/50 text-green-200 rounded-lg text-sm">
                {success}
              </div>
            )}

            <form onSubmit={handleRequestOTP} className="space-y-4">
              <div>
                <label className="text-sm text-slate-300 block mb-2">Email Address</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full p-3 rounded-lg bg-black/30 border border-slate-600 focus:border-cyan-500 outline-none transition text-white placeholder-slate-500"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full p-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-semibold transition text-white"
              >
                {loading ? 'Sending OTP...' : 'Send OTP'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-slate-400 text-sm">
                Remember your password?{' '}
                <Link to="/login" className="text-cyan-400 hover:text-cyan-300 font-semibold">
                  Back to Login
                </Link>
              </p>
            </div>
          </>
        ) : (
          <>
            <h2 className="text-3xl font-bold mb-2 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Check Your Email</h2>
            <p className="text-slate-400 text-center mb-6 text-sm">We've sent a password reset OTP to {email}</p>

            <div className="mb-6 p-4 bg-blue-600/10 border border-blue-500/30 rounded-lg">
              <p className="text-blue-300 text-sm">
                <strong>⏰ OTP expires in 10 minutes.</strong> Check your spam folder if you don't see the email.
              </p>
            </div>

            <button
              onClick={() => navigate('/reset-password')}
              className="w-full p-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 rounded-lg font-semibold transition text-white"
            >
              Got OTP? Continue to Reset Password
            </button>

            <button
              onClick={() => {
                setShowOtpStep(false)
                setSuccess('')
                setEmail('')
              }}
              className="w-full mt-3 p-3 border border-slate-600 hover:border-slate-500 rounded-lg font-semibold transition text-slate-300 hover:text-white"
            >
              Try Another Email
            </button>
          </>
        )}

      </div>

      <style jsx>{`
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
        .animate-float {
          animation: float 8s ease-in-out infinite;
        }
        .animate-float-particle {
          animation: float-particle 6s ease-in-out infinite;
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
