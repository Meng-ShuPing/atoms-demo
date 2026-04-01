import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Project } from '@/types'
import { projectApi } from '@/services/api'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref(false)

  // 获取项目列表
  async function fetchProjects() {
    loading.value = true
    try {
      const { data } = await projectApi.getProjects()
      if (data.success && data.data) {
        projects.value = data.data.projects
      }
    } catch (error) {
      console.error('获取项目列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 获取项目详情
  async function fetchProject(id: number) {
    loading.value = true
    try {
      const { data } = await projectApi.getProject(id)
      if (data.success && data.data) {
        currentProject.value = data.data.project
      }
    } catch (error) {
      console.error('获取项目详情失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 创建项目
  async function createProject(data: Partial<Project>) {
    try {
      const response = await projectApi.createProject(data)
      if (response.data.success && response.data.data) {
        await fetchProjects()
        return response.data.data.project
      }
    } catch (error) {
      console.error('创建项目失败:', error)
      throw error
    }
  }

  // 更新项目
  async function updateProject(id: number, data: Partial<Project>) {
    try {
      const response = await projectApi.updateProject(id, data)
      if (response.data.success && response.data.data) {
        await fetchProjects()
        currentProject.value = response.data.data.project
        return response.data.data.project
      }
    } catch (error) {
      console.error('更新项目失败:', error)
      throw error
    }
  }

  // 删除项目
  async function deleteProject(id: number) {
    try {
      await projectApi.deleteProject(id)
      await fetchProjects()
      if (currentProject.value?.id === id) {
        currentProject.value = null
      }
    } catch (error) {
      console.error('删除项目失败:', error)
      throw error
    }
  }

  // 设置当前项目
  function setCurrentProject(project: Project | null) {
    currentProject.value = project
  }

  return {
    projects,
    currentProject,
    loading,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    setCurrentProject,
  }
})
