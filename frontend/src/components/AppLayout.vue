<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue"
import SideBar from "./SideBar.vue"
import { appStore } from "../store"

const collapsed = ref(true)
const mobileMenuOpen = ref(false)
const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) mobileMenuOpen.value = false
}

onMounted(() => {
  checkMobile()
  window.addEventListener("resize", checkMobile)
})
onBeforeUnmount(() => window.removeEventListener("resize", checkMobile))
</script>

<template>
  <div class="app-root" :class="{ 'app-root--mobile': isMobile }">
    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div
        v-if="isMobile && mobileMenuOpen"
        class="backdrop"
        @click="mobileMenuOpen = false"
      />
    </Transition>

    <SideBar
      :collapsed="collapsed"
      :mobile="isMobile"
      :mobile-open="mobileMenuOpen"
      @update:collapsed="collapsed = $event"
      @update:mobile-open="mobileMenuOpen = $event"
    />

    <div
      class="main-area"
      :style="{ marginLeft: isMobile ? '0' : collapsed ? 'var(--sidebar-collapsed)' : 'var(--sidebar-width)' }"
    >
      <!-- Header -->
      <header class="header">
        <div class="header__left">
          <button
            v-if="isMobile"
            class="header__menu-btn"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
              <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <h1 class="header__title">nieTTS 2.0</h1>
        </div>
        <div class="header__right">
          <div class="header__status" :class="appStore.wsConnected ? 'header__status--on' : 'header__status--off'">
            <span class="header__status-dot" />
            <span class="header__status-label">{{ appStore.wsConnected ? "已连接" : "已断开" }}</span>
          </div>
        </div>
      </header>

      <!-- Content -->
      <main class="content">
        <router-view v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-root {
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  background: var(--bg-deep);
}

.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 90;
  backdrop-filter: blur(4px);
}

.main-area {
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: margin-left var(--duration-slow) var(--ease-out);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--sp-6);
  height: 56px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-base);
  backdrop-filter: blur(12px);
}

.header__left {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.header__menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.header__menu-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.header__title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.header__right {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.header__status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 500;
  transition: all var(--duration-normal) var(--ease-out);
}

.header__status--on {
  background: var(--success-muted);
  color: var(--success);
}
.header__status--off {
  background: var(--error-muted);
  color: var(--error);
}

.header__status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.header__status--on .header__status-dot {
  background: var(--success);
  box-shadow: 0 0 6px rgba(61, 168, 92, 0.3);
}
.header__status--off .header__status-dot {
  background: var(--error);
}

.header__status-label {
  white-space: nowrap;
}

.content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: var(--sp-6);
}

.content > * {
  width: 100%;
  max-width: 680px;
  margin: 0 auto;
}

/* Page transition */
.page-enter-active {
  transition: opacity 200ms var(--ease-out), transform 200ms var(--ease-out);
}
.page-leave-active {
  transition: opacity 120ms var(--ease-out);
}
.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.page-leave-to {
  opacity: 0;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms var(--ease-out);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .content {
    padding: var(--sp-3);
  }
}
</style>
