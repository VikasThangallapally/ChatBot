module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        neon: '#00e6ff',
        accent: '#0ff',
        glass: 'rgba(255,255,255,0.06)'
      },
      boxShadow: {
        neon: '0 8px 30px rgba(0,230,255,0.08), 0 0 30px rgba(0,230,255,0.08)'
      }
    }
  },
  plugins: []
}
