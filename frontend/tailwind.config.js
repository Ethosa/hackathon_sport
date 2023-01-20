/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,ts,html,js}",
    "./src/*.{vue,ts,html,js}",
  ],
  theme: {
    extend: {
      screens: {
        compact: { max: "640px" },
        extended: { min: "641px", max: "1280px" },
        maximized: { min: "1281px" },
      },
      colors: {
        "back-left": "#0e111c",
        "back-right": "#090d1e",
        surface: "#26293b",
        back: "#303748",
        fore: "#abb8da",
        accent: "#b7b9e8",
        primary: "#c6c7f5",
      },
    },
  },
  plugins: [],
};
