import React from 'react';
import { View } from 'react-native';
import { cn } from '@/lib/utils';

export interface IconContainerProps {
  /**
   * 아이콘 또는 기타 콘텐츠
   */
  children: React.ReactNode;

  /**
   * 크기 변형
   * - xs: 20x20 (w-5 h-5)
   * - sm: 32x32 (w-8 h-8)
   * - md: 40x40 (w-10 h-10)
   * - lg: 56x56 (w-14 h-14)
   * - xl: 64x64 (w-16 h-16)
   * - 2xl: 80x80 (w-20 h-20)
   */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';

  /**
   * 스타일 변형
   * - primary: 기본 프라이머리 배경
   * - primary-muted: 반투명 프라이머리 배경
   * - secondary: 세컨더리 배경
   * - muted: 뮤트 배경
   * - glass: 유리 효과 (backdrop-blur)
   */
  variant?: 'primary' | 'primary-muted' | 'secondary' | 'muted' | 'glass';

  /**
   * 추가 className
   */
  className?: string;
}

const sizeVariants = {
  xs: 'w-5 h-5',
  sm: 'w-8 h-8',
  md: 'w-10 h-10',
  lg: 'w-14 h-14',
  xl: 'w-16 h-16',
  '2xl': 'w-20 h-20',
};

const variantStyles = {
  primary: 'bg-primary',
  'primary-muted': 'bg-primary/10',
  secondary: 'bg-secondary',
  muted: 'bg-muted',
  glass: 'bg-white/10 backdrop-blur-xl border border-white/20',
};

/**
 * 아이콘을 감싸는 원형 컨테이너 컴포넌트
 *
 * 앱 전체에서 일관된 아이콘 컨테이너 스타일을 제공합니다.
 *
 * @example
 * ```tsx
 * <IconContainer size="md" variant="primary">
 *   <Plus size={20} className="text-primary-foreground" />
 * </IconContainer>
 * ```
 */
export function IconContainer({
  children,
  size = 'md',
  variant = 'primary',
  className,
}: IconContainerProps) {
  return (
    <View
      className={cn(
        'rounded-full items-center justify-center',
        sizeVariants[size],
        variantStyles[variant],
        className
      )}
    >
      {children}
    </View>
  );
}
