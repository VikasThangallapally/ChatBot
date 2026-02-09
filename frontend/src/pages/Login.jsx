import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
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
    <div className="min-h-screen flex items-center justify-center bg-[#061018] text-white">
      <div className="w-full max-w-md p-8 rounded-xl bg-[rgba(255,255,255,0.03)]">
        <h2 className="text-2xl font-semibold mb-4">Login</h2>
        {message && <div className="mb-3 p-2 bg-green-600/20 text-green-200 rounded">{message}</div>}
        {error && <div className="mb-3 p-2 bg-red-600/20 text-red-200 rounded">{error}</div>}
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="text-sm text-slate-300">Email</label>
            <input value={email} onChange={(e)=>setEmail(e.target.value)} className="w-full mt-1 p-2 rounded bg-black/20" />
          </div>
          <div>
            <label className="text-sm text-slate-300">Password</label>
            <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} className="w-full mt-1 p-2 rounded bg-black/20" />
          </div>
          <div className="flex items-center justify-between">
            <button type="submit" className="px-4 py-2 bg-neon/10 border border-neon text-neon rounded-lg">Login</button>
            <a href="/register" className="text-sm text-slate-300">Create account</a>
          </div>
          <div className="text-center">
            <a href="/forgot-password" className="text-sm text-cyan-400 hover:text-cyan-300">Forgot password?</a>
          </div>
        </form>
      </div>
    </div>
  )
}
