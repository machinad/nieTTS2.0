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
  <div style="height: 100vh">
    <!-- Mobile backdrop -->
    <div
      v-if="isMobile && mobileMenuOpen"
      style="position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 90"
      @click="mobileMenuOpen = false"
    />

    <SideBar
      :collapsed="collapsed"
      :mobile="isMobile"
      :mobile-open="mobileMenuOpen"
      @update:collapsed="collapsed = $event"
      @update:mobile-open="mobileMenuOpen = $event"
    />

    <div
      :style="{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        marginLeft: isMobile ? '0' : '64px',
      }"
    >
      <div
        style="
          display: flex;
          align-items: center;
          justify-content: space-between;
          border-bottom: 1px solid var(--el-border-color-light);
          padding: 0 16px;
          height: 56px;
          flex-shrink: 0;
        "
      >
        <div style="display: flex; align-items: center; gap: 12px">
          <el-button
            v-if="isMobile"
            text
            style="font-size: 20px"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            &#9776;
          </el-button>
          <span style="font-size: 18px; font-weight: 600">nieTTS 2.0</span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px">
          <span
            :style="{
              display: 'inline-block',
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: appStore.wsConnected ? '#67c23a' : '#f56c6c',
            }"
          />
          <span style="font-size: 13px; color: var(--el-text-color-secondary)">
            {{ appStore.wsConnected ? "已连接" : "已断开" }}
          </span>
        </div>
      </div>
      <div style="flex: 1; overflow-y: auto; padding: 16px; display: flex; justify-content: center">
        <div style="width: 100%; max-width: 720px">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>
