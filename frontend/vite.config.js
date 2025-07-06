import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    open: false,
  },
  build: {
    outDir: 'dist'
  },
  // 👇 IMPORTANT: ensures routes like /submission/5 work
  resolve: {
    alias: {
      '@': '/src',
    }
  },
  base: '/', // or set to your deployed subpath if using GitHub Pages etc.
})