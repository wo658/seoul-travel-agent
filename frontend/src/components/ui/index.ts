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
  type CardProps,
  type CardHeaderProps,
  type CardTitleProps,
  type CardDescriptionProps,
  type CardContentProps,
} from './card';
export { Input, type InputProps } from './input';
export { Text } from './text';
export { Separator } from './separator';
export { Chip, chipTextVariants, chipVariants, type ChipProps } from './chip';
export { Badge, badgeTextVariants, badgeVariants, type BadgeProps } from './badge';
export { TextArea, type TextAreaProps } from './textarea';
export { IconContainer, type IconContainerProps } from './icon-container';
export { LoadingState, ErrorState, EmptyState, type LoadingStateProps, type ErrorStateProps, type EmptyStateProps } from './states';
