<template>
  <div class="history-panel">
    <div class="header">
      <h3>历史项目</h3>
      <n-button v-if="projects.length > 0" @click="emit('refresh')" size="small" quaternary>
        <template #icon>
          <n-icon :component="RefreshOutline" />
        </template>
      </n-button>
    </div>

    <div v-if="loading" class="loading">
      <n-spin size="medium" />
    </div>

    <div v-else-if="projects.length === 0" class="empty">
      <n-icon :component="FolderOpenOutline" size="48" color="#ddd" />
      <p>暂无历史项目</p>
    </div>

    <div v-else class="project-list">
      <div
        v-for="project in projects"
        :key="project.id"
        :class="['project-item', { active: currentProject?.id === project.id }]"
        @click="handleSelect(project)"
      >
        <div class="project-info">
          <div class="project-name">{{ project.name }}</div>
          <div class="project-time">{{ formatTime(project.updated_at) }}</div>
        </div>
        <n-button
          @click.stop="handleDelete(project.id)"
          size="tiny"
          quaternary
          type="error"
        >
          <template #icon>
            <n-icon :component="TrashOutline" />
          </template>
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { NButton, NIcon, NSpin } from 'naive-ui'
import { RefreshOutline, TrashOutline, FolderOpenOutline } from '@vicons/ionicons5'
import { useProjectStore } from '@/stores/project'
import type { Project } from '@/types'

const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)
const currentProject = computed(() => projectStore.currentProject)
const loading = computed(() => projectStore.loading)

const emit = defineEmits(['select', 'refresh'])

const handleSelect = (project: Project) => {
  emit('select', project)
}

const handleDelete = async (id: number) => {
  try {
    await projectStore.deleteProject(id)
  } catch (error) {
    console.error('删除失败:', error)
  }
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days}天前`
  } else {
    return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
  }
}

onMounted(() => {
  projectStore.fetchProjects()
})
</script>

<style scoped>
.history-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: #999;
}

.empty p {
  margin-top: 16px;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.project-item:hover {
  background: #f0f0f0;
}

.project-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.project-info {
  flex: 1;
  overflow: hidden;
}

.project-name {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 4px;
}
</style>
