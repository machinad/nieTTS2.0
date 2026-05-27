import { ElMessage } from "element-plus"
import { postConfig, getConfig } from "./api"
import { appStore } from "./store"

export function useAutoSave() {
  let timer: ReturnType<typeof setTimeout> | null = null

  async function saveConfig(payload: Record<string, any>) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(async () => {
      try {
        await postConfig(payload)
      } catch (e: any) {
        ElMessage.error(`配置保存失败: ${e.message}`)
      }
    }, 300)
  }

  return { saveConfig }
}

export async function updateConfigAndStore(key: string, value: any) {
  const payload: Record<string, any> = {}
  const keys = key.split(".")
  let obj = payload
  for (let i = 0; i < keys.length - 1; i++) {
    obj[keys[i]] = {}
    obj = obj[keys[i]]
  }
  obj[keys[keys.length - 1]] = value

  try {
    await postConfig(payload)
    await getConfig()
  } catch (e: any) {
    ElMessage.error(`配置保存失败: ${e.message}`)
  }
}
