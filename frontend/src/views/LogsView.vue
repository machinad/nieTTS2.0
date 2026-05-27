<script setup lang="ts">
import { ref, computed, watch, nextTick } from "vue"
import { appStore } from "../store"
import type { LogEntry } from "../store"

const filterLevel = ref<"all" | LogEntry["level"]>("all")
const container = ref<HTMLElement | null>(null)

const filteredLogs = computed(() => {
  if (filterLevel.value === "all") return appStore.logs
  return appStore.logs.filter((l) => l.level === filterLevel.value)
})

const tagType = (level: LogEntry["level"]) =>
  level === "error" ? "danger" : level === "warn" ? "warning" : "info"

watch(
  () => filteredLogs.value.length,
  async () => {
    await nextTick()
    if (container.value) {
      container.value.scrollTop = container.value.scrollHeight
    }
  }
)

function clearLogs() {
  appStore.logs.length = 0
}
</script>

<template>
  <div>
    <div style="display: flex; gap: 8px; margin-bottom: 12px; align-items: center">
      <el-radio-group v-model="filterLevel" size="small">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button value="info">info</el-radio-button>
        <el-radio-button value="warn">warn</el-radio-button>
        <el-radio-button value="error">error</el-radio-button>
      </el-radio-group>
      <el-button size="small" @click="clearLogs" style="margin-left: auto">清空</el-button>
    </div>

    <div
      ref="container"
      style="
        max-height: calc(100vh - 250px);
        overflow-y: auto;
        font-family: monospace;
        font-size: 13px;
        border: 1px solid var(--el-border-color-light);
        border-radius: 4px;
        padding: 8px;
      "
    >
      <div
        v-for="(log, i) in filteredLogs"
        :key="i"
        style="padding: 2px 0; border-bottom: 1px solid var(--el-border-color-extra-light)"
      >
        <span style="color: var(--el-text-color-secondary)">[{{ log.time }}]</span>
        <el-tag :type="tagType(log.level)" size="small" style="margin: 0 4px">{{ log.level }}</el-tag>
        <span>{{ log.message }}</span>
      </div>
      <div v-if="filteredLogs.length === 0" style="text-align: center; color: var(--el-text-color-secondary); padding: 24px">
        暂无日志
      </div>
    </div>
  </div>
</template>
