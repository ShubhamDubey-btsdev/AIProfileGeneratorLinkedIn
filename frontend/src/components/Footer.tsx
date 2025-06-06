/**
 * Footer Component
 * 
 * The main footer for the AI Profile Generator application.
 * Includes links, attribution, and responsive design.
 * 
 * Features:
 * - Professional links and information
 * - Responsive design
 * - Modern styling
 * - Attribution and legal links
 */

import React from 'react';
import { Heart, Code, ExternalLink, Mail, Shield } from 'lucide-react';

/**
 * Footer Component
 */
const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="container mx-auto px-4 py-12">
        
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* About Section */}
          <div className="space-y-4">
            <h3 className="text-white font-semibold text-lg">
              AI Profile Generator
            </h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Generate comprehensive LinkedIn profile briefings with AI-powered insights 
              for better business meetings and networking opportunities.
            </p>
            <div className="flex items-center gap-2 text-sm">
              <Code className="w-4 h-4" />
              <span>Built with React & TypeScript</span>
            </div>
          </div>

          {/* Features Section */}
          <div className="space-y-4">
            <h4 className="text-white font-medium">Features</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#search-methods" className="hover:text-white transition-colors">
                  Dual Search Methods
                </a>
              </li>
              <li>
                <a href="#ai-briefings" className="hover:text-white transition-colors">
                  AI-Powered Briefings
                </a>
              </li>
              <li>
                <a href="#profile-validation" className="hover:text-white transition-colors">
                  Profile Validation
                </a>
              </li>
              <li>
                <a href="#news-integration" className="hover:text-white transition-colors">
                  News Integration
                </a>
              </li>
            </ul>
          </div>

          {/* Resources Section */}
          <div className="space-y-4">
            <h4 className="text-white font-medium">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a 
                  href="http://localhost:5000/api/profile/examples"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors flex items-center gap-1"
                >
                  API Documentation
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a 
                  href="http://localhost:5000/api/health"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors flex items-center gap-1"
                >
                  API Status
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a href="#usage-guide" className="hover:text-white transition-colors">
                  Usage Guide
                </a>
              </li>
              <li>
                <a href="#troubleshooting" className="hover:text-white transition-colors">
                  Troubleshooting
                </a>
              </li>
            </ul>
          </div>

          {/* Contact & Legal Section */}
          <div className="space-y-4">
            <h4 className="text-white font-medium">Support</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a 
                  href="mailto:support@aiprofilegenerator.com"
                  className="hover:text-white transition-colors flex items-center gap-1"
                >
                  <Mail className="w-3 h-3" />
                  Contact Support
                </a>
              </li>
              <li>
                <a href="#privacy" className="hover:text-white transition-colors flex items-center gap-1">
                  <Shield className="w-3 h-3" />
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#terms" className="hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a 
                  href="https://github.com/yourusername/ai-profile-generator"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors flex items-center gap-1"
                >
                  GitHub Repository
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          
          {/* Bottom Row */}
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            
            {/* Copyright */}
            <div className="text-sm text-gray-400">
              © {currentYear} AI Profile Generator. All rights reserved.
            </div>

            {/* Tech Stack & Attribution */}
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <div className="flex items-center gap-1">
                <span>Made with</span>
                <Heart className="w-4 h-4 text-red-500" />
                <span>using React, TypeScript & Flask</span>
              </div>
            </div>
          </div>

          {/* Additional Info */}
          <div className="mt-4 text-xs text-gray-500 text-center md:text-left">
            <p>
              This application uses LinkedIn profile data for professional networking purposes. 
              All profile information is processed in accordance with LinkedIn's terms of service 
              and applicable privacy regulations.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 