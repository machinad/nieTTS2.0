<script setup lang="ts">
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import { appStore } from "../store"
import { postTTS, postConfig } from "../api"
import { wsManager } from "../ws"
import LogBar from "../components/LogBar.vue"

const router = useRouter()
const text = ref("")
const sourceLang = ref(appStore.langs.source)
const targetLang = ref(appStore.langs.target)

const isRecording = ref(false)
const canvasRef = ref<HTMLCanvasElement | null>(null)

let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let scriptNode: ScriptProcessorNode | null = null
let mediaStream: MediaStream | null = null
let unsubWs: (() => void) | null = null
let animFrame = 0
let freqData: Uint8Array<ArrayBuffer> | null = null

function draw() {
  const canvas = canvasRef.value
  if (!canvas || !analyser) return
  const ctx = canvas.getContext("2d")!
  const W = canvas.width
  const H = canvas.height

  if (!freqData) freqData = new Uint8Array(analyser.frequencyBinCount)
  analyser.getByteFrequencyData(freqData)

  ctx.clearRect(0, 0, W, H)

  const grad = ctx.createLinearGradient(0, H, 0, 0)
  grad.addColorStop(0, "#409EFF")
  grad.addColorStop(0.5, "#67c23a")
  grad.addColorStop(1, "#e6a23c")
  ctx.fillStyle = grad

  const barW = Math.max(2, (W / analyser.frequencyBinCount) * 2)
  for (let i = 0; i < freqData.length; i++) {
    const h = (freqData[i] / 255) * H
    const x = i * (barW + 1)
    ctx.fillRect(x, H - h, barW, h)
  }

  if (isRecording.value) {
    animFrame = requestAnimationFrame(draw)
  }
}

function cleanupAudio() {
  cancelAnimationFrame(animFrame)
  if (scriptNode) { scriptNode.disconnect(); scriptNode = null }
  if (audioContext) { audioContext.close(); audioContext = null }
  if (mediaStream) { mediaStream.getTracks().forEach(t => t.stop()); mediaStream = null }
  if (unsubWs) { unsubWs(); unsubWs = null }
  analyser = null
  freqData = null
}

async function startRecording() {
  try {
    const deviceId = localStorage.getItem("nietts_input_device_id")
    const constraints: MediaTrackConstraints = {
      sampleRate: 16000,
      channelCount: 1,
      echoCancellation: true,
      noiseSuppression: true,
    }
    if (deviceId) {
      constraints.deviceId = { exact: deviceId }
    }
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: constraints })
    audioContext = new AudioContext({ sampleRate: 16000 })
    const source = audioContext.createMediaStreamSource(mediaStream)

    analyser = audioContext.createAnalyser()
    analyser.fftSize = 256
    source.connect(analyser)

    scriptNode = audioContext.createScriptProcessor(4096, 1, 1)
    scriptNode.onaudioprocess = (event) => {
      const inputData = event.inputBuffer.getChannelData(0)
      const int16 = new Int16Array(inputData.length)
      for (let i = 0; i < inputData.length; i++) {
        const s = Math.max(-1, Math.min(1, inputData[i]))
        int16[i] = s < 0 ? s * 0x8000 : s * 0x7fff
      }
      wsManager.send(int16.buffer)
    }

    analyser.connect(scriptNode)
    scriptNode.connect(audioContext.destination)

    unsubWs = wsManager.onMessage(() => {})

    wsManager.send(JSON.stringify({ type: "start" }))
    isRecording.value = true
    animFrame = requestAnimationFrame(draw)
  } catch (e: any) {
    ElMessage.error(`无法访问麦克风: ${e.message}`)
  }
}

function stopRecording() {
  wsManager.send(JSON.stringify({ type: "stop" }))
  isRecording.value = false
  cleanupAudio()
}

function toggleRecording() {
  if (isRecording.value) { stopRecording() } else { startRecording() }
}

const sourceOptions = computed(() => appStore.voices.source_languages || [])
const targetOptions = computed(() => appStore.voices.target_languages || [])

const engineLabel = computed(() => {
  const engine = appStore.engine || "edge_tts"
  const voice = appStore.voice || ""
  return `${engine}${voice ? " / " + voice : ""}`
})

async function onSourceLangChange(lang: string) {
  sourceLang.value = lang
  appStore.langs.source = lang
  try { await postConfig({ source_lang: lang }) } catch (e: any) { ElMessage.error(`保存语言失败: ${e.message}`) }
}

async function onTargetLangChange(lang: string) {
  targetLang.value = lang
  appStore.langs.target = lang
  try { await postConfig({ target_lang: lang }) } catch (e: any) { ElMessage.error(`保存语言失败: ${e.message}`) }
}

async function onSend() {
  if (!text.value.trim()) { ElMessage.warning("请输入文本"); return }
  try {
    await postTTS({
      text: text.value,
      tts_provider: appStore.config.tts_provider?.provider || appStore.engine,
      voice: appStore.voice,
      translate: appStore.config.isTranslate,
      play_audio: appStore.config.isPlayAudio,
      play_translation: appStore.config.isPlayTranslation,
      osc_enabled: appStore.config.osc_enabled,
      source_lang: sourceLang.value,
      target_lang: targetLang.value,
    })
    text.value = ""
    ElMessage.success("已提交")
  } catch (e: any) { ElMessage.error(`发送失败: ${e.message}`) }
}

function onTextareaKeydown(e: KeyboardEvent) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault()
    onSend()
  }
}
</script>

<template>
  <div style="display: flex; flex-direction: column; gap: 16px">
    <el-input
      v-model="text"
      type="textarea"
      :autosize="{ minRows: 6, maxRows: 12 }"
      maxlength="5000"
      show-word-limit
      placeholder="请输入要合成的文本... (Enter 发送, Shift+Enter 换行)"
      @keydown="onTextareaKeydown"
    />

    <div style="display: flex; gap: 12px; align-items: center">
      <span style="font-size: 14px; white-space: nowrap; color: var(--el-text-color-secondary)">源语言</span>
      <el-select :model-value="sourceLang" @change="onSourceLangChange" style="flex: 1">
        <el-option v-for="lang in sourceOptions" :key="lang" :label="lang" :value="lang" />
      </el-select>
      <span style="font-size: 14px; white-space: nowrap; color: var(--el-text-color-secondary)">目标语言</span>
      <el-select :model-value="targetLang" @change="onTargetLangChange" style="flex: 1">
        <el-option v-for="lang in targetOptions" :key="lang" :label="lang" :value="lang" />
      </el-select>
    </div>

    <div style="display: flex; align-items: center; gap: 8px; cursor: pointer" @click="router.push('/settings')">
      <span style="font-size: 13px; color: var(--el-text-color-secondary)">当前引擎:</span>
      <el-tag size="small" type="info">{{ engineLabel }}</el-tag>
    </div>

    <div style="display: flex; gap: 12px">
      <el-button type="primary" @click="onSend" style="flex: 1">发送</el-button>
      <el-button :type="isRecording ? 'danger' : 'default'" @click="toggleRecording" style="flex: 1">
        {{ isRecording ? "停止录音" : "语音输入" }}
      </el-button>
    </div>

    <canvas
      v-show="isRecording"
      ref="canvasRef"
      width="600"
      height="80"
      style="width: 100%; height: 80px; border-radius: 4px; background: rgba(0,0,0,0.03)"
    />

    <LogBar />
  </div>
</template>
