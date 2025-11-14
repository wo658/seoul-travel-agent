/**
 * Icon exports for the application
 * Platform-aware icon system:
 * - Web: Uses @expo/vector-icons (Feather) for better compatibility
 * - Native: Uses lucide-react-native
 */
import { Platform } from 'react-native';
import * as WebIcons from './web-icons';
import * as LucideIcons from 'lucide-react-native';

// Select icon source based on platform
const Icons = Platform.OS === 'web' ? WebIcons : LucideIcons;

// Main navigation icons (web-compatible)
export const Home = Icons.Home;
export const Calendar = Icons.Calendar;
export const Settings = Icons.Settings;

// Common icons (web-compatible)
export const MapPin = Icons.MapPin;
export const Clock = Icons.Clock;
export const Star = Icons.Star;
export const ArrowLeft = Icons.ArrowLeft;
export const ArrowRight = Icons.ArrowRight;
export const Sparkles = Icons.Sparkles;
export const TrendingUp = Icons.TrendingUp;
export const User = Icons.User;
export const Search = Icons.Search;
export const Heart = Icons.Heart;
export const Bell = Icons.Bell;
export const Menu = Icons.Menu;
export const X = Icons.X;
export const Plus = Icons.Plus;
export const ChevronDown = Icons.ChevronDown;
export const ChevronUp = Icons.ChevronUp;
export const ChevronLeft = Icons.ChevronLeft;
export const ChevronRight = Icons.ChevronRight;
export const Check = Icons.Check;

// Additional icons (lucide only)
export const {
  Share2,
  Minus,
  Edit,
  Edit3,
  Trash2,
  Filter,
  Info,
  AlertCircle,
  CheckCircle,
  XCircle,
  Loader2,
  Send,
  MessageCircle,
  List,
  MoreVertical,
  DollarSign,
  Save,
  RefreshCw,
  GripVertical,
  Lock,
  Eye,
  Globe,
  Palette,
  Shield,
  HelpCircle,
  LogOut,
} = LucideIcons;

export type { LucideIcon } from 'lucide-react-native';
