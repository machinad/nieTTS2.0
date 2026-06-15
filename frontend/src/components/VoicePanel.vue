<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue"
import { ElMessage } from "element-plus"
import { wsManager } from "../ws"

const emit = defineEmits(["close"])

const BAR_COUNT = 32

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
  <div class="voice-panel">
    <!-- Record button -->
    <button
      class="rec-btn"
      :class="state === 'recording' ? 'rec-btn--active' : 'rec-btn--idle'"
      @click="state === 'idle' ? startRecording() : stopRecording()"
    >
      <div class="rec-btn__ring" />
      <div class="rec-btn__inner">
        <svg v-if="state === 'idle'" viewBox="0 0 24 24" fill="none" width="28" height="28">
          <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" fill="currentColor"/>
          <path d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" width="28" height="28">
          <rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"/>
        </svg>
      </div>
    </button>

    <!-- Waveform bars -->
    <div class="waveform">
      <div
        v-for="(h, i) in barHeights"
        :key="i"
        class="waveform__bar"
        :class="{ 'waveform__bar--active': state === 'recording' }"
        :style="{ height: h + 'px' }"
      />
    </div>

    <!-- Status text -->
    <div class="voice-status" :class="{ 'voice-status--recording': state === 'recording' }">
      <span v-if="state === 'recording'" class="voice-status__dot" />
      {{ state === 'recording' ? '录音中...' : '点击开始录音' }}
    </div>

    <button class="close-btn" @click="emit('close')">
      收起
    </button>
  </div>
</template>

<style scoped>
.voice-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

/* ---- Record button ---- */
.rec-btn {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-normal) var(--ease-out);
}

.rec-btn--idle {
  background: var(--accent);
  color: #ffffff;
  box-shadow: 0 4px 20px rgba(214, 96, 138, 0.25);
}
.rec-btn--idle:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 28px rgba(214, 96, 138, 0.35);
}

.rec-btn--active {
  background: var(--error);
  color: #fff;
  box-shadow: 0 4px 20px rgba(208, 72, 64, 0.25);
}
.rec-btn--active:hover {
  transform: scale(1.05);
}

.rec-btn__ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 2px solid transparent;
}
.rec-btn--active .rec-btn__ring {
  border-color: rgba(208, 72, 64, 0.25);
  animation: pulse-glow 1.5s ease-in-out infinite;
}

.rec-btn__inner {
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

/* ---- Waveform ---- */
.waveform {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 2px;
  height: 48px;
  width: 100%;
  max-width: 240px;
}

.waveform__bar {
  width: 4px;
  border-radius: 2px;
  background: var(--bg-hover);
  transition: height 0.05s linear, background var(--duration-fast) var(--ease-out);
  min-height: 2px;
}

.waveform__bar--active {
  background: var(--accent);
}

/* ---- Status ---- */
.voice-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.voice-status--recording {
  color: var(--error);
}

.voice-status__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--error);
  animation: pulse-glow 1s ease-in-out infinite;
}

/* ---- Close button ---- */
.close-btn {
  padding: 6px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--text-tertiary);
  font-family: var(--font-body);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.close-btn:hover {
  border-color: var(--border-default);
  color: var(--text-secondary);
  background: var(--bg-elevated);
}
</style>
