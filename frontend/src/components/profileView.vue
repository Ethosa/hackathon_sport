<template>
  <div class="flex w-full h-full justify-center items-center">
    <transition name="fade" mode="out-in">
      <div
        v-if="user.isLoggedIn"
        class="flex flex-col items-center gap-4 bg-white p-8 rounded-xl drop-shadow-lg"
      >
        <div class="flex flex-col">
          <p class="text-2xl">{{ user.name }}</p>
          <div class="flex w-full gap-2 self-start items-baseline justify-between">
            <p class="text-lg">{{ user.group }}</p>
            <p class="text-base lowercase">{{ user.role }}</p>
          </div>
        </div>
        <div class="flex flex-col w-full divide-y-[1px] divide-fore items-start self-start">
          <p>Решено задач: {{ user.markCount }}</p>
          <p>Общее количество очков: {{ user.score }}</p>
        </div>
      </div>
      <div v-else class="flex flex-col gap-2 items-center bg-white p-8 rounded-xl drop-shadow-lg fade-in-animation">
        <p class="uppercase tracking-wide font-semibold text-lg">
          Авторизация
        </p>
        <div class="flex flex-col gap-4 w-full items-center">
          <EditText ref="login" placeholder="Логин" />
          <EditText ref="pass" placeholder="Пароль" input-type="password" />
        </div>
        <div class="flex justify-center w-full">
          <Button class="py-0 px-2 text-base -mr-1" @click="auth()">
            Войти
          </Button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { userStore } from '@/store'
import EditText from "@/components/ui/editText"
import Button from "@/components/ui/button"
import API from "@/mixins/api"

export default {
  name: "profileView",
  components: {Button, EditText},
  data() {
    return {
      user: userStore(),
    }
  },
  methods: {
    auth() {
      API.auth(this.$refs.login.getText(), this.$refs.pass.getText()).then((e) => {
        if ('error' in e) {
          this.$refs.pass.setError(e.error)
        } else {
          this.user.userId = e.response.id
          this.user.token = e.response.access_token
          API.getUser(this.user.userId).then((e) => {
            this.user.name = e.response.name
            this.user.marks = e.response.marks
            this.user.group = e.response.group
            let role = e.response.role
            API.getRole(role).then((res) => {
              this.user.role = res.response.title
            })
          })
          console.log(e)
        }
      })
    },
  }
}
</script>

<style scoped>
.fade-leave-active, .fade-enter-active {
  transition: all .3s ease-in-out;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(-50px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(50px);
}

@keyframes fadeOnShow {
  0% {
    opacity: 0;
    transform: translateY(-50px);
  }
  100% {
    opacity: 1;
    transform: translateY(0px);
  }
}

.fade-in-animation {
  animation: fadeOnShow .3s ease-in-out;
}
</style>
