import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'
import { API_BASE_URL } from '../config/api'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const submit = async (e) =>{
    e.preventDefault()
    setError('')
    try{
      const res = await axios.post(`${API_BASE_URL}/api/login`, { email, password })
      const token = res.data.access_token
      if(token){
        localStorage.setItem('token', token)
      }
      setMessage('Login successful')
      // show message briefly then redirect
      setTimeout(()=> navigate('/prediction'), 700)
    }catch(err){
      setError(err.response?.data?.detail || err.message || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#061018] text-white relative overflow-hidden">
      {/* Animated background effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
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

      <div className="w-full max-w-md relative z-10">
        {/* Welcome Header */}
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent animate-gradient">
            WELCOME
          </h1>
          <h2 className="text-3xl font-semibold bg-gradient-to-r from-purple-400 via-pink-500 to-cyan-400 bg-clip-text text-transparent">
            NEURO ASSIST UI
          </h2>
          <div className="mt-2 h-1 w-32 mx-auto bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full"></div>
        </div>

        {/* Login Form with glow effect */}
        <div className="p-8 rounded-xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg shadow-2xl border border-cyan-500/20 hover:border-cyan-500/40 transition-all duration-300 hover:shadow-cyan-500/20">
          <h2 className="text-2xl font-semibold mb-6 text-center bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Login to Continue</h2>
          
          {message && (
            <div className="mb-3 p-3 bg-green-600/20 text-green-200 rounded-lg border border-green-500/30 animate-fade-in">
              {message}
            </div>
          )}
          {error && (
            <div className="mb-3 p-3 bg-red-600/20 text-red-200 rounded-lg border border-red-500/30 animate-fade-in">
              {error}
            </div>
          )}
          
          <form onSubmit={submit} className="space-y-5">
            <div className="space-y-2">
              <label className="text-sm text-slate-300 font-medium">Email</label>
              <input 
                value={email} 
                onChange={(e)=>setEmail(e.target.value)} 
                className="w-full p-3 rounded-lg bg-black/30 border border-cyan-500/20 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 transition-all duration-300" 
                placeholder="Enter your email"
                required
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm text-slate-300 font-medium">Password</label>
              <input 
                type="password" 
                value={password} 
                onChange={(e)=>setPassword(e.target.value)} 
                className="w-full p-3 rounded-lg bg-black/30 border border-cyan-500/20 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 transition-all duration-300" 
                placeholder="Enter your password"
                required
              />
            </div>
            
            <button 
              type="submit" 
              className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/50"
            >
              Login
            </button>
            
            <div className="flex items-center justify-between pt-2">
              <Link to="/register" className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors duration-300">
                Create account →
              </Link>
              <Link to="/forgot-password" className="text-sm text-purple-400 hover:text-purple-300 transition-colors duration-300">
                Forgot password?
              </Link>
            </div>
          </form>
        </div>
      </div>

      <style jsx>{`
        @keyframes gradient {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
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
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
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
