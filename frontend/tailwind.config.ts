import { nextui } from '@nextui-org/theme'
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
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
              foreground: "#f0f8ff",
              '50': '#f0f8ff',
              '100': '#e0f0fe',
              '200': '#bae2fd',
              '300': '#81cefd',
              '400': '#37b3f9',
              '500': '#0c99eb',
              '600': '#0179c8',
              '700': '#0260a2',
              '800': '#065286',
              '900': '#0b446f',

            },
            secondary: {
              DEFAULT: "#cc8840",
              foreground: "#ECE5DC",
              '50': '#fbf8ef',
              '100': '#f4e9d1',
              '200': '#e8d19f',
              '300': '#dbb66e',
              '400': '#d39e4c',
              '500': '#cc8840',
              '600': '#b2652d',
              '700': '#944b29',
              '800': '#793d27',
              '900': '#643323',
            },
            default: {
              DEFAULT: "#f2e9bd",
              foreground: "#0c0b03",
              '50': '#fcf9ee',
              '100': '#f2e9bd',
              '200': '#ebdd9c',
              '300': '#e1c968',
              '400': '#dab545',
              '500': '#d19a2f',
              '600': '#b97926',
              '700': '#9a5b23',
              '800': '#7e4822',
              '900': '#683b1f',
            },
            success: {
              DEFAULT: "#91C613",
              foreground: "#f9fee7",
              '50': '#f9fee7',
              '100': '#f1fdca',
              '200': '#e2fa9c',
              '300': '#cdf462',
              '400': '#b6e833',
              '500': '#91c613',
              '600': '#74a50b',
              '700': '#587d0e',
              '800': '#476311',
              '900': '#3c5413',
            },
            warning: {
              DEFAULT: "#FFBE0C",
              foreground: "#0c0b03",
              '50': '#fffeea',
              '100': '#fffac5',
              '200': '#fff685',
              '300': '#ffea46',
              '400': '#ffdb1b',
              '500': '#ffbe0c',
              '600': '#e29000',
              '700': '#bb6502',
              '800': '#984e08',
              '900': '#7c400b',
            },
            danger: {
              DEFAULT: "#faa671",
              foreground: "#fee8d6",
              '50': '#fff5ed',
              '100': '#fee8d6',
              '200': '#fccdac',
              '300': '#faa671',
              '400': '#f77b40',
              '500': '#f4591b',
              '600': '#e53f11',
              '700': '#be2d10',
              '800': '#972515',
              '900': '#7a2114',
            }
          }
        },
      }
    })
  ]
};

export default config;
