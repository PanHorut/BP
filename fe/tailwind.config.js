/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1d3557',
        },
        secondary: {
          DEFAULT: '#457b9d', 
        },
        tertiary: {
          DEFAULT: '#a8dadc', 
        },
        white: {
          DEFAULT: '#f1faee', 
        },
        accent: {
          DEFAULT: '#e63946', 
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
