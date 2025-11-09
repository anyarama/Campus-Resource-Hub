// =============================================================================
// THEME SWITCHER - Light / Dark Mode Toggle
// =============================================================================
// Manages theme switching with localStorage persistence
// =============================================================================

(function() {
  'use strict';
  
  // Get current theme from localStorage or default to 'light'
  const getTheme = () => localStorage.getItem('theme') || 'light';
  
  // Set theme on document root
  const setTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  };
  
  // Initialize theme on page load
  const initTheme = () => {
    const currentTheme = getTheme();
    setTheme(currentTheme);
  };
  
  // Toggle between light and dark
  const toggleTheme = () => {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
  };
  
  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
  
  // Export toggle function to global scope
  window.toggleTheme = toggleTheme;
  
  // Auto-attach to theme toggle buttons
  document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('[data-theme-toggle]');
    toggleButtons.forEach(button => {
      button.addEventListener('click', toggleTheme);
    });
  });
})();
