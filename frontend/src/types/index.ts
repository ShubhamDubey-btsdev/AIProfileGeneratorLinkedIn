/**
 * TypeScript Type Definitions for AI Profile Generator Frontend
 * 
 * This file contains all the type definitions used throughout the application
 * to ensure type safety and better developer experience.
 */

// ===== API Response Types =====

/**
 * Standard API response wrapper used by all endpoints
 */
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  timestamp: string;
  data: T;
  error?: {
    code: number;
    message: string;
    details?: any;
  };
}

/**
 * LinkedIn profile data structure returned from scraping
 */
export interface LinkedInProfile {
  name: string;
  title: string;
  company: string;
  url: string;
  location?: string;
  summary?: string;
  experience?: Array<{
    title: string;
    company: string;
    duration: string;
    description?: string;
  }>;
  education?: Array<{
    school: string;
    degree: string;
    field?: string;
    years?: string;
  }>;
  skills?: string[];
  connections?: number;
}

/**
 * AI-generated briefing structure
 */
export interface AIBriefing {
  executive_summary: string;
  key_insights: string[];
  conversation_starters: string[];
  recent_activity: string;
  meeting_preparation: string[];
  strategic_notes: string[];
  confidence_score: number;
}

/**
 * News article structure from news API
 */
export interface NewsArticle {
  title: string;
  description: string;
  url: string;
  source: string;
  published_at: string;
  relevance_score?: number;
}

/**
 * Complete profile generation response
 */
export interface ProfileGenerationResult {
  linkedin_profile: LinkedInProfile | null;
  briefing: AIBriefing | null;
  news_articles: NewsArticle[];
  search_method: string;
  processing_time: number;
  profile_found: boolean;
  briefing_generated: boolean;
  news_found: number;
}

// ===== Search Request Types =====

/**
 * Request structure for URL-based search
 */
export interface SearchByUrlRequest {
  linkedin_url: string;
  meeting_context?: string;
}

/**
 * Request structure for name-based search
 */
export interface SearchByNameRequest {
  person_name: string;
  company_name?: string;
  meeting_context?: string;
}

/**
 * Request for LinkedIn URL validation
 */
export interface ValidateUrlRequest {
  url: string;
}

/**
 * Response for LinkedIn URL validation
 */
export interface ValidateUrlResponse {
  url: string;
  is_valid: boolean;
  url_type: string;
}

/**
 * LinkedIn URL search response (without full briefing)
 */
export interface LinkedInUrlSearchResult {
  linkedin_url: string | null;
  person_name: string;
  company_name: string;
  search_method: string;
  processing_time: number;
  found: boolean;
  error?: string;
}

// ===== Component Props Types =====

/**
 * Props for the main search form component
 */
export interface SearchFormProps {
  onSearch: (request: SearchByUrlRequest | SearchByNameRequest) => void;
  isLoading: boolean;
}

/**
 * Props for the profile display component
 */
export interface ProfileDisplayProps {
  result: ProfileGenerationResult | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * Props for individual profile sections
 */
export interface ProfileSectionProps {
  profile: LinkedInProfile;
  className?: string;
}

export interface BriefingSectionProps {
  briefing: AIBriefing;
  className?: string;
}

export interface NewsSectionProps {
  articles: NewsArticle[];
  className?: string;
}

// ===== UI State Types =====

/**
 * Search form state
 */
export interface SearchFormState {
  searchType: 'url' | 'name';
  personName: string;
  companyName: string;
  linkedinUrl: string;
  meetingContext: string;
}

/**
 * Application state for search functionality
 */
export interface SearchState {
  isLoading: boolean;
  result: ProfileGenerationResult | null;
  error: string | null;
  searchHistory: SearchHistoryItem[];
}

/**
 * Search history item
 */
export interface SearchHistoryItem {
  id: string;
  timestamp: string;
  searchType: 'url' | 'name';
  query: string;
  success: boolean;
  processingTime: number;
}

// ===== Utility Types =====

/**
 * Loading states for different operations
 */
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

/**
 * Theme configuration
 */
export interface ThemeConfig {
  primaryColor: string;
  secondaryColor: string;
  backgroundColor: string;
  textColor: string;
  borderColor: string;
}

/**
 * Toast notification types
 */
export type ToastType = 'success' | 'error' | 'info' | 'warning';

/**
 * Export all types for easy importing
 */
export type {
  // Re-export commonly used types
  ApiResponse as API,
  LinkedInProfile as Profile,
  AIBriefing as Briefing,
  NewsArticle as Article,
  ProfileGenerationResult as Result
}; 