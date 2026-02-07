/**
 * API Configuration
 * Uses environment variables for flexible deployment
 */

export const getApiBaseUrl = () => {
  // For development
  if (import.meta.env.DEV) {
    return import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  }
  
  // For production
  return import.meta.env.VITE_API_BASE_URL || window.location.origin
}

export const API_BASE_URL = getApiBaseUrl()

export default {
  getApiBaseUrl,
  API_BASE_URL
}
