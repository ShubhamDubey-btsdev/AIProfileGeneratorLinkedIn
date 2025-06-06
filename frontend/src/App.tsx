/**
 * Main App Component
 * 
 * This is the root component of the AI Profile Generator frontend application.
 * It manages the overall application state, coordinates API calls, and renders
 * the main UI components with proper error handling and loading states.
 * 
 * Features:
 * - Centralized state management
 * - API integration with error handling
 * - Toast notifications
 * - Responsive layout
 * - Loading states
 */

import React, { useState } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import SearchForm from './components/SearchForm';
import ProfileDisplay from './components/ProfileDisplay';
// import Header from './components/Header';
// import Footer from './components/Footer';
import { apiService, isApiError } from './services/api';
import { SearchState, SearchByUrlRequest, SearchByNameRequest } from './types';
import './styles/globals.css';

/**
 * Main Application Component
 */
const App: React.FC = () => {
  // ===== Application State =====
  
  const [searchState, setSearchState] = useState<SearchState>({
    isLoading: false,
    result: null,
    error: null,
    searchHistory: []
  });

  // ===== API Integration =====

  /**
   * Handle profile search request (both URL and name-based)
   * 
   * @param request - Search request (URL or name-based)
   */
  const handleSearch = async (request: SearchByUrlRequest | SearchByNameRequest) => {
    // Set loading state
    setSearchState(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));

    try {
      let response: any;
      let searchType: 'url' | 'name';
      let query: string;

      // Determine search type and call appropriate API method
      if ('linkedin_url' in request) {
        // URL-based search
        searchType = 'url';
        query = request.linkedin_url;
        response = await apiService.generateProfileFromUrl(request);
      } else {
        // Name-based search
        searchType = 'name';
        query = `${request.person_name}${request.company_name ? ` at ${request.company_name}` : ''}`;
        response = await apiService.generateProfileFromName(request);
      }

      // Handle successful response
      if (response.success && response.data) {
        setSearchState(prev => ({
          ...prev,
          isLoading: false,
          result: response.data,
          error: null,
          searchHistory: [
            {
              id: Date.now().toString(),
              timestamp: new Date().toISOString(),
              searchType,
              query,
              success: true,
              processingTime: response.data.processing_time || 0
            },
            ...prev.searchHistory.slice(0, 9) // Keep last 10 searches
          ]
        }));

        // Show success toast
        if (response.data.profile_found) {
          toast.success('Profile generated successfully!', {
            duration: 4000,
            position: 'top-right'
          });
        } else {
          toast.error('Profile not found. Please try a different search.', {
            duration: 5000,
            position: 'top-right'
          });
        }

      } else {
        // Handle API error response
        throw new Error(response.message || 'Failed to generate profile');
      }

    } catch (error) {
      console.error('Search error:', error);

      let errorMessage = 'An unexpected error occurred';

      if (isApiError(error)) {
        errorMessage = error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }

      // Update state with error
      setSearchState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
        result: null,
        searchHistory: [
          {
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            searchType: 'linkedin_url' in request ? 'url' : 'name',
            query: 'linkedin_url' in request ? request.linkedin_url : request.person_name,
            success: false,
            processingTime: 0
          },
          ...prev.searchHistory.slice(0, 9)
        ]
      }));

      // Show error toast
      toast.error(errorMessage, {
        duration: 6000,
        position: 'top-right'
      });
    }
  };

  /**
   * Clear search results and error state
   */
  const handleClearResults = () => {
    setSearchState(prev => ({
      ...prev,
      result: null,
      error: null
    }));
  };

  /**
   * Check if we have any results to display
   */
  const hasResults = searchState.result || searchState.error;

  // ===== Render Application =====

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            style: {
              background: '#10b981',
            },
          },
          error: {
            style: {
              background: '#ef4444',
            },
          },
        }}
      />

      {/* Header */}
      {/* <Header /> */}

      {/* Main Content */}
      <main className="flex-1 container py-8">
        <div className="max-w-6xl mx-auto">
          
          {/* Page Title and Description */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI Profile Generator
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Generate comprehensive LinkedIn profile briefings with AI-powered insights 
              for better business meetings and networking opportunities.
            </p>
          </div>

          {/* Main Content Grid */}
          <div className={`grid gap-8 ${hasResults ? 'lg:grid-cols-2' : 'max-w-2xl mx-auto'}`}>
            
            {/* Search Form */}
            <div className="space-y-6">
              <SearchForm
                onSearch={handleSearch}
                isLoading={searchState.isLoading}
              />

              {/* Search History (when not loading and no current results) */}
              {!searchState.isLoading && !hasResults && searchState.searchHistory.length > 0 && (
                <div className="card">
                  <div className="card-header">
                    <h3 className="text-lg font-semibold">Recent Searches</h3>
                  </div>
                  <div className="card-body">
                    <div className="space-y-2">
                      {searchState.searchHistory.slice(0, 5).map((item) => (
                        <div
                          key={item.id}
                          className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                        >
                          <div className="flex-1">
                            <p className="text-sm font-medium truncate">{item.query}</p>
                            <p className="text-xs text-gray-500">
                              {new Date(item.timestamp).toLocaleDateString()} • 
                              {item.searchType === 'url' ? 'URL Search' : 'Name Search'}
                            </p>
                          </div>
                          <div className={`text-xs px-2 py-1 rounded ${
                            item.success 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {item.success ? 'Success' : 'Failed'}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Results Display */}
            {hasResults && (
              <div className="space-y-6">
                <ProfileDisplay
                  result={searchState.result}
                  isLoading={searchState.isLoading}
                  error={searchState.error}
                />

                {/* Clear Results Button */}
                {!searchState.isLoading && (
                  <button
                    onClick={handleClearResults}
                    className="btn btn-secondary w-full"
                  >
                    Start New Search
                  </button>
                )}
              </div>
            )}
          </div>

          {/* Feature Highlights (shown when no results) */}
          {!hasResults && !searchState.isLoading && (
            <div className="mt-16">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                  How It Works
                </h2>
                <p className="text-gray-600">
                  Our AI-powered system generates comprehensive briefings in three steps
                </p>
              </div>

              <div className="grid md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">🔍</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">1. Find Profile</h3>
                  <p className="text-gray-600">
                    Search by LinkedIn URL or person name. Our system finds and extracts comprehensive profile data.
                  </p>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">🤖</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">2. AI Analysis</h3>
                  <p className="text-gray-600">
                    Advanced AI processes the profile data and recent news to generate strategic insights.
                  </p>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">📋</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">3. Get Briefing</h3>
                  <p className="text-gray-600">
                    Receive a comprehensive briefing with conversation starters and meeting preparation notes.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      {/* <Footer /> */}
    </div>
  );
};

export default App; 