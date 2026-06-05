<script setup lang="ts">
import { computed } from "vue"
import { appStore } from "../store"

const apiUrl = computed(() => `${window.location.protocol}//${window.location.host}`)
</script>

<template>
  <div class="about">
    <!-- Hero -->
    <div class="hero">
      <div class="hero__icon">
        <svg viewBox="0 0 24 24" fill="none" width="32" height="32">
          <path d="M12 3v18M8 7v10M4 10v4M16 5v14M20 8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="hero__info">
        <h2 class="hero__title">nieTTS 2.0</h2>
        <p class="hero__version">v2.1.2</p>
      </div>
      <p class="hero__desc">一体化 TTS + STT + 翻译工具</p>
    </div>

    <!-- Tech stack -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>技术栈</span>
      </div>
      <div class="stack-grid">
        <div class="stack-item">
          <span class="stack-item__label">前端</span>
          <span class="stack-item__value">Vue 3 + Element Plus + Vite</span>
        </div>
        <div class="stack-item">
          <span class="stack-item__label">后端</span>
          <span class="stack-item__value">Python Quart + Hypercorn</span>
        </div>
        <div class="stack-item">
          <span class="stack-item__label">通信</span>
          <span class="stack-item__value">WebSocket 实时通信</span>
        </div>
      </div>
    </div>

    <!-- Connection status -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.386-3.04a4.5 4.5 0 00-1.242-7.244l-4.5-4.5a4.5 4.5 0 00-6.364 6.364L5.25 8.689" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>连接状态</span>
      </div>
      <div class="status-row">
        <div class="status-badge" :class="appStore.wsConnected ? 'status-badge--on' : 'status-badge--off'">
          <span class="status-badge__dot" />
          <span>WebSocket {{ appStore.wsConnected ? "已连接" : "已断开" }}</span>
        </div>
      </div>
      <div class="api-info">
        <span class="api-info__label">API 地址</span>
        <code class="api-info__value">{{ apiUrl }}</code>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about {
  display: flex;
  flex-direction: column;
  gap: 16px;
  animation: fadeInUp 400ms var(--ease-out) both;
}

/* ---- Hero ---- */
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px 24px;
  background: linear-gradient(135deg, var(--bg-surface) 0%, var(--bg-elevated) 100%);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 30%, var(--accent-glow) 0%, transparent 50%);
  pointer-events: none;
}

.hero__icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  box-shadow: 0 4px 20px rgba(214, 96, 138, 0.15);
  position: relative;
}

.hero__info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hero__title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.hero__version {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--accent);
  font-weight: 500;
}

.hero__desc {
  font-size: 14px;
  color: var(--text-secondary);
}

/* ---- Card ---- */
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

/* ---- Stack grid ---- */
.stack-grid {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.stack-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-subtle);
}
.stack-item:last-child {
  border-bottom: none;
}

.stack-item__label {
  width: 48px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.stack-item__value {
  font-size: 14px;
  color: var(--text-primary);
}

/* ---- Status ---- */
.status-row {
  display: flex;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
}
.status-badge--on {
  background: var(--success-muted);
  color: var(--success);
}
.status-badge--off {
  background: var(--error-muted);
  color: var(--error);
}

.status-badge__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.status-badge--on .status-badge__dot {
  background: var(--success);
  box-shadow: 0 0 6px rgba(61, 168, 92, 0.3);
}
.status-badge--off .status-badge__dot {
  background: var(--error);
  box-shadow: 0 0 6px rgba(208, 72, 64, 0.2);
}

.api-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 4px;
}

.api-info__label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-tertiary);
}

.api-info__value {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-secondary);
  padding: 8px 12px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
}
</style>
