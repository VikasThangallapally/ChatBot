import React, { useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { API_BASE_URL } from '../config/api'

export default function ChatBot(){
  const [messages, setMessages] = useState([
    { id: 1, from: 'bot', text: 'Hello! I can answer questions about Brain MRI and Brain Tumors. You can ask in English, Hindi, or Telugu.', lang: 'en' }
  ])
  const [text, setText] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('auto')
  const [isLoading, setIsLoading] = useState(false)

  const send = async () => {
    if(!text.trim()) return
    
    setIsLoading(true)
    const user = { id: Date.now(), from: 'user', text, lang: selectedLanguage }
    setMessages(prev => [...prev, user])
    setText('')

    try {
      // Build request payload
      const payload = { 
        message: text,
        language: selectedLanguage 
      }
      
      // Add MRI prediction context if available
      if(window.latestPrediction) {
        payload.prediction_label = window.latestPrediction.label
        payload.confidence_score = window.latestPrediction.confidence
      }

      const apiUrl = API_BASE_URL ? `${API_BASE_URL}/api/chat` : '/api/chat'
      const res = await axios.post(apiUrl, payload)
      
      const botResponse = res.data.response || 'No response received'
      const botLanguage = res.data.language || 'en'
      const source = res.data.source || 'unknown'
      const isUnrelated = res.data.is_unrelated || false
      
      // Add visual indicator for different response types
      let botMsg = botResponse
      if(source === 'domain_filter') {
        botMsg = `🚫 ${botResponse}`
      } else if(source === 'emergency') {
        botMsg = `🚨 URGENT: ${botResponse}`
      }
      
      setMessages(prev => [
        ...prev, 
        { 
          id: Date.now() + 1, 
          from: 'bot', 
          text: botMsg,
          lang: botLanguage,
          source: source
        }
      ])
    } catch (err) {
      console.error('Chat error:', err)
      const errorMsg = err.response?.data?.response || 'Sorry, the chat service is unavailable.'
      setMessages(prev => [
        ...prev, 
        { 
          id: Date.now() + 1, 
          from: 'bot', 
          text: errorMsg,
          lang: 'en',
          source: 'error'
        }
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <motion.div 
      initial={{ y: 20, opacity: 0 }} 
      animate={{ y: 0, opacity: 1 }} 
      transition={{ duration: 0.6 }} 
      className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)] h-[520px] flex flex-col"
    >
      {/* Header with Language Dropdown */}
      <div className="flex justify-between items-center mb-4">
        <h4 className="text-lg font-semibold">Brain MRI ChatBot</h4>
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Language:</label>
          <select 
            value={selectedLanguage} 
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="text-xs px-2 py-1 rounded bg-[rgba(255,255,255,0.05)] border border-[rgba(0,230,255,0.1)] text-white cursor-pointer"
          >
            <option value="auto">🔄 Auto Detect</option>
            <option value="en">🇬🇧 English</option>
            <option value="hi">🇮🇳 Hindi (हिंदी)</option>
            <option value="te">🇮🇳 Telugu (తెలుగు)</option>
          </select>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-auto space-y-3 py-2 mb-4">
        {messages.map(m => (
          <motion.div 
            key={m.id} 
            initial={{ scale: 0.98, opacity: 0 }} 
            animate={{ scale: 1, opacity: 1 }}
            className={`flex ${m.from === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-[75%] p-3 rounded-xl text-sm ${
                m.from === 'user' 
                  ? 'bg-neon/10 text-white border border-neon/30' 
                  : 'bg-[rgba(255,255,255,0.03)] text-slate-200 border border-[rgba(255,255,255,0.05)]'
              }`}
            >
              {/* Show language tag for bot messages */}
              {m.from === 'bot' && (
                <div className="text-xs text-slate-400 mb-1">
                  {m.lang === 'en' && '🇬🇧 English'}
                  {m.lang === 'hi' && '🇮🇳 हिंदी'}
                  {m.lang === 'te' && '🇮🇳 తెలుగు'}
                </div>
              )}
              <div>{m.text}</div>
              
              {/* Show source indicator for bot messages */}
              {m.from === 'bot' && m.source && (
                <div className="text-xs text-slate-500 mt-1 font-normal">
                  {m.source === 'llm' && 'AI Response'}
                  {m.source === 'domain_filter' && 'Domain Filter'}
                  {m.source === 'emergency' && 'Medical Alert'}
                  {m.source === 'fallback' && 'Fallback Response'}
                  {m.source === 'error' && 'Error'}
                </div>
              )}
            </div>
          </motion.div>
        ))}
        
        {/* Loading indicator */}
        {isLoading && (
          <motion.div 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-[rgba(255,255,255,0.03)] p-3 rounded-xl">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input Area */}
      <div className="mt-4 flex gap-3">
        <textarea 
          value={text} 
          onChange={(e) => setText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about Brain MRI or Brain Tumors..."
          rows="2"
          disabled={isLoading}
          className="flex-1 rounded-lg p-2 bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.03)] text-white resize-none disabled:opacity-50"
        />
        <button 
          onClick={send}
          disabled={isLoading || !text.trim()}
          className="px-4 py-2 bg-neon text-[#012024] rounded-lg font-medium hover:bg-neon/90 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Send...' : 'Send'}
        </button>
      </div>

      {/* Helper Text */}
      <div className="mt-3 text-xs text-slate-500">
        💡 Supports: English, Hindi, Telugu • Auto-detects language • Domain: Brain MRI only
      </div>
    </motion.div>
  )
}

