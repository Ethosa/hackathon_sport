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
            'back-left': '#130e1c',
            'back-right': '#09151e',
            surface: '#2d263b',
            back: '#383048',
            fore: '#bcabda',
            accent: '#c5b7e8',
            primary: '#d5c6f5',
        }
    },
  },
  plugins: [],
}
