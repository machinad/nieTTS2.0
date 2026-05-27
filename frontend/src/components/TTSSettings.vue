<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { updateConfigAndStore } from "../useConfig"
import { appStore } from "../store"

const activeTab = ref("edge_tts")

const engines = computed(() => {
  return appStore.voices.all_tts_engines || []
})

const engineVoices = computed(() => {
  const voices = (appStore.voices as any)?.voices || {}
  return (voices[activeTab.value] || []) as string[]
})

const isDefault = computed(() => {
  return appStore.config.tts_provider?.provider === activeTab.value
})

const currentProvider = computed(() => {
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

const aliApiKey = computed({
  get: () => currentProvider.value.ali_api_key || "",
  set: (val: string) => {
    const providers = [...(appStore.config.tts_provider?.providers || [])]
    const idx = providers.findIndex((p: any) => p.name === activeTab.value)
    if (idx >= 0) {
      providers[idx] = { ...providers[idx], ali_api_key: val }
      updateConfigAndStore("tts_provider.providers", providers)
    }
  },
})

const matchaKeys = ["acoustic_model", "vocoder", "tokens", "lexicon", "data_dir", "dict_dir"]

function matchaValue(key: string) {
  return computed({
    get: () => currentProvider.value?.[`matcha_${key}`] || "",
    set: (val: string) => {
      const providers = [...(appStore.config.tts_provider?.providers || [])]
      const idx = providers.findIndex((p: any) => p.name === activeTab.value)
      if (idx >= 0) {
        providers[idx] = { ...providers[idx], [`matcha_${key}`]: val }
        updateConfigAndStore("tts_provider.providers", providers)
      }
    },
  })
}

async function onSetDefault(val: boolean) {
  if (val) {
    await updateConfigAndStore("tts_provider.provider", activeTab.value)
  }
}

const needsApiKey = computed(() =>
  ["cosyvoice", "sambert"].includes(activeTab.value)
)
const isMatcha = computed(() => activeTab.value === "MatchaTTS")
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
            <el-input
              :model-value="aliApiKey"
              @update:model-value="(v: string) => aliApiKey = v"
              type="password"
              show-password
              placeholder="请输入 API Key"
            />
          </div>

          <template v-if="isMatcha">
            <div v-for="key in matchaKeys" :key="key">
              <span style="font-size: 14px; margin-bottom: 4px; display: block">{{ key }}</span>
              <el-input
                :model-value="matchaValue(key).value"
                @update:model-value="(v: string) => matchaValue(key).value = v"
                :placeholder="`请输入 ${key}`"
              />
            </div>
          </template>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
