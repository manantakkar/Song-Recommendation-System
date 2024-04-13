/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        solitude: "#E9EDF5",
        hover_color: "#7a7f978c",
        blue_charcoal: "#252C32",
        primary: "#0039A6",
        raven: "#687182",
        pristine_oceanic:"#00d8bf",

      },
      fontFamily: {
        Inter: "'Inter Variable', sans-serif",
        Oxanium: '"Oxanium", sans-serif'
      },
    },
  },
  plugins: [],
};
