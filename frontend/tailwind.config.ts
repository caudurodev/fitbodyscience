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
    extend: {},
  },
  darkMode: 'class',
  plugins: [
    nextui({
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
              foreground: "#0e0801",
            },
            default: {
              DEFAULT: "#f2e9bd",
              foreground: "#0c0b03",
            },
            success: {
              DEFAULT: "#c8c8c5",
              foreground: "#0c0b03",
            },
            warning: {
              DEFAULT: "#cc8840",
              foreground: "#0c0b03",
            },
            danger: {
              DEFAULT: "#faa671",
              foreground: "#0c0b03",
            }
          }
        },
        dark: {
          layout: {},
          colors: {
            background: "#000000",
            foreground: "#ECEDEE",
            focus: "#006FEE",

            primary: {
              50: "#e6f1ff",
              100: "#cce3ff",
              200: "#99c7ff",
              300: "#66aaff",
              400: "#338eff",
              500: "#006FEE",
              600: "#005bc4",
              700: "#004493",
              800: "#002e62",
              900: "#001731",
              DEFAULT: "#006FEE",
              foreground: "#ffffff",
            },
            secondary: {
              50: "#f2e6ff",
              100: "#e6ccff",
              200: "#cc99ff",
              300: "#b366ff",
              400: "#9933ff",
              500: "#7828C8",
              600: "#6620a0",
              700: "#4d1878",
              800: "#331050",
              900: "#1a0828",
              DEFAULT: "#7828C8",
              foreground: "#ffffff",
            },
            danger: {
              50: "#fee6eb",
              100: "#fdccd7",
              200: "#fb99af",
              300: "#f96687",
              400: "#f7335f",
              500: "#E31B54",
              600: "#b61543",
              700: "#881032",
              800: "#5b0a22",
              900: "#2d0511",
              DEFAULT: "#E31B54",
              foreground: "#ffffff",
            }
          }
        }
      }
    })
  ]
};

export default config;
