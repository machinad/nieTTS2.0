<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import { ElMessage } from "element-plus"
import { getModelsStatus, postModelsDownload } from "../api"
import { wsManager } from "../ws"
import type { WSMessage } from "../store"

interface EngineStatus {
  engine: string
  total: number
  ok: number
}

const source = ref("huggingface_mirror")
const downloading = ref(false)
const engines = ref<EngineStatus[]>([])
let cleanupWs: (() => void) | null = null

async function loadStatus() {
  try {
    engines.value = await getModelsStatus()
  } catch {
    // ignore
  }
}

async function startDownload() {
  downloading.value = true
  try {
    await postModelsDownload(source.value)
    ElMessage.info("开始下载模型，进度请查看日志页面")
  } catch (e: any) {
    ElMessage.error("启动下载失败: " + (e.message || e))
    downloading.value = false
  }
}

function onWsMessage(msg: WSMessage) {
  if (msg.type === "download_done") {
    downloading.value = false
    if (msg.ok !== undefined && msg.ok >= 0) {
      ElMessage.success(`模型下载完成: ${msg.ok} 成功, ${msg.fail} 失败`)
    } else {
      ElMessage.error("模型下载异常，请查看日志")
    }
    setTimeout(() => loadStatus(), 500)
  }
}

onMounted(() => {
  downloading.value = false
  loadStatus()
  cleanupWs = wsManager.onMessage(onWsMessage)
})

onUnmounted(() => {
  cleanupWs?.()
})
</script>

<template>
  <div style="display: flex; flex-direction: column; gap: 16px">
    <el-card>
      <template #header>下载源</template>
      <el-radio-group v-model="source" style="display: flex; flex-direction: column; gap: 8px">
        <el-radio value="huggingface">HuggingFace 官方源</el-radio>
        <el-radio value="huggingface_mirror">HuggingFace 镜像源（国内推荐）</el-radio>
        <el-radio value="modelscope">ModelScope 源（国内推荐）</el-radio>
      </el-radio-group>
    </el-card>

    <el-button type="primary" :loading="downloading" @click="startDownload">
      {{ downloading ? "下载中..." : "开始下载" }}
    </el-button>

    <el-card>
      <template #header>引擎状态</template>
      <div style="display: flex; flex-direction: column; gap: 8px">
        <div
          v-for="e in engines"
          :key="e.engine"
          style="display: flex; justify-content: space-between; align-items: center"
        >
          <span>{{ e.engine }}</span>
          <el-tag :type="e.ok === e.total ? 'success' : e.ok > 0 ? 'warning' : 'info'" size="small">
            {{ e.ok }} / {{ e.total }}
          </el-tag>
        </div>
        <div v-if="engines.length === 0" style="color: #909399; font-size: 13px">加载中...</div>
      </div>
    </el-card>
  </div>
</template>
