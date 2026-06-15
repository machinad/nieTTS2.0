<script setup lang="ts">
import TTSSettings from "../components/TTSSettings.vue"
import STTSettings from "../components/STTSettings.vue"
import TranslateSettings from "../components/TranslateSettings.vue"
import AudioOSCSettings from "../components/AudioOSCSettings.vue"
import ModelDownloadSettings from "../components/ModelDownloadSettings.vue"
</script>

<template>
  <div class="settings">
    <el-tabs class="settings-tabs">
      <el-tab-pane label="语音合成">
        <TTSSettings />
      </el-tab-pane>
      <el-tab-pane label="语音识别">
        <STTSettings />
      </el-tab-pane>
      <el-tab-pane label="翻译">
        <TranslateSettings />
      </el-tab-pane>
      <el-tab-pane label="音频 & 其它">
        <AudioOSCSettings />
      </el-tab-pane>
      <el-tab-pane label="模型下载">
        <ModelDownloadSettings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.settings {
  animation: fadeInUp 400ms var(--ease-out) both;
}

.settings-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.settings-tabs :deep(.el-tabs__content) {
  padding: 0;
}
</style>
