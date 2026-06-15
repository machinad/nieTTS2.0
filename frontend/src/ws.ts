import { appStore, addLog } from "./store"
import type { WSMessage } from "./store"

type MessageHandler = (msg: WSMessage) => void

class WSManager {
  private ws: WebSocket | null = null
  private handlers = new Set<MessageHandler>()
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private reconnectDelay = 3000
  private _cleanedUp = false
  connected = false

  connect() {
    if (this.ws) return
    this._cleanedUp = false

    const protocol = location.protocol === "https:" ? "wss:" : "ws:"
    const url = `${protocol}//${location.host}/ws`

    try {
      this.ws = new WebSocket(url)
      this.ws.binaryType = "arraybuffer"

      this.ws.onopen = () => {
        this.connected = true
        appStore.wsConnected = true
        this.reconnectDelay = 3000
        addLog("info", "WebSocket 已连接")
      }

      this.ws.onclose = () => {
        this.connected = false
        appStore.wsConnected = false
        if (!this._cleanedUp) {
          addLog("warn", "WebSocket 已断开，尝试重连...")
          this.scheduleReconnect()
        }
      }

      this.ws.onerror = () => {
        addLog("error", "WebSocket 连接错误")
      }

      this.ws.onmessage = (event) => {
        if (typeof event.data === "string") {
          try {
            const msg = JSON.parse(event.data) as WSMessage
            this.handlers.forEach((fn) => fn(msg))
          } catch {
            // ignore parse errors
          }
        }
      }
    } catch {
      addLog("error", "WebSocket 连接失败")
      this.scheduleReconnect()
    }
  }

  private scheduleReconnect() {
    if (this._cleanedUp) return
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer)
    this.reconnectTimer = setTimeout(() => {
      this.connect()
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000)
    }, this.reconnectDelay)
  }

  disconnect() {
    this._cleanedUp = true
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.connected = false
    appStore.wsConnected = false
  }

  onMessage(fn: MessageHandler): () => void {
    this.handlers.add(fn)
    return () => this.handlers.delete(fn)
  }

  send(data: string | ArrayBuffer) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(data)
    }
  }
}

export const wsManager = new WSManager()
