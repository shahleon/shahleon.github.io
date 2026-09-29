/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: '#1A1A1A',
        muted: '#5F6368',
        line: '#D0D4D9',
        panel: '#F7F8F9',
        individual: '#2E6DB4',
        social: '#7B3FB8',
        'social-tint': '#F0E7F9',
        collective: '#0E8A6A',
        'collective-tint': '#E2F3EE',
      },
      maxWidth: {
        content: '56rem',
      },
    },
  },
  plugins: [],
}
