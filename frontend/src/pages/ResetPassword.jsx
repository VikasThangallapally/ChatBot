import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'
import { API_BASE_URL } from '../config/api'

export default function ResetPassword() {
  const [email, setEmail] = useState('')
  const [otpCode, setOtpCode] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    // Auto-redirect to forgot password if no email
    setTimeout(() => {
      if (!email) {
        // Show a message but don't force redirect immediately
      }
    }, 500)
  }, [email])

  const handleResetPassword = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // Validate inputs
    if (!email || !otpCode || !newPassword || !confirmPassword) {
      setError('Please fill in all fields')
      return
    }

    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters long')
      return
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (otpCode.length !== 6 || !/^\d+$/.test(otpCode)) {
      setError('OTP must be 6 digits')
      return
    }

    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/reset-password`, {
        email,
        otp_code: otpCode,
        new_password: newPassword
      })

      setSuccess(response.data.message || 'Password has been reset successfully!')
      
      // Redirect to login after 2 seconds
      setTimeout(() => {
        navigate('/login')
      }, 2000)

    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to reset password')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#061018] text-white relative overflow-hidden">
      {/* Animated background effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Animated grid background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-blue-500/10 animate-gradient-shift"></div>
          <div className="absolute inset-0" style={{
            backgroundImage: 'linear-gradient(rgba(6, 182, 212, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(6, 182, 212, 0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px',
            animation: 'grid-flow 20s linear infinite'
          }}></div>
        </div>

        {/* Gradient orbs with smooth floating animation */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-float" style={{animationDuration: '9s', animationDelay: '0s'}}></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-float" style={{animationDuration: '11s', animationDelay: '2s'}}></div>
        <div className="absolute top-1/3 left-1/3 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-float" style={{animationDuration: '10s', animationDelay: '4s'}}></div>
        
        {/* Floating particles with glow */}
        <div className="absolute top-32 right-20 w-3 h-3 bg-cyan-400 rounded-full animate-float-particle shadow-lg shadow-cyan-400/50" style={{animationDuration: '7s'}}></div>
        <div className="absolute top-48 left-32 w-4 h-4 bg-blue-400 rounded-full animate-float-particle shadow-lg shadow-blue-400/50" style={{animationDuration: '9s', animationDelay: '1s'}}></div>
        <div className="absolute bottom-40 right-40 w-3 h-3 bg-indigo-400 rounded-full animate-float-particle shadow-lg shadow-indigo-400/50" style={{animationDuration: '8s', animationDelay: '2s'}}></div>
        
        {/* Rotating rings */}
        <div className="absolute top-1/4 right-1/4 w-64 h-64 border border-cyan-500/10 rounded-full animate-spin-slow"></div>
        <div className="absolute bottom-1/4 left-1/4 w-80 h-80 border border-blue-500/10 rounded-full animate-spin-reverse"></div>
      </div>

      <div className="w-full max-w-md p-8 rounded-xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg shadow-2xl border border-cyan-500/20 hover:border-cyan-500/40 transition-all duration-300 relative z-10">
        
        <h2 className="text-3xl font-bold mb-2 text-center bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Reset Password</h2>
        <p className="text-slate-400 text-center mb-6 text-sm">Enter your OTP and new password</p>

        {error && (
          <div className="mb-4 p-3 bg-red-600/20 border border-red-500/50 text-red-200 rounded-lg text-sm">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-600/20 border border-green-500/50 text-green-200 rounded-lg text-sm flex items-center gap-2">
            <span className="text-xl">✅</span>
            {success}
          </div>
        )}

        <form onSubmit={handleResetPassword} className="space-y-4">
          
          <div>
            <label className="text-sm text-slate-300 block mb-2">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
              className="w-full p-3 rounded-lg bg-black/30 border border-slate-600 focus:border-cyan-500 outline-none transition text-white placeholder-slate-500"
            />
            <p className="mt-2 text-xs text-slate-500">The email where you received the OTP</p>
          </div>

          <div>
            <label className="text-sm text-slate-300 block mb-2">OTP Code (6 digits)</label>
            <input
              type="text"
              value={otpCode}
              onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              maxLength="6"
              required
              className="w-full p-3 rounded-lg bg-black/30 border border-slate-600 focus:border-cyan-500 outline-none transition text-white placeholder-slate-500 text-center font-mono text-lg tracking-widest"
            />
          </div>

          <div>
            <label className="text-sm text-slate-300 block mb-2">New Password</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="At least 8 characters"
                required
                className="w-full p-3 rounded-lg bg-black/30 border border-slate-600 focus:border-cyan-500 outline-none transition text-white placeholder-slate-500 pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            <p className="mt-2 text-xs text-slate-500">Must be at least 8 characters</p>
          </div>

          <div>
            <label className="text-sm text-slate-300 block mb-2">Confirm Password</label>
            <div className="relative">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                required
                className="w-full p-3 rounded-lg bg-black/30 border border-slate-600 focus:border-cyan-500 outline-none transition text-white placeholder-slate-500 pr-10"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
              >
                {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || success}
            className="w-full p-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-semibold transition text-white"
          >
            {loading ? '⏳ Resetting Password...' : success ? '✅ Password Reset!' : 'Reset Password'}
          </button>

        </form>

        <div className="mt-6 text-center">
          <p className="text-slate-400 text-sm">
            Didn't receive an OTP?{' '}
            <Link to="/forgot-password" className="text-cyan-400 hover:text-cyan-300 font-semibold">
              Request another one
            </Link>
          </p>
        </div>

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
