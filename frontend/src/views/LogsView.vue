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

function levelIcon(level: LogEntry["level"]) {
  switch (level) {
    case "error": return "✕"
    case "warn": return "⚠"
    default: return "●"
  }
}

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

const logCounts = computed(() => {
  const counts = { all: appStore.logs.length, info: 0, warn: 0, error: 0 }
  for (const l of appStore.logs) {
    counts[l.level]++
  }
  return counts
})
</script>

<template>
  <div class="logs-view">
    <!-- Toolbar -->
    <div class="toolbar">
      <div class="toolbar__filters">
        <button
          v-for="level in (['all', 'info', 'warn', 'error'] as const)"
          :key="level"
          class="filter-btn"
          :class="{ 'filter-btn--active': filterLevel === level, [`filter-btn--${level}`]: filterLevel === level }"
          @click="filterLevel = level"
        >
          <span class="filter-btn__label">{{ level === 'all' ? '全部' : level }}</span>
          <span class="filter-btn__count">{{ logCounts[level] }}</span>
        </button>
      </div>
      <button class="clear-btn" @click="clearLogs">
        <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
          <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        清空
      </button>
    </div>

    <!-- Terminal -->
    <div class="terminal" ref="container">
      <div
        v-for="(log, i) in filteredLogs"
        :key="i"
        class="terminal__line"
      >
        <span class="terminal__ln">{{ String(i + 1).padStart(3, ' ') }}</span>
        <span class="terminal__time">{{ log.time }}</span>
        <span class="terminal__level" :class="`terminal__level--${log.level}`">{{ levelIcon(log.level) }}</span>
        <span class="terminal__msg" :class="`terminal__msg--${log.level}`">{{ log.message }}</span>
      </div>
      <div v-if="filteredLogs.length === 0" class="terminal__empty">
        <svg viewBox="0 0 24 24" fill="none" width="32" height="32">
          <path d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>暂无日志</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logs-view {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  height: calc(100vh - 140px);
  animation: fadeInUp 400ms var(--ease-out) both;
}

/* ---- Toolbar ---- */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-3);
  flex-shrink: 0;
}

.toolbar__filters {
  display: flex;
  gap: 6px;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-secondary);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.filter-btn:hover {
  border-color: var(--border-default);
  background: var(--bg-elevated);
}
.filter-btn--active {
  border-color: var(--accent);
  background: var(--accent-muted);
  color: var(--accent);
}
.filter-btn--active.filter-btn--error {
  border-color: var(--error);
  background: var(--error-muted);
  color: var(--error);
}
.filter-btn--active.filter-btn--warn {
  border-color: var(--warning);
  background: var(--warning-muted);
  color: var(--warning);
}
.filter-btn--active.filter-btn--info {
  border-color: var(--info);
  background: var(--info-muted);
  color: var(--info);
}

.filter-btn__count {
  font-family: var(--font-mono);
  font-size: 11px;
  opacity: 0.6;
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  color: var(--text-tertiary);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  margin-left: auto;
}
.clear-btn:hover {
  border-color: var(--error);
  color: var(--error);
  background: var(--error-muted);
}

/* ---- Terminal ---- */
.terminal {
  flex: 1;
  overflow-y: auto;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 12px 0;
  font-family: var(--font-mono);
  font-size: 13px;
}

.terminal__line {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 3px 16px;
  transition: background var(--duration-fast) var(--ease-out);
}
.terminal__line:hover {
  background: rgba(0, 0, 0, 0.02);
}

.terminal__ln {
  color: var(--text-disabled);
  font-size: 11px;
  flex-shrink: 0;
  user-select: none;
  width: 24px;
  text-align: right;
}

.terminal__time {
  color: var(--text-tertiary);
  font-size: 11px;
  flex-shrink: 0;
}

.terminal__level {
  flex-shrink: 0;
  font-size: 10px;
  width: 14px;
  text-align: center;
}
.terminal__level--info { color: var(--info); }
.terminal__level--warn { color: var(--warning); }
.terminal__level--error { color: var(--error); }

.terminal__msg {
  color: var(--text-secondary);
  word-break: break-all;
  line-height: 1.5;
}
.terminal__msg--error {
  color: var(--error);
}
.terminal__msg--warn {
  color: var(--warning);
}

.terminal__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: var(--text-tertiary);
  font-family: var(--font-body);
}
</style>
