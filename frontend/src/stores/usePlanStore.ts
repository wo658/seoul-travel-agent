import { create } from 'zustand';
import { plansApi } from '@/lib/api';
import type { TypedPlanResponse } from '@/types';
import { toTypedPlanResponse } from '@/types';

/**
 * Plan 데이터 전역 스토어
 *
 * 여러 화면/컴포넌트에서 공유되는 plan 데이터를 관리합니다.
 * prop drilling을 방지하고 데이터 흐름을 단순화합니다.
 */

interface PlanState {
  // Current plan data
  currentPlan: TypedPlanResponse | null;
  plans: TypedPlanResponse[];

  // Loading states (specific to plan operations)
  isLoadingPlan: boolean;
  isLoadingPlans: boolean;

  // Actions
  setCurrentPlan: (plan: TypedPlanResponse | null) => void;
  setPlans: (plans: TypedPlanResponse[]) => void;

  // Async actions
  fetchPlan: (planId: number) => Promise<void>;
  fetchPlans: () => Promise<void>;
  updatePlan: (planId: number, data: any) => Promise<void>;
  deletePlan: (planId: number) => Promise<void>;

  // Clear
  clearCurrentPlan: () => void;
  reset: () => void;
}

export const usePlanStore = create<PlanState>((set, get) => ({
  // Initial state
  currentPlan: null,
  plans: [],
  isLoadingPlan: false,
  isLoadingPlans: false,

  // Setters
  setCurrentPlan: (plan) => set({ currentPlan: plan }),
  setPlans: (plans) => set({ plans }),

  // Fetch single plan
  fetchPlan: async (planId) => {
    set({ isLoadingPlan: true });
    try {
      const plan = await plansApi.get(planId);
      set({ currentPlan: toTypedPlanResponse(plan), isLoadingPlan: false });
    } catch (error) {
      set({ isLoadingPlan: false });
      throw error;
    }
  },

  // Fetch all plans
  fetchPlans: async () => {
    set({ isLoadingPlans: true });
    try {
      const plans = await plansApi.list();
      set({ plans: plans.map(toTypedPlanResponse), isLoadingPlans: false });
    } catch (error) {
      set({ isLoadingPlans: false });
      throw error;
    }
  },

  // Update plan
  updatePlan: async (planId, data) => {
    const updatedPlan = await plansApi.update(planId, data);
    const typedPlan = toTypedPlanResponse(updatedPlan);
    set({ currentPlan: typedPlan });

    // Also update in plans list if it exists
    const { plans } = get();
    const updatedPlans = plans.map(p => p.id === planId ? typedPlan : p);
    set({ plans: updatedPlans });
  },

  // Delete plan
  deletePlan: async (planId) => {
    await plansApi.delete(planId);

    // Remove from plans list
    const { plans } = get();
    set({ plans: plans.filter(p => p.id !== planId) });

    // Clear current plan if it's the deleted one
    const { currentPlan } = get();
    if (currentPlan?.id === planId) {
      set({ currentPlan: null });
    }
  },

  // Clear
  clearCurrentPlan: () => set({ currentPlan: null }),
  reset: () => set({ currentPlan: null, plans: [], isLoadingPlan: false, isLoadingPlans: false }),
}));

/**
 * Convenience hooks
 */
export const useCurrentPlan = () => {
  const { currentPlan, isLoadingPlan, fetchPlan, setCurrentPlan, clearCurrentPlan } = usePlanStore();
  return { currentPlan, isLoadingPlan, fetchPlan, setCurrentPlan, clearCurrentPlan };
};

export const usePlans = () => {
  const { plans, isLoadingPlans, fetchPlans, setPlans } = usePlanStore();
  return { plans, isLoadingPlans, fetchPlans, setPlans };
};
