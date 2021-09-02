module.exports = {
  purge: { content: ['./**/templates/**/*.html', '../envs/**/*.html'], },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        yellow: "#EAC543",
        orange: "#F59E0B"
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.gray.100'),
            a: {
              color: '#EAC543',
              '&:hover': {
                color: '#F59E0B',
              },
            },
            h2: {
              color: '#EAC543',
              '&:hover': {
                color: '#F59E0B',
              },
            },


            // ...
          },
        },
      }),
      /*
      typography: {

        DEFAULT: {
          css: {

            a: {
              color: '#EAC543',
              '&:hover': {
                color: '#F59E0B',
              },
            },

          },

        },
      }*/

    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms")
    ,]
};


