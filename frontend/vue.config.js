const { defineConfig } = require('@vue/cli-service')
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = defineConfig({
  transpileDependencies: true,
  pages: {
    index: {
      title: "Спортпрог ⚽",
      entry: "src/main.js"
    }
  },
  configureWebpack: (config) => {
    config.plugins.push(new MonacoWebpackPlugin({
      languages: ['python', 'csharp', 'java']
    }));
  }
})
