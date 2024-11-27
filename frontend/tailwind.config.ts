import { nextui } from '@nextui-org/theme'
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        'fade-bg': {
          '0%': { backgroundColor: 'var(--bg-from)' },
          '100%': { backgroundColor: 'var(--bg-to)' }
        }
      },
      animation: {
        'fade-bg': 'fade-bg 2s ease-out forwards'
      }
    },
  },
  darkMode: 'class',
  plugins: [
    nextui({
      // prefix: 'nextui',
      addCommonColors: true,
      layout: {},
      themes: {
        light: {
          layout: {},
          colors: {
            background: "#f6f0ee",
            foreground: "#220705",
            focus: "#006FEE",
            primary: {
              DEFAULT: "#81cefd",
              foreground: "#673915",
            },
            secondary: {
              DEFAULT: "#cc8840",
              foreground: "#ECE5DC",
            },
            default: {
              DEFAULT: "#f2e9bd",
              foreground: "#0c0b03",
            },
            success: {
              DEFAULT: "#91C613",
              foreground: "#D2F189",
            },
            warning: {
              DEFAULT: "#FFBE0C",
              foreground: "#0c0b03",
            },
            danger: {
              DEFAULT: "#faa671",
              foreground: "#0c0b03",
            }
          }
        },
      }
    })
  ]
};

export default config;
