<template>
  <div class="flex-auto flex flex-col gap-3 px-40 showTask">
    <p class="text-3xl uppercase font-semibold self-center tracking-widest">
      Секция: "{{ title }}"
    </p>
    <p class="indent-8 text-xl">{{ description }}</p>

    <div class="flex-auto flex">
      <div ref="editor" class="w-3/4" />
      <div
        class="font-mono flex flex-col gap-2 w-1/4 border-b-[1px] border-t-[1px] border-r-[1px] rounded-r-[10px] p-3"
      >
        <p v-if="apiStatus === false" class="text-center">
          Ошибка компилятора ❌
        </p>
        <p v-else-if="apiStatus === true" class="text-center">
          Скомпилировано ✅
        </p>
        <p v-else-if="apiStatus === 'sending'" class="text-center">
          Компилирование...
        </p>
        <p v-else class="text-center">Ожидание запуска...</p>

        <div
          :class="`w-full border-b-[1px] ${
            apiStatus === false
              ? 'border-red-400'
              : apiStatus === true
              ? 'border-green-400'
              : apiStatus === 'sending'
              ? 'border-orange-400'
              : 'border-white'
          } transition-all duration-300`"
        />

        <div class="flex-auto overflow-x-scroll">
          <div v-if="compiled.compile_result.compile.stdout !== ''" class="showTask">
            <p
              v-for="str in compiled.compile_result.compile.stdout.split('\n')"
              :key="
                compiled.compile_result.compile.stdout
                  .split('\n')
                  .findIndex((el) => el === str) + 1
              "
            >
              {{ str }}
            </p>
          </div>
          <p v-if="compiled.compile_result.compile.stderr !== ''">
            {{ compiled.compile_result.compile.stderr.split('",')[1] }}
          </p>
          <div v-if="compiled.compile_result.run.stdout !== ''" class="showTask">
            <p
              v-for="str in compiled.compile_result.run.stdout.split('\n')"
              :key="
                compiled.compile_result.run.stdout.split('\n').findIndex((el) => el === str) +
                1
              "
            >
              {{ str }}
            </p>
          </div>
          <div v-if="compiled.compile_result.run.stderr !== ''" class="flex flex-col gap-6">
            <p>
              {{ compiled.compile_result.compile.stderr }}
            </p>
            <p>
              {{ compiled.compile_result.run.stderr }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="flex w-full justify-center items-center gap-10 my-4">
      <div class="flex justify-center">
        <div
          v-for="(lang, index) in languages"
          :key="index"
          class="font-semibold tracking-widest cursor-pointer"
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

      <Button :flat="false" @click="run(code)" class="w-full text-sm"
        ><svg xmlns="http://www.w3.org/2000/svg" height="25" width="24">
          <path d="M8.5 18.1V5.9l9.575 6.1Z" />
        </svg>
        <p>Запустить</p></Button
      >
    </div>
  </div>
</template>

<script>
import API from "@/mixins/api";
import loader from "@monaco-editor/loader";
import Button from "@/components/ui/button.vue";
import { userStore } from "@/store";

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
      editor: undefined,
      monaco: undefined,
      code: "",
      compiled: {
        success: 0,
        errors: 0,
        max_success: 0,
        compile_result: {
          compile: {
            stdout: "",
            stderr: "",
          },
          run: {
            stdout: "",
            stderr: "",
          },
        }
      },
      apiStatus: undefined,
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
      let values = this;

      loader
        .init()
        .then((monaco) => {
          values.monaco = monaco;
          import("monaco-themes/themes/GitHub Dark.json")
            .then((data) => {
              monaco.editor.defineTheme("myTheme", data);

              const code = monaco.editor.create(this.$refs.editor, {
                language: this.languages[this.selectedLanguage - 1].name,
                theme: "myTheme",
                automaticLayout: true,
                wordWrap: "on",
                fontSize: 16,
                smoothScrolling: true,
                tabCompletion: true,
              });

              values.editor = code;

              code.onKeyUp(() => {
                values.code = code.getValue();
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
    async run(code) {
      this.apiStatus = "sending";
      this.compiled = {
        success: 0,
        errors: 0,
        max_success: 0,
        compile_result: {
          compile: {
            stdout: "",
            stderr: "",
          },
          run: {
            stdout: "",
            stderr: "",
          },
        }
      };

      this.compiled = await API.sendSolution(
        code,
        parseInt(this.taskId),
        this.selectedLanguage
      );
      console.log(this.compiled);

      this.compiled.compile_result.run.stdout === ""
        ? (this.apiStatus = false)
        : (this.apiStatus = true);
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
