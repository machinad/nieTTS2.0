<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"
import { appStore } from "../store"
import type { LogEntry } from "../store"

const router = useRouter()

const recentLogs = computed(() => appStore.logs.slice(-5).reverse())

function levelIcon(level: LogEntry["level"]) {
  switch (level) {
    case "error": return "✕"
    case "warn": return "⚠"
    default: return "●"
  }
}
</script>

<template>
  <div class="logbar">
    <div class="logbar__header">
      <div class="logbar__title">
        <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
          <path d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>日志</span>
      </div>
      <button class="logbar__expand" @click="router.push('/logs')">
        展开全部
        <svg viewBox="0 0 24 24" fill="none" width="12" height="12">
          <path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <div class="logbar__body">
      <div
        v-for="(log, i) in recentLogs"
        :key="i"
        class="logbar__entry"
        :class="`logbar__entry--${log.level}`"
      >
        <span class="logbar__time">{{ log.time }}</span>
        <span class="logbar__level" :class="`logbar__level--${log.level}`">{{ levelIcon(log.level) }}</span>
        <span class="logbar__msg">{{ log.message }}</span>
      </div>
      <div
        v-if="recentLogs.length === 0"
        class="logbar__empty"
      >
        暂无日志
      </div>
    </div>
  </div>
</template>

<style scoped>
.logbar {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.logbar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.logbar__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.logbar__expand {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--accent);
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.logbar__expand:hover {
  background: var(--accent-muted);
}

.logbar__body {
  max-height: 180px;
  overflow-y: auto;
  padding: 8px 0;
}

.logbar__entry {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 4px 16px;
  font-size: 12px;
  line-height: 1.6;
  transition: background var(--duration-fast) var(--ease-out);
}
.logbar__entry:hover {
  background: rgba(0, 0, 0, 0.02);
}

.logbar__time {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.logbar__level {
  flex-shrink: 0;
  font-size: 10px;
  width: 14px;
  text-align: center;
}
.logbar__level--info { color: var(--info); }
.logbar__level--warn { color: var(--warning); }
.logbar__level--error { color: var(--error); }

.logbar__msg {
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: var(--font-mono);
  font-size: 12px;
}
.logbar__entry--error .logbar__msg {
  color: var(--error);
}
.logbar__entry--warn .logbar__msg {
  color: var(--warning);
}

.logbar__empty {
  text-align: center;
  color: var(--text-tertiary);
  padding: 20px;
  font-size: 13px;
}
</style>
