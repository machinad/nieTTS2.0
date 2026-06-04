import { appStore, settingsTab } from "./store"

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

export async function getConfig() {
  const data = await request<import("./store").AppConfig>("/config")
  appStore.config = data
  // 初始化 settings tab 状态（仅首次）
  if (!settingsTab.tts) {
    settingsTab.tts = data.tts_provider?.provider || "edge_tts"
  }
  if (!settingsTab.stt) {
    settingsTab.stt = data.stt_provider?.provider || "Qwen3"
  }
  if (!settingsTab.translate) {
    settingsTab.translate = data.translation_provider?.provider || ""
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

export async function postReload() {
  return request<{ success: boolean }>("/config/reload", {
    method: "POST",
  })
}

export async function postTTS(params: Record<string, any>) {
  const data = await request<{ request_id: string }>("/tts", {
    method: "POST",
    body: JSON.stringify(params),
  })
  return data
}
