import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Message } from '@/types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const input = ref('')
  const isGenerating = ref(false)

  // 添加用户消息
  function addUserMessage(content: string) {
    messages.value.push({
      id: Date.now(),
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    })
  }

  // 添加助手消息
  function addAssistantMessage(content: string) {
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content,
      created_at: new Date().toISOString(),
    })
  }

  // 清空消息
  function clearMessages() {
    messages.value = []
  }

  return {
    messages,
    input,
    isGenerating,
    addUserMessage,
    addAssistantMessage,
    clearMessages,
  }
})
