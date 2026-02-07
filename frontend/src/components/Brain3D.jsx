import React, { useRef, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Preload } from '@react-three/drei'

// Simple stylized brain: wireframe sphere + layered meshes for glow
function BrainMesh(){
  const ref = useRef()
  useFrame((state, delta) => {
    // continuous smooth rotation
    if(ref.current) ref.current.rotation.y += delta * 0.4
  })

  return (
    <group ref={ref}>
      <mesh>
        <sphereGeometry args={[1.6, 64, 64]} />
        <meshStandardMaterial color="#052b3a" metalness={0.4} roughness={0.2} emissive={'#002c3b'} emissiveIntensity={0.2} />
      </mesh>

      {/* wireframe overlay */}
      <mesh>
        <sphereGeometry args={[1.605, 64, 64]} />
        <meshBasicMaterial color="#00e6ff" wireframe opacity={0.9} transparent />
      </mesh>

      {/* inner glow */}
      <mesh>
        <sphereGeometry args={[1.45, 64, 64]} />
        <meshStandardMaterial color="#003a50" emissive={'#00cfff'} emissiveIntensity={0.08} roughness={0.9} metalness={0.1} transparent opacity={0.6} />
      </mesh>
    </group>
  )
}

// GLTF loader wrapper - loads optional model and falls back to BrainMesh
// To use: place a GLB file at frontend/public/models/brain.glb
// For now, just render the stylized BrainMesh to avoid loading errors
function ModelRenderer(){
  return <BrainMesh />
}

export default function Brain3D(){
  const [preview, setPreview] = useState(null)

  useEffect(()=>{
    // listen for uploads to show preview beside model
    const onUploaded = (e)=>{
      const url = e.detail?.url || window.latestUploadedImage
      setPreview(url)
    }
    window.addEventListener('mriUploaded', onUploaded)
    // also check global var if already set
    if(window.latestUploadedImage) setPreview(window.latestUploadedImage)
    return ()=> window.removeEventListener('mriUploaded', onUploaded)
  },[])

  return (
    <div className="w-full h-full rounded-lg overflow-hidden flex items-center gap-4">
      {/* Left: preview image (appear only after upload) */}
      <div className="flex-shrink-0">
        {preview ? (
          <div className="w-48 h-48 rounded-lg overflow-hidden border border-[rgba(0,230,255,0.12)] p-1" style={{boxShadow:'0 8px 30px rgba(0,230,255,0.06)'}}>
            <img src={preview} alt="MRI preview" className="w-full h-full object-contain rounded-md" />
          </div>
        ) : (
          <div className="w-48 h-48 rounded-lg bg-[rgba(255,255,255,0.02)] border border-[rgba(255,255,255,0.03)] flex items-center justify-center text-sm text-slate-400">No MRI preview</div>
        )}
      </div>

      {/* Right: 3D canvas */}
      <div className="flex-1 h-80 rounded-lg bg-gradient-to-br from-[#071021] to-[#091428] p-2">
        <Canvas camera={{ position: [0, 0, 4.5], fov: 45 }}>
          {/* soft medical lighting */}
          <ambientLight intensity={0.5} />
          <directionalLight position={[5, 5, 5]} intensity={0.9} color={'#00e6ff'} />
          <directionalLight position={[-5, -5, -5]} intensity={0.3} />

          <ModelRenderer />

          <OrbitControls enableZoom={false} enablePan={false} autoRotate={false} />
          <Preload all />
        </Canvas>
      </div>
    </div>
  )
}
