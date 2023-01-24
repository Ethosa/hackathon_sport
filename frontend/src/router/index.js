import { createRouter, createWebHistory } from "vue-router";

import TasksView from "@/components/tasksView";
import LeadersView from "@/components/leadersView";
import ProfileView from "@/components/profileView";
import TaskView from "@/components/taskView";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: TasksView,
    },
    {
      path: "/tasks",
      component: TasksView,
    },
    {
      path: "/leaders",
    },
    // нам похуииии)))))
    {
      path: "/profile",
      component: ProfileView,
    },
    {
      path: "/task/:id",
      component: TaskView,
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/profile",
    },
  ],
});
