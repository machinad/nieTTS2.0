<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { ElMessage } from "element-plus"
import { appStore } from "../store"
import { postConfig, getConfig } from "../api"

const INPUT_DEVICE_KEY = "nietts_input_device_id"

const devices = computed(() => appStore.config.available_devices || [])
const inputDevices = ref<MediaDeviceInfo[]>([])
const selectedInputDevice = ref(localStorage.getItem(INPUT_DEVICE_KEY) || "")

async function loadInputDevices() {
  try {
    const all = await navigator.mediaDevices.enumerateDevices()
    inputDevices.value = all.filter(d => d.kind === "audioinput" && d.deviceId)
  } catch {
    inputDevices.value = []
  }
}

onMounted(loadInputDevices)

function onInputDeviceChange(deviceId: string) {
  selectedInputDevice.value = deviceId
  localStorage.setItem(INPUT_DEVICE_KEY, deviceId)
}

async function onChangeField(key: string, value: any) {
  try {
    await postConfig({ [key]: value })
    await getConfig()
  } catch (e: any) {
    ElMessage.error(`保存失败: ${e.message}`)
  }
}
</script>

<template>
  <div style="display: flex; flex-direction: column; gap: 16px">
    <el-card>
      <template #header>播放设备</template>
      <el-select
        :model-value="appStore.config.device"
        @change="(v: string) => onChangeField('device', v)"
        style="width: 100%"
      >
        <el-option
          v-for="d in devices"
          :key="d.name"
          :label="d.name"
          :value="d.name"
        />
      </el-select>
    </el-card>

    <el-card>
      <template #header>输入设备（麦克风）</template>
      <el-select
        :model-value="selectedInputDevice"
        @change="onInputDeviceChange"
        style="width: 100%"
        placeholder="选择麦克风设备"
      >
        <el-option
          v-for="d in inputDevices"
          :key="d.deviceId"
          :label="d.label || `设备 ${d.deviceId.slice(0, 8)}...`"
          :value="d.deviceId"
        />
      </el-select>
      <div v-if="inputDevices.length === 0" style="font-size: 13px; color: var(--el-text-color-secondary); margin-top: 8px">
        未检测到输入设备，请确保已连接麦克风并授权浏览器访问
      </div>
    </el-card>

    <el-card>
      <template #header>默认行为</template>
      <div style="display: flex; flex-direction: column; gap: 12px">
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span>播放音频</span>
          <el-switch
            :model-value="appStore.config.isPlayAudio"
            @change="(v: boolean) => onChangeField('isPlayAudio', v)"
          />
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span>翻译</span>
          <el-switch
            :model-value="appStore.config.isTranslate"
            @change="(v: boolean) => onChangeField('isTranslate', v)"
          />
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span>播放译文</span>
          <el-switch
            :model-value="appStore.config.isPlayTranslation"
            @change="(v: boolean) => onChangeField('isPlayTranslation', v)"
          />
        </div>
      </div>
    </el-card>

    <el-card>
      <template #header>OSC 设置</template>
      <div style="display: flex; flex-direction: column; gap: 12px">
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span>启用 OSC</span>
          <el-switch
            :model-value="appStore.config.osc_enabled"
            @change="(v: boolean) => onChangeField('osc_enabled', v)"
          />
        </div>
        <div>
          <span style="font-size: 14px; margin-bottom: 4px; display: block">OSC Host</span>
          <el-input
            :model-value="appStore.config.osc_host"
            @update:model-value="(v: string) => onChangeField('osc_host', v)"
          />
        </div>
        <div>
          <span style="font-size: 14px; margin-bottom: 4px; display: block">OSC Port</span>
          <el-input-number
            :model-value="appStore.config.osc_port"
            :min="1"
            :max="65535"
            @change="(v: any) => onChangeField('osc_port', v)"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>
