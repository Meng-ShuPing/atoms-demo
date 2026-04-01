export interface Project {
  id: number
  name: string
  html_code: string
  css_code: string
  js_code: string
  user_prompt: string
  created_at: string
  updated_at: string
}

export interface Code {
  html: string
  css: string
  js: string
}

export interface GenerateRequest {
  prompt: string
  project_id?: number
  context?: string
  conversation_history?: Array<{ role: string; content: string }>
  current_code?: { html: string; css: string; js: string } | null
}

export interface GenerateResponse {
  html: string
  css: string
  js: string
}

export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
}
