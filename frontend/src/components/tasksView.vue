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
        <div class="flex w-full justify-between">
          <p
            class="text-3xl uppercase tracking-widest font-semibold cursor-pointer hover:text-fore transition-all"
            @click="$router.push(`/task/${task.id}`)"
          >
            {{ task.title }}
          </p>
          <p
            :class="`${
              checkTask(task.id) !== undefined
                ? 'text-green-500'
                : 'text-red-500'
            } font-bold`"
          >
            {{
              checkTask(task.id) !== undefined
                ? `${checkTask(task.id)} баллов`
                : "Задание не выполнено"
            }}
          </p>
        </div>
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
    <div
      v-if="tasks.length === 0"
      class="w-full h-full flex items-center justify-center"
    >
      <div class="h-20 w-20">
        <svg
          version="1.1"
          id="L5"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          x="0px"
          y="0px"
          viewBox="0 0 100 100"
          enable-background="new 0 0 0 0"
          xml:space="preserve"
        >
          <circle fill="#fff" stroke="none" cx="6" cy="50" r="6">
            <animateTransform
              attributeName="transform"
              dur="1s"
              type="translate"
              values="0 15 ; 0 -15; 0 15"
              repeatCount="indefinite"
              begin="0.1"
            ></animateTransform>
          </circle>
          <circle fill="#fff" stroke="none" cx="30" cy="50" r="6">
            <animateTransform
              attributeName="transform"
              dur="1s"
              type="translate"
              values="0 10 ; 0 -10; 0 10"
              repeatCount="indefinite"
              begin="0.2"
            ></animateTransform>
          </circle>
          <circle fill="#fff" stroke="none" cx="54" cy="50" r="6">
            <animateTransform
              attributeName="transform"
              dur="1s"
              type="translate"
              values="0 5 ; 0 -5; 0 5"
              repeatCount="indefinite"
              begin="0.3"
            ></animateTransform>
          </circle>
        </svg>
      </div>
    </div>
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
  methods: {
    checkTask(taskID) {
      let result = undefined;
      userStore().marks.forEach((mark) => {
        mark.task.forEach((task) => {
          if (task.id === parseInt(taskID)) {
            result = mark.score;
          }
        });
      });
      return result;
    },
  },
  mounted() {
    API.getAllTasks().then((v) => {
      this.tasks = v.response;
    });
    API.getUser(userStore().userId).then((e) => {
      userStore().marks = e.response.marks;
    });
  },
};
</script>

<style scoped></style>
