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
    await updateConfigAndStore("stt_provider.provider", activeTab.value)
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

          <template v-if="Object.keys(currentConfig).length > 1">
            <div style="font-size: 14px; color: var(--el-text-color-secondary); margin-top: 4px">模型路径</div>
            <div v-for="field in modelFields" :key="field.key" style="display: flex; align-items: center; gap: 8px">
              <span style="width: 120px; font-size: 14px">{{ field.label }}</span>
              <el-input
                :model-value="currentConfig[field.key] || ''"
                disabled
                style="flex: 1"
              />
            </div>
          </template>

          <div style="font-size: 14px; color: var(--el-text-color-secondary); margin-top: 4px">VAD 参数</div>
          <div style="display: flex; align-items: center; gap: 8px">
            <span style="width: 180px; font-size: 14px">Threshold (0-1)</span>
            <el-input-number
              :model-value="vad.threshold"
              :min="0"
              :max="1"
              :step="0.05"
              @change="(v: any) => onVadChange('threshold', v)"
            />
          </div>
          <div style="display: flex; align-items: center; gap: 8px">
            <span style="width: 180px; font-size: 14px">Min Silence (s)</span>
            <el-input-number
              :model-value="vad.min_silence_duration"
              :min="0"
              :max="10"
              :step="0.05"
              @change="(v: any) => onVadChange('min_silence_duration', v)"
            />
          </div>
          <div style="display: flex; align-items: center; gap: 8px">
            <span style="width: 180px; font-size: 14px">Min Speech (s)</span>
            <el-input-number
              :model-value="vad.min_speech_duration"
              :min="0"
              :max="10"
              :step="0.05"
              @change="(v: any) => onVadChange('min_speech_duration', v)"
            />
          </div>
          <div style="display: flex; align-items: center; gap: 8px">
            <span style="width: 180px; font-size: 14px">Max Speech (s)</span>
            <el-input-number
              :model-value="vad.max_speech_duration"
              :min="0"
              :max="60"
              :step="0.5"
              @change="(v: any) => onVadChange('max_speech_duration', v)"
            />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
