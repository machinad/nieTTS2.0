<script setup lang="ts">
import { useRouter } from "vue-router"
import {
  House,
  Setting,
  Document,
  InfoFilled,
  Expand,
  Fold,
} from "@element-plus/icons-vue"
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

function onMenuClick() {
  if (props.mobile) {
    emit("update:mobileOpen", false)
  }
}
</script>

<template>
  <el-aside
    :style="{
      position: 'fixed',
      left: 0,
      top: 0,
      bottom: 0,
      zIndex: 100,
      transition: props.mobile ? 'transform 0.3s' : 'width 0.3s',
      transform: props.mobile && !props.mobileOpen ? 'translateX(-100%)' : 'translateX(0)',
      backgroundColor: '#1d1e2c',
      color: '#fff',
      display: 'flex',
      flexDirection: 'column',
    }"
    :width="props.mobile ? '220px' : props.collapsed ? '64px' : '220px'"
  >
    <el-menu
      :default-active="router.currentRoute.value.path"
      :collapse="!props.mobile && props.collapsed"
      :router="true"
      background-color="#1d1e2c"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      style="border-right: none; flex: 1"
      @select="onMenuClick"
    >
      <div
        style="
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 16px 0;
        "
      >
        <el-button
          v-if="!props.mobile"
          :icon="props.collapsed ? Expand : Fold"
          text
          style="color: #bfcbd9; font-size: 18px"
          @click="emit('update:collapsed', !props.collapsed)"
        />
      </div>
      <el-menu-item index="/">
        <el-icon><House /></el-icon>
        <template #title>主页</template>
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>设置</template>
      </el-menu-item>
      <el-menu-item index="/logs">
        <el-icon><Document /></el-icon>
        <template #title>日志</template>
      </el-menu-item>
      <el-menu-item index="/about">
        <el-icon><InfoFilled /></el-icon>
        <template #title>关于</template>
      </el-menu-item>
    </el-menu>

    <div
      style="
        padding: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
      "
    >
      <span
        :style="{
          display: 'inline-block',
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          backgroundColor: appStore.wsConnected ? '#67c23a' : '#f56c6c',
          flexShrink: 0,
        }"
      />
      <span style="font-size: 13px; color: #bfcbd9" v-if="!props.collapsed || props.mobile">
        {{ appStore.wsConnected ? "已连接" : "已断开" }}
      </span>
    </div>
  </el-aside>
</template>
