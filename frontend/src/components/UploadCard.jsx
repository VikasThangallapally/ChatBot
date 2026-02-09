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
    <motion.div whileHover={{ y: -4 }} className={`p-6 rounded-2xl bg-[rgba(255,255,255,0.03)] border border-[rgba(0,230,255,0.08)] shadow-neon`}>
      <h3 className="text-xl font-semibold">Upload MRI Scan</h3>
      <p className="text-sm text-slate-300">Drag & drop or click to upload a DICOM/JPEG/PNG MRI image</p>

      {error && (
        <div className="mt-3 p-3 bg-red-500/20 border border-red-500/50 rounded text-red-200 text-sm">
          ❌ {error}
        </div>
      )}

      <div
        onDragOver={(e)=>{ e.preventDefault(); setDragOver(true)}}
        onDragLeave={()=>setDragOver(false)}
        onDrop={handleDrop}
        onClick={()=>inputRef.current.click()}
        className={`mt-4 h-40 rounded-lg flex items-center justify-center border-2 ${dragOver? 'border-neon/60 bg-[rgba(0,230,255,0.02)]' : 'border-[rgba(255,255,255,0.04)]'} cursor-pointer`}
      >
        <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={(e)=>onFile(e.target.files[0])} />
        {uploading ? (
          <div className="w-3/4">
            <div className="h-3 bg-[rgba(255,255,255,0.06)] rounded-full overflow-hidden">
              <div style={{width: `${progress}%`}} className={`h-full bg-neon`} />
            </div>
            <p className="text-sm mt-2">Uploading... {progress}%</p>
          </div>
        ) : (
          <div className="text-slate-300 text-center">
            <p className="text-lg">Drop MRI here</p>
            <p className="text-sm mt-2">or click to select a file</p>
          </div>
        )}
      </div>
    </motion.div>
  )
}
