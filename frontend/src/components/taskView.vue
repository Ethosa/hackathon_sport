<template>
  <div class="flex-auto flex flex-col gap-3 px-40 showTask">
    <div class="flex justify-between items-center tracking-widest">
      <p class="text-3xl font-semibold uppercase">Секция: "{{ title }}"</p>

      <p :class="`${completed === false ? 'text-red-500' : 'text-green-500'}`">
        {{
          completed === false ? "Задание не выполнено" : `${completed} баллов `
        }}
      </p>
    </div>
    <p class="indent-8 text-xl">{{ description }}</p>

    <div class="flex-auto flex max-h-[700px]">
      <div ref="editor" class="w-3/4" />
      <div
        class="font-mono flex flex-col gap-2 w-1/4 border-b-[1px] border-t-[1px] border-r-[1px] rounded-r-[10px] p-3"
      >
        <div class="w-full text-center cursor-default">
          {{
            apiStatus === false
              ? "Ошибка ❌"
              : apiStatus === true && compiled.success === compiled.max_success
              ? "Тесты пройдены ✅"
              : apiStatus === true && compiled.success !== compiled.max_success
              ? "Тесты не пройдены ❌"
              : apiStatus === "sending"
              ? "Компилирование 🛠"
              : apiStatus === null
              ? "Вывод отстутствует ❌"
              : "Ожидание запуска..."
          }}
        </div>

        <div
          :class="`w-full border-b-[1px] ${
            apiStatus === false
              ? 'border-red-400'
              : apiStatus === true && compiled.success === compiled.max_success
              ? 'border-green-400'
              : apiStatus === true && compiled.success !== compiled.max_success
              ? 'border-red-400'
              : apiStatus === 'sending'
              ? 'border-orange-400'
              : apiStatus === null
              ? 'border-red-400'
              : 'border-white'
          } transition-all duration-300`"
        />

        <div
          class="flex-auto overflow-scroll text-sm"
          v-if="compiled.compile_result"
        >
          <div v-if="compiled.compile_result.length > 0">
            <div
              v-if="
                compiled.compile_result[0].run.stderr !== '' ||
                compiled.compile_result[0].compile.stderr !== ''
              "
            >
              <div class="flex flex-col gap-6">
                <p>
                  {{ compiled.compile_result[0].compile.stderr }}
                </p>
                <p>
                  {{ compiled.compile_result[0].run.stderr.split('",')[1] }}
                </p>
              </div>
            </div>
            <div v-else>
              <div
                v-for="(result, index) in compiled.compile_result"
                :key="index"
              >
                <div v-if="result.compile.stdout !== ''" class="showTask">
                  <p
                    v-for="str in result.compile.stdout.split('\n')"
                    :key="
                      result.compile.stdout
                        .split('\n')
                        .findIndex((el) => el === str) + 1
                    "
                  >
                    {{ str }}
                  </p>
                </div>

                <div
                  v-if="
                    result.run.stderr === '' &&
                    result.compile.stderr === '' &&
                    apiStatus === true
                  "
                  :class="`flex justify-between items-center my-2 border-[1px] border-white p-2 border-opacity-40 rounded-md cursor-default ${
                    result.run.stdout === result.output
                      ? 'text-green-500'
                      : 'text-red-500'
                  } hover:border-opacity-90 transition-all duration-200`"
                >
                  <div>Ввод: {{ result.input }}</div>
                  <div class="flex flex-col">
                    <p>Результат: {{ result.run.stdout }}</p>
                    <p>Нужно: {{ result.output }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="compiled.max_success !== 0 && apiStatus === true">
              <div
                v-for="index in compiled.max_success -
                compiled.compile_result.length"
                :key="index"
                class="w-full opacity-60 text-center cursor-default"
              >
                Скрытый тест
              </div>
            </div>

            <div
              :class="`w-full border-b-[1px] border-white my-2 transition-all duration-300`"
              v-if="apiStatus === true"
            />

            <div
              class="flex flex-col gap-1 items-center justify-center cursor-default"
              v-if="apiStatus === true"
            >
              <p>
                Пройдено тестов: {{ this.compiled.success }}/{{
                  this.compiled.max_success
                }}
              </p>
              <p>Время прохождения: {{ compiled.time }} мс</p>
              <p>Размер файла: {{ compiled.weight }} байтов</p>
            </div>
          </div>
        </div>
        <div v-else>
          <div
            v-if="compiled.error === 'import is forbidden'"
            class="text-sm flex flex-col gap-3 cursor-default"
          >
            <p>Вы пытаетесь импортировать запрещённую библиотеку.</p>
            <p>Список разрешённых библиотек:</p>
            <ul>
              <li v-for="(lib, index) in compiled.available_list" :key="index">
                {{ lib }}
              </li>
            </ul>
          </div>
          <div
            v-else-if="compiled.error === 'Mark is exists'"
            class="text-sm flex flex-col gap-3 cursor-default"
          >
            <p>Работа уже была засчитана, переделать её невозможно)</p>
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
import { userStore } from "@/store";

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
      interpreterErr: false,
      description: "",
      selectedLanguage: 1,
      completed: false,
      languages: [],
      editor: undefined,
      monaco: undefined,
      code: "",
      compiled: this.reset(),
      apiStatus: undefined,
    };
  },
  components: {
    Button,
  },
  methods: {
    reset() {
      return {
        success: 0,
        errors: 0,
        max_success: 0,
        weight: 0,
        time: 0,
        score: 0,
        compile_result: [
          {
            input: "",
            output: "",
            compile: {
              stdout: "",
              stderr: "",
            },
            run: {
              stdout: "",
              stderr: "",
            },
          },
        ],
      };
    },
    updateTasks() {
      API.getUser(userStore().userId).then((e) => {
        userStore().marks = e.marks;
        userStore().marks.forEach((mark) => {
          mark.task.forEach((task) => {
            if (task.id == parseInt(this.taskId)) {
              this.completed = mark.score;
            }
          });
        });
      });
    },
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

      this.compiled = this.reset();
      this.compiled = await API.sendSolution(
        code,
        parseInt(this.taskId),
        this.selectedLanguage
      );

      if (this.compiled.compile_result) {
        this.compiled.compile_result.forEach((el) => {
          el.run.stderr !== "" || el.compile.stderr !== ""
            ? (this.apiStatus = false)
            : (this.apiStatus = true);
        });

        if (this.compiled.compile_result.length === 0) {
          this.apiStatus = null;
        }
      } else {
        this.apiStatus = false;
      }

      this.updateTasks();
    },
  },
  async mounted() {
    let res = await API.getTask(this.taskId)
    this.title = res.response.title;
    this.description = res.response.description;
    res = await API.getAllLangs()
    this.languages = res.response;
    this.updateEditor();
    this.updateTasks();
  },
};
</script>
