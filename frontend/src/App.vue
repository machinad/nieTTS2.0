<script setup lang="ts">
import { onMounted } from "vue"
import { getConfig } from "./api"
import { wsManager } from "./ws"
import { addLog } from "./store"
import AppLayout from "./components/AppLayout.vue"

onMounted(async () => {
  try {
    await getConfig()
  } catch (e: any) {
    addLog("error", `获取配置失败: ${e.message}`)
  }

  wsManager.onMessage((msg) => {
    if (msg.type === "log") {
      addLog(msg.level || "info", msg.message || "")
    } else if (msg.type === "status") {
      addLog("info", `请求 ${msg.request_id || ""} ${msg.state || ""}`)
    } else if (msg.type === "config_changed") {
      getConfig()
    }
  })

  wsManager.connect()
})
</script>

<template>
  <AppLayout />
</template>
