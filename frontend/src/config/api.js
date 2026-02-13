/**
 * API Configuration
 * Uses environment variables for flexible deployment across Netlify frontend + Render backend
 */

export const getApiBaseUrl = () => {
  // For development - use VITE_API_URL if provided, otherwise localhost
  if (import.meta.env.DEV) {
    return import.meta.env.VITE_API_URL || 'http://localhost:8000'
  }
  
  // For production - use VITE_API_URL environment variable (e.g., https://brain-tumor-api.onrender.com)
  // This allows frontend on Netlify to communicate with backend on Render
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Fallback for single-domain deployments (legacy)
  return ''
}

export const API_BASE_URL = getApiBaseUrl()

// Log API configuration for debugging (only in development)
if (import.meta.env.DEV) {
  console.log(`[API Config] Using API_BASE_URL: ${API_BASE_URL}`)
}

export default {
  getApiBaseUrl,
  API_BASE_URL
}
