/**
 * 应用配置
 */
interface AppConfig {
  API_BASE_URL: string
  APP_TITLE: string
}

// 全局变量类型声明
declare const __APP_ENV__: AppConfig

/**
 * 应用配置
 * 开发和生产环境都使用 VITE_API_BASE_URL 环境变量
 */
const appConfig: AppConfig = (typeof __APP_ENV__ !== 'undefined' ? __APP_ENV__ : {
  API_BASE_URL: 'http://localhost:8000',
  APP_TITLE: 'Atoms Demo',
}) as AppConfig

export const config = {
  // API 基础 URL
  apiBaseUrl: appConfig.API_BASE_URL,

  // 应用标题
  appTitle: appConfig.APP_TITLE,

  // 超时设置
  timeout: 60000,

  // 重试配置
  retry: {
    count: 3,
    delay: 1000,
  },
}

// 导出 API 配置供外部使用
export const apiConfig = {
  baseURL: config.apiBaseUrl,
  timeout: config.timeout,
}
