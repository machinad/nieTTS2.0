<script setup lang="ts">
import { computed } from "vue"
import { ElMessage } from "element-plus"
import { appStore, settingsTab } from "../store"
import { postConfig, getConfig } from "../api"
import { updateConfigAndStore } from "../useConfig"

const activeTab = computed({
  get: () => settingsTab.stt,
  set: (v: string) => { settingsTab.stt = v },
})

const engines = computed(() => (appStore.config.stt_provider?.providers || []).map((p: any) => p.name))

const sttProvider = computed(() => appStore.config.stt_provider)
const currentConfig = computed(() => {
  const providers = sttProvider.value?.providers || []
  return providers.find((p: any) => p.name === activeTab.value) || {}
})

const engineDescription = computed(() => {
  const providers = appStore.config.stt_provider?.providers || []
  const p = providers.find((p: any) => p.name === activeTab.value)
  return p?.description || ""
})

const isDefault = computed(() => sttProvider.value?.provider === activeTab.value)

async function onSetDefault(val: boolean) {
  if (val) {
    await updateConfigAndStore("stt_provider.provider", activeTab.value, true)
  }
}

const modelFields = [
  { key: "conv_frontend", label: "Conv Frontend" },
  { key: "encoder", label: "Encoder" },
  { key: "decoder", label: "Decoder" },
  { key: "tokenizer", label: "Tokenizer" },
]

const vad = computed(() => appStore.config.vad || {})

async function onVadChange(key: string, value: number) {
  const currentVad = { ...appStore.config.vad }
  currentVad[key] = value
  try {
    await postConfig({ vad: currentVad })
    await getConfig()
  } catch (e: any) {
    ElMessage.error(`保存失败: ${e.message}`)
  }
}
</script>

<template>
  <div class="stt-settings">
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

          <template v-if="Object.keys(currentConfig).length > 1">
            <div class="section-title">模型路径</div>
            <div v-for="field in modelFields" :key="field.key" class="model-row">
              <span class="model-row__label">{{ field.label }}</span>
              <el-input :model-value="currentConfig[field.key] || ''" disabled />
            </div>
          </template>

          <div class="section-title">VAD 参数</div>
          <div class="vad-grid">
            <div class="vad-field">
              <span class="vad-field__label">Threshold</span>
              <span class="vad-field__range">0 — 1</span>
              <el-input-number
                :model-value="vad.threshold"
                :min="0"
                :max="1"
                :step="0.05"
                @change="(v: any) => onVadChange('threshold', v)"
              />
            </div>
            <div class="vad-field">
              <span class="vad-field__label">Min Silence</span>
              <span class="vad-field__range">秒</span>
              <el-input-number
                :model-value="vad.min_silence_duration"
                :min="0"
                :max="10"
                :step="0.05"
                @change="(v: any) => onVadChange('min_silence_duration', v)"
              />
            </div>
            <div class="vad-field">
              <span class="vad-field__label">Min Speech</span>
              <span class="vad-field__range">秒</span>
              <el-input-number
                :model-value="vad.min_speech_duration"
                :min="0"
                :max="10"
                :step="0.05"
                @change="(v: any) => onVadChange('min_speech_duration', v)"
              />
            </div>
            <div class="vad-field">
              <span class="vad-field__label">Max Speech</span>
              <span class="vad-field__range">秒</span>
              <el-input-number
                :model-value="vad.max_speech_duration"
                :min="0"
                :max="60"
                :step="0.5"
                @change="(v: any) => onVadChange('max_speech_duration', v)"
              />
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.stt-settings {
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

.section-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-tertiary);
  padding-top: 4px;
}

.model-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.model-row__label {
  width: 120px;
  font-size: 14px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.vad-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.vad-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.vad-field__label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.vad-field__range {
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-tertiary);
}

@media (max-width: 640px) {
  .vad-grid {
    grid-template-columns: 1fr;
  }
}
</style>
