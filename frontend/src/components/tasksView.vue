<template>
  <div
    class="w-full h-full flex flex-col gap-2 divide-y-[1px] divide-fore divide-solid overflow-y-scroll"
  >
    <transition-group name="tasksAnim">
      <div
        class="flex flex-col items-start py-5 gap-3"
        v-for="task in tasks"
        :key="task"
      >
        <p
          class="text-3xl uppercase tracking-widest font-semibold cursor-pointer hover:text-fore transition-all"
          @click="$router.push(`/task/${task.id}`)"
        >
          {{ task.title }}
        </p>
        <p class="text-xl text-left indent-8 tracking-wider cursor-default">
          {{ task.description }}
        </p>
        <Button
          class="self-end text-md"
          @click="$router.push(`/task/${task.id}`)"
          >решить
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="25px"
            height="25px"
            viewBox="0 0 25 28"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              d="m9 6l6 6l-6 6"
            />
          </svg>
        </Button>
      </div>
    </transition-group>
    <div v-if="tasks.length === 0">please wait</div>
  </div>
</template>

<script>
import API from "../mixins/api";
import Button from "@/components/ui/button";
import { userStore } from "@/store";

export default {
  name: "tasksView",
  components: { Button },
  mixins: [API],
  data() {
    return {
      tasks: [],
    };
  },
  mounted() {
    API.getAllTasks().then((v) => {
      this.tasks = v.response;
      console.log(v);
    });
  },
};
</script>

<style scoped></style>
