import React, { useState, useRef } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'
import { API_BASE_URL } from '../config/api'

export default function UploadCard(){
  const [dragOver, setDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')
  const inputRef = useRef(null)

  const onFile = async (file)=>{
    const form = new FormData()
    form.append('file', file)
    setError('')

    try{
      setUploading(true)
      setProgress(0)
      console.log('API_BASE_URL:', API_BASE_URL)
      console.log('Uploading file:', file.name)
      const token = localStorage.getItem('token')
      const headers = { 'Content-Type': 'multipart/form-data' }
      if(token) headers['Authorization'] = `Bearer ${token}`
      const res = await axios.post(`${API_BASE_URL}/api/predict`, form, {
        headers,
        onUploadProgress: (e)=>{
          setProgress(Math.round((e.loaded / e.total) * 100))
        }
      })
      // handle response - store or emit event
      console.log('prediction', res.data)
      // Minimal glue: expose latest uploaded image and prediction globally
      try{
        const previewUrl = URL.createObjectURL(file)
        // store globally for other components (non-invasive)
        window.latestUploadedImage = previewUrl
        window.dispatchEvent(new CustomEvent('mriUploaded', { detail: { url: previewUrl, fileName: file.name } }))
      }catch(e){ /* ignore */ }
      try{
        window.latestPrediction = res.data
        window.dispatchEvent(new CustomEvent('predictionUpdated', { detail: res.data }))
      }catch(e){ /* ignore */ }
      setUploading(false)
    }catch(err){
      console.error('Upload error:', err)
      setError(err.response?.data?.detail || err.message || 'Upload failed. Make sure backend is running on http://localhost:8000')
      setUploading(false)
    }
  }

  const handleDrop = (e)=>{
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if(file) onFile(file)
  }

  return (
    <motion.div 
      whileHover={{ y: -4, scale: 1.01 }} 
      className="p-6 rounded-2xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg border border-cyan-500/20 hover:border-cyan-500/40 shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300"
    >
      <h3 className="text-2xl font-semibold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">Upload MRI Scan</h3>
      <p className="text-sm text-slate-300">Drag & drop or click to upload a DICOM/JPEG/PNG MRI image</p>

      {error && (
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-3 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-sm"
        >
          ❌ {error}
        </motion.div>
      )}

      <div
        onDragOver={(e)=>{ e.preventDefault(); setDragOver(true)}}
        onDragLeave={()=>setDragOver(false)}
        onDrop={handleDrop}
        onClick={()=>inputRef.current.click()}
        className={`mt-4 h-40 rounded-lg flex items-center justify-center border-2 transition-all duration-300 cursor-pointer ${
          dragOver 
            ? 'border-cyan-400 bg-cyan-500/10 shadow-lg shadow-cyan-500/30 scale-105' 
            : 'border-cyan-500/20 bg-black/20 hover:border-cyan-500/40 hover:bg-cyan-500/5'
        }`}
      >
        <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={(e)=>onFile(e.target.files[0])} />
        {uploading ? (
          <div className="w-3/4">
            <div className="h-3 bg-[rgba(255,255,255,0.06)] rounded-full overflow-hidden border border-cyan-500/30">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 shadow-lg shadow-cyan-500/50"
              />
            </div>
            <p className="text-sm mt-2 text-cyan-300 text-center font-medium">Uploading... {progress}%</p>
          </div>
        ) : (
          <div className="text-slate-300 text-center">
            <motion.div
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              className="text-5xl mb-2"
            >
              📤
            </motion.div>
            <p className="text-lg font-medium text-cyan-300">Drop MRI here</p>
            <p className="text-sm mt-2 text-slate-400">or click to select a file</p>
          </div>
        )}
      </div>
    </motion.div>
  )
}
