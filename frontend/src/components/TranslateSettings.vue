<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { ElMessage } from "element-plus"
import { appStore } from "../store"
import { updateConfigAndStore } from "../useConfig"

const activeTab = ref(appStore.config.translation_provider?.provider || "")

const engines = computed(() => appStore.voices.all_translate_engines || [])

const transProvider = computed(() => appStore.config.translation_provider)
const currentConfig = computed(() => {
  const providers = transProvider.value?.providers || []
  return providers.find((p: any) => p.name === activeTab.value) || {}
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

// openai 字段
const apiKey = computed({
  get: () => currentConfig.value.api_key || "",
  set: (val: string) => updateProviderField("api_key", val),
})
const apiUrl = computed({
  get: () => currentConfig.value.url || "",
  set: (val: string) => updateProviderField("url", val),
})
const model = computed({
  get: () => currentConfig.value.model || "",
  set: (val: string) => updateProviderField("model", val),
})

// hy_mt15 字段
const serverUrl = computed({
  get: () => currentConfig.value.server_url || "",
  set: (val: string) => updateProviderField("server_url", val),
})
const modelPath = computed({
  get: () => currentConfig.value.model_path || "",
  set: (val: string) => updateProviderField("model_path", val),
})
const llamaCppPath = computed({
  get: () => currentConfig.value.llama_cpp_path || "",
  set: (val: string) => updateProviderField("llama_cpp_path", val),
})
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
              <el-input
                v-model="apiKey"
                type="password"
                show-password
                placeholder="请输入 API Key"
              />
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">API URL</span>
              <el-input
                v-model="apiUrl"
                placeholder="请输入 API URL"
              />
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Model</span>
              <el-input
                v-model="model"
                placeholder="请输入模型名称"
              />
            </div>
          </template>

          <!-- hy_mt15 专用字段 -->
          <template v-if="activeTab === 'hy_mt15'">
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Server URL</span>
              <el-input
                v-model="serverUrl"
                placeholder="默认 http://127.0.0.1:8081"
              />
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Model Path</span>
              <el-input
                v-model="modelPath"
                placeholder="默认 models/HY-mt/HY-MT1.5-1.8B-Q8_0.gguf"
              />
            </div>
            <div>
              <span style="font-size: 14px; margin-bottom: 4px; display: block">Llama.cpp Path</span>
              <el-input
                v-model="llamaCppPath"
                placeholder="默认 llama-cpp"
              />
            </div>
          </template>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
