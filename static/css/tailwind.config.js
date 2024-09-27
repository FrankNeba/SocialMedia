/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}",
     "../../templates/**/*.{html,js}",
    "../../posts/templates/posts/**/*.{html,js}",
    "../../authenticate/templates/authenticate/**/*.{html,js}",
    "../../adminpanel/templates/adminpanel/**/*.{html,js}",
    "../../message/templates/message/**/*.{html,js}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#428af5'
      },
      keyframes: {
        beat: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.5)' },
        },
      },
      animation: {
        beat: 'beat 1s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}

