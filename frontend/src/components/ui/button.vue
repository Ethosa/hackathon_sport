<template>
  <div class="w-fit h-fit tracking-wider font-semibold uppercase text-xl">
    <div
      v-if="flat"
      class="flex gap-3 items-center px-4 py-1 text-fore cursor-pointer select-none hover:text-back hover:bg-fore active:bg-primary active:text-back transition-all duration-300"
    >
      <slot></slot>
    </div>
    <div
      v-else
      class="flex gap-4 items-center px-4 py-1 bg-fore text-back cursor-pointer select-none transition-all duration-300 hover:bg-accent active:bg-primary"
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
  },
};
</script>
