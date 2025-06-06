/**
 * API Service Layer for AI Profile Generator Frontend
 * 
 * This service handles all communication with the Flask backend API.
 * It provides type-safe methods for all API endpoints and includes
 * proper error handling, request transformation, and response parsing.
 */

import axios, { AxiosResponse, AxiosError } from 'axios';
import {
  ApiResponse,
  ProfileGenerationResult,
  SearchByUrlRequest,
  SearchByNameRequest,
  ValidateUrlRequest,
  ValidateUrlResponse,
  LinkedInUrlSearchResult
} from '@/types';

// ===== API Configuration =====

/**
 * Base API URL - uses proxy configuration in package.json for development
 * In production, this would be replaced with the actual API URL
 */
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

/**
 * Axios instance with default configuration
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout for profile generation
  headers: {
    'Content-Type': 'application/json',
  },
});

// ===== Request Interceptor =====

/**
 * Add request interceptor for logging and authentication
 */
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// ===== Response Interceptor =====

/**
 * Add response interceptor for consistent error handling
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error: AxiosError) => {
    console.error(`❌ API Error: ${error.response?.status} ${error.config?.url}`);
    
    // Transform error for consistent handling
    const apiError = {
      message: 'An error occurred',
      status: error.response?.status || 500,
      data: error.response?.data || null
    };

    if (error.response?.data && typeof error.response.data === 'object') {
      const errorData = error.response.data as any;
      apiError.message = errorData.message || errorData.error?.message || 'API Error';
    }

    return Promise.reject(apiError);
  }
);

// ===== API Service Class =====

/**
 * Main API service class with all endpoint methods
 */
class ApiService {
  
  // ===== Health Check Methods =====

  /**
   * Check API health status
   */
  async checkHealth(): Promise<ApiResponse> {
    const response = await apiClient.get('/health');
    return response.data;
  }

  /**
   * Get detailed API status
   */
  async getStatus(): Promise<ApiResponse> {
    const response = await apiClient.get('/status');
    return response.data;
  }

  // ===== Profile Generation Methods =====

  /**
   * Generate profile briefing from LinkedIn URL
   * 
   * @param request - URL and optional meeting context
   * @returns Complete profile with AI briefing and news
   */
  async generateProfileFromUrl(request: SearchByUrlRequest): Promise<ApiResponse<ProfileGenerationResult>> {
    const response = await apiClient.post('/search/by-url', request);
    return response.data;
  }

  /**
   * Generate profile briefing by searching for person name
   * 
   * @param request - Person name, optional company, and meeting context
   * @returns Complete profile with AI briefing and news
   */
  async generateProfileFromName(request: SearchByNameRequest): Promise<ApiResponse<ProfileGenerationResult>> {
    const response = await apiClient.post('/search/by-name', request);
    return response.data;
  }

  // ===== Utility Methods =====

  /**
   * Search for LinkedIn URL only (without generating full briefing)
   * 
   * @param personName - Full name of the person
   * @param companyName - Optional company name
   * @returns LinkedIn URL if found
   */
  async searchLinkedInUrlOnly(personName: string, companyName?: string): Promise<ApiResponse<LinkedInUrlSearchResult>> {
    const request = {
      person_name: personName,
      company_name: companyName || ''
    };
    
    const response = await apiClient.post('/search/linkedin-url-only', request);
    return response.data;
  }

  /**
   * Validate if a URL is a valid LinkedIn profile URL
   * 
   * @param url - URL to validate
   * @returns Validation result
   */
  async validateLinkedInUrl(url: string): Promise<ApiResponse<ValidateUrlResponse>> {
    const request: ValidateUrlRequest = { url };
    const response = await apiClient.post('/search/validate-url', request);
    return response.data;
  }

  // ===== Information Methods =====

  /**
   * Get information about available search methods
   */
  async getSearchMethods(): Promise<ApiResponse> {
    const response = await apiClient.get('/search/methods');
    return response.data;
  }

  /**
   * Get profile generation capabilities and features
   */
  async getProfileInfo(): Promise<ApiResponse> {
    const response = await apiClient.get('/profile/info');
    return response.data;
  }

  /**
   * Get API usage examples
   */
  async getExamples(): Promise<ApiResponse> {
    const response = await apiClient.get('/profile/examples');
    return response.data;
  }

  // ===== Convenience Methods =====

  /**
   * Quick search method that automatically determines search type
   * 
   * @param query - LinkedIn URL or person name
   * @param companyName - Optional company name (for name searches)
   * @param meetingContext - Optional meeting context
   * @returns Profile generation result
   */
  async quickSearch(
    query: string, 
    companyName?: string, 
    meetingContext?: string
  ): Promise<ApiResponse<ProfileGenerationResult>> {
    
    // Determine if query is a LinkedIn URL
    const isLinkedInUrl = this.isLinkedInUrl(query);
    
    if (isLinkedInUrl) {
      // Search by URL
      return this.generateProfileFromUrl({
        linkedin_url: query,
        meeting_context: meetingContext
      });
    } else {
      // Search by name
      return this.generateProfileFromName({
        person_name: query,
        company_name: companyName,
        meeting_context: meetingContext
      });
    }
  }

  /**
   * Helper method to check if a string is a LinkedIn URL
   * 
   * @param url - String to check
   * @returns True if it's a LinkedIn URL
   */
  private isLinkedInUrl(url: string): boolean {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname.includes('linkedin.com') && urlObj.pathname.includes('/in/');
    } catch {
      return false;
    }
  }
}

// ===== Export API Service Instance =====

/**
 * Single instance of the API service to be used throughout the application
 */
export const apiService = new ApiService();

/**
 * Export the service class for testing or custom instances
 */
export { ApiService };

/**
 * Export common error types for error handling
 */
export interface ApiError {
  message: string;
  status: number;
  data: any;
}

/**
 * Helper function to check if an error is an API error
 */
export const isApiError = (error: any): error is ApiError => {
  return error && typeof error.message === 'string' && typeof error.status === 'number';
}; 