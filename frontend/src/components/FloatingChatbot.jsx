import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { API_BASE_URL } from '../config/api'

export default function FloatingChatbot() {
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [messages, setMessages] = useState([
    { id: 1, from: 'bot', text: 'Hello! I\'m your medical AI assistant. How can I help you today?' }
  ])
  const [text, setText] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const send = async () => {
    if (!text.trim()) return

    const userMsg = { id: Date.now(), from: 'user', text }
    setMessages(prev => [...prev, userMsg])
    setText('')
    setIsLoading(true)

    try {
      const payload = { message: text }
      if (window.latestPrediction) {
        payload.prediction_label = window.latestPrediction.label
        payload.confidence_score = window.latestPrediction.confidence
      }
      
      const res = await axios.post(`${API_BASE_URL}/api/chat`, payload)
      const botMsg = {
        id: Date.now() + 1,
        from: 'bot',
        text: res.data.response || res.data
      }
      setMessages(prev => [...prev, botMsg])
    } catch (err) {
      const errorMsg = {
        id: Date.now() + 1,
        from: 'bot',
        text: 'Sorry, I\'m temporarily unavailable. Please try again.'
      }
      setMessages(prev => [...prev, errorMsg])
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
    <>
      {/* Floating Button */}
      <motion.button
        onClick={() => setIsChatOpen(!isChatOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        className="fixed bottom-8 right-8 z-40 w-14 h-14 rounded-full bg-gradient-to-br from-neon to-cyan-500 text-[#012024] flex items-center justify-center font-bold text-xl shadow-lg hover:shadow-neon/50"
        style={{
          boxShadow: '0 0 30px rgba(0, 230, 255, 0.3)',
          animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite'
        }}
      >
        {isChatOpen ? '✕' : '💬'}
      </motion.button>

      {/* Chat Panel */}
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.3 }}
            className="fixed bottom-24 right-8 z-40 w-96 max-h-96 rounded-2xl bg-[#061018] border border-[rgba(0,230,255,0.15)] shadow-2xl flex flex-col"
            style={{
              boxShadow: '0 0 40px rgba(0, 230, 255, 0.1)'
            }}
          >
            {/* Header */}
            <div className="p-4 border-b border-[rgba(0,230,255,0.1)] flex items-center justify-between bg-gradient-to-r from-[rgba(0,230,255,0.05)] to-transparent">
              <div>
                <h4 className="font-semibold text-neon">Doctor-Bot</h4>
                <p className="text-xs text-slate-400">Medical AI Assistant</p>
              </div>
              <button
                onClick={() => setIsChatOpen(false)}
                className="text-slate-400 hover:text-neon transition-colors"
              >
                ✕
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map(msg => (
                <motion.div
                  key={msg.id}
                  initial={{ scale: 0.95, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] p-3 rounded-lg text-sm leading-relaxed ${
                      msg.from === 'user'
                        ? 'bg-neon/15 text-white border border-neon/30'
                        : 'bg-[rgba(255,255,255,0.03)] text-slate-200 border border-[rgba(0,230,255,0.1)]'
                    }`}
                  >
                    {msg.text}
                  </div>
                </motion.div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-[rgba(255,255,255,0.03)] p-3 rounded-lg">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-neon rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-neon rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-neon rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-[rgba(0,230,255,0.1)] space-y-2">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={text}
                  onChange={e => setText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me..."
                  disabled={isLoading}
                  className="flex-1 p-2 rounded-lg bg-[rgba(255,255,255,0.03)] border border-[rgba(0,230,255,0.1)] text-sm text-white placeholder-slate-500 focus:outline-none focus:border-neon/50 disabled:opacity-50"
                />
                <button
                  onClick={send}
                  disabled={isLoading || !text.trim()}
                  className="px-3 py-2 rounded-lg bg-neon text-[#012024] font-semibold text-sm hover:bg-cyan-400 transition-colors disabled:opacity-50"
                >
                  Send
                </button>
              </div>
              <p className="text-xs text-slate-500 text-center">
                Educational purposes only. Always consult medical professionals.
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Glow animation style */}
      <style>{`
        @keyframes pulse {
          0%, 100% {
            box-shadow: 0 0 30px rgba(0, 230, 255, 0.3);
          }
          50% {
            box-shadow: 0 0 50px rgba(0, 230, 255, 0.5);
          }
        }
      `}</style>
    </>
  )
}
