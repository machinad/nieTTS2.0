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

function progressPercent(e: EngineStatus) {
  return e.total > 0 ? Math.round((e.ok / e.total) * 100) : 0
}

function progressClass(e: EngineStatus) {
  const pct = progressPercent(e)
  if (pct === 100) return "progress--done"
  if (pct > 0) return "progress--partial"
  return "progress--empty"
}
</script>

<template>
  <div class="download-settings">
    <!-- Source selection -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>下载源</span>
      </div>
      <div class="source-list">
        <label v-for="opt in [
          { value: 'huggingface', label: 'HuggingFace 官方源' },
          { value: 'huggingface_mirror', label: 'HuggingFace 镜像源（国内推荐）' },
          { value: 'modelscope', label: 'ModelScope 源（国内推荐）' },
        ]" :key="opt.value" class="source-option" :class="{ 'source-option--active': source === opt.value }">
          <input type="radio" v-model="source" :value="opt.value" class="source-option__radio" />
          <span class="source-option__indicator" />
          <span class="source-option__label">{{ opt.label }}</span>
        </label>
      </div>
    </div>

    <!-- Download button -->
    <button class="download-btn" :class="{ 'download-btn--loading': downloading }" @click="startDownload" :disabled="downloading">
      <svg v-if="!downloading" viewBox="0 0 24 24" fill="none" width="20" height="20">
        <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <div v-else class="download-btn__spinner" />
      <span>{{ downloading ? "下载中..." : "开始下载" }}</span>
    </button>

    <!-- Engine status -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>引擎状态</span>
      </div>
      <div class="engine-list">
        <div v-for="e in engines" :key="e.engine" class="engine-row">
          <div class="engine-row__info">
            <span class="engine-row__name">{{ e.engine }}</span>
            <span class="engine-row__count">{{ e.ok }} / {{ e.total }}</span>
          </div>
          <div class="progress" :class="progressClass(e)">
            <div class="progress__bar" :style="{ width: progressPercent(e) + '%' }" />
          </div>
        </div>
        <div v-if="engines.length === 0" class="empty">
          加载中...
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.download-settings {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: border-color var(--duration-fast) var(--ease-out);
}
.card:hover {
  border-color: var(--border-default);
}

.card__header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}
.card__header svg {
  color: var(--accent);
}

.source-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.source-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.source-option:hover {
  border-color: var(--border-default);
  background: var(--bg-elevated);
}
.source-option--active {
  border-color: var(--accent);
  background: var(--accent-muted);
}

.source-option__radio {
  display: none;
}

.source-option__indicator {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid var(--border-strong);
  flex-shrink: 0;
  position: relative;
  transition: all var(--duration-fast) var(--ease-out);
}
.source-option--active .source-option__indicator {
  border-color: var(--accent);
}
.source-option--active .source-option__indicator::after {
  content: "";
  position: absolute;
  top: 3px;
  left: 3px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
}

.source-option__label {
  font-size: 14px;
  color: var(--text-primary);
}

.download-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 24px;
  border-radius: var(--radius-md);
  border: none;
  background: var(--accent);
  color: #ffffff;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.download-btn:hover:not(:disabled) {
  background: var(--accent-hover);
  box-shadow: var(--shadow-glow);
  transform: translateY(-1px);
}
.download-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.download-btn__spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.engine-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.engine-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.engine-row__info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.engine-row__name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.engine-row__count {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-secondary);
}

.progress {
  height: 6px;
  border-radius: 3px;
  background: var(--bg-hover);
  overflow: hidden;
}

.progress__bar {
  height: 100%;
  border-radius: 3px;
  transition: width 500ms var(--ease-out);
}

.progress--done .progress__bar {
  background: var(--success);
}
.progress--partial .progress__bar {
  background: var(--accent);
}
.progress--empty .progress__bar {
  background: var(--text-tertiary);
}

.empty {
  text-align: center;
  color: var(--text-tertiary);
  font-size: 13px;
  padding: 12px;
}
</style>
