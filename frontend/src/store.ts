import { reactive } from "vue"

export interface LogEntry {
  time: string
  level: "info" | "warn" | "error"
  message: string
}

export interface WSMessage {
  type: "stt_result" | "status" | "log"
  text?: string
  request_id?: string
  state?: "queued" | "processing" | "playing" | "done"
  level?: "info" | "warn" | "error"
  message?: string
}

export interface VoiceData {
  tts_engines: string[]
  all_tts_engines: string[]
  translate_engines: string[]
  stt_engines: string[]
  voices: Record<string, string[]>
  source_languages: string[]
  target_languages: string[]
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
  target_lang: string
  isPlayAudio: boolean
  isTranslate: boolean
  isPlayTranslation: boolean
  osc_enabled: boolean
  osc_host: string
  osc_port: number
  vad: Record<string, number>
  ali_api_key: string
  available_devices: { name: string }[]
}

export const appStore = reactive({
  engine: "edge_tts",
  voice: "",
  langs: { source: "中文", target: "英语" },
  config: {} as Record<string, any>,
  voices: {
    tts_engines: [],
    all_tts_engines: [],
    translate_engines: [],
    stt_engines: [],
    voices: {},
    source_languages: [],
    target_languages: [],
  } as VoiceData,
  logs: [] as LogEntry[],
  wsConnected: false,
})

export function addLog(level: LogEntry["level"], message: string) {
  const d = new Date()
  appStore.logs.push({
    time: d.toTimeString().slice(0, 8),
    level,
    message,
  })
  if (appStore.logs.length > 500) appStore.logs.shift()
}
