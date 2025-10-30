/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./src/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Light mode colors from global.css :root
        background: "oklch(0.9232 0.0026 48.7171)",
        foreground: "oklch(0.2795 0.0368 260.0310)",
        card: {
          DEFAULT: "oklch(0.9699 0.0013 106.4238)",
          foreground: "oklch(0.2795 0.0368 260.0310)",
        },
        popover: {
          DEFAULT: "oklch(0.9699 0.0013 106.4238)",
          foreground: "oklch(0.2795 0.0368 260.0310)",
        },
        primary: {
          DEFAULT: "oklch(0.5854 0.2041 277.1173)",
          foreground: "oklch(1.0000 0 0)",
        },
        secondary: {
          DEFAULT: "oklch(0.8687 0.0043 56.3660)",
          foreground: "oklch(0.4461 0.0263 256.8018)",
        },
        muted: {
          DEFAULT: "oklch(0.9232 0.0026 48.7171)",
          foreground: "oklch(0.5510 0.0234 264.3637)",
        },
        accent: {
          DEFAULT: "oklch(0.9376 0.0260 321.9388)",
          foreground: "oklch(0.3729 0.0306 259.7328)",
        },
        destructive: {
          DEFAULT: "oklch(0.6368 0.2078 25.3313)",
          foreground: "oklch(1.0000 0 0)",
        },
        border: "oklch(0.8687 0.0043 56.3660)",
        input: "oklch(0.8687 0.0043 56.3660)",
        ring: "oklch(0.5854 0.2041 277.1173)",
        chart: {
          1: "oklch(0.5854 0.2041 277.1173)",
          2: "oklch(0.5106 0.2301 276.9656)",
          3: "oklch(0.4568 0.2146 277.0229)",
          4: "oklch(0.3984 0.1773 277.3662)",
          5: "oklch(0.3588 0.1354 278.6973)",
        },
        sidebar: {
          DEFAULT: "oklch(0.8687 0.0043 56.3660)",
          foreground: "oklch(0.2795 0.0368 260.0310)",
          primary: "oklch(0.5854 0.2041 277.1173)",
          "primary-foreground": "oklch(1.0000 0 0)",
          accent: "oklch(0.9376 0.0260 321.9388)",
          "accent-foreground": "oklch(0.3729 0.0306 259.7328)",
          border: "oklch(0.8687 0.0043 56.3660)",
          ring: "oklch(0.5854 0.2041 277.1173)",
        },
      },
      fontFamily: {
        sans: ["Plus Jakarta Sans", "sans-serif"],
        serif: ["Lora", "serif"],
        mono: ["Roboto Mono", "monospace"],
      },
      borderRadius: {
        sm: "calc(1.25rem - 4px)",
        md: "calc(1.25rem - 2px)",
        lg: "1.25rem",
        xl: "calc(1.25rem + 4px)",
      },
      boxShadow: {
        // Light mode shadows
        "2xs": "2px 2px 10px 4px hsl(240 4% 60% / 0.09)",
        xs: "2px 2px 10px 4px hsl(240 4% 60% / 0.09)",
        sm: "2px 2px 10px 4px hsl(240 4% 60% / 0.18), 2px 1px 2px 3px hsl(240 4% 60% / 0.18)",
        DEFAULT: "2px 2px 10px 4px hsl(240 4% 60% / 0.18), 2px 1px 2px 3px hsl(240 4% 60% / 0.18)",
        md: "2px 2px 10px 4px hsl(240 4% 60% / 0.18), 2px 2px 4px 3px hsl(240 4% 60% / 0.18)",
        lg: "2px 2px 10px 4px hsl(240 4% 60% / 0.18), 2px 4px 6px 3px hsl(240 4% 60% / 0.18)",
        xl: "2px 2px 10px 4px hsl(240 4% 60% / 0.18), 2px 8px 10px 3px hsl(240 4% 60% / 0.18)",
        "2xl": "2px 2px 10px 4px hsl(240 4% 60% / 0.45)",
      },
    },
  },
  plugins: [
    // Dark mode color overrides plugin
    function ({ addBase }) {
      addBase({
        '.dark': {
          '--tw-shadow-color': 'hsl(0 0% 0%)',
        },
      });
    },
    // Custom plugin to add dark mode colors
    function ({ addUtilities }) {
      const darkColors = {
        '.dark .bg-background': { backgroundColor: 'oklch(0.2244 0.0074 67.4370)' },
        '.dark .text-foreground': { color: 'oklch(0.9288 0.0126 255.5078)' },
        '.dark .bg-card': { backgroundColor: 'oklch(0.2801 0.0080 59.3379)' },
        '.dark .text-card-foreground': { color: 'oklch(0.9288 0.0126 255.5078)' },
        '.dark .bg-popover': { backgroundColor: 'oklch(0.2801 0.0080 59.3379)' },
        '.dark .text-popover-foreground': { color: 'oklch(0.9288 0.0126 255.5078)' },
        '.dark .bg-primary': { backgroundColor: 'oklch(0.6801 0.1583 276.9349)' },
        '.dark .text-primary-foreground': { color: 'oklch(0.2244 0.0074 67.4370)' },
        '.dark .bg-secondary': { backgroundColor: 'oklch(0.3359 0.0077 59.4197)' },
        '.dark .text-secondary-foreground': { color: 'oklch(0.8717 0.0093 258.3382)' },
        '.dark .bg-muted': { backgroundColor: 'oklch(0.2287 0.0074 67.4469)' },
        '.dark .text-muted-foreground': { color: 'oklch(0.7137 0.0192 261.3246)' },
        '.dark .bg-accent': { backgroundColor: 'oklch(0.3896 0.0074 59.4734)' },
        '.dark .text-accent-foreground': { color: 'oklch(0.8717 0.0093 258.3382)' },
        '.dark .bg-destructive': { backgroundColor: 'oklch(0.6368 0.2078 25.3313)' },
        '.dark .text-destructive-foreground': { color: 'oklch(0.2244 0.0074 67.4370)' },
        '.dark .border-border': { borderColor: 'oklch(0.3359 0.0077 59.4197)' },
        '.dark .bg-input': { backgroundColor: 'oklch(0.3359 0.0077 59.4197)' },
        '.dark .ring-ring': { '--tw-ring-color': 'oklch(0.6801 0.1583 276.9349)' },
      };
      addUtilities(darkColors);
    },
  ],
}
