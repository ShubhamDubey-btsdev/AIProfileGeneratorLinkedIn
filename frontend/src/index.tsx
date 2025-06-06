/**
 * Main Application Entry Point
 * 
 * This file bootstraps the React application and renders it to the DOM.
 * It includes the main App component and sets up the React rendering.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Get the root element from the HTML
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found. Make sure you have a div with id="root" in your HTML.');
}

// Create React root and render the application
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); 