import React from 'react'
import { motion } from 'framer-motion'

// Simple circular progress indicator
function CircularProgress({value, color}){
  const stroke = 8
  const radius = 48 - stroke
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (value / 100) * circumference
  return (
    <svg width="120" height="120" viewBox="0 0 120 120">
      <circle cx="60" cy="60" r={radius} stroke="rgba(255,255,255,0.08)" strokeWidth={stroke} fill="none" />
      <circle cx="60" cy="60" r={radius} stroke={color} strokeWidth={stroke} fill="none" strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round" transform="rotate(-90 60 60)" />
      <text x="60" y="66" textAnchor="middle" fontSize="18" fill="#fff">{value}%</text>
    </svg>
  )
}

export default function ResultPanel({result}){
  // If no result yet, show placeholder
  if (!result || result.status === 'waiting') {
    return (
      <motion.div 
        initial={{ y: 20, opacity: 0 }} 
        animate={{ y: 0, opacity: 1 }} 
        transition={{ duration: 0.6 }} 
        className="p-6 rounded-2xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg border border-cyan-500/20 shadow-2xl"
      >
        <h4 className="text-lg font-semibold mb-4 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Analysis Results</h4>
        <div className="text-slate-400 text-center py-8">Upload an image to see detailed analysis here</div>
      </motion.div>
    )
  }

  // Handle invalid image - STRICT: Do NOT show any predictions
  if (result.status === 'invalid_image' || !result.is_valid_brain_image) {
    return (
      <motion.div 
        initial={{ y: 20, opacity: 0 }} 
        animate={{ y: 0, opacity: 1 }} 
        transition={{ duration: 0.6 }} 
        className="p-6 rounded-2xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg border border-red-500/30 shadow-2xl hover:shadow-red-500/20"
      >
        <h4 className="text-lg font-semibold mb-4 text-red-400">❌ Not a Valid Brain MRI</h4>
        <p className="text-slate-300 mb-4 font-semibold">The uploaded file is NOT a brain MRI scan.</p>
        <p className="text-slate-400 mb-4 text-sm">{result.error || result.validation_reason || 'The image does not match brain MRI characteristics.'}</p>
        
        <div className="space-y-3">
          <div className="bg-red-500/15 border border-red-500/30 rounded p-4">
            <p className="text-red-200 font-semibold text-sm mb-2">❌ Rejected Images Include:</p>
            <ul className="text-red-200 text-xs space-y-1">
              <li>• Human/person photos</li>
              <li>• Random images or drawings</li>
              <li>• Medical images from other body parts (chest, abdomen, etc.)</li>
              <li>• Non-grayscale or highly colored images</li>
              <li>• Low contrast or corrupted images</li>
            </ul>
          </div>

          <div className="bg-green-500/15 border border-green-500/30 rounded p-4">
            <p className="text-green-200 font-semibold text-sm mb-2">✅ Valid Images Should Be:</p>
            <ul className="text-green-200 text-xs space-y-1">
              <li>• Brain MRI scans (DICOM, JPEG, PNG)</li>
              <li>• At least 150x150 pixels</li>
              <li>• Grayscale or properly formatted</li>
              <li>• Clear with good contrast</li>
              <li>• Actual medical imaging data</li>
            </ul>
          </div>
        </div>

        <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded">
          <p className="text-yellow-300 text-xs">
            ⚠️ NO PREDICTIONS are shown for invalid images. This is intentional to prevent misclassification.
          </p>
        </div>
      </motion.div>
    )
  }

  // Handle error
  if (result.status === 'error') {
    return (
      <motion.div 
        initial={{ y: 20, opacity: 0 }} 
        animate={{ y: 0, opacity: 1 }} 
        transition={{ duration: 0.6 }} 
        className="p-6 rounded-2xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg border border-red-500/20 shadow-2xl"
      >
        <h4 className="text-lg font-semibold mb-4 text-red-400">⚠️ Error</h4>
        <p className="text-slate-300">{result.error || 'An error occurred during analysis'}</p>
      </motion.div>
    )
  }

  // Handle success with full analysis - SAFEGUARD: Only if is_valid_brain_image is true
  if (result.status === 'success' && result.is_valid_brain_image === true && result.top_prediction && result.medical_analysis) {
    const top = result.top_prediction
    const analysis = result.medical_analysis
    const color = top.confidence > 0.75 ? '#22c55e' : top.confidence > 0.5 ? '#f59e0b' : '#ef4444'
    const severityColor = {
      'None': 'text-green-400',
      'Low': 'text-blue-400',
      'Low to Medium': 'text-yellow-400',
      'Medium': 'text-orange-400',
      'High': 'text-red-400'
    }

    return (
      <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.6 }} className="space-y-6">
        {/* Main Prediction */}
        <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg border border-cyan-500/20 hover:border-cyan-500/40 shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
          <h4 className="text-lg font-semibold mb-6 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Prediction Result</h4>
          <div className="flex items-center gap-8 mb-6">
            <div>
              <CircularProgress value={Math.round(top.confidence * 100)} color={color} />
            </div>
            <div className="flex-1">
              <div className="text-3xl font-bold text-white">{top.label}</div>
              <div className="mt-2 text-sm text-slate-300">Predicted Tumor Type</div>
              <div className={`mt-3 text-sm font-semibold ${severityColor[analysis.severity_level] || 'text-slate-300'}`}>
                Severity: {analysis.severity_level}
              </div>
              {analysis.severity_note && (
                <div className="mt-3 text-xs text-orange-400 bg-orange-500/10 p-2 rounded border border-orange-500/20">
                  {analysis.severity_note}
                </div>
              )}
            </div>
          </div>

          {/* Confidence Breakdown */}
          <div className="mt-8 pt-6 border-t border-slate-600">
            <h5 className="text-sm font-semibold mb-4 text-slate-200">Confidence Breakdown</h5>
            <div className="space-y-3">
              {result.predictions.map((pred, idx) => (
                <div key={idx} className="flex items-center gap-4">
                  <div className="w-32 text-sm text-slate-300">{pred.label}</div>
                  <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }} 
                      animate={{ width: `${pred.percentage}%` }} 
                      transition={{ delay: idx * 0.1, duration: 0.6 }}
                      className={pred.class_index === top.class_index ? 'h-full bg-gradient-to-r from-cyan-500 to-blue-500' : 'h-full bg-slate-600'}
                    />
                  </div>
                  <div className="w-16 text-right text-sm font-semibold">{pred.percentage}%</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Medical Analysis */}
        <div className="p-6 rounded-2xl bg-[rgba(255,255,255,0.05)] backdrop-blur-lg border border-cyan-500/20 hover:border-cyan-500/40 shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300">
          <h4 className="text-lg font-semibold mb-4 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Medical Analysis & Information</h4>

          {/* Description */}
          <div className="mb-6">
            <h5 className="text-sm font-semibold text-cyan-400 mb-2">About {top.label}</h5>
            <p className="text-sm text-slate-300 leading-relaxed">{analysis.description}</p>
          </div>

          {/* Key Characteristics */}
          {analysis.key_characteristics && analysis.key_characteristics.length > 0 && (
            <div className="mb-6">
              <h5 className="text-sm font-semibold text-cyan-400 mb-3">Key Characteristics</h5>
              <ul className="space-y-2">
                {analysis.key_characteristics.map((char, idx) => (
                  <li key={idx} className="text-sm text-slate-300 flex gap-3">
                    <span className="text-cyan-400 font-bold">•</span>
                    <span>{char}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Advantages */}
          {analysis.advantages && analysis.advantages.length > 0 && (
            <div className="mb-6 bg-green-500/5 border border-green-500/20 rounded-lg p-4">
              <h5 className="text-sm font-semibold text-green-400 mb-3">✓ Positive Aspects</h5>
              <ul className="space-y-2">
                {analysis.advantages.map((adv, idx) => (
                  <li key={idx} className="text-sm text-slate-300 flex gap-3">
                    <span className="text-green-400">✓</span>
                    <span>{adv}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Disadvantages */}
          {analysis.disadvantages && analysis.disadvantages.length > 0 && (
            <div className="mb-6 bg-red-500/5 border border-red-500/20 rounded-lg p-4">
              <h5 className="text-sm font-semibold text-red-400 mb-3">⚠ Concerns & Challenges</h5>
              <ul className="space-y-2">
                {analysis.disadvantages.map((dis, idx) => (
                  <li key={idx} className="text-sm text-slate-300 flex gap-3">
                    <span className="text-red-400">!</span>
                    <span>{dis}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended Next Steps */}
          {analysis.recommended_next_steps && analysis.recommended_next_steps.length > 0 && (
            <div className="bg-blue-500/5 border border-blue-500/20 rounded-lg p-4">
              <h5 className="text-sm font-semibold text-blue-400 mb-3">📋 Recommended Next Steps</h5>
              <ol className="space-y-2">
                {analysis.recommended_next_steps.map((step, idx) => (
                  <li key={idx} className="text-sm text-slate-300 flex gap-3">
                    <span className="text-blue-400 font-bold">{idx + 1}.</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>

        {/* Disclaimer */}
        {/* <div className="p-4 bg-yellow-500/5 border border-yellow-500/30 rounded-lg">
          <p className="text-xs text-yellow-200">
            <strong>⚠️ IMPORTANT DISCLAIMER:</strong> This AI-assisted analysis is for educational and informational purposes only. It is <strong>NOT</strong> a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals (radiologists, neurologists, or neurosurgeons) for accurate medical diagnosis and treatment decisions.
          </p>
        </div> */}
      </motion.div>
    )
  }

  return null
}

