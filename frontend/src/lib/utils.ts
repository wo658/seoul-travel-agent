import { type ClassValue, clsx } from 'clsx';

/**
 * Utility function to merge class names using clsx
 * Similar to shadcn/ui's cn utility
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}
