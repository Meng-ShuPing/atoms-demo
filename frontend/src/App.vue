<template>
  <n-config-provider :theme="lightTheme">
    <n-message-provider>
      <n-modal-provider>
        <div class="app-container">
          <n-layout-header class="header">
            <div class="logo">
              <n-icon :component="SparklesOutline" size="24" />
              <span>Atoms Demo</span>
            </div>
            <div class="header-actions">
              <template v-if="userStore.isAuthenticated">
                <n-avatar round :size="32">
                  <n-icon :component="PersonOutline" />
                </n-avatar>
                <span class="user-info">
                  {{ userStore.user?.username }}
                </span>
                <n-button @click="handleLogout" size="small" quaternary>
                  退出
                </n-button>
                <n-divider vertical />
                <n-button @click="createNewProject" type="primary">
                  <template #icon>
                    <n-icon :component="AddOutline" />
                  </template>
                  新建项目
                </n-button>
              </template>
              <template v-else>
                <n-button @click="showAuthModal = true" size="small">
                  登录 / 注册
                </n-button>
              </template>
              <n-divider vertical />
              <n-button @click="showHistory = !showHistory">
                <template #icon>
                  <n-icon :component="TimeOutline" />
                </template>
                历史记录
              </n-button>
            </div>
          </n-layout-header>

          <n-layout class="main-content" has-sider>
            <n-layout-sider
              v-if="showHistory"
              :width="280"
              show-trigger
              @collapse="showHistory = false"
              bordered
            >
              <HistoryPanel @select="handleSelectProject" />
            </n-layout-sider>

            <n-layout class="workspace">
              <div class="panels">
                <div class="left-panel">
                  <ChatPanel />
                </div>
                <div class="right-panel">
                  <div class="tabs">
                    <n-tabs type="line" animated>
                      <n-tab-pane name="code" tab="代码预览">
                        <CodeEditor />
                      </n-tab-pane>
                      <n-tab-pane name="preview" tab="应用预览">
                        <PreviewPanel />
                      </n-tab-pane>
                    </n-tabs>
                  </div>
                </div>
              </div>
            </n-layout>
          </n-layout>

          <!-- 认证模态框 -->
          <AuthModal
            v-if="showAuthModal"
            v-model="showAuthModal"
          />
        </div>
      </n-modal-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NLayout, NLayoutHeader, NLayoutSider, NButton, NIcon, NTabs, NTabPane, NMessageProvider, NDivider, NConfigProvider, NModalProvider, NAvatar, lightTheme } from 'naive-ui'
import { SparklesOutline, AddOutline, TimeOutline, PersonOutline } from '@vicons/ionicons5'
import { useProjectStore } from '@/stores/project'
import { useChatStore } from '@/stores/chat'
import { useUserStore } from '@/stores/user'
import ChatPanel from '@/components/ChatPanel.vue'
import CodeEditor from '@/components/CodeEditor.vue'
import PreviewPanel from '@/components/PreviewPanel.vue'
import HistoryPanel from '@/components/HistoryPanel.vue'
import AuthModal from '@/components/AuthModal.vue'

const projectStore = useProjectStore()
const userStore = useUserStore()
const showHistory = ref(false)
const showAuthModal = ref(false)

const createNewProject = async () => {
  // 清空聊天记录
  const chatStore = useChatStore()
  chatStore.clearMessages()

  // 创建新项目
  const newProject = await projectStore.createProject({ name: '新项目' })

  // 设置当前项目
  if (newProject) {
    projectStore.setCurrentProject(newProject)
  }
}

const handleSelectProject = (project: any) => {
  projectStore.setCurrentProject(project)
}

const handleLogout = () => {
  userStore.logout()
  // 清空项目数据
  projectStore.projects = []
  projectStore.currentProject = null
}
</script>

<style scoped>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  font-size: 18px;
  font-weight: bold;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  font-size: 14px;
  margin-right: 8px;
}

.main-content {
  flex: 1;
  overflow: hidden;
}

.workspace {
  height: 100%;
  overflow: hidden;
}

.panels {
  display: flex;
  height: 100%;
}

.left-panel {
  width: 400px;
  border-right: 1px solid #eee;
}

.right-panel {
  flex: 1;
  padding: 16px;
}

.tabs {
  height: 100%;
}
</style>
