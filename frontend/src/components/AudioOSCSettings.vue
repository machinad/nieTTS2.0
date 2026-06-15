<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import { ElMessage } from "element-plus"
import { Check } from "@element-plus/icons-vue"
import { appStore } from "../store"
import { postConfig, getConfig, postReload } from "../api"

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

const oscHost = ref("")
watch(() => appStore.config.osc_host, (v) => { oscHost.value = v || "" }, { immediate: true })

async function saveOscHost() {
  await onChangeField("osc_host", oscHost.value)
  await postReload()
  ElMessage.success("已保存")
}

async function onOscPortChange(v: any) {
  await onChangeField("osc_port", v)
  await postReload()
}
</script>

<template>
  <div class="audio-settings">
    <!-- Playback device -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M15.536 8.464a5 5 0 010 7.072M12 6l-4 4H4v4h4l4 4V6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M18.364 5.636a9 9 0 010 12.728" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>播放设备</span>
      </div>
      <el-select
        :model-value="appStore.config.device"
        @change="(v: string) => onChangeField('device', v)"
        style="width: 100%"
      >
        <el-option v-for="d in devices" :key="d.name" :label="d.name" :value="d.name" />
      </el-select>
    </div>

    <!-- Input device -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M19 10v2a7 7 0 01-14 0v-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>输入设备（麦克风）</span>
      </div>
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
      <div v-if="inputDevices.length === 0" class="card__hint">
        未检测到输入设备，请确保已连接麦克风并授权浏览器访问
      </div>
    </div>

    <!-- Default behavior -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>默认行为</span>
      </div>
      <div class="toggle-list">
        <div class="toggle-row">
          <span>播放音频</span>
          <el-switch :model-value="appStore.config.isPlayAudio" @change="(v: boolean) => onChangeField('isPlayAudio', v)" />
        </div>
        <div class="toggle-row">
          <span>翻译</span>
          <el-switch :model-value="appStore.config.isTranslate" @change="(v: boolean) => onChangeField('isTranslate', v)" />
        </div>
        <div class="toggle-row">
          <span>播放译文</span>
          <el-switch :model-value="appStore.config.isPlayTranslation" @change="(v: boolean) => onChangeField('isPlayTranslation', v)" />
        </div>
      </div>
    </div>

    <!-- OSC settings -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>OSC 设置</span>
      </div>
      <div class="toggle-list">
        <div class="toggle-row">
          <span>启用 OSC</span>
          <el-switch :model-value="appStore.config.osc_enabled" @change="(v: boolean) => onChangeField('osc_enabled', v)" />
        </div>
      </div>
      <div class="osc-fields">
        <div class="field">
          <label class="field__label">OSC Host</label>
          <div class="field__input-row">
            <el-input v-model="oscHost" />
            <button v-if="oscHost !== (appStore.config.osc_host || '')" class="save-icon" @click="saveOscHost">
              <el-icon><Check /></el-icon>
            </button>
          </div>
        </div>
        <div class="field">
          <label class="field__label">OSC Port</label>
          <el-input-number
            :model-value="appStore.config.osc_port"
            :min="1"
            :max="65535"
            @change="onOscPortChange"
          />
        </div>
      </div>
    </div>

    <!-- Web port settings -->
    <div class="card">
      <div class="card__header">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Web 端口</span>
      </div>
      <div class="osc-fields">
        <div class="field">
          <label class="field__label">web端口（重启生效）</label>
          <el-input-number
            :model-value="appStore.config.port || 11451"
            :min="1"
            :max="65535"
            @change="(v: number) => onChangeField('port', v)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.audio-settings {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

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

.card__hint {
  font-size: 13px;
  color: var(--text-tertiary);
  line-height: 1.5;
}

.toggle-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 14px;
  color: var(--text-primary);
}
.toggle-row:last-child {
  border-bottom: none;
}

.osc-fields {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-top: 4px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-tertiary);
}

.field__input-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--accent);
  background: var(--accent-muted);
  color: var(--accent);
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--duration-fast) var(--ease-out);
}
.save-icon:hover {
  background: var(--accent);
  color: #ffffff;
}
</style>
