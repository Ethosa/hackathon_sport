<template>
  <div class="flex-auto flex flex-col gap-2 p-10">
    <p class="text-2xl uppercase font-semibold tracking-widest">{{ title }}</p>
    <p class="indent-8 text-xl">{{ description }}</p>
    <div class="flex w-full justify-center">
      <div
        v-for="(lang, index) in languages"
        :key="index"
        class="font-semibold tracking-widest"
      >
        <div
          v-if="index + 1 === selectedLanguage"
          class="px-8 py-1 bg-fore select-none hover:px-16 hover:bg-accent active:bg-primary transition-all duration-300 text-back"
        >
          {{ lang.title }}
        </div>
        <div
          v-else
          class="px-8 py-1 bg-back select-none hover:px-16 hover:bg-accent hover:text-back active:text-back active:bg-primary transition-all duration-300"
          @click="setLang(index)"
        >
          {{ lang.title }}
        </div>
      </div>
    </div>
    <div ref="editor" class="flex-auto w-full h-full self-center" />
    <div class="w-full flex justify-center">
      <Button :flat="false">Отправить на проверку</Button>
    </div>
  </div>
</template>

<script>
import API from "@/mixins/api";
import loader from "@monaco-editor/loader";
import Button from "@/components/ui/button.vue";
import { editor } from "monaco-editor";

export default {
  name: "taskView",
  mixins: [API],
  data() {
    return {
      taskId: this.$route.params.id,
      title: "",
      description: "",
      selectedLanguage: 1,
      languages: [],
      editor: null,
      monaco: null,
    };
  },
  components: {
    Button,
  },
  methods: {
    setLang(index) {
      let lang = this.languages[index].name;
      this.selectedLanguage = index + 1;
      this.monaco.editor.setModelLanguage(this.editor.getModel(), lang);
      this.editor.updateOptions({ language: lang });
    },
    updateEditor() {
      loader
        .init()
        .then((monaco) => {
          this.monaco = monaco;
          import("monaco-themes/themes/GitHub Dark.json")
            .then((data) => {
              monaco.editor.defineTheme("myTheme", data);
              this.editor = monaco.editor.create(this.$refs.editor, {
                language: this.languages[this.selectedLanguage - 1].name,
                theme: "myTheme",
                automaticLayout: true,
                wordWrap: "on",
                fontSize: 20,
                smoothScrolling: true,
              });
            })
            .catch((err) => {
              console.error("Monaco onImport exception: ", err);
            });
        })
        .catch((err) => {
          console.error("Monaco onLoad exception: ", err);
        });
    },
  },
  mounted() {
    API.getTask(this.taskId).then((r) => {
      this.title = r.response.title;
      this.description = r.response.description;
    });
    API.getAllLangs().then((r) => {
      this.languages = r.response;
      this.updateEditor();
    });
  },
};
</script>
