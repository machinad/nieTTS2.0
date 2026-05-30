<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { ElMessage } from "element-plus"
import { Check } from "@element-plus/icons-vue"
import { appStore, settingsTab } from "../store"
import { updateConfigAndStore } from "../useConfig"

const activeTab = computed({
  get: () => settingsTab.translate,
  set: (v: string) => { settingsTab.translate = v },
})

const engines = computed(() => (appStore.config.translation_provider?.providers || []).map((p: any) => p.name))

const transProvider = computed(() => appStore.config.translation_provider)
const currentConfig = computed(() => {
  const providers = transProvider.value?.providers || []
  return providers.find((p: any) => p.name === activeTab.value) || {}
})

const engineDescription = computed(() => {
  const providers = appStore.config.translation_provider?.providers || []
  const p = providers.find((p: any) => p.name === activeTab.value)
  return p?.description || ""
})

const isDefault = computed(() => transProvider.value?.provider === activeTab.value)

async function onSetDefault(val: boolean) {
  if (val) {
    await updateConfigAndStore("translation_provider.provider", activeTab.value)
  }
}

function updateProviderField(key: string, value: any) {
  const list = [...(transProvider.value?.providers || [])]
  const idx = list.findIndex((p: any) => p.name === activeTab.value)
  if (idx >= 0) {
    list[idx] = { ...list[idx], [key]: value }
    updateConfigAndStore("translation_provider.providers", list)
  }
}

// 手动保存的文本输入框
const apiKey = ref("")
const apiUrl = ref("")
const model = ref("")
const serverUrl = ref("")
const modelPath = ref("")
const llamaCppPath = ref("")

function syncLocalValues() {
  apiKey.value = currentConfig.value.api_key || ""
  apiUrl.value = currentConfig.value.url || ""
  model.value = currentConfig.value.model || ""
  serverUrl.value = currentConfig.value.server_url || ""
  modelPath.value = currentConfig.value.model_path || ""
  llamaCppPath.value = currentConfig.value.llama_cpp_path || ""
}

watch(activeTab, syncLocalValues, { immediate: true })

function saveField(key: string, value: string) {
  updateProviderField(key, value)
  ElMessage.success("已保存")
}
</script>

<template>
  <div>
    <el-tabs v-model="activeTab">
      <el-tab-pane
        v-for="engine in engines"
        :key="engine"
        :label="engine"
        :name="engine"
      >
        <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 8px">
          <div v-if="engineDescription" style="color: #909399; font-size: 13px; line-height: 1.5; padding: 8px 12px; background: #f5f7fa; border-radius: 4px">
            {{ engineDescription }}
          </div>

          <div style="display: flex; align-items: center; gap: 8px">
            <span style="font-size: 14px">设为默认引擎</span>
            <el-switch
              :model-value="isDefault"
              @change="onSetDefault"
            />
          </div>

          <!-- openai 专用字段 -->
          <template v-if="activeTab === 'openai'">
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">API Key</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="apiKey"
                  type="password"
                  show-password
                  placeholder="请输入 API Key"
                />
                <el-icon v-if="apiKey !== (currentConfig.api_key || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveField('api_key', apiKey)"><Check /></el-icon>
              </div>
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">API URL</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="apiUrl"
                  placeholder="请输入 API URL"
                />
                <el-icon v-if="apiUrl !== (currentConfig.url || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveField('url', apiUrl)"><Check /></el-icon>
              </div>
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Model</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="model"
                  placeholder="请输入模型名称"
                />
                <el-icon v-if="model !== (currentConfig.model || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveField('model', model)"><Check /></el-icon>
              </div>
            </div>
          </template>

          <!-- hy_mt15 专用字段 -->
          <template v-if="activeTab === 'hy_mt15'">
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Server URL</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="serverUrl"
                  placeholder="默认 http://127.0.0.1:8081"
                />
                <el-icon v-if="serverUrl !== (currentConfig.server_url || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveField('server_url', serverUrl)"><Check /></el-icon>
              </div>
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Model Path</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="modelPath"
                  placeholder="默认 models/HY-mt/HY-MT1.5-1.8B-Q8_0.gguf"
                />
                <el-icon v-if="modelPath !== (currentConfig.model_path || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveField('model_path', modelPath)"><Check /></el-icon>
              </div>
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Llama.cpp Path</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="llamaCppPath"
                  placeholder="默认 llama-cpp"
                />
                <el-icon v-if="llamaCppPath !== (currentConfig.llama_cpp_path || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveField('llama_cpp_path', llamaCppPath)"><Check /></el-icon>
              </div>
            </div>
          </template>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
