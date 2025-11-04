/**
 * UI Components based on react-native-reusables
 * Following shadcn/ui philosophy for React Native
 * All styling managed through Tailwind CSS with single source of truth
 */

export { Button, buttonTextVariants, buttonVariants, type ButtonProps } from './button';
export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  type CardProps,
  type CardHeaderProps,
  type CardTitleProps,
  type CardDescriptionProps,
  type CardContentProps,
  type CardFooterProps,
} from './card';
export { Input, type InputProps } from './input';
export { Text } from './text';
export { Separator } from './separator';

// Re-export chat components for convenience
export * from '../chat';
