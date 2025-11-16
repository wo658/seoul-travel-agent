/**
 * 여행 계획 뷰어/편집기 타입 정의
 */

import { Activity, DayItinerary, TravelPlan } from './index';

// ============================================================================
// Enhanced Activity Types (드래그앤드롭, 제스처)
// ============================================================================

export interface EditableActivity extends Activity {
  id: string; // 고유 ID (드래그앤드롭용)
  is_custom: boolean; // 사용자 직접 추가 여부
  is_locked: boolean; // 수정 잠금 여부
  alternatives?: VenueAlternative[]; // AI 추천 대안
}

export interface VenueAlternative {
  venue_name: string;
  venue_type: Activity['venue_type'];
  cost: number;
  description: string;
  rating?: number;
}

// ============================================================================
// Editable Day Itinerary
// ============================================================================

export interface EditableDayItinerary extends Omit<DayItinerary, 'activities'> {
  activities: EditableActivity[];
  is_expanded: boolean; // 접기/펼치기 상태
}

// ============================================================================
// Chat Messages for Plan Modification
// ============================================================================

export interface PlanChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  plan_snapshot?: TravelPlan; // 해당 메시지 시점의 계획 스냅샷
}

export interface ChatSuggestion {
  id: string;
  label: string;
  prompt: string;
}

// ============================================================================
// Plan Modification State
// ============================================================================

export interface PlanModificationState {
  original_plan: TravelPlan;
  current_plan: TravelPlan;
  modification_history: PlanChatMessage[];
  is_modifying: boolean;
  error?: string;
}

// ============================================================================
// Drag & Drop Types
// ============================================================================

export type DragItemType = 'activity';

export interface DragItem {
  type: DragItemType;
  activity: EditableActivity;
  dayIndex: number;
  activityIndex: number;
}

export interface DropResult {
  targetDayIndex: number;
  targetActivityIndex: number;
}

// ============================================================================
// Gesture Actions
// ============================================================================

export type ActivityAction =
  | 'edit'
  | 'delete'
  | 'duplicate'
  | 'lock'
  | 'unlock'
  | 'alternatives';

export interface ActivityGestureConfig {
  swipeThreshold: number; // 스와이프 감지 임계값 (px)
  longPressDelay: number; // 롱프레스 감지 시간 (ms)
}

// ============================================================================
// Quick Actions (빠른 수정 제안)
// ============================================================================

export interface QuickAction {
  id: string;
  icon: string;
  label: string;
  action: () => void;
}

// ============================================================================
// Plan Viewer Mode
// ============================================================================

export type PlanViewerMode = 'view' | 'edit' | 'chat';

export interface PlanViewerState {
  mode: PlanViewerMode;
  selectedActivity?: EditableActivity;
  selectedDayIndex?: number;
  chatVisible: boolean;
  quickActionsVisible: boolean;
}
