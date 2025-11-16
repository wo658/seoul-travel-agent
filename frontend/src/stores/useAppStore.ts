import { create } from 'zustand';

/**
 * 전역 앱 상태 스토어
 *
 * loading, error 상태를 전역으로 관리하여
 * 각 화면에서 useState를 반복하지 않도록 합니다.
 */

interface AppState {
  // Loading states
  isLoading: boolean;
  loadingMessage?: string;

  // Error states
  error: string | null;

  // Actions
  setLoading: (loading: boolean, message?: string) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  reset: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  isLoading: false,
  loadingMessage: undefined,
  error: null,

  // Actions
  setLoading: (loading, message) => set({ isLoading: loading, loadingMessage: message }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
  reset: () => set({ isLoading: false, loadingMessage: undefined, error: null }),
}));

/**
 * 편의 hooks
 */
export const useLoading = () => {
  const { isLoading, loadingMessage, setLoading } = useAppStore();
  return { isLoading, loadingMessage, setLoading };
};

export const useError = () => {
  const { error, setError, clearError } = useAppStore();
  return { error, setError, clearError };
};
