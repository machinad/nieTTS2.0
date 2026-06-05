<script setup lang="ts">
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import { appStore, getActiveEngine, getActiveVoice, getSourceLang, getTargetLang, addLog } from "../store"
import { postTTS, postConfig } from "../api"
import { wsManager } from "../ws"
import LogBar from "../components/LogBar.vue"

const router = useRouter()
const text = ref("")

const isRecording = ref(false)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const showVoicePanel = ref(false)

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

  const barCount = Math.min(freqData.length, 64)
  const barW = Math.max(3, (W / barCount) * 0.7)
  const gap = (W - barCount * barW) / (barCount - 1)

  for (let i = 0; i < barCount; i++) {
    const h = Math.max(2, (freqData[i] / 255) * H * 0.9)
    const x = i * (barW + gap)
    const y = H - h

    const grad = ctx.createLinearGradient(x, y, x, H)
    grad.addColorStop(0, "rgba(214, 96, 138, 0.9)")
    grad.addColorStop(1, "rgba(214, 96, 138, 0.2)")
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.roundRect(x, y, barW, h, [2, 2, 0, 0])
    ctx.fill()
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
    showVoicePanel.value = true
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

const sourceOptions = computed(() => appStore.config.source_languages || [])
const targetOptions = computed(() => appStore.config.target_languages || [])

const engineLabel = computed(() => {
  const engine = getActiveEngine()
  const voice = getActiveVoice()
  return `${engine}${voice ? " / " + voice : ""}`
})

async function onSourceLangChange(lang: string) {
  appStore.config.source_lang = lang
  try { await postConfig({ source_lang: lang }) } catch (e: any) { ElMessage.error(`保存语言失败: ${e.message}`) }
}

async function onTargetLangChange(lang: string) {
  appStore.config.target_lang = lang
  try { await postConfig({ target_lang: lang }) } catch (e: any) { ElMessage.error(`保存语言失败: ${e.message}`) }
}

function onSend() {
  const payload = {
    text: text.value,
    tts_provider: getActiveEngine(),
    voice: getActiveVoice(),
    translate: appStore.config.isTranslate,
    play_audio: appStore.config.isPlayAudio,
    play_translation: appStore.config.isPlayTranslation,
    osc_enabled: appStore.config.osc_enabled,
    source_lang: getSourceLang(),
    target_lang: getTargetLang(),
  }
  if (!payload.text.trim()) { ElMessage.warning("请输入文本"); return }
  text.value = ""
  ElMessage.success("已提交")
  postTTS(payload).catch((e: any) => {
    addLog("error", `发送失败: ${e.message}`)
  })
}

function onTextareaKeydown(e: KeyboardEvent) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault()
    onSend()
  }
}
</script>

<template>
  <div class="home">
    <!-- Text input section -->
    <div class="editor">
      <div class="editor__header">
        <div class="editor__tab">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>文本输入</span>
        </div>
        <span class="editor__char-count">{{ text.length }} / 5000</span>
      </div>
      <textarea
        v-model="text"
        class="editor__textarea"
        placeholder="输入要合成的文本...&#10;&#10;Enter 发送 · Shift+Enter 换行"
        maxlength="5000"
        rows="8"
        @keydown="onTextareaKeydown"
      />
    </div>

    <!-- Language selector -->
    <div class="lang-row">
      <div class="lang-field">
        <label class="lang-field__label">源语言</label>
        <el-select :model-value="getSourceLang()" @change="onSourceLangChange" size="default" style="width: 100%">
          <el-option v-for="lang in sourceOptions" :key="lang" :label="lang" :value="lang" />
        </el-select>
      </div>
      <div class="lang-arrow">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M5 12h14m-4-4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="lang-field">
        <label class="lang-field__label">目标语言</label>
        <el-select :model-value="getTargetLang()" @change="onTargetLangChange" size="default" style="width: 100%">
          <el-option v-for="lang in targetOptions" :key="lang" :label="lang" :value="lang" />
        </el-select>
      </div>
    </div>

    <!-- Engine info -->
    <button class="engine-badge" @click="router.push('/settings')">
      <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
        <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      <span class="engine-badge__label">引擎</span>
      <span class="engine-badge__value">{{ engineLabel }}</span>
      <svg viewBox="0 0 24 24" fill="none" width="12" height="12">
        <path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Actions -->
    <div class="actions">
      <button class="btn btn--primary" @click="onSend">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>发送合成</span>
      </button>
      <button
        class="btn"
        :class="isRecording ? 'btn--danger' : 'btn--secondary'"
        @click="toggleRecording"
      >
        <svg v-if="!isRecording" viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" width="18" height="18">
          <rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"/>
        </svg>
        <span>{{ isRecording ? "停止录音" : "语音输入" }}</span>
      </button>
    </div>

    <!-- Waveform visualizer -->
    <Transition name="expand">
      <div v-show="isRecording" class="visualizer">
        <canvas
          ref="canvasRef"
          width="600"
          height="80"
          class="visualizer__canvas"
        />
        <div class="visualizer__label">
          <span class="visualizer__pulse" />
          录音中...
        </div>
      </div>
    </Transition>

    <!-- Logs -->
    <LogBar />
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
  animation: fadeInUp 400ms var(--ease-out) both;
}

/* ---- Editor ---- */
.editor {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color var(--duration-fast) var(--ease-out);
}
.editor:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-muted);
}

.editor__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.editor__tab {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.editor__char-count {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-tertiary);
}

.editor__textarea {
  width: 100%;
  min-height: 180px;
  max-height: 320px;
  padding: 16px;
  border: none;
  outline: none;
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.7;
  resize: vertical;
}
.editor__textarea::placeholder {
  color: var(--text-tertiary);
}

/* ---- Language row ---- */
.lang-row {
  display: flex;
  align-items: flex-end;
  gap: var(--sp-3);
}

.lang-field {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.lang-field__label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
}

.lang-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 8px;
  color: var(--text-tertiary);
}

/* ---- Engine badge ---- */
.engine-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  font-family: var(--font-body);
  color: var(--text-secondary);
  font-size: 13px;
}
.engine-badge:hover {
  border-color: var(--border-default);
  background: var(--bg-elevated);
}

.engine-badge__label {
  color: var(--text-tertiary);
}

.engine-badge__value {
  flex: 1;
  color: var(--text-primary);
  font-weight: 500;
  font-family: var(--font-mono);
  font-size: 13px;
}

/* ---- Actions ---- */
.actions {
  display: flex;
  gap: var(--sp-3);
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-default);
  background: var(--bg-elevated);
  color: var(--text-secondary);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.btn:hover {
  background: var(--bg-hover);
  border-color: var(--border-strong);
  color: var(--text-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}
.btn:active {
  transform: translateY(0);
}

.btn--primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #ffffff;
}
.btn--primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: #ffffff;
  box-shadow: var(--shadow-glow);
}

.btn--danger {
  background: var(--error);
  border-color: var(--error);
  color: #fff;
}
.btn--danger:hover {
  background: #c04440;
  border-color: #c04440;
  color: #fff;
}

.btn--secondary {
  background: var(--bg-surface);
  border-color: var(--border-default);
  color: var(--text-secondary);
}

/* ---- Visualizer ---- */
.visualizer {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.visualizer__canvas {
  width: 100%;
  height: 80px;
  border-radius: var(--radius-sm);
}

.visualizer__label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--error);
  font-weight: 500;
}

.visualizer__pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--error);
  animation: pulse-glow 1.5s ease-in-out infinite;
}

/* ---- Expand transition ---- */
.expand-enter-active {
  transition: all 300ms var(--ease-out);
}
.expand-leave-active {
  transition: all 200ms var(--ease-out);
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-8px);
  max-height: 0;
}

@media (max-width: 768px) {
  .lang-row {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
    align-items: flex-end;
  }
  .lang-arrow {
    display: none;
  }
  .lang-field {
    flex: 1 1 0;
    min-width: 0;
  }
  .actions {
    flex-direction: column;
  }
}
</style>
