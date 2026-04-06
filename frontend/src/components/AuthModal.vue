<template>
  <div class="auth-modal" @click="emit('update:modelValue', false)">
    <div class="auth-container" @click.stop>
      <div class="auth-header">
        <h2>{{ isLogin ? '用户登录' : '用户注册' }}</h2>
        <n-button text @click="emit('update:modelValue', false)">
          <template #icon>
            <n-icon :component="CloseOutline" />
          </template>
        </n-button>
      </div>

      <n-form
        ref="formRef"
        :model="formModel"
        :rules="formRules"
        label-placement="top"
      >
        <n-form-item label="用户名" path="username">
          <n-input
            v-model:value="formModel.username"
            placeholder="请输入用户名（3-50 个字符）"
            :disabled="loading"
          />
        </n-form-item>

        <n-form-item v-if="!isLogin" label="邮箱" path="email">
          <n-input
            v-model:value="formModel.email"
            placeholder="请输入邮箱地址"
            :disabled="loading"
          />
        </n-form-item>

        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="formModel.password"
            type="password"
            placeholder="请输入密码（至少 6 位）"
            :disabled="loading"
            show-password-on="click"
          />
        </n-form-item>

        <n-form-item v-if="!isLogin" label="确认密码" path="confirmPassword">
          <n-input
            v-model:value="formModel.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            :disabled="loading"
            show-password-on="click"
          />
        </n-form-item>

        <n-form-item>
          <n-button
            type="primary"
            block
            size="large"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ isLogin ? '登录' : '注册' }}
          </n-button>
        </n-form-item>

        <div class="auth-footer">
          <n-button text @click="toggleMode">
            {{ isLogin ? '没有账号？立即注册' : '已有账号？返回登录' }}
          </n-button>
        </div>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { NForm, NFormItem, NInput, NButton, NIcon, useMessage } from 'naive-ui'
import { CloseOutline } from '@vicons/ionicons5'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/services/api'
import type { FormRules, FormInst } from 'naive-ui'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const userStore = useUserStore()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const isLogin = ref(true)

const formModel = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const formRules = computed<FormRules>(() => ({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应在 3-50 个字符之间', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (_rule, value) => {
        if (value !== formModel.password) {
          return new Error('两次输入的密码不一致')
        }
        return true
      },
      trigger: 'blur',
    },
  ],
}))

const resetForm = () => {
  formModel.username = ''
  formModel.email = ''
  formModel.password = ''
  formModel.confirmPassword = ''
  if (formRef.value) {
    formRef.value.restoreValidation()
  }
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  resetForm()
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (errors) => {
    if (errors) return

    loading.value = true
    try {
      if (isLogin.value) {
        // 登录
        const res = await authApi.login({
          username: formModel.username,
          password: formModel.password,
        })

        console.log('Login response:', res)

        if (res.data.success) {
          const { access_token, user } = res.data.data!
          // 直接保存用户信息
          userStore.setAuth(access_token, user)
          // 显示成功消息
          message.success('登录成功')
          // 重置表单
          resetForm()
          // 关闭模态框
          console.log('Closing modal, modelValue:', props.modelValue)
          emit('update:modelValue', false)
        }
      } else {
        // 注册
        const res = await authApi.register({
          username: formModel.username,
          email: formModel.email,
          password: formModel.password,
        })

        if (res.data.success) {
          message.success('注册成功，请登录')
          isLogin.value = true
          resetForm()
        }
      }
    } catch (error: any) {
      console.error('Auth error:', error)
      message.error(error.response?.data?.detail || '操作失败，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.auth-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.auth-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
}

.auth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.auth-header h2 {
  margin: 0;
  font-size: 24px;
  color: #1a1a1a;
}

.auth-footer {
  text-align: center;
  margin-top: 16px;
}
</style>
