import React, { useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'

export default function ChatBot(){
  const [messages, setMessages] = useState([
    { id: 1, from: 'bot', text: 'Hello, I am your assistant. Upload an MRI to begin.' }
  ])
  const [text, setText] = useState('')

  const send = async ()=>{
    if(!text.trim()) return
    const user = { id: Date.now(), from: 'user', text }
    setMessages(prev=>[...prev, user])
    setText('')

    try{
      // Send user message along with latest prediction (if any)
      const payload = { message: text }
      if(window.latestPrediction) payload.prediction = window.latestPrediction
      const res = await axios.post('/api/chat', payload)
      const botMsg = res.data.response || res.data
      setMessages(prev=>[...prev, { id: Date.now()+1, from: 'bot', text: botMsg }])
    }catch(err){
      setMessages(prev=>[...prev, { id: Date.now()+1, from: 'bot', text: 'Sorry, the chat service is unavailable.' }])
    }
  }

  return (
    <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.6 }} className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)] h-[420px] flex flex-col">
      <h4 className="text-lg font-semibold mb-4">Doctor-Bot</h4>
      <div className="flex-1 overflow-auto space-y-3 py-2">
        {messages.map(m=> (
          <div key={m.id} className={`flex ${m.from==='user' ? 'justify-end' : 'justify-start'}`}>
            <motion.div initial={{ scale: 0.98 }} animate={{ scale: 1 }} className={`max-w-[70%] p-3 rounded-xl ${m.from==='user' ? 'bg-neon/6 text-white' : 'bg-[rgba(255,255,255,0.03)] text-slate-200'}`}>
              <div className="text-sm">{m.text}</div>
            </motion.div>
          </div>
        ))}
      </div>

      <div className="mt-4 flex gap-3">
        <input value={text} onChange={e=>setText(e.target.value)} placeholder="Ask a question..." className="flex-1 rounded-lg p-2 bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.03)]" />
        <button onClick={send} className="px-4 py-2 bg-neon text-[#012024] rounded-lg">Send</button>
      </div>
    </motion.div>
  )
}
