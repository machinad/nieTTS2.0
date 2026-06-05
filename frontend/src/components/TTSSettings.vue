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
  <div class="tts-settings">
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

          <div class="field">
            <label class="field__label">音色</label>
            <el-select
              :model-value="selectedVoice"
              @update:model-value="(v: string) => selectedVoice = v"
              filterable
              clearable
              style="width: 100%"
            >
              <el-option v-for="v in engineVoices" :key="v" :label="v" :value="v" />
            </el-select>
          </div>

          <div v-if="needsApiKey" class="field">
            <label class="field__label">阿里 API Key</label>
            <div class="field__input-row">
              <el-input v-model="aliApiKey" type="password" show-password placeholder="请输入 API Key" />
              <button v-if="aliApiKey !== (currentProvider.ali_api_key || '')" class="save-icon" @click="saveAliApiKey">
                <el-icon><Check /></el-icon>
              </button>
            </div>
          </div>

          <template v-if="isMatcha">
            <div v-for="key in matchaKeys" :key="key" class="field">
              <label class="field__label">{{ key }}</label>
              <div class="field__input-row">
                <el-input v-model="matchaValues[key]" :placeholder="`请输入 ${key}`" />
                <button v-if="matchaValues[key] !== (currentProvider[`matcha_${key}`] || '')" class="save-icon" @click="saveMatchaValue(key)">
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
.tts-settings {
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
