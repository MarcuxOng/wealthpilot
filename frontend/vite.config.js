import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    server: {
      port: 3000,
      proxy: {
        '/client_analysis': {
          target: `http://${env.VITE_APP_HOST}:${env.VITE_APP_PORT}`,
          changeOrigin: true,
        },
        '/products': {
          target: `http://${env.VITE_APP_HOST}:${env.VITE_APP_PORT}`,
          changeOrigin: true,
        },
        '/clients': {
          target: `http://${env.VITE_APP_HOST}:${env.VITE_APP_PORT}`,
          changeOrigin: true,
        },
        '/analysis_history': {
          target: `http://${env.VITE_APP_HOST}:${env.VITE_APP_PORT}`,
          changeOrigin: true,
        }
      }
    }
  }
})
