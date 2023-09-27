/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')
module.exports = {
  content: ["./static/**/*.{html,js}", "./templates/**/*.{html,js}"],
    theme: {
      screens: {
        'xs': '475px',
        ...defaultTheme.screens,
      },
    extend: {},
  },
  plugins: [],
}
