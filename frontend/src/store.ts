import { reactive } from "vue"

export interface LogEntry {
  time: string
  level: "info" | "warn" | "error"
  message: string
}

export interface WSMessage {
  type: "stt_result" | "status" | "log" | "download_done" | "config_changed"
  text?: string
  request_id?: string
  state?: "queued" | "processing" | "playing" | "done"
  level?: "info" | "warn" | "error"
  message?: string
  ok?: number
  fail?: number
}

export interface ProviderConfig {
  name: string
  voice: string
  [key: string]: any
}

export interface AppConfig {
  tts_provider: { provider: string; providers: ProviderConfig[] }
  stt_provider: { provider: string; providers: any[] }
  translation_provider: { provider: string; providers: any[] }
  device: string
  source_lang: string
  target_lang: string
  isPlayAudio: boolean
  isTranslate: boolean
  isPlayTranslation: boolean
  osc_enabled: boolean
  osc_host: string
  osc_port: number
  port: number
  vad: Record<string, number>
  available_devices: { name: string }[]
  voices: Record<string, string[]>
  source_languages: string[]
  target_languages: string[]
  [key: string]: any
}

export const appStore = reactive({
  config: {} as AppConfig,
  logs: [] as LogEntry[],
  wsConnected: false,
})

// Settings tab 状态（跨页面保持）
export const settingsTab = reactive({
  tts: "",
  stt: "",
  translate: "",
})

// ---- Computed getters: config 是唯一真实来源 ----

export function getActiveEngine(): string {
  return appStore.config?.tts_provider?.provider || "edge_tts"
}

export function getActiveVoice(): string {
  const provider = appStore.config?.tts_provider?.provider || "edge_tts"
  const providers = appStore.config?.tts_provider?.providers || []
  const active = providers.find((p: ProviderConfig) => p.name === provider)
  return active?.voice || ""
}

export function getSourceLang(): string {
  return appStore.config?.source_lang || "中文"
}

export function getTargetLang(): string {
  return appStore.config?.target_lang || "英语"
}

export function addLog(level: LogEntry["level"], message: string) {
  const d = new Date()
  appStore.logs.push({
    time: d.toTimeString().slice(0, 8),
    level,
    message,
  })
  if (appStore.logs.length > 500) appStore.logs.shift()
}
