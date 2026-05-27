<script setup lang="ts">
import TTSSettings from "../components/TTSSettings.vue"
import STTSettings from "../components/STTSettings.vue"
import TranslateSettings from "../components/TranslateSettings.vue"
import AudioOSCSettings from "../components/AudioOSCSettings.vue"
</script>

<template>
  <el-tabs>
    <el-tab-pane label="TTS">
      <TTSSettings />
    </el-tab-pane>
    <el-tab-pane label="STT">
      <STTSettings />
    </el-tab-pane>
    <el-tab-pane label="翻译">
      <TranslateSettings />
    </el-tab-pane>
    <el-tab-pane label="音频 & OSC">
      <AudioOSCSettings />
    </el-tab-pane>
  </el-tabs>
</template>
