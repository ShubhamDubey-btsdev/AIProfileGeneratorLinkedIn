/**
/**
 * ProfileDisplay Component
 * 
 * This component displays the complete results from a profile search including:
 * - LinkedIn profile information
 * - AI-generated briefing
 * - Related news articles
 * - Loading states and error handling
 * 
 * Features:
 * - Modern responsive card-based layout
 * - Smooth loading animations and skeletons
 * - Enhanced error state handling
 * - Expandable sections with smooth transitions
 * - Copy to clipboard functionality
 * - Professional visual design
 */

import React, { useState } from 'react';
import { 
  User, 
  Building, 
  MapPin, 
  ExternalLink, 
  Clock, 
  TrendingUp, 
  MessageSquare,
  CheckCircle,
  Copy,
  AlertCircle,
  Newspaper,
  Calendar,
  Target,
  Lightbulb,
  Star,
  Briefcase,
  ChevronDown,
  ChevronUp,
  Award,
  Users,
  Globe,
  Zap
} from 'lucide-react';
import { ProfileDisplayProps, LinkedInProfile, AIBriefing, NewsArticle } from '@/types';

/**
 * ProfileDisplay Component
 * 
 * @param result - The profile generation result
 * @param isLoading - Whether the request is still loading
 * @param error - Any error message to display
 */
const ProfileDisplay: React.FC<ProfileDisplayProps> = ({ result, isLoading, error }) => {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState<{[key: string]: boolean}>({
    briefing: true,
    profile: true,
    news: false
  });

  // ===== Helper Functions =====

  /**
   * Copy text to clipboard with feedback
   */
  const copyToClipboard = async (text: string, section: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedSection(section);
      setTimeout(() => setCopiedSection(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  /**
   * Toggle section expansion
   */
  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  /**
   * Format confidence score
   */
  const formatConfidence = (score: number) => {
    if (score >= 90) return { 
      label: 'Exceptional', 
      color: 'text-emerald-600', 
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
      dot: 'bg-emerald-500'
    };
    if (score >= 75) return { 
      label: 'High Quality', 
      color: 'text-blue-600', 
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      dot: 'bg-blue-500'
    };
    if (score >= 60) return { 
      label: 'Good', 
      color: 'text-amber-600', 
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      dot: 'bg-amber-500'
    };
    return { 
      label: 'Needs Review', 
      color: 'text-red-600', 
      bg: 'bg-red-50',
      border: 'border-red-200',
      dot: 'bg-red-500'
    };
  };

  // ===== Enhanced Loading State =====

  if (isLoading) {
    return (
      <div className="space-y-8">
        {/* Enhanced Loading Header */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl border border-blue-100 shadow-sm">
          <div className="p-8">
            <div className="flex items-center gap-4 mb-6">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
                  <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-1">
                  Generating Your AI Profile Briefing
                </h3>
                <p className="text-gray-600">
                  Processing LinkedIn data and generating insights...
                </p>
              </div>
            </div>
            
            {/* Enhanced Progress Steps */}
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-green-200">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="font-medium text-green-700">LinkedIn profile discovered</span>
                <div className="ml-auto text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full">
                  Complete
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-blue-200">
                <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                <span className="font-medium text-blue-700">Extracting profile data</span>
                <div className="ml-auto text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                  In Progress
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="w-5 h-5 border-2 border-gray-300 rounded-full"></div>
                <span className="text-gray-500">Generating AI insights</span>
                <div className="ml-auto text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  Waiting
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="w-5 h-5 border-2 border-gray-300 rounded-full"></div>
                <span className="text-gray-500">Collecting relevant news</span>
                <div className="ml-auto text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  Waiting
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mt-6">
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span>Processing...</span>
                <span>~30 seconds</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-500 to-indigo-600 h-2 rounded-full animate-pulse" style={{width: '40%'}}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Loading Skeleton */}
        <div className="space-y-6">
          {[
            { height: 'h-32', width: 'w-full' },
            { height: 'h-48', width: 'w-full' },
            { height: 'h-24', width: 'w-full' }
          ].map((item, i) => (
            <div key={i} className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="p-6">
                <div className="animate-pulse">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-6 h-6 bg-gray-200 rounded"></div>
                    <div className="h-5 bg-gray-200 rounded w-1/3"></div>
                  </div>
                  <div className={`${item.height} bg-gray-100 rounded-xl`}></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // ===== Enhanced Error State =====

  if (error) {
    return (
      <div className="bg-white rounded-2xl border border-red-200 shadow-sm overflow-hidden">
        <div className="p-8">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <AlertCircle className="w-6 h-6 text-red-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-red-700 mb-2">
                Profile Generation Failed
              </h3>
              <p className="text-gray-700 mb-6 leading-relaxed">{error}</p>
              
              <div className="bg-red-50 border border-red-200 rounded-xl p-6">
                <h4 className="font-semibold text-red-800 mb-4 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  Troubleshooting Guide
                </h4>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="font-medium text-red-700 mb-2">LinkedIn URL Issues:</h5>
                    <ul className="text-sm text-red-600 space-y-1">
                      <li>• Ensure URL is complete and valid</li>
                      <li>• Check profile is publicly accessible</li>
                      <li>• Try copying URL directly from browser</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-medium text-red-700 mb-2">Name Search Issues:</h5>
                    <ul className="text-sm text-red-600 space-y-1">
                      <li>• Use full professional name</li>
                      <li>• Include accurate company name</li>
                      <li>• Try different name variations</li>
                    </ul>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-red-200">
                  <p className="text-sm text-red-600">
                    Still having issues? Check that the Flask API is running on localhost:5000
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ===== Enhanced No Results State =====

  if (!result) {
    return (
      <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl border border-gray-200 shadow-sm">
        <div className="p-12 text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <User className="w-10 h-10 text-blue-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-3">
            Ready to Generate Your Profile Briefing
          </h3>
          <p className="text-gray-600 max-w-md mx-auto leading-relaxed">
            Use the search form above to analyze LinkedIn profiles and generate 
            comprehensive AI-powered briefings for your meetings.
          </p>
          <div className="flex items-center justify-center gap-6 mt-8 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-yellow-500" />
              <span>AI-Powered</span>
            </div>
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-blue-500" />
              <span>LinkedIn Integration</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-green-500" />
              <span>Meeting Ready</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ===== Success State - Render Results =====

  const { linkedin_profile, briefing, news_articles, search_method, processing_time } = result;
  const confidence = briefing ? formatConfidence(briefing.confidence_score) : null;

  return (
    <div className="space-y-8">
      
      {/* Enhanced Result Summary Header */}
      <div className="bg-gradient-to-r from-emerald-50 to-green-50 rounded-2xl border border-emerald-200 shadow-sm overflow-hidden">
        <div className="p-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-r from-emerald-500 to-green-600 rounded-xl flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-1">
                  Profile Generated Successfully
                </h3>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span className="flex items-center gap-1">
                    <Target className="w-4 h-4" />
                    {search_method.replace('_', ' ').charAt(0).toUpperCase() + search_method.replace('_', ' ').slice(1)}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {processing_time.toFixed(1)}s processing time
                  </span>
                </div>
              </div>
            </div>
            
            {confidence && briefing && (
              <div className={`${confidence.bg} ${confidence.border} border rounded-xl p-4 text-right`}>
                <div className={`text-lg font-bold ${confidence.color} mb-1`}>
                  {confidence.label}
                </div>
                <div className="text-sm text-gray-600 flex items-center gap-2">
                  <div className={`w-2 h-2 ${confidence.dot} rounded-full`}></div>
                  {briefing.confidence_score}% accuracy
                </div>
              </div>
            )}
          </div>

          {/* Enhanced Quick Stats */}
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-white rounded-xl p-4 text-center border border-gray-100">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                {linkedin_profile ? (
                  <CheckCircle className="w-5 h-5 text-blue-600" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-gray-400" />
                )}
              </div>
              <div className="text-sm font-semibold text-gray-900">Profile Data</div>
              <div className="text-xs text-gray-500 mt-1">
                {linkedin_profile ? 'Successfully extracted' : 'Not found'}
              </div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center border border-gray-100">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                {briefing ? (
                  <TrendingUp className="w-5 h-5 text-green-600" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-gray-400" />
                )}
              </div>
              <div className="text-sm font-semibold text-gray-900">AI Briefing</div>
              <div className="text-xs text-gray-500 mt-1">
                {briefing ? 'Generated' : 'Failed'}
              </div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center border border-gray-100">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                <Newspaper className="w-5 h-5 text-purple-600" />
              </div>
              <div className="text-sm font-semibold text-gray-900">News Articles</div>
              <div className="text-xs text-gray-500 mt-1">
                {news_articles?.length || 0} found
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* LinkedIn Profile Section */}
      {linkedin_profile && (
        <ProfileSection 
          profile={linkedin_profile} 
          expanded={expandedSections.profile}
          onToggle={() => toggleSection('profile')}
          onCopy={copyToClipboard}
          copiedSection={copiedSection}
        />
      )}

      {/* AI Briefing Section */}
      {briefing && (
        <BriefingSection 
          briefing={briefing}
          expanded={expandedSections.briefing}
          onToggle={() => toggleSection('briefing')}
          onCopy={copyToClipboard}
          copiedSection={copiedSection}
        />
      )}

      {/* News Articles Section */}
      {news_articles && news_articles.length > 0 && (
        <NewsSection 
          articles={news_articles}
          expanded={expandedSections.news}
          onToggle={() => toggleSection('news')}
        />
      )}
    </div>
  );
};

// ===== Enhanced Profile Section Component =====

interface ProfileSectionProps {
  profile: LinkedInProfile;
  expanded: boolean;
  onToggle: () => void;
  onCopy: (text: string, section: string) => void;
  copiedSection: string | null;
}

const ProfileSection: React.FC<ProfileSectionProps> = ({ 
  profile, expanded, onToggle, onCopy, copiedSection 
}) => {
  const profileText = `
Name: ${profile.name}
Title: ${profile.title}
Company: ${profile.company}
Location: ${profile.location || 'Not specified'}
LinkedIn: ${profile.url}
Summary: ${profile.summary || 'No summary available'}
  `.trim();

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden transition-all duration-200 hover:shadow-md">
      <div 
        className="p-6 cursor-pointer hover:bg-gray-50 transition-colors duration-200 border-b border-gray-100"
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">LinkedIn Profile</h3>
              <p className="text-sm text-gray-500">Professional information & experience</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onCopy(profileText, 'profile');
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                copiedSection === 'profile'
                  ? 'bg-green-100 text-green-700 border border-green-200'
                  : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
              }`}
            >
              {copiedSection === 'profile' ? (
                <>
                  <CheckCircle className="w-4 h-4 inline mr-1" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 inline mr-1" />
                  Copy
                </>
              )}
            </button>
            <div className="w-8 h-8 flex items-center justify-center">
              {expanded ? (
                <ChevronUp className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-400" />
              )}
            </div>
          </div>
        </div>
      </div>

      {expanded && (
        <div className="p-8 bg-gradient-to-br from-white to-blue-50">
          <div className="space-y-8">
            
            {/* Enhanced Basic Info */}
            <div className="flex items-start gap-6">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center flex-shrink-0">
                <User className="w-10 h-10 text-blue-600" />
              </div>
              <div className="flex-1">
                <h4 className="text-2xl font-bold text-gray-900 mb-2">{profile.name}</h4>
                <p className="text-lg text-gray-700 mb-4">{profile.title}</p>
                <div className="flex flex-wrap items-center gap-6 mb-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                      <Building className="w-4 h-4" />
                    </div>
                    <span className="font-medium">{profile.company}</span>
                  </div>
                  {profile.location && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                        <MapPin className="w-4 h-4" />
                      </div>
                      <span>{profile.location}</span>
                    </div>
                  )}
                </div>
                <a
                  href={profile.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
                >
                  <ExternalLink className="w-4 h-4" />
                  View LinkedIn Profile
                </a>
              </div>
            </div>

            {/* Enhanced Summary */}
            {profile.summary && (
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h5 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                  <div className="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
                    <MessageSquare className="w-4 h-4 text-blue-600" />
                  </div>
                  Professional Summary
                </h5>
                <p className="text-gray-700 leading-relaxed">
                  {profile.summary}
                </p>
              </div>
            )}

            {/* Enhanced Experience & Skills Grid */}
            <div className="grid lg:grid-cols-2 gap-8">
              
              {/* Enhanced Experience */}
              {profile.experience && profile.experience.length > 0 && (
                <div className="bg-white rounded-xl p-6 border border-gray-200">
                  <h5 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <div className="w-6 h-6 bg-purple-100 rounded-lg flex items-center justify-center">
                      <Briefcase className="w-4 h-4 text-purple-600" />
                    </div>
                    Work Experience
                  </h5>
                  <div className="space-y-4">
                    {profile.experience.slice(0, 3).map((exp, index) => (
                      <div key={index} className="relative pl-6 pb-4 last:pb-0">
                        <div className="absolute left-0 top-2 w-2 h-2 bg-purple-500 rounded-full"></div>
                        <div className="absolute left-1 top-4 w-0.5 bg-purple-200 h-full last:hidden"></div>
                        <div>
                          <div className="font-semibold text-gray-900">{exp.title}</div>
                          <div className="text-purple-600 font-medium">{exp.company}</div>
                          <div className="text-sm text-gray-500 mt-1">{exp.duration}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Enhanced Skills */}
              {profile.skills && profile.skills.length > 0 && (
                <div className="bg-white rounded-xl p-6 border border-gray-200">
                  <h5 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <div className="w-6 h-6 bg-yellow-100 rounded-lg flex items-center justify-center">
                      <Star className="w-4 h-4 text-yellow-600" />
                    </div>
                    Core Skills
                  </h5>
                  <div className="flex flex-wrap gap-3">
                    {profile.skills.slice(0, 12).map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 text-sm font-medium rounded-lg border border-blue-200 hover:from-blue-100 hover:to-indigo-100 transition-colors duration-200"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// ===== Enhanced Briefing Section Component =====

interface BriefingSectionProps {
  briefing: AIBriefing;
  expanded: boolean;
  onToggle: () => void;
  onCopy: (text: string, section: string) => void;
  copiedSection: string | null;
}

const BriefingSection: React.FC<BriefingSectionProps> = ({ 
  briefing, expanded, onToggle, onCopy, copiedSection 
}) => {
  const briefingText = `
AI BRIEFING SUMMARY

Executive Summary:
${briefing.executive_summary}

Key Insights:
${briefing.key_insights.map(insight => `• ${insight}`).join('\n')}

Conversation Starters:
${briefing.conversation_starters.map(starter => `• ${starter}`).join('\n')}

Meeting Preparation:
${briefing.meeting_preparation.map(prep => `• ${prep}`).join('\n')}

Strategic Notes:
${briefing.strategic_notes.map(note => `• ${note}`).join('\n')}

Recent Activity:
${briefing.recent_activity}

Confidence Score: ${briefing.confidence_score}%
  `.trim();

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden transition-all duration-200 hover:shadow-md">
      <div 
        className="p-6 cursor-pointer hover:bg-gray-50 transition-colors duration-200 border-b border-gray-100"
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">AI-Generated Briefing</h3>
              <p className="text-sm text-gray-500">Strategic insights & conversation starters</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onCopy(briefingText, 'briefing');
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                copiedSection === 'briefing'
                  ? 'bg-green-100 text-green-700 border border-green-200'
                  : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
              }`}
            >
              {copiedSection === 'briefing' ? (
                <>
                  <CheckCircle className="w-4 h-4 inline mr-1" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 inline mr-1" />
                  Copy
                </>
              )}
            </button>
            <div className="w-8 h-8 flex items-center justify-center">
              {expanded ? (
                <ChevronUp className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-400" />
              )}
            </div>
          </div>
        </div>
      </div>

      {expanded && (
        <div className="p-8 bg-gradient-to-br from-white to-green-50">
          <div className="space-y-8">
            
            {/* Executive Summary */}
            <div className="bg-white rounded-xl p-6 border border-gray-200">
              <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <div className="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Target className="w-4 h-4 text-blue-600" />
                </div>
                Executive Summary
              </h4>
              <p className="text-gray-700 leading-relaxed text-lg">
                {briefing.executive_summary}
              </p>
            </div>

            {/* Two Column Layout */}
            <div className="grid lg:grid-cols-2 gap-8">
              
              {/* Key Insights */}
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <div className="w-6 h-6 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <Lightbulb className="w-4 h-4 text-yellow-600" />
                  </div>
                  Key Insights
                </h4>
                <ul className="space-y-3">
                  {briefing.key_insights.map((insight, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                      </div>
                      <span className="text-gray-700 leading-relaxed">{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Conversation Starters */}
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <div className="w-6 h-6 bg-green-100 rounded-lg flex items-center justify-center">
                    <MessageSquare className="w-4 h-4 text-green-600" />
                  </div>
                  Conversation Starters
                </h4>
                <ul className="space-y-3">
                  {briefing.conversation_starters.map((starter, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      </div>
                      <span className="text-gray-700 leading-relaxed">{starter}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Meeting Preparation */}
            <div className="bg-white rounded-xl p-6 border border-gray-200">
              <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <div className="w-6 h-6 bg-purple-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-4 h-4 text-purple-600" />
                </div>
                Meeting Preparation Checklist
              </h4>
              <div className="grid md:grid-cols-2 gap-4">
                {briefing.meeting_preparation.map((prep, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg border border-purple-100">
                    <div className="w-5 h-5 bg-purple-100 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
                      <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                    </div>
                    <span className="text-gray-700 text-sm leading-relaxed">{prep}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Strategic Notes */}
            {briefing.strategic_notes.length > 0 && (
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <div className="w-6 h-6 bg-indigo-100 rounded-lg flex items-center justify-center">
                    <Award className="w-4 h-4 text-indigo-600" />
                  </div>
                  Strategic Notes
                </h4>
                <ul className="space-y-3">
                  {briefing.strategic_notes.map((note, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <Star className="w-3 h-3 text-indigo-600" />
                      </div>
                      <span className="text-gray-700 leading-relaxed">{note}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recent Activity */}
            {briefing.recent_activity && (
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <div className="w-6 h-6 bg-gray-100 rounded-lg flex items-center justify-center">
                    <Clock className="w-4 h-4 text-gray-600" />
                  </div>
                  Recent Activity & Updates
                </h4>
                <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg border border-gray-200">
                  {briefing.recent_activity}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// ===== Enhanced News Section Component =====

interface NewsSectionProps {
  articles: NewsArticle[];
  expanded: boolean;
  onToggle: () => void;
}

const NewsSection: React.FC<NewsSectionProps> = ({ articles, expanded, onToggle }) => {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden transition-all duration-200 hover:shadow-md">
      <div 
        className="p-6 cursor-pointer hover:bg-gray-50 transition-colors duration-200 border-b border-gray-100"
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl flex items-center justify-center">
              <Newspaper className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">Related News & Updates</h3>
              <p className="text-sm text-gray-500">{articles.length} relevant articles found</p>
            </div>
          </div>
          <div className="w-8 h-8 flex items-center justify-center">
            {expanded ? (
              <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
          </div>
        </div>
      </div>

      {expanded && (
        <div className="p-8 bg-gradient-to-br from-white to-purple-50">
          <div className="space-y-6">
            {articles.slice(0, 5).map((article, index) => (
              <div key={index} className="bg-white rounded-xl p-6 border border-gray-200 hover:border-purple-200 transition-colors duration-200">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <Newspaper className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900 mb-2 hover:text-purple-600 transition-colors duration-200">
                      <a 
                        href={article.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="flex items-start gap-2 group"
                      >
                        {article.title}
                        <ExternalLink className="w-4 h-4 flex-shrink-0 mt-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                      </a>
                    </h4>
                    <p className="text-gray-600 mb-4 leading-relaxed">
                      {article.description}
                    </p>
                    <div className="flex items-center gap-6 text-sm text-gray-500">
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 bg-gray-100 rounded-lg flex items-center justify-center">
                          <Globe className="w-3 h-3" />
                        </div>
                        <span className="font-medium">{article.source}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 bg-gray-100 rounded-lg flex items-center justify-center">
                          <Calendar className="w-3 h-3" />
                        </div>
                        <span>{new Date(article.published_at).toLocaleDateString('en-US', { 
                          year: 'numeric', 
                          month: 'short', 
                          day: 'numeric' 
                        })}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileDisplay; 