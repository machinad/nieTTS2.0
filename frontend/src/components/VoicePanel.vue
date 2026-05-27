<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue"
import { ElMessage } from "element-plus"
import { wsManager } from "../ws"

const emit = defineEmits(["close"])

const BAR_COUNT = 24

const state = ref<"idle" | "recording">("idle")
const audioLevel = ref(0)
const barHeights = ref<number[]>(Array.from({ length: BAR_COUNT }, () => 2))

let audioContext: AudioContext | null = null
let scriptNode: ScriptProcessorNode | null = null
let mediaStream: MediaStream | null = null
let unsubWs: (() => void) | null = null
let animFrame = 0
let lastLevel = 0

function updateBars() {
  const target = audioLevel.value
  lastLevel = lastLevel * 0.7 + target * 0.3
  const heights: number[] = []
  for (let i = 0; i < BAR_COUNT; i++) {
    const seed = Math.sin(i * 0.7 + Date.now() * 0.005) * 0.5 + 0.5
    const h = Math.max(2, (lastLevel * 40 + seed * 8) * (state.value === "recording" ? 1 : 0.15))
    heights.push(h)
  }
  barHeights.value = heights
  if (state.value === "recording") {
    animFrame = requestAnimationFrame(updateBars)
  }
}

async function startRecording() {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: 16000,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      },
    })

    audioContext = new AudioContext({ sampleRate: 16000 })
    const source = audioContext.createMediaStreamSource(mediaStream)

    scriptNode = audioContext.createScriptProcessor(4096, 1, 1)
    scriptNode.onaudioprocess = (event) => {
      const inputData = event.inputBuffer.getChannelData(0)
      let sum = 0
      for (let i = 0; i < inputData.length; i++) {
        sum += Math.abs(inputData[i])
      }
      audioLevel.value = sum / inputData.length

      const int16 = new Int16Array(inputData.length)
      for (let i = 0; i < inputData.length; i++) {
        const s = Math.max(-1, Math.min(1, inputData[i]))
        int16[i] = s < 0 ? s * 0x8000 : s * 0x7fff
      }
      wsManager.send(int16.buffer)
    }

    source.connect(scriptNode)
    scriptNode.connect(audioContext.destination)

    unsubWs = wsManager.onMessage((msg) => {
      if (msg.type === "stt_result" && msg.text) {
        // STT result handled by backend pipeline silently
      }
    })

    wsManager.send(JSON.stringify({ type: "start" }))
    state.value = "recording"
    animFrame = requestAnimationFrame(updateBars)
  } catch (e: any) {
    ElMessage.error(`无法访问麦克风: ${e.message}`)
  }
}

function stopRecording() {
  cancelAnimationFrame(animFrame)
  wsManager.send(JSON.stringify({ type: "stop" }))
  state.value = "idle"
  barHeights.value = Array.from({ length: BAR_COUNT }, () => 2)

  if (scriptNode) {
    scriptNode.disconnect()
    scriptNode = null
  }
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }
  if (mediaStream) {
    mediaStream.getTracks().forEach((t) => t.stop())
    mediaStream = null
  }
  if (unsubWs) {
    unsubWs()
    unsubWs = null
  }
}

onBeforeUnmount(() => {
  cancelAnimationFrame(animFrame)
  if (state.value === "recording") {
    stopRecording()
  }
})
</script>

<template>
  <div
    style="
      border: 1px solid var(--el-border-color-light);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    "
  >
    <el-button
      v-if="state === 'idle'"
      circle
      size="large"
      style="width: 72px; height: 72px; background-color: #f56c6c; border: none; animation: voice-pulse 2s infinite"
      @click="startRecording"
    >
      <span style="color: #fff; font-size: 28px">🎤</span>
    </el-button>

    <el-button
      v-if="state === 'recording'"
      circle
      size="large"
      style="width: 72px; height: 72px; background-color: #e6a23c; border: none"
      @click="stopRecording"
    >
      <span style="color: #fff; font-size: 28px">⏹</span>
    </el-button>

    <!-- Waveform bars -->
    <div
      style="
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 2px;
        height: 48px;
        width: 100%;
        max-width: 200px;
      "
    >
      <div
        v-for="(h, i) in barHeights"
        :key="i"
        :style="{
          width: '4px',
          height: h + 'px',
          borderRadius: '2px',
          backgroundColor: state === 'recording' ? '#409EFF' : '#c0c4cc',
          transition: 'height 0.05s linear',
          minHeight: '2px',
        }"
      />
    </div>

    <el-button size="small" @click="emit('close')">收起</el-button>
  </div>
</template>

<style scoped>
@keyframes voice-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.5);
  }
  70% {
    box-shadow: 0 0 0 16px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}
</style>
