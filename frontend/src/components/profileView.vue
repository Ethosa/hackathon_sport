<template>
  <div class="flex-auto flex w-full h-full justify-center items-center">
    <transition name="fade" mode="out-in">
      <div
        v-if="user.isLoggedIn"
        class="flex flex-col items-center gap-4 bg-back px-8 py-4 rounded-xl font-sans drop-shadow-lg"
      >
        <div class="flex flex-col items-center">
          <p class="text-2xl tracking-widest font-light self-start">
            @{{ user.login }}
          </p>
          <p class="text-xl">{{ user.name }}</p>
          <div
            class="flex w-full gap-2 self-start items-baseline justify-between"
          >
            <p class="text-lg select-none">{{ user.group }}</p>
            <p class="text-base lowercase select-none">{{ user.role }}</p>
          </div>
        </div>
        <div class="flex flex-col w-full items-start self-start gap-2">
          <div class="flex w-full justify-between">
            <p>Решено задач:</p>
            <p>{{ user.markCount }}</p>
          </div>
          <hr class="bg-black/[0.5]" />
          <div class="flex w-full justify-between">
            <p>Общее количество очков:</p>
            <p>{{ user.score }}</p>
          </div>
        </div>
      </div>
      <form
        v-else
        class="flex flex-col gap-4 items-center bg-back p-8 rounded-xl drop-shadow-lg fade-in-animation"
        @submit.prevent="auth()"
      >
        <p class="uppercase tracking-wide font-semibold text-lg">Авторизация</p>
        <div class="flex flex-col gap-4 w-full items-center">
          <EditText ref="login" placeholder="Логин" />
          <EditText ref="pass" placeholder="Пароль" input-type="password" />
        </div>
        <div class="flex flex-col gap-2 justify-center items-center w-full">
          <Button type="submit" class="py-0 px-2 text-base -mr-1">
            Войти
          </Button>
          <p class="text-sm text-center">
            <strong>Внимание:</strong> у вас будет активна только одна сессия.
            <br />
            При перезагрузке страницы, она истекает <br />
            и необходимо будет войти в аккаунт заново.
          </p>
        </div>
      </form>
    </transition>
  </div>
</template>

<script>
import { userStore } from "@/store";
import EditText from "@/components/ui/editText";
import Button from "@/components/ui/button";
import API from "@/mixins/api";

export default {
  name: "profileView",
  components: { Button, EditText },
  data() {
    return {
      user: userStore(),
    };
  },
  methods: {
    auth() {
      API.auth(this.$refs.login.getText(), this.$refs.pass.getText()).then(
        (e) => {
          if ("error" in e) {
            this.$refs.pass.setError(e.error);
          } else {
            this.user.userId = e.response.id;
            this.user.token = e.response.access_token;
            this.user.login = this.$refs.login.getText();
            API.getUser(this.user.userId).then((e) => {
              this.user.name = e.response.name;
              this.user.marks = e.response.marks;
              this.user.group = e.response.group;
              let role = e.response.role;
              API.getRole(role).then((res) => {
                this.user.role = res.response.title;
              });
            });
            console.log(e);
          }
        }
      );
      console.log(this.user);
    },
  },
};
</script>

<style scoped>
.fade-leave-active,
.fade-enter-active {
  transition: all 0.3s ease-in-out;
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
  animation: fadeOnShow 0.3s ease-in-out;
}
</style>
