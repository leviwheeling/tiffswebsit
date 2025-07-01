/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./app/templates/**/*.html",
      "./app/static/js/**/*.js"
    ],
    theme: {
      extend: {
        colors: {
          brand: "#002654",
          coral: "#F0645A",
          "warm-gray": "#F4F4F5",
        },
        textColor: {
          brand: "#002654",
          coral: "#F0645A",
        },
        backgroundColor: {
          brand: "#002654",
          coral: "#F0645A",
        },
        fontFamily: {
          sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "Helvetica Neue", "Arial", "Noto Sans", "sans-serif"],
        },
      },
    },
    plugins: [require('@tailwindcss/forms')],
  };
  