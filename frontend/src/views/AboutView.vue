<script setup lang="ts">
import { computed } from "vue"
import { appStore } from "../store"

const apiUrl = computed(() => `${window.location.protocol}//${window.location.host}`)
</script>

<template>
  <div style="display: flex; flex-direction: column; gap: 16px">
    <el-card>
      <template #header>nieTTS 2.0</template>
      <p>版本: v2.1.2</p>
      <p>一体化 TTS + STT + 翻译工具</p>
    </el-card>

    <el-card>
      <template #header>技术栈</template>
      <p>前端: Vue 3 + Element Plus + Vite</p>
      <p>后端: Python Quart + Hypercorn</p>
      <p>WebSocket 实时通信</p>
    </el-card>

    <el-card>
      <template #header>连接状态</template>
      <div style="display: flex; align-items: center; gap: 8px">
        <span
          :style="{
            display: 'inline-block',
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            backgroundColor: appStore.wsConnected ? '#67c23a' : '#f56c6c',
          }"
        />
        <span>WebSocket: {{ appStore.wsConnected ? "已连接" : "已断开" }}</span>
      </div>
      <p style="margin-top: 8px; color: var(--el-text-color-secondary)">
        API 地址: {{ apiUrl }}
      </p>
    </el-card>
  </div>
</template>
