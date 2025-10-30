const { getDefaultConfig } = require('expo/metro-config');
const { withNativeWind } = require('nativewind/metro');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Add support for path aliases
config.resolver.extraNodeModules = {
  '@': path.resolve(__dirname, 'src'),
  '@/components': path.resolve(__dirname, 'src/components'),
  '@/ui': path.resolve(__dirname, 'src/components/ui'),
  '@/screens': path.resolve(__dirname, 'src/screens'),
  '@/hooks': path.resolve(__dirname, 'src/hooks'),
  '@/lib': path.resolve(__dirname, 'src/lib'),
  '@/utils': path.resolve(__dirname, 'src/utils'),
  '@/services': path.resolve(__dirname, 'src/services'),
  '@/constants': path.resolve(__dirname, 'src/constants'),
  '@/types': path.resolve(__dirname, 'src/types'),
  '@/navigation': path.resolve(__dirname, 'src/navigation'),
  '@/assets': path.resolve(__dirname, 'src/assets'),
};

module.exports = withNativeWind(config, { input: './global.css' });
