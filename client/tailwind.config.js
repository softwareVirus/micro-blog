/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}']
}

