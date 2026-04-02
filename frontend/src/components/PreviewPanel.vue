<template>
  <div class="preview-panel">
    <div class="toolbar">
      <div class="device-selector">
        <n-button
          :type="device === 'desktop' ? 'primary' : 'default'"
          @click="device = 'desktop'"
          size="small"
        >
          <template #icon>
            <n-icon :component="DesktopOutline" />
          </template>
        </n-button>
        <n-button
          :type="device === 'tablet' ? 'primary' : 'default'"
          @click="device = 'tablet'"
          size="small"
        >
          <template #icon>
            <n-icon :component="TabletPortraitOutline" />
          </template>
        </n-button>
        <n-button
          :type="device === 'mobile' ? 'primary' : 'default'"
          @click="device = 'mobile'"
          size="small"
        >
          <template #icon>
            <n-icon :component="PhonePortraitOutline" />
          </template>
        </n-button>
      </div>
      <n-button @click="refresh" size="small">
        <template #icon>
          <n-icon :component="RefreshOutline" />
        </template>
        刷新
      </n-button>
    </div>

    <div class="preview-container">
      <div :class="['preview-wrapper', device]">
        <iframe
          :key="refreshKey"
          :srcdoc="iframeContent"
          sandbox="allow-scripts allow-modals"
          frameborder="0"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { NButton, NIcon } from 'naive-ui'
import { DesktopOutline, TabletPortraitOutline, PhonePortraitOutline, RefreshOutline } from '@vicons/ionicons5'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()

const device = ref<'desktop' | 'tablet' | 'mobile'>('desktop')
const refreshKey = ref(0)

const iframeContent = computed(() => {
  const project = projectStore.currentProject
  console.log('PreviewPanel - currentProject:', project)

  if (!project) {
    return '<html><body style="display:flex;justify-content:center;align-items:center;height:100vh;color:#999;"><p>暂无内容，请先生成代码</p></body></html>'
  }

  // 如果没有代码，显示等待提示
  if (!project.html_code && !project.css_code && !project.js_code) {
    return '<html><body style="display:flex;justify-content:center;align-items:center;height:100vh;color:#667eea;"><p>正在生成代码...</p></body></html>'
  }

  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    ${project.css_code || ''}
  </style>
</head>
<body>
  ${project.html_code || ''}
  <script>
    try {
      ${project.js_code || ''}
    } catch (e) {
      console.error('Preview error:', e);
    }
  <\/script>
</body>
</html>
`.trim()
})

const refresh = () => {
  refreshKey.value++
}

// 监听设备变化
watch(device, () => {
  refresh()
})
</script>

<style scoped>
.preview-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.device-selector {
  display: flex;
  gap: 8px;
}

.preview-container {
  flex: 1;
  overflow: auto;
  background: #f5f5f5;
  padding: 16px;
}

.preview-wrapper {
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preview-wrapper.desktop {
  width: 100%;
  min-height: 500px;
}

.preview-wrapper.tablet {
  width: 768px;
  min-height: 500px;
}

.preview-wrapper.mobile {
  width: 375px;
  min-height: 500px;
}

iframe {
  width: 100%;
  height: 100%;
  min-height: 500px;
}
</style>
