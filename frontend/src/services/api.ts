import axios from 'axios'
import type { ApiResponse, GenerateRequest, GenerateResponseData, Project, User } from '@/types'
import { apiConfig } from '@/config'

// API 基础 URL - 从配置读取
const API_BASE_URL = apiConfig.baseURL

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 自动添加 token
api.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 统一错误处理
    if (error.response) {
      // 服务器返回错误响应
      console.error('API 错误:', error.response.status, error.response.data)
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.error('网络错误:', error.message)
    } else {
      // 请求配置有问题
      console.error('请求错误:', error.message)
    }
    return Promise.reject(error)
  }
)

// 项目相关 API
export const projectApi = {
  // 获取项目列表
  getProjects: () => api.get<ApiResponse<{ projects: Project[] }>>('/api/projects'),

  // 获取项目详情
  getProject: (id: number) =>
    api.get<ApiResponse<{ project: Project }>>(`/api/projects/${id}`),

  // 创建项目
  createProject: (data: Partial<Project>) =>
    api.post<ApiResponse<{ project: Project }>>('/api/projects', data),

  // 更新项目
  updateProject: (id: number, data: Partial<Project>) =>
    api.put<ApiResponse<{ project: Project }>>(`/api/projects/${id}`, data),

  // 删除项目
  deleteProject: (id: number) =>
    api.delete<ApiResponse>(`/api/projects/${id}`),
}

// 代码生成 API
export const generateApi = {
  generateCode: (data: GenerateRequest) =>
    api.post<ApiResponse<GenerateResponseData>>(
      '/api/generate',
      data
    ),
}

// 用户认证 API
export const authApi = {
  // 用户注册
  register: (data: { username: string; email: string; password: string }) =>
    api.post<ApiResponse<{ user: User }>>('/api/auth/register', data),

  // 用户登录
  login: (data: { username: string; password: string }) =>
    api.post<ApiResponse<{ access_token: string; token_type: string }>>('/api/auth/login', data),

  // 获取当前用户信息
  getCurrentUser: () =>
    api.get<ApiResponse<{ user: User }>>('/api/auth/me'),
}
