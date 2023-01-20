<template>
  <div class="flex flex-col w-screen min-h-screen h-full bg-gradient-to-tr from-back-left to-back-right text-white">
    <div
      :class="`flex gap-4 p-2 w-full h-24 items-center from-back-left to-back-right transition-all bg-gradient-to-br` + toolbarClass"
    >
      <h3 class="w-fit whitespace-nowrap">спортпрог ⚽</h3>
      <div class="flex items-center justify-end w-full">
        <div class="flex">
          <Button
            text="задачи"
            flat
            @click="goTo('/tasks', 'tasks')"
          >задачи</Button>
          <Button
            text="лидеры"
            flat
            @click="goTo('/leaders', 'leaders')"
          >лидеры</Button>
          <Button
            text="профиль"
            flat
            @click="goTo('/profile', 'profile')"
          >профиль</Button>
        </div>
      </div>
    </div>
    <div class="p-8">
      <router-view />
    </div>
  </div>
</template>

<script>
import Button from "@/components/ui/button";
import { userStore } from "@/store";

export default {
  name: 'App',
  components: {Button},
  data() {
    return {
      user: userStore(),
      toolbarClass: ""
    }
  },
  methods: {
    goTo(path, page) {
      this.$router.push(this.user.isLoggedIn ? path : '/profile')
    }
  },
  mounted() {
    window.addEventListener('scroll', ev => {
      if (window.scrollY > 10) {
        this.toolbarClass = "/75"
      } else {
        this.toolbarClass = ""
      }
    })
  }
}
</script>

<style>
#app {
  font-family: Nunito, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
