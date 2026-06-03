import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    base: '/k12-knowledge-repository/',
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true
  }
})
