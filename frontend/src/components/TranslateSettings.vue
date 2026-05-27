<script setup lang="ts">
import { computed } from "vue"
import { ElMessage } from "element-plus"
import { appStore } from "../store"
import { postConfig, getConfig } from "../api"

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
    await postConfig({ translation_provider: { provider: name } })
    await getConfig()
  } catch (e: any) {
    ElMessage.error(`保存失败: ${e.message}`)
  }
}

async function onChangeField(key: string, value: any) {
  try {
    await postConfig({ [key]: value })
    await getConfig()
  } catch (e: any) {
    ElMessage.error(`保存失败: ${e.message}`)
  }
}
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

    <div>
      <span style="font-size: 14px; margin-bottom: 4px; display: block">API Key</span>
      <el-input
        :model-value="activeConfig.api_key || ''"
        @update:model-value="(v: string) => onChangeField('api_key', v)"
        type="password"
        show-password
        placeholder="请输入 API Key"
      />
    </div>

    <div>
      <span style="font-size: 14px; margin-bottom: 4px; display: block">API URL</span>
      <el-input
        :model-value="activeConfig.api_url || ''"
        @update:model-value="(v: string) => onChangeField('api_url', v)"
        placeholder="请输入 API URL"
      />
    </div>

    <div>
      <span style="font-size: 14px; margin-bottom: 4px; display: block">Model</span>
      <el-input
        :model-value="activeConfig.model || ''"
        @update:model-value="(v: string) => onChangeField('model', v)"
        placeholder="请输入模型名称"
      />
    </div>

    <div>
      <span style="font-size: 14px; margin-bottom: 4px; display: block">目标翻译语言</span>
      <el-select
        :model-value="appStore.config.target_lang"
        @change="(v: string) => onChangeField('target_lang', v)"
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
