import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), 'VITE_')
  const isDev = mode === 'development'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
    define: {
      __APP_ENV__: JSON.stringify({
        API_BASE_URL: env.VITE_API_BASE_URL || 'http://localhost:8000',
        APP_TITLE: env.VITE_APP_TITLE || 'Atoms Demo',
      }),
      __DEV__: isDev,
    },
  }
})
