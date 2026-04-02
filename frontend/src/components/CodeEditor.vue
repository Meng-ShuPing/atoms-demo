<template>
  <div class="code-editor">
    <n-tabs type="line" animated>
      <n-tab-pane name="html" tab="HTML">
        <n-input
          v-model:value="htmlCode"
          type="textarea"
          :rows="15"
          placeholder="HTML 代码"
          @blur="saveCode"
        />
      </n-tab-pane>
      <n-tab-pane name="css" tab="CSS">
        <n-input
          v-model:value="cssCode"
          type="textarea"
          :rows="15"
          placeholder="CSS 代码"
          @blur="saveCode"
        />
      </n-tab-pane>
      <n-tab-pane name="js" tab="JavaScript">
        <n-input
          v-model:value="jsCode"
          type="textarea"
          :rows="15"
          placeholder="JavaScript 代码"
          @blur="saveCode"
        />
      </n-tab-pane>
    </n-tabs>

    <div class="actions">
      <n-button @click="copyCode" size="small">
        <template #icon>
          <n-icon :component="CopyOutline" />
        </template>
        复制代码
      </n-button>
      <n-button @click="downloadCode" size="small">
        <template #icon>
          <n-icon :component="DownloadOutline" />
        </template>
        下载
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { NTabs, NTabPane, NInput, NButton, NIcon, useMessage } from 'naive-ui'
import { CopyOutline, DownloadOutline } from '@vicons/ionicons5'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()
const message = useMessage()

const htmlCode = ref('')
const cssCode = ref('')
const jsCode = ref('')

// 监听当前项目变化
watch(
  () => projectStore.currentProject,
  (project) => {
    if (project) {
      htmlCode.value = project.html_code || ''
      cssCode.value = project.css_code || ''
      jsCode.value = project.js_code || ''
    }
  },
  { immediate: true }
)

// 保存代码
const saveCode = async () => {
  if (!projectStore.currentProject) return

  await projectStore.updateProject(projectStore.currentProject.id, {
    html_code: htmlCode.value,
    css_code: cssCode.value,
    js_code: jsCode.value,
  })
  message.success('代码已保存')
}

// 复制代码
const copyCode = async () => {
  const code = `
<!DOCTYPE html>
<html>
<head>
  <style>${cssCode.value}</style>
</head>
<body>
  ${htmlCode.value}
  <script>${jsCode.value}<\/script>
</body>
</html>
`.trim()

  try {
    await navigator.clipboard.writeText(code)
    message.success('代码已复制到剪贴板')
  } catch (error) {
    message.error('复制失败')
  }
}

// 下载代码
const downloadCode = () => {
  const html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atoms Demo</title>
  <style>
    ${cssCode.value}
  </style>
</head>
<body>
  ${htmlCode.value}
  <script>
    ${jsCode.value}
  <\/script>
</body>
</html>
`.trim()

  const blob = new Blob([html], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'index.html'
  a.click()
  URL.revokeObjectURL(url)
  message.success('文件已下载')
}
</script>

<style scoped>
.code-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}
</style>
