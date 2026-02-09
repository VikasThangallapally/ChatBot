import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import { API_BASE_URL } from '../config/api'

export default function Register(){
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  const submit = async (e) =>{
    e.preventDefault()
    setError('')
    try{
      await axios.post(`${API_BASE_URL}/api/register`, { name, email, password })
      setMessage('Account created. Redirecting to login...')
      setTimeout(()=> navigate('/login'), 900)
    }catch(err){
      setError(err.response?.data?.detail || err.message || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#061018] text-white">
      <div className="w-full max-w-md p-8 rounded-xl bg-[rgba(255,255,255,0.03)]">
        <h2 className="text-2xl font-semibold mb-4">Register</h2>
        {message && <div className="mb-3 p-2 bg-green-600/20 text-green-200 rounded">{message}</div>}
        {error && <div className="mb-3 p-2 bg-red-600/20 text-red-200 rounded">{error}</div>}
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="text-sm text-slate-300">Name</label>
            <input value={name} onChange={(e)=>setName(e.target.value)} className="w-full mt-1 p-2 rounded bg-black/20" />
          </div>
          <div>
            <label className="text-sm text-slate-300">Email</label>
            <input value={email} onChange={(e)=>setEmail(e.target.value)} className="w-full mt-1 p-2 rounded bg-black/20" />
          </div>
          <div>
            <label className="text-sm text-slate-300">Password</label>
            <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} className="w-full mt-1 p-2 rounded bg-black/20" />
          </div>
          <div className="flex items-center justify-between">
            <button type="submit" className="px-4 py-2 bg-neon/10 border border-neon text-neon rounded-lg">Create account</button>
            <a href="/login" className="text-sm text-slate-300">Already have an account?</a>
          </div>
        </form>
      </div>
    </div>
  )
}
