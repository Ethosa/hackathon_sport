<template>
  <div class="flex justify-center w-screen min-h-screen h-full bg-back text-black">
    <div class="flex flex-col gap-4 p-8 w-4/6 extended:w-5/6 compact:w-full items-start">
      <h1>спортпрог ⚽</h1>
      <p class="text-xl">
        Вашей задачей является решение всех четырех заданий.
      </p>
      <div class="flex flex-col items-center w-full mt-10">
        <div class="flex">
          <Button
            text="задачи"
            :flat="currentPage !== 'tasks'"
            bordered
            @click="goTo('/tasks', 'tasks')"
          >задачи</Button>
          <Button
            text="лидеры"
            :flat="currentPage !== 'leaders'"
            @click="goTo('/leaders', 'leaders')"
          >лидеры</Button>
          <Button
            text="профиль"
            :flat="currentPage !== 'profile'"
            @click="goTo('/profile', 'profile')"
          >профиль</Button>
        </div>
        <hr>
      </div>
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
      currentPage: "profile",
      user: userStore()
    }
  },
  methods: {
    goTo(path, page) {
      this.$router.push(this.user.isLoggedIn ? path : '/profile')
      this.currentPage = page
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
