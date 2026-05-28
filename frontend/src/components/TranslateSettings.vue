<script setup lang="ts">
import { computed } from "vue"
import { ElMessage } from "element-plus"
import { appStore } from "../store"
import { updateConfigAndStore } from "../useConfig"

const transProvider = computed(() => appStore.config.translation_provider)
const engines = computed(() => appStore.voices.translate_engines || [])
const activeName = computed(() => transProvider.value?.provider || "")
const providers = computed(() => transProvider.value?.providers || [])
const activeConfig = computed(() =>
  providers.value.find((p: any) => p.name === activeName.value) || {}
)

const languages = ["中文", "英语", "日语", "法语", "德语", "韩语", "俄语", "西班牙语"]

async function onChangeProvider(name: string) {
  try {
    await updateConfigAndStore("translation_provider.provider", name)
  } catch (e: any) {
    ElMessage.error(`保存失败: ${e.message}`)
  }
}

function updateProviderField(key: string, value: any) {
  const list = [...(transProvider.value?.providers || [])]
  const idx = list.findIndex((p: any) => p.name === activeName.value)
  if (idx >= 0) {
    list[idx] = { ...list[idx], [key]: value }
    updateConfigAndStore("translation_provider.providers", list)
  }
}

// openai 字段
const apiKey = computed({
  get: () => activeConfig.value.api_key || "",
  set: (val: string) => updateProviderField("api_key", val),
})
const apiUrl = computed({
  get: () => activeConfig.value.url || "",
  set: (val: string) => updateProviderField("url", val),
})
const model = computed({
  get: () => activeConfig.value.model || "",
  set: (val: string) => updateProviderField("model", val),
})

// hy_mt15 字段
const serverUrl = computed({
  get: () => activeConfig.value.server_url || "",
  set: (val: string) => updateProviderField("server_url", val),
})
const modelPath = computed({
  get: () => activeConfig.value.model_path || "",
  set: (val: string) => updateProviderField("model_path", val),
})
const llamaCppPath = computed({
  get: () => activeConfig.value.llama_cpp_path || "",
  set: (val: string) => updateProviderField("llama_cpp_path", val),
})
</script>

<template>
  <div style="display: flex; flex-direction: column; gap: 16px">
    <div>
      <span style="font-size: 14px; margin-bottom: 4px; display: block">翻译引擎</span>
      <el-select
        :model-value="activeName"
        @change="onChangeProvider"
        style="width: 100%"
      >
        <el-option
          v-for="engine in engines"
          :key="engine"
          :label="engine"
          :value="engine"
        />
      </el-select>
    </div>

    <!-- openai 专用字段 -->
    <template v-if="activeName === 'openai'">
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
    <template v-if="activeName === 'hy_mt15'">
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

    <div>
      <span style="font-size: 14px; margin-bottom: 4px; display: block">目标翻译语言</span>
      <el-select
        :model-value="appStore.config.target_lang"
        @change="(v: string) => updateConfigAndStore('target_lang', v)"
        style="width: 100%"
      >
        <el-option
          v-for="lang in languages"
          :key="lang"
          :label="lang"
          :value="lang"
        />
      </el-select>
    </div>
  </div>
</template>
