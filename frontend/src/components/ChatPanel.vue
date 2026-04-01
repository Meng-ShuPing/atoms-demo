<template>
  <div class="chat-panel">
    <div class="messages-container">
      <div v-if="messages.length === 0" class="empty-state">
        <n-icon :component="SparklesOutline" size="48" color="#667eea" />
        <p>描述你想要创建的应用</p>
        <p class="hint">例如：创建一个待办事项应用、创建一个计算器...</p>
      </div>
      <div v-else class="messages">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', message.role]"
        >
          <div class="message-content">{{ message.content }}</div>
        </div>
        <div v-if="isGenerating" class="message assistant">
          <n-spin size="small" />
          <span class="loading-text">正在生成代码...</span>
        </div>
      </div>
    </div>

    <div class="input-container">
      <n-input
        v-model:value="inputValue"
        type="textarea"
        placeholder="描述你想要创建的应用..."
        :rows="3"
        @keydown="handleKeydown"
      />
      <n-button
        type="primary"
        :loading="isGenerating"
        @click="sendMessage"
        :disabled="!inputValue.trim()"
      >
        生成
        <template #icon>
          <n-icon :component="SendOutline" />
        </template>
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NInput, NButton, NIcon, NSpin } from 'naive-ui'
import { SparklesOutline, SendOutline } from '@vicons/ionicons5'
import { useChatStore } from '@/stores/chat'
import { useProjectStore } from '@/stores/project'
import { generateApi } from '@/services/api'

const chatStore = useChatStore()
const projectStore = useProjectStore()

const inputValue = ref('')
const messages = computed(() => chatStore.messages)
const isGenerating = computed(() => chatStore.isGenerating)

const handleKeydown = (e: KeyboardEvent) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
    sendMessage()
  }
}

const sendMessage = async () => {
  const prompt = inputValue.value.trim()
  if (!prompt || isGenerating.value) return

  // 添加用户消息
  chatStore.addUserMessage(prompt)
  chatStore.isGenerating = true
  inputValue.value = ''

  try {
    // 如果没有当前项目，先创建一个新项目
    if (!projectStore.currentProject) {
      const newProject = await projectStore.createProject({
        name: prompt.slice(0, 20),
        user_prompt: prompt,
      })
      if (newProject) {
        projectStore.setCurrentProject(newProject)
      }
    }

    // 构建对话历史（只包含用户和助手的对话内容）
    const conversationHistory = chatStore.messages.map(msg => ({
      role: msg.role === 'user' ? 'user' : 'assistant',
      content: msg.content
    }))

    // 获取当前项目代码
    const currentProject = projectStore.currentProject
    const currentCode = currentProject ? {
      html: currentProject.html_code || '',
      css: currentProject.css_code || '',
      js: currentProject.js_code || ''
    } : null

    // 调用 API 生成代码
    const { data } = await generateApi.generateCode({
      prompt,
      project_id: projectStore.currentProject?.id,
      conversation_history: conversationHistory,
      current_code: currentCode
    })

    if (data.success && data.data) {
      const { code, project_id } = data.data

      console.log('代码生成成功:', { code, project_id })

      // 添加助手消息
      chatStore.addAssistantMessage('代码生成成功！')

      // 更新当前项目
      const targetProjectId = project_id || projectStore.currentProject?.id
      if (targetProjectId) {
        const updatedProject = await projectStore.updateProject(targetProjectId, {
          html_code: code.html,
          css_code: code.css,
          js_code: code.js,
        })
        console.log('项目已更新:', updatedProject)
      }
    }
  } catch (error) {
    console.error('生成代码失败:', error)
    chatStore.addAssistantMessage('生成失败，请稍后重试')
  } finally {
    chatStore.isGenerating = false
  }
}
</script>

<style scoped>
.chat-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 16px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #999;
}

.empty-state p {
  margin: 10px 0;
}

.hint {
  font-size: 12px;
  color: #bbb;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 90%;
}

.message.user {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  align-self: flex-end;
  margin-left: auto;
}

.message.assistant {
  background: #f5f5f5;
  color: #333;
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 8px;
}

.message-content {
  line-height: 1.5;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
