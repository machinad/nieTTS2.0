<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"
import { appStore } from "../store"
import type { LogEntry } from "../store"

const router = useRouter()

const recentLogs = computed(() => appStore.logs.slice(-5).reverse())

const tagType = (level: LogEntry["level"]) =>
  level === "error" ? "danger" : level === "warn" ? "warning" : "info"
</script>

<template>
  <div
    style="
      background: rgba(0, 0, 0, 0.03);
      border-radius: 4px;
      padding: 8px 12px;
      max-height: 180px;
      overflow-y: auto;
      font-size: 12px;
      font-family: monospace;
    "
  >
    <div
      style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 4px;
      "
    >
      <span style="color: var(--el-text-color-secondary); font-size: 12px">日志</span>
      <el-button
        link
        size="small"
        @click="router.push('/logs')"
        style="font-size: 12px"
      >
        展开全部
      </el-button>
    </div>
    <div
      v-for="(log, i) in recentLogs"
      :key="i"
      style="padding: 1px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
    >
      <span style="color: var(--el-text-color-secondary)">[{{ log.time }}]</span>
      <el-tag :type="tagType(log.level)" size="small" style="margin: 0 2px; font-size: 10px; padding: 0 4px">{{ log.level }}</el-tag>
      <span>{{ log.message }}</span>
    </div>
    <div
      v-if="recentLogs.length === 0"
      style="text-align: center; color: var(--el-text-color-secondary); padding: 12px"
    >
      暂无日志
    </div>
  </div>
</template>
