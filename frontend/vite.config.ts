import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import ElementPlus from "unplugin-element-plus/vite"
import { resolve } from "path"

export default defineConfig({
  plugins: [vue(), ElementPlus()],
  base: "/",
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  build: {
    outDir: "../templates",
    emptyOutDir: true,
  },
})
