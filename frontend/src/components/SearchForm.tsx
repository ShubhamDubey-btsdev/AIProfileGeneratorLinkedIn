/**
 * SearchForm Component
 * 
 * This is the main search form component that allows users to generate
 * LinkedIn profile briefings either by URL or by searching for a person's name.
 * 
 * Features:
 * - Toggle between URL and name search modes
 * - Real-time input validation
 * - Responsive design
 * - Loading states
 * - Error handling
 */

import React, { useState, useEffect } from 'react';
import { Search, User, Link, Briefcase, MessageSquare } from 'lucide-react';
import { SearchFormProps, SearchFormState } from '@/types';

/**
 * SearchForm Component
 * 
 * @param onSearch - Callback function called when form is submitted
 * @param isLoading - Whether the search is currently in progress
 */
const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  // ===== Component State =====
  
  const [formState, setFormState] = useState<SearchFormState>({
    searchType: 'name', // Default to name search
    personName: '',
    companyName: '',
    linkedinUrl: '',
    meetingContext: ''
  });

  const [errors, setErrors] = useState<Partial<SearchFormState>>({});
  const [touched, setTouched] = useState<Partial<SearchFormState>>({});

  // ===== Validation Functions =====

  /**
   * Validate LinkedIn URL format
   */
  const validateLinkedInUrl = (url: string): string | null => {
    if (!url.trim()) return 'LinkedIn URL is required';
    
    try {
      const urlObj = new URL(url);
      if (!urlObj.hostname.includes('linkedin.com')) {
        return 'Must be a LinkedIn URL';
      }
      if (!urlObj.pathname.includes('/in/')) {
        return 'Must be a LinkedIn profile URL (contains /in/)';
      }
      return null;
    } catch {
      return 'Please enter a valid URL';
    }
  };

  /**
   * Validate person name
   */
  const validatePersonName = (name: string): string | null => {
    if (!name.trim()) return 'Person name is required';
    if (name.trim().length < 2) return 'Name must be at least 2 characters';
    if (name.trim().length > 100) return 'Name must be less than 100 characters';
    
    // Check for valid name characters (letters, spaces, hyphens, apostrophes)
    const namePattern = /^[A-Za-z\s\-'\.]+$/;
    if (!namePattern.test(name.trim())) {
      return 'Name can only contain letters, spaces, hyphens, and apostrophes';
    }
    
    return null;
  };

  /**
   * Validate company name (optional field)
   */
  const validateCompanyName = (company: string): string | null => {
    if (!company) return null; // Optional field
    
    if (company.length > 100) return 'Company name must be less than 100 characters';
    
    // Allow more characters for company names (numbers, &, etc.)
    const companyPattern = /^[A-Za-z0-9\s\-'\.&,()]+$/;
    if (!companyPattern.test(company)) {
      return 'Company name contains invalid characters';
    }
    
    return null;
  };

  /**
   * Validate meeting context (optional field)
   */
  const validateMeetingContext = (context: string): string | null => {
    if (!context) return null; // Optional field
    
    if (context.length > 1000) return 'Meeting context must be less than 1000 characters';
    
    return null;
  };

  // ===== Validation Effect =====

  /**
   * Validate form fields when they change
   */
  useEffect(() => {
    const newErrors: Partial<SearchFormState> = {};

    if (formState.searchType === 'url') {
      const urlError = validateLinkedInUrl(formState.linkedinUrl);
      if (urlError && touched.linkedinUrl) newErrors.linkedinUrl = urlError;
    } else {
      const nameError = validatePersonName(formState.personName);
      if (nameError && touched.personName) newErrors.personName = nameError;
      
      const companyError = validateCompanyName(formState.companyName);
      if (companyError && touched.companyName) newErrors.companyName = companyError;
    }

    const contextError = validateMeetingContext(formState.meetingContext);
    if (contextError && touched.meetingContext) newErrors.meetingContext = contextError;

    setErrors(newErrors);
  }, [formState, touched]);

  // ===== Event Handlers =====

  /**
   * Handle input field changes
   */
  const handleInputChange = (field: keyof SearchFormState) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormState(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  };

  /**
   * Handle field blur (mark as touched for validation)
   */
  const handleFieldBlur = (field: keyof SearchFormState) => () => {
    setTouched(prev => ({
      ...prev,
      [field]: true
    }));
  };

  /**
   * Handle search type toggle
   */
  const handleSearchTypeChange = (type: 'url' | 'name') => {
    setFormState(prev => ({
      ...prev,
      searchType: type
    }));
    
    // Clear errors when switching modes
    setErrors({});
    setTouched({});
  };

  /**
   * Handle form submission
   */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Mark all relevant fields as touched
    const touchedFields: Partial<SearchFormState> = {
      meetingContext: 'true'
    };
    
    if (formState.searchType === 'url') {
      touchedFields.linkedinUrl = 'true';
    } else {
      touchedFields.personName = 'true';
      touchedFields.companyName = 'true';
    }
    
    setTouched(touchedFields);

    // Validate all fields
    const allErrors: Partial<SearchFormState> = {};
    
    if (formState.searchType === 'url') {
      const urlError = validateLinkedInUrl(formState.linkedinUrl);
      if (urlError) allErrors.linkedinUrl = urlError;
    } else {
      const nameError = validatePersonName(formState.personName);
      if (nameError) allErrors.personName = nameError;
      
      const companyError = validateCompanyName(formState.companyName);
      if (companyError) allErrors.companyName = companyError;
    }
    
    const contextError = validateMeetingContext(formState.meetingContext);
    if (contextError) allErrors.meetingContext = contextError;

    setErrors(allErrors);

    // If no errors, submit the form
    if (Object.keys(allErrors).length === 0) {
      if (formState.searchType === 'url') {
        onSearch({
          linkedin_url: formState.linkedinUrl.trim(),
          meeting_context: formState.meetingContext.trim() || undefined
        });
      } else {
        onSearch({
          person_name: formState.personName.trim(),
          company_name: formState.companyName.trim() || undefined,
          meeting_context: formState.meetingContext.trim() || undefined
        });
      }
    }
  };

  // ===== Helper Functions =====

  /**
   * Check if form is valid for submission
   */
  const isFormValid = () => {
    if (formState.searchType === 'url') {
      return formState.linkedinUrl.trim() && !errors.linkedinUrl;
    } else {
      return formState.personName.trim() && !errors.personName && !errors.companyName;
    }
  };

  // ===== Render Component =====

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <Search className="w-5 h-5 text-primary" />
          Generate LinkedIn Profile Briefing
        </h2>
        <p className="text-sm text-secondary mt-2">
          Get AI-powered insights and briefings for better business meetings
        </p>
      </div>

      <div className="card-body">
        {/* Search Type Toggle */}
        <div className="form-group">
          <label className="form-label">Search Method</label>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => handleSearchTypeChange('name')}
              className={`btn flex-1 ${
                formState.searchType === 'name' ? 'btn-primary' : 'btn-secondary'
              }`}
            >
              <User className="w-4 h-4" />
              Search by Name
            </button>
            <button
              type="button"
              onClick={() => handleSearchTypeChange('url')}
              className={`btn flex-1 ${
                formState.searchType === 'url' ? 'btn-primary' : 'btn-secondary'
              }`}
            >
              <Link className="w-4 h-4" />
              Search by URL
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* URL Search Fields */}
          {formState.searchType === 'url' && (
            <div className="form-group">
              <label htmlFor="linkedin-url" className="form-label">
                LinkedIn Profile URL *
              </label>
              <input
                id="linkedin-url"
                type="url"
                value={formState.linkedinUrl}
                onChange={handleInputChange('linkedinUrl')}
                onBlur={handleFieldBlur('linkedinUrl')}
                placeholder="https://www.linkedin.com/in/username/"
                className={`form-input ${errors.linkedinUrl ? 'border-error' : ''}`}
                disabled={isLoading}
              />
              {errors.linkedinUrl && (
                <p className="text-sm text-error mt-1">{errors.linkedinUrl}</p>
              )}
              <p className="text-xs text-muted mt-1">
                Enter the full LinkedIn profile URL (e.g., linkedin.com/in/username)
              </p>
            </div>
          )}

          {/* Name Search Fields */}
          {formState.searchType === 'name' && (
            <>
              <div className="form-group">
                <label htmlFor="person-name" className="form-label">
                  Full Name *
                </label>
                <input
                  id="person-name"
                  type="text"
                  value={formState.personName}
                  onChange={handleInputChange('personName')}
                  onBlur={handleFieldBlur('personName')}
                  placeholder="David Ackley"
                  className={`form-input ${errors.personName ? 'border-error' : ''}`}
                  disabled={isLoading}
                />
                {errors.personName && (
                  <p className="text-sm text-error mt-1">{errors.personName}</p>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="company-name" className="form-label">
                  <Briefcase className="w-4 h-4 inline mr-1" />
                  Company Name (Optional)
                </label>
                <input
                  id="company-name"
                  type="text"
                  value={formState.companyName}
                  onChange={handleInputChange('companyName')}
                  onBlur={handleFieldBlur('companyName')}
                  placeholder="BTS"
                  className={`form-input ${errors.companyName ? 'border-error' : ''}`}
                  disabled={isLoading}
                />
                {errors.companyName && (
                  <p className="text-sm text-error mt-1">{errors.companyName}</p>
                )}
                <p className="text-xs text-muted mt-1">
                  Adding company name improves search accuracy
                </p>
              </div>
            </>
          )}

          {/* Meeting Context (for both search types) */}
          <div className="form-group">
            <label htmlFor="meeting-context" className="form-label">
              <MessageSquare className="w-4 h-4 inline mr-1" />
              Meeting Context (Optional)
            </label>
            <textarea
              id="meeting-context"
              value={formState.meetingContext}
              onChange={handleInputChange('meetingContext')}
              onBlur={handleFieldBlur('meetingContext')}
              placeholder="Partnership discussion, sales meeting, networking event..."
              className={`form-textarea ${errors.meetingContext ? 'border-error' : ''}`}
              disabled={isLoading}
              rows={3}
            />
            {errors.meetingContext && (
              <p className="text-sm text-error mt-1">{errors.meetingContext}</p>
            )}
            <p className="text-xs text-muted mt-1">
              Describe the meeting purpose for more targeted insights
            </p>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!isFormValid() || isLoading}
            className="btn btn-primary w-full py-3 text-base font-semibold"
          >
            {isLoading ? (
              <>
                <div className="loading-spinner" />
                Generating Briefing...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                Generate Profile Briefing
              </>
            )}
          </button>
        </form>

        {/* Help Text */}
        <div className="mt-6 p-4 bg-gray-50 rounded-md">
          <h4 className="font-medium mb-2">💡 Tips for better results:</h4>
          <ul className="text-sm text-secondary space-y-1">
            <li>• Use full names (e.g., "David Ackley" instead of "Dave")</li>
            <li>• Include company name when searching by name</li>
            <li>• Be specific about meeting context for targeted insights</li>
            <li>• Ensure LinkedIn URLs are complete profile links</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SearchForm; 