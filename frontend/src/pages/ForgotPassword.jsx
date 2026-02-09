import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#061018] via-[#0a1929] to-[#061018] text-white">
      <div className="w-full max-w-md p-8 rounded-xl bg-[rgba(255,255,255,0.03)] backdrop-blur-sm border border-[rgba(255,255,255,0.1)]">
        
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
                <a href="/login" className="text-cyan-400 hover:text-cyan-300 font-semibold">
                  Back to Login
                </a>
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
    </div>
  )
}
