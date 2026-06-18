<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { appStore } from "../store"

const apiUrl = computed(() => `${window.location.protocol}//${window.location.host}`)
const version = ref("v2.5.0")

onMounted(async () => {
  try {
    const res = await fetch(`${apiUrl.value}/api/version`)
    if (res.ok) {
      const data = await res.json()
      if (data.version) version.value = data.version
    }
  } catch {}
})
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
        <p class="hero__version">{{ version }}</p>
      </div>
      <p class="hero__desc">一体化 TTS + STT + 翻译工具</p>
    </div>

    <!-- Intro -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
          <line x1="12" y1="16" x2="12" y2="12" stroke="currentColor" stroke-width="1.5"/>
          <line x1="12" y1="8" x2="12.01" y2="8" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span>软件简介</span>
      </div>
      <p class="intro-text">
        nieTTS 2.0 是一款专为 VR 社交平台（如 VRChat）设计的桌面应用，集成了语音合成（TTS）、语音识别（STT）和翻译功能。
        支持多种在线和离线引擎，提供 PySide6 桌面 GUI 和 Vue 3 Web 界面，可通过 OSC 协议与 VRChat 无缝集成。
      </p>
    </div>

    <!-- Author -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span>作者信息</span>
      </div>
      <div class="info-grid">
        <div class="info-row">
          <span class="info-label">作者</span>
          <span class="info-value">machina</span>
        </div>
        <div class="info-row">
          <span class="info-label">GitHub</span>
          <a class="info-link" href="https://github.com/machinad" target="_blank">@machinad</a>
        </div>
        <div class="info-row">
          <span class="info-label">邮箱</span>
          <a class="info-link" href="mailto:l1531829828@163.com">l1531829828@163.com</a>
        </div>
      </div>
    </div>

    <!-- Links -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <polyline points="15 3 21 3 21 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="10" y1="14" x2="21" y2="3" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span>项目链接</span>
      </div>
      <div class="link-buttons">
        <a class="link-btn" href="https://github.com/machinad/nieTTS2.0" target="_blank">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          GitHub 仓库
        </a>
        <a class="link-btn" href="https://github.com/machinad/nieTTS2.0/issues" target="_blank">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
            <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="1.5"/>
            <line x1="12" y1="16" x2="12.01" y2="16" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          问题反馈
        </a>
      </div>
    </div>

    <!-- License -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="1.5"/>
          <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="1.5"/>
          <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <span>许可证</span>
      </div>
      <p class="license-text">
        本项目基于 <a href="http://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License 2.0</a> 开源。
      </p>
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

    <!-- Dependencies -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>开源致谢</span>
      </div>

      <div class="dep-section">
        <h4 class="dep-section__title">核心运行时</h4>
        <div class="dep-list">
          <a v-for="[name, lic, url] in [
            ['sherpa-onnx', 'Apache-2.0', 'https://github.com/k2-fsa/sherpa-onnx'],
            ['edge-tts', 'MIT', 'https://github.com/rany2/edge-tts'],
            ['dashscope', 'Apache-2.0', 'https://github.com/dashscope/dashscope-sdk-python'],
            ['openai', 'Apache-2.0', 'https://github.com/openai/openai-python'],
            ['numpy', 'BSD-3-Clause', 'https://github.com/numpy/numpy'],
            ['miniaudio', 'Unlicense', 'https://github.com/mackron/miniaudio'],
            ['python-osc', 'MIT', 'https://github.com/attwad/python-osc'],
            ['httpx', 'BSD-3-Clause', 'https://github.com/encode/httpx'],
          ]" :key="name" :href="url" target="_blank" class="dep-item">
            <span class="dep-item__name">{{ name }}</span>
            <span class="dep-item__lic">{{ lic }}</span>
          </a>
        </div>
      </div>

      <div class="dep-section">
        <h4 class="dep-section__title">Web 服务</h4>
        <div class="dep-list">
          <a v-for="[name, lic, url] in [
            ['quart', 'MIT', 'https://github.com/pallets/quart'],
            ['quart-cors', 'MIT', 'https://github.com/pallets/quart-cors'],
            ['cryptography', 'Apache-2.0/BSD-3-Clause', 'https://github.com/pyca/cryptography'],
          ]" :key="name" :href="url" target="_blank" class="dep-item">
            <span class="dep-item__name">{{ name }}</span>
            <span class="dep-item__lic">{{ lic }}</span>
          </a>
        </div>
      </div>

      <div class="dep-section">
        <h4 class="dep-section__title">前端</h4>
        <div class="dep-list">
          <a v-for="[name, lic, url] in [
            ['Vue 3', 'MIT', 'https://github.com/vuejs/core'],
            ['Vue Router 4', 'MIT', 'https://github.com/vuejs/router'],
            ['Element Plus', 'MIT', 'https://github.com/element-plus/element-plus'],
            ['Vite', 'MIT', 'https://github.com/vitejs/vite'],
          ]" :key="name" :href="url" target="_blank" class="dep-item">
            <span class="dep-item__name">{{ name }}</span>
            <span class="dep-item__lic">{{ lic }}</span>
          </a>
        </div>
      </div>

      <div class="dep-section">
        <h4 class="dep-section__title">模型下载</h4>
        <div class="dep-list">
          <a v-for="[name, lic, url] in [
            ['huggingface-hub', 'Apache-2.0', 'https://github.com/huggingface/huggingface_hub'],
            ['modelscope', 'Apache-2.0', 'https://github.com/modelscope/modelscope'],
          ]" :key="name" :href="url" target="_blank" class="dep-item">
            <span class="dep-item__name">{{ name }}</span>
            <span class="dep-item__lic">{{ lic }}</span>
          </a>
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

/* ---- Intro ---- */
.intro-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

/* ---- Info grid ---- */
.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-subtle);
}
.info-row:last-child {
  border-bottom: none;
}

.info-label {
  width: 64px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.info-value {
  font-size: 14px;
  color: var(--text-primary);
}

.info-link {
  font-size: 14px;
  color: var(--accent);
  text-decoration: none;
}
.info-link:hover {
  text-decoration: underline;
}

/* ---- Link buttons ---- */
.link-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--accent);
  background: var(--accent-muted);
  border: 1px solid rgba(214, 96, 138, 0.2);
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-out);
}
.link-btn:hover {
  background: rgba(214, 96, 138, 0.15);
}
.link-btn svg {
  flex-shrink: 0;
}

/* ---- License ---- */
.license-text {
  font-size: 14px;
  color: var(--text-secondary);
}
.license-text a {
  color: var(--accent);
  text-decoration: none;
}
.license-text a:hover {
  text-decoration: underline;
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

/* ---- Dependencies ---- */
.dep-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.dep-section__title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
  margin: 8px 0 0;
}

.dep-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dep-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-out);
}
.dep-item:hover {
  border-color: var(--accent);
  background: var(--accent-muted);
}

.dep-item__name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.dep-item__lic {
  font-size: 11px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
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
