module.exports = {
  purge: { content: ['./**/templates/**/*.html','../envs/**/*.html'],},
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        yellow: "#EAC543",
        orange: "#F59E0B"
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require("@tailwindcss/forms")],
};
