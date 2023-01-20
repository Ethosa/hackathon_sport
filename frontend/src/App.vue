<template>
  <div
    class="flex flex-col px-10 w-screen min-h-screen h-full bg-gradient-to-tr from-back-left to-back-right text-white overflow-hidden"
  >
    <div
      :class="
        `flex gap-4 py-9 justify-between items-center from-back-left to-back-right transition-all bg-gradient-to-br` +
        toolbarClass
      "
    >
      <h3 class="whitespace-nowrap opacity-60 hover:opacity-100 transition-all cursor-pointer" @click="router().push('/tasks')">спортпрог ⚽</h3>
        <div class="flex">
          <Button text="задачи" flat @click="goTo('/tasks', 'tasks')"
            >задачи</Button
          >
          <Button text="лидеры" flat @click="goTo('/leaders', 'leaders')"
            >лидеры</Button
          >
          <Button text="профиль" flat @click="goTo('/profile', 'profile')"
            >профиль</Button
          >
        </div>
    </div>
    <router-view  />
  </div>
</template>

<script>
import Button from "@/components/ui/button";
import { userStore } from "@/store";
import {router} from "@/router";

export default {
  name: "App",
  components: { Button },
  data() {
    return {
      user: userStore(),
      toolbarClass: "",
    };
  },
  methods: {
    router() {
      return router
    },
    goTo(path, page) {
      this.$router.push(this.user.isLoggedIn ? path : "/profile");
    },
  },
  mounted() {
    window.addEventListener("scroll", (ev) => {
      if (window.scrollY > 10) {
        this.toolbarClass = "/75";
      } else {
        this.toolbarClass = "";
      }
    });
  },
};
</script>

<style>
#app {
  font-family: Nunito, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
