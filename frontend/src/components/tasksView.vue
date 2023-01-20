<template>
  <div
    class="w-full h-full flex flex-col gap-2 divide-y-[1px] divide-fore divide-solid overflow-y-scroll"
  >
    <transition-group name="ok">
      <div
        class="flex flex-col items-start py-5"
        v-for="task in tasks"
        :key="task"
      >
        <p class="text-2xl uppercase tracking-widest font-semibold">
          {{ task.title }}
        </p>
        <p class="text-left indent-8 tracking-wider">{{ task.description }}</p>
        <Button
          class="self-end text-base"
          @click="$router.push(`/task/${task.id}`)"
          >решить
        </Button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import API from "../mixins/api";
import Button from "@/components/ui/button";

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
