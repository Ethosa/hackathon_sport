import { defineStore } from "pinia";

export const userStore = defineStore("userStore", {
  state: () => ({
    token: "",
    userId: 0,
    name: "",
    marks: [],
    group: "",
    role: "",
    login: "",
  }),
  getters: {
    isLoggedIn: (state) => {
      return state.userId !== 0;
    },
    markCount: (state) => {
      return state.marks.length;
    },
    score: (state) => {
      let score = 0;
      state.marks.forEach((mark) => {
        score += mark.score;
      });
      return score;
    },
  },
  actions: () => {},
});
