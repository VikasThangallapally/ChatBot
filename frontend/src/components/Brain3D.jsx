import React from 'react'

export default function Brain3D(){
  return (
    <div className="w-full h-full rounded-lg overflow-hidden flex items-center justify-center">
      {/* Animated brain video */}
      <div className="flex-1 h-full rounded-lg bg-gradient-to-br from-[#071021] to-[#091428] p-2 flex items-center justify-center relative overflow-hidden">
        {/* Glowing background effect */}
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 animate-pulse" style={{animationDuration: '4s'}}></div>
        
        {/* Animated brain video */}
        <div className="relative z-10 brain-container">
          <video
            src="/media/brain-animation.webm"
            autoPlay
            loop
            muted
            playsInline
            className="brain-video object-cover"
            style={{
              maxWidth: '100%',
              maxHeight: '100%',
              filter: 'drop-shadow(0 0 30px rgba(6, 182, 212, 0.5))'
            }}
          />
        </div>
      </div>

      {/* Video Container Styles */}
      <style>{`
        .brain-container {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .brain-video {
          border-radius: 12px;
          transition: all 0.3s ease;
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
      `}</style>
    </div>
  )
}
