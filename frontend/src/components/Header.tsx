/**
 * Header Component
 * 
 * The main navigation header for the AI Profile Generator application.
 * Includes branding, navigation links, and responsive design.
 * 
 * Features:
 * - Professional branding
 * - Navigation links
 * - Responsive design
 * - Modern styling
 */

import React from 'react';
import { Brain, Github, ExternalLink } from 'lucide-react';

/**
 * Header Component
 */
const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo and Branding */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                AI Profile Generator
              </h1>
              <p className="text-xs text-gray-500 hidden sm:block">
                LinkedIn Briefing Tool
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-6">
            <a
              href="#features"
              className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium"
            >
              Features
            </a>
            <a
              href="#how-it-works"
              className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium"
            >
              How it Works
            </a>
            <a
              href="http://localhost:5000/api/profile/examples"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium flex items-center gap-1"
            >
              API Docs
              <ExternalLink className="w-3 h-3" />
            </a>
          </nav>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            {/* GitHub Link */}
            <a
              href="https://github.com/yourusername/ai-profile-generator"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 transition-colors p-2 rounded-md hover:bg-gray-100"
              title="View on GitHub"
            >
              <Github className="w-5 h-5" />
            </a>

            {/* Status Indicator */}
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              API Online
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu (if needed in the future) */}
      <div className="md:hidden border-t border-gray-200 bg-gray-50 px-4 py-3">
        <div className="flex flex-wrap gap-4">
          <a
            href="#features"
            className="text-gray-600 hover:text-gray-900 text-sm font-medium"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            className="text-gray-600 hover:text-gray-900 text-sm font-medium"
          >
            How it Works
          </a>
          <a
            href="http://localhost:5000/api/profile/examples"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-600 hover:text-gray-900 text-sm font-medium flex items-center gap-1"
          >
            API Docs
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header; 