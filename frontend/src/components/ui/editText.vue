<template>
  <div
    :class="`flex w-fit text-white bg-transparent outline outline-2 ${
      isError ? 'outline-red-500' : 'outline-primary'
    } p-2 cursor-text transition-all duration-300`"
    @click="focus()"
  >
    <div class="flex items-center gap-2 relative group cursor-text">
      <input
        :type="InputType"
        :id="uniqueId"
        ref="input"
        required
        class="outline-0 bg-back/[0.3] px-2 peer"
        @input="handleInput($event)"
      />
      <label
        :for="uniqueId"
        class="select-none text-fore/[0.5] bg-back transform transition-all absolute top-0 left-0 h-full flex items-center pl-2 text-sm group-focus-within:text-xs peer-valid:text-xs group-focus-within:h-1/2 peer-valid:h-1/2 group-focus-within:-translate-y-full peer-valid:-translate-y-full group-focus-within:px-1 peer-valid:px-1 peer-valid:-my-1 group-focus-within:-my-1 cursor-text group-focus-within-text-fore peer-valid:text-fore peer-valid:rounded-xl"
      >
        {{ Placeholder }}
      </label>
      <Transition name="error">
        <label
          :for="uniqueId"
          v-show="isError"
          class="select-none text-red-500 translate-y-full px-1 bg-back -my-1 transform transition-all absolute top-0 left-0 h-full flex items-center text-sm"
        >
          {{ error }}
        </label>
      </Transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "editText",
  emits: ["onInput"],
  props: {
    placeholder: String,
    inputType: String,
    errorText: String,
    leadingIcon: String,
    trailingIcon: String,
    important: Boolean,
    minLength: Number,
    maxLength: Number,
  },
  computed: {
    InputType() {
      return this.inputType ? this.inputType : "text";
    },
    Placeholder() {
      return this.placeholder ? this.placeholder : "Write something ...";
    },
  },
  data() {
    return {
      uniqueId: Date.now(),
      error: this.errorText == null ? "" : this.errorText,
      isImportant: this.important == null ? false : this.important,
      isError: false,
      minLen: typeof this.minLength === "number" ? this.minLength : -1,
      maxLen: typeof this.maxLength === "number" ? this.maxLength : -1,
    };
  },
  methods: {
    getText() {
      return this.$refs.input.value;
    },
    focus() {
      this.$refs.input.focus();
    },
    setError(error) {
      this.error = error;
      this.isError = true;
    },
    hideError() {
      this.isError = false;
    },
    showError() {
      this.isError = true;
    },
    clear() {
      this.$refs.input.value = "";
      this.isError = false;
    },
    handleInput(event) {
      let text = this.$refs.input.value;
      this.$emit("onInput", text, event.data);
      // miss
      this.hideError();
      if (text === "" && this.isImportant) this.setError("field missed");
      // minimum length
      if (this.minLen > 0 && text.length < this.minLen)
        this.setError(`requires more then ${this.minLen} chars`);
      // maximum length
      if (this.maxLen > 0 && text.length > this.maxLen)
        this.setError(`requires less then ${this.maxLen} chars`);
    },
  },
  mounted() {
    if (this.isImportant) {
      this.setError("field missed");
    }
  },
};
</script>

<style scoped>
.error-enter-active,
.error-leave-active {
  transition: opacity 0.3s ease;
}

.error-enter-from,
.error-leave-to {
  opacity: 0;
}
</style>
