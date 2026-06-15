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
    await updateConfigAndStore("translation_provider.provider", activeTab.value, true)
  }
}

function updateProviderField(key: string, value: any, needReload = false) {
  const list = [...(transProvider.value?.providers || [])]
  const idx = list.findIndex((p: any) => p.name === activeTab.value)
  if (idx >= 0) {
    list[idx] = { ...list[idx], [key]: value }
    updateConfigAndStore("translation_provider.providers", list, needReload)
  }
}

function saveField(key: string, value: string) {
  updateProviderField(key, value, true)
  ElMessage.success("已保存")
}

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
watch(currentConfig, syncLocalValues)
</script>

<template>
  <div class="trans-settings">
    <el-tabs v-model="activeTab">
      <el-tab-pane
        v-for="engine in engines"
        :key="engine"
        :label="engine"
        :name="engine"
      >
        <div class="panel">
          <div v-if="engineDescription" class="desc">
            {{ engineDescription }}
          </div>

          <div class="row">
            <span class="row__label">设为默认引擎</span>
            <el-switch :model-value="isDefault" @change="onSetDefault" />
          </div>

          <template v-if="activeTab === 'openai'">
            <div class="field">
              <label class="field__label">API Key</label>
              <div class="field__input-row">
                <el-input v-model="apiKey" type="password" show-password placeholder="请输入 API Key" />
                <button v-if="apiKey !== (currentConfig.api_key || '')" class="save-icon" @click="saveField('api_key', apiKey)">
                  <el-icon><Check /></el-icon>
                </button>
              </div>
            </div>
            <div class="field">
              <label class="field__label">API URL</label>
              <div class="field__input-row">
                <el-input v-model="apiUrl" placeholder="请输入 API URL" />
                <button v-if="apiUrl !== (currentConfig.url || '')" class="save-icon" @click="saveField('url', apiUrl)">
                  <el-icon><Check /></el-icon>
                </button>
              </div>
            </div>
            <div class="field">
              <label class="field__label">Model</label>
              <div class="field__input-row">
                <el-input v-model="model" placeholder="请输入模型名称" />
                <button v-if="model !== (currentConfig.model || '')" class="save-icon" @click="saveField('model', model)">
                  <el-icon><Check /></el-icon>
                </button>
              </div>
            </div>
          </template>

          <template v-if="activeTab === 'hy_mt15'">
            <div class="field">
              <label class="field__label">Server URL</label>
              <div class="field__input-row">
                <el-input v-model="serverUrl" placeholder="默认 http://127.0.0.1:8081" />
                <button v-if="serverUrl !== (currentConfig.server_url || '')" class="save-icon" @click="saveField('server_url', serverUrl)">
                  <el-icon><Check /></el-icon>
                </button>
              </div>
            </div>
            <div class="field">
              <label class="field__label">Model Path</label>
              <div class="field__input-row">
                <el-input v-model="modelPath" placeholder="默认 models/HY-mt/HY-MT1.5-1.8B-Q8_0.gguf" />
                <button v-if="modelPath !== (currentConfig.model_path || '')" class="save-icon" @click="saveField('model_path', modelPath)">
                  <el-icon><Check /></el-icon>
                </button>
              </div>
            </div>
            <div class="field">
              <label class="field__label">Llama.cpp Path</label>
              <div class="field__input-row">
                <el-input v-model="llamaCppPath" placeholder="默认 llama-cpp" />
                <button v-if="llamaCppPath !== (currentConfig.llama_cpp_path || '')" class="save-icon" @click="saveField('llama_cpp_path', llamaCppPath)">
                  <el-icon><Check /></el-icon>
                </button>
              </div>
            </div>
          </template>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.trans-settings {
  margin-top: 4px;
}

.panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 12px;
}

.desc {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
  padding: 12px 16px;
  background: var(--bg-elevated);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--accent);
}

.row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row__label {
  font-size: 14px;
  color: var(--text-primary);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-tertiary);
}

.field__input-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--accent);
  background: var(--accent-muted);
  color: var(--accent);
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--duration-fast) var(--ease-out);
}
.save-icon:hover {
  background: var(--accent);
  color: #ffffff;
}
</style>
