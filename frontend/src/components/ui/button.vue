<template>
  <div class="w-fit h-fit tracking-wider font-semibold uppercase text-xl">
    <div
      v-if="flat"
      class="px-4 py-1 text-black cursor-pointer select-none hover:text-back hover:bg-fore active:bg-primary active:text-back transition-all duration-300"
    >
      <slot></slot>
    </div>
    <div
      v-else
      class="px-4 py-1 bg-fore text-back cursor-pointer select-none transition-all duration-300 hover:bg-accent active:bg-primary"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "Button",
  props: {
    flat: Boolean,
    text: String
  }
}
</script>
