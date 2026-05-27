import { createRouter, createWebHashHistory } from "vue-router"

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("./views/HomeView.vue"),
    },
    {
      path: "/settings",
      name: "Settings",
      component: () => import("./views/SettingsView.vue"),
    },
    {
      path: "/logs",
      name: "Logs",
      component: () => import("./views/LogsView.vue"),
    },
    {
      path: "/about",
      name: "About",
      component: () => import("./views/AboutView.vue"),
    },
  ],
})

export default router
