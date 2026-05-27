import { appStore } from "./store"

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error((body as any).error || `HTTP ${res.status}`)
  }
  return res.json()
}

export async function getVoices() {
  const data = await request<import("./store").VoiceData>("/voices")
  appStore.voices = data
  if (data.tts_engines.length > 0) {
    const engine = data.tts_engines[0]
    const voiceList = data.voices[engine]
    if (voiceList && voiceList.length > 0) {
      appStore.voice = voiceList[0]
    }
  }
  return data
}

export async function getConfig() {
  const data = await request<Record<string, any>>("/config")
  appStore.config = data
  if (data.tts_provider) {
    appStore.engine = data.tts_provider.provider || "edge_tts"
    const providers = data.tts_provider.providers || []
    const active = providers.find(
      (p: any) => p.name === data.tts_provider.provider
    )
    if (active?.voice) appStore.voice = active.voice
  }
  if (data.target_lang) {
    appStore.langs.target = data.target_lang
  }
  return data
}

export async function postConfig(partial: Record<string, any>) {
  const data = await request<{ success: boolean }>("/config", {
    method: "POST",
    body: JSON.stringify(partial),
  })
  return data
}

export async function postTTS(params: Record<string, any>) {
  const data = await request<{ request_id: string }>("/tts", {
    method: "POST",
    body: JSON.stringify(params),
  })
  return data
}
