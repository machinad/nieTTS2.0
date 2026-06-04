<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { ElMessage } from "element-plus"
import { Check } from "@element-plus/icons-vue"
import { updateConfigAndStore } from "../useConfig"
import { appStore, settingsTab } from "../store"

const activeTab = computed({
  get: () => settingsTab.tts,
  set: (v: string) => { settingsTab.tts = v },
})

const engines = computed(() => {
  return (appStore.config.tts_provider?.providers || []).map((p: any) => p.name)
})

const engineVoices = computed(() => {
  const voices = appStore.config.voices || {}
  return (voices[activeTab.value] || []) as string[]
})

const isDefault = computed(() => {
  return appStore.config.tts_provider?.provider === activeTab.value
})

const currentProvider = computed((): Record<string, any> => {
  const providers = appStore.config.tts_provider?.providers || []
  return providers.find((p: any) => p.name === activeTab.value) || {}
})

const selectedVoice = computed({
  get: () => currentProvider.value.voice || "",
  set: (val: string) => {
    const providers = [...(appStore.config.tts_provider?.providers || [])]
    const idx = providers.findIndex((p: any) => p.name === activeTab.value)
    if (idx >= 0) {
      providers[idx] = { ...providers[idx], voice: val }
      updateConfigAndStore("tts_provider.providers", providers)
    }
  },
})

// 手动保存的文本输入框
const aliApiKey = ref("")
const matchaKeys = ["acoustic_model", "vocoder", "tokens", "lexicon", "data_dir", "dict_dir"]
const matchaValues = ref<Record<string, string>>({})

function syncLocalValues() {
  aliApiKey.value = currentProvider.value.ali_api_key || ""
  const mv: Record<string, string> = {}
  for (const k of matchaKeys) {
    mv[k] = currentProvider.value?.[`matcha_${k}`] || ""
  }
  matchaValues.value = mv
}

watch(activeTab, syncLocalValues, { immediate: true })

function updateProviderField(key: string, value: string, needReload = false) {
  const providers = [...(appStore.config.tts_provider?.providers || [])]
  const idx = providers.findIndex((p: any) => p.name === activeTab.value)
  if (idx >= 0) {
    providers[idx] = { ...providers[idx], [key]: value }
    updateConfigAndStore("tts_provider.providers", providers, needReload)
  }
}

function saveAliApiKey() {
  updateProviderField("ali_api_key", aliApiKey.value, true)
  ElMessage.success("已保存")
}

function saveMatchaValue(key: string) {
  updateProviderField(`matcha_${key}`, matchaValues.value[key], true)
  ElMessage.success("已保存")
}

async function onSetDefault(val: boolean) {
  if (val) {
    await updateConfigAndStore("tts_provider.provider", activeTab.value, true)
  }
}

const needsApiKey = computed(() =>
  ["cosyvoice", "sambert"].includes(activeTab.value)
)
const isMatcha = computed(() => activeTab.value === "MatchaTTS")

const engineDescription = computed(() => {
  const providers = appStore.config.tts_provider?.providers || []
  const p = providers.find((p: any) => p.name === activeTab.value)
  return p?.description || ""
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
        <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 8px">
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

          <div>
            <span style="font-size: 14px; margin-bottom: 4px; display: block">音色</span>
            <el-select
              :model-value="selectedVoice"
              @update:model-value="(v: string) => selectedVoice = v"
              filterable
              clearable
              style="width: 100%"
            >
              <el-option
                v-for="v in engineVoices"
                :key="v"
                :label="v"
                :value="v"
              />
            </el-select>
          </div>

          <div v-if="needsApiKey">
            <span style="font-size: 14px; margin-bottom: 4px; display: block">阿里 API Key</span>
            <div style="display: flex; align-items: center; gap: 8px">
              <el-input
                v-model="aliApiKey"
                type="password"
                show-password
                placeholder="请输入 API Key"
              />
              <el-icon v-if="aliApiKey !== (currentProvider.ali_api_key || '')"
                style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                @click="saveAliApiKey"><Check /></el-icon>
            </div>
          </div>

          <template v-if="isMatcha">
            <div v-for="key in matchaKeys" :key="key">
              <span style="font-size: 14px; margin-bottom: 4px; display: block">{{ key }}</span>
              <div style="display: flex; align-items: center; gap: 8px">
                <el-input
                  v-model="matchaValues[key]"
                  :placeholder="`请输入 ${key}`"
                />
                <el-icon v-if="matchaValues[key] !== (currentProvider[`matcha_${key}`] || '')"
                  style="cursor: pointer; color: var(--el-color-primary); font-size: 18px; flex-shrink: 0"
                  @click="saveMatchaValue(key)"><Check /></el-icon>
              </div>
            </div>
          </template>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
