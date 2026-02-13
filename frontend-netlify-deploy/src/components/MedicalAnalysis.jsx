import React from 'react'
import { motion } from 'framer-motion'
import { ANALYSIS_DATA } from '../config/analysisData'

export default function MedicalAnalysis({ result }) {
  // Only show if result exists and is a successful prediction
  if (!result || result.status !== 'success' || !result.top_prediction) {
    return null
  }

  const tumorType = result.top_prediction.label
  const data = ANALYSIS_DATA[tumorType] || ANALYSIS_DATA["No Tumor"]

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.1 }}
      className="space-y-4 col-span-2"
    >
      {/* About Result */}
      <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)]">
        <h5 className="text-md font-semibold mb-3 flex items-center gap-2">
          <span className="text-neon">📋</span> About This Result
        </h5>
        <p className="text-sm text-slate-300 leading-relaxed">{data.aboutResult}</p>
      </div>

      {/* Symptoms / Effects */}
      {data.symptoms.length > 0 && (
        <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)]">
          <h5 className="text-md font-semibold mb-3 flex items-center gap-2">
            <span className="text-neon">⚕️</span> Possible Symptoms & Effects
          </h5>
          <ul className="space-y-2">
            {data.symptoms.map((symptom, idx) => (
              <li key={idx} className="text-sm text-slate-300 flex gap-3">
                <span className="text-cyan-400">•</span>
                <span>{symptom}</span>
              </li>
            ))}
          </ul>
          <p className="text-xs text-slate-400 mt-4 italic">
            ⚠️ Symptoms vary greatly between individuals. This is for informational purposes only.
          </p>
        </div>
      )}

      {/* Medical Consultation */}
      <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)]">
        <h5 className="text-md font-semibold mb-3 flex items-center gap-2">
          <span className="text-neon">👨‍⚕️</span> Medical Consultation
        </h5>
        <p className="text-sm text-slate-300 mb-4">Consider consulting with these specialists:</p>
        <div className="space-y-2">
          {data.specialists.map((specialist, idx) => (
            <div key={idx} className="text-sm text-slate-300 flex gap-3 p-2 bg-[rgba(0,230,255,0.05)] rounded">
              <span className="text-neon min-w-fit">→</span>
              <span>{specialist}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Lifestyle & Diet */}
      <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)]">
        <h5 className="text-md font-semibold mb-3 flex items-center gap-2">
          <span className="text-neon">🏥</span> Lifestyle & General Health
        </h5>
        <ul className="space-y-2">
          {data.lifestyle.map((item, idx) => (
            <li key={idx} className="text-sm text-slate-300 flex gap-3">
              <span className="text-cyan-400">•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
        <p className="text-xs text-slate-400 mt-4 italic">
          💡 These are general health recommendations, not medical treatment.
        </p>
      </div>

      {/* Monitoring & Next Steps */}
      <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.02)] border border-[rgba(0,230,255,0.06)]">
        <h5 className="text-md font-semibold mb-3 flex items-center gap-2">
          <span className="text-neon">📊</span> Monitoring & Next Steps
        </h5>
        <ul className="space-y-2">
          {data.monitoring.map((step, idx) => (
            <li key={idx} className="text-sm text-slate-300 flex gap-3">
              <span className="text-cyan-400">→</span>
              <span>{step}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Medical Disclaimer */}
      <div className="p-4 rounded-xl bg-yellow-500/10 border border-yellow-500/30">
        <h6 className="text-sm font-semibold text-yellow-400 mb-2">⚠️ Medical Disclaimer</h6>
        <p className="text-xs text-yellow-200 leading-relaxed">{data.disclaimer}</p>
      </div>
    </motion.div>
  )
}
