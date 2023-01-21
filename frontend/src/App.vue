<template>
  <div
    :class="`flex flex-col w-screen min-h-screen h-full bg-gradient-to-tr from-back-left to-back-right text-white overflow-hidden`"
  >
    <div
      :class="`${
        fixedHeader ? 'showHeader fixed w-full bg-black bg-opacity-90' : ''
      } flex gap-4 h-20 px-40 justify-between items-center transition-all select-none`"
    >
      <h3
        class="whitespace-nowrap opacity-60 hover:opacity-100 transition-all cursor-pointer"
        @click="$router.push(user.isLoggedIn ? '/tasks' : '/profile')"
      >
        Winter IT Hack: спортпрог ⚽
        <!-- что здесь написать то? @ethosa-->
      </h3>
      <div class="flex">
        <Button
          text="задачи"
          flat
          @click="$router.push(user.isLoggedIn ? '/tasks' : '/profile')"
          >задачи</Button
        >
        <Button
          text="лидеры"
          flat
          @click="$router.push(user.isLoggedIn ? '/leaders' : '/profile')"
          >лидеры</Button
        >
        <Button text="профиль" flat @click="$router.push('/profile')"
          >профиль</Button
        >
      </div>
    </div>
    <router-view :class="`${fixedHeader ? 'py-20' : ''} px-40`" />
  </div>
</template>

<script>
import Button from "@/components/ui/button";

import { userStore } from "@/store";

export default {
  name: "App",
  components: { Button },

  data() {
    return {
      user: userStore(),
      toolbarClass: "",
      fixedHeader: false,
    };
  },

  mounted() {
    if (!this.user.isLoggedIn) {
      this.$router.push("/profile");
    }

    window.addEventListener("scroll", () => {
      if (window.scrollY > 100) {
        this.fixedHeader = true;
      } else {
        this.fixedHeader = false;
      }
    });
  },
};
</script>
