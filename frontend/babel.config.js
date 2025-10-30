module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      ["babel-preset-expo", { jsxImportSource: "nativewind" }],
      "nativewind/babel",
    ],
    plugins: [
      [
        "module-resolver",
        {
          root: ["./"],
          alias: {
            "@": "./src",
            "@/components": "./src/components",
            "@/ui": "./src/components/ui",
            "@/screens": "./src/screens",
            "@/hooks": "./src/hooks",
            "@/lib": "./src/lib",
            "@/utils": "./src/utils",
            "@/services": "./src/services",
            "@/constants": "./src/constants",
            "@/types": "./src/types",
            "@/navigation": "./src/navigation",
            "@/assets": "./src/assets",
          },
        },
      ],
      "react-native-reanimated/plugin",
    ],
  };
};
