/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './index.html',
      './src/**/*.{vue,ts,html,js}',
      './src/*.{vue,ts,html,js}',
  ],
  theme: {
    extend: {
        screens: {
            compact: {max: '640px'},
            extended: {min: '641px', max: '1280px'},
            maximized: {min: '1281px'}
        },
        colors: {
            surface: '#cffafe',
            back: '#ecfeff',
            fore: '#155e75',
            accent: '#0e7490',
            primary: '#164e63',
        }
    },
  },
  plugins: [],
}
