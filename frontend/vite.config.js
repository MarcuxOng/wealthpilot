import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/client': {
        target: `http://${process.env.APP_HOST || '127.0.0.1'}:${process.env.APP_PORT || '8000'}`,
        changeOrigin: true,
      },
      '/products': {
        target: `http://${process.env.APP_HOST || '127.0.0.1'}:${process.env.APP_PORT || '8000'}`,
        changeOrigin: true,
      }
    }
  }
})
