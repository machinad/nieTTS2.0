<script setup lang="ts">
import { computed } from "vue"
import { ElMessage } from "element-plus"
import { appStore } from "../store"
import { postConfig, getConfig } from "../api"

const sttProvider = computed(() => appStore.config.stt_provider)
const sttName = computed(() => sttProvider.value?.provider || "未配置")
const sttConfig = computed(() => {
  const providers = sttProvider.value?.providers || []
  return providers.find((p: any) => p.name === sttName.value) || {}
})

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
  <div style="display: flex; flex-direction: column; gap: 16px">
    <el-card>
      <template #header>STT 引擎</template>
      <p>当前引擎: <el-tag>{{ sttName }}</el-tag></p>
    </el-card>

    <el-card v-if="Object.keys(sttConfig).length > 0">
      <template #header>模型路径（只读）</template>
      <div style="display: flex; flex-direction: column; gap: 8px">
        <div v-for="field in modelFields" :key="field.key" style="display: flex; align-items: center; gap: 8px">
          <span style="width: 120px; font-size: 14px">{{ field.label }}:</span>
          <el-input
            :model-value="sttConfig[field.key] || ''"
            disabled
            style="flex: 1"
          />
        </div>
      </div>
    </el-card>

    <el-card>
      <template #header>VAD 参数</template>
      <div style="display: flex; flex-direction: column; gap: 12px">
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
    </el-card>
  </div>
</template>
