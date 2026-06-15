<script setup lang="ts">
import { useRouter } from "vue-router"
import { House, Setting, Document, InfoFilled } from "@element-plus/icons-vue"
import { appStore } from "../store"

const props = defineProps<{
  collapsed: boolean
  mobile: boolean
  mobileOpen: boolean
}>()
const emit = defineEmits<{
  "update:collapsed": [value: boolean]
  "update:mobileOpen": [value: boolean]
}>()

const router = useRouter()

const navItems = [
  { path: "/", icon: House, label: "主页" },
  { path: "/settings", icon: Setting, label: "设置" },
  { path: "/logs", icon: Document, label: "日志" },
  { path: "/about", icon: InfoFilled, label: "关于" },
]

function onNavClick(path: string) {
  router.push(path)
  if (props.mobile) {
    emit("update:mobileOpen", false)
  }
}

function isActive(path: string) {
  return router.currentRoute.value.path === path
}
</script>

<template>
  <aside
    class="sidebar"
    :class="{
      'sidebar--collapsed': !props.mobile && props.collapsed,
      'sidebar--mobile': props.mobile,
      'sidebar--open': props.mobile && props.mobileOpen,
    }"
  >
    <!-- Logo area -->
    <div class="sidebar__logo">
      <div class="sidebar__logo-icon">
        <svg viewBox="0 0 24 24" fill="none" width="22" height="22">
          <path d="M12 3v18M8 7v10M4 10v4M16 5v14M20 8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <span v-if="!props.collapsed || props.mobile" class="sidebar__logo-text">nieTTS</span>
    </div>

    <!-- Navigation -->
    <nav class="sidebar__nav">
      <button
        v-for="item in navItems"
        :key="item.path"
        class="sidebar__item"
        :class="{ 'sidebar__item--active': isActive(item.path) }"
        @click="onNavClick(item.path)"
        :title="props.collapsed && !props.mobile ? item.label : undefined"
      >
        <el-icon :size="20"><component :is="item.icon" /></el-icon>
        <span v-if="!props.collapsed || props.mobile" class="sidebar__item-label">{{ item.label }}</span>
        <span v-if="isActive(item.path)" class="sidebar__item-indicator" />
      </button>
    </nav>

    <!-- Collapse toggle (desktop only) -->
    <button
      v-if="!props.mobile"
      class="sidebar__toggle"
      @click="emit('update:collapsed', !props.collapsed)"
      :title="props.collapsed ? '展开' : '收起'"
    >
      <svg viewBox="0 0 24 24" fill="none" width="18" height="18" :style="{ transform: props.collapsed ? 'rotate(180deg)' : 'none' }" style="transition: transform 0.3s var(--ease-out)">
        <path d="M15 6l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Connection status -->
    <div class="sidebar__status">
      <span class="sidebar__status-dot" :class="appStore.wsConnected ? 'sidebar__status-dot--on' : 'sidebar__status-dot--off'" />
      <span v-if="!props.collapsed || props.mobile" class="sidebar__status-text">
        {{ appStore.wsConnected ? "已连接" : "已断开" }}
      </span>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
  width: var(--sidebar-width);
  background: var(--bg-surface);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  transition: width var(--duration-slow) var(--ease-out),
              transform var(--duration-slow) var(--ease-out);
  overflow: hidden;
}

.sidebar--collapsed {
  width: var(--sidebar-collapsed);
}

.sidebar--mobile {
  transform: translateX(-100%);
  width: var(--sidebar-width);
  box-shadow: var(--shadow-lg);
}
.sidebar--mobile.sidebar--open {
  transform: translateX(0);
}

.sidebar__logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 16px 16px;
  min-height: 64px;
  flex-shrink: 0;
}

.sidebar__logo-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(214, 96, 138, 0.2);
}

.sidebar__logo-text {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.sidebar__nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 10px;
  overflow-y: auto;
}

.sidebar__item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  position: relative;
  transition: all var(--duration-fast) var(--ease-out);
  white-space: nowrap;
  width: 100%;
  text-align: left;
}

.sidebar__item:hover {
  background: rgba(0, 0, 0, 0.04);
  color: var(--text-primary);
}

.sidebar__item--active {
  background: var(--accent-muted);
  color: var(--accent);
}

.sidebar__item--active:hover {
  background: rgba(214, 96, 138, 0.14);
}

.sidebar__item-label {
  flex: 1;
}

.sidebar__item-indicator {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 6px var(--accent);
}

.sidebar__toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 4px 10px;
  padding: 8px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}
.sidebar__toggle:hover {
  background: rgba(0, 0, 0, 0.04);
  color: var(--text-secondary);
}

.sidebar__status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.sidebar__status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
  transition: all var(--duration-normal) var(--ease-out);
}
.sidebar__status-dot--on {
  background: var(--success);
  box-shadow: 0 0 6px rgba(61, 168, 92, 0.3);
}
.sidebar__status-dot--off {
  background: var(--error);
  box-shadow: 0 0 6px rgba(208, 72, 64, 0.2);
}

.sidebar__status-text {
  font-size: 13px;
  color: var(--text-tertiary);
  white-space: nowrap;
}
</style>
