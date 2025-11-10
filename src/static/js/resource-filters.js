// =============================================================================
// RESOURCE FILTERS - Filter Drawer Logic for Resources List
// =============================================================================
// AI Contribution: Cline created this module on 2025-11-09
// Features: Filter drawer, keyboard nav, URL params, view toggle, collapsible sections
// =============================================================================

class ResourceFilters {
  constructor() {
    this.drawer = document.querySelector('[data-drawer="filters"]');
    this.backdrop = document.querySelector('[data-drawer-backdrop]');
    this.toggle = document.querySelector('[data-filter-toggle]');
    this.closeBtn = document.querySelector('[data-drawer-close]');
    this.clearBtn = document.querySelector('[data-filter-clear]');
    this.applyBtn = document.querySelector('[data-filter-apply]');
    this.filterSections = document.querySelectorAll('.filter-section');
    this.filterInputs = document.querySelectorAll('[data-filter-input]');
    this.viewToggle = document.querySelectorAll('[data-view]');
    this.searchClear = document.querySelector('.input-clear');
    
    this.activeFilters = new Map();
    this.isOpen = false;
    
    this.init();
  }

  init() {
    // Load filters from URL
    this.loadFiltersFromURL();
    
    // Setup event listeners
    this.setupDrawerControls();
    this.setupFilterSections();
    this.setupFilterInputs();
    this.setupViewToggle();
    this.setupSearchClear();
    this.setupKeyboardNavigation();
    
    // Update UI state
    this.updateActiveFiltersUI();
    this.updateFilterCount();
    
    // Auto-open drawer on desktop if filters active
    if (window.innerWidth >= 1024 && this.activeFilters.size > 0) {
      this.drawer.classList.add('is-open');
    }
  }

  // ========================================================================
  // Drawer Controls
  // ========================================================================
  
  setupDrawerControls() {
    // Toggle button (mobile)
    if (this.toggle) {
      this.toggle.addEventListener('click', () => this.toggleDrawer());
    }
    
    // Close button
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.closeDrawer());
    }
    
    // Backdrop click
    if (this.backdrop) {
      this.backdrop.addEventListener('click', () => this.closeDrawer());
    }
    
    // Clear all filters
    if (this.clearBtn) {
      this.clearBtn.addEventListener('click', () => this.clearAllFilters());
    }
    
    // Apply filters (mobile)
    if (this.applyBtn) {
      this.applyBtn.addEventListener('click', () => {
        this.applyFilters();
        this.closeDrawer();
      });
    }
  }

  toggleDrawer() {
    if (this.isOpen) {
      this.closeDrawer();
    } else {
      this.openDrawer();
    }
  }

  openDrawer() {
    this.isOpen = true;
    this.drawer.classList.add('is-open');
    this.backdrop.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    
    // Focus first interactive element
    const firstInput = this.drawer.querySelector('input, button');
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }
    
    // Trap focus
    this.trapFocus();
  }

  closeDrawer() {
    this.isOpen = false;
    this.drawer.classList.remove('is-open');
    this.backdrop.classList.remove('is-open');
    document.body.style.overflow = '';
    
    // Return focus to toggle button
    if (this.toggle) {
      this.toggle.focus();
    }
  }

  // ========================================================================
  // Filter Sections (Collapsible)
  // ========================================================================
  
  setupFilterSections() {
    this.filterSections.forEach(section => {
      const header = section.querySelector('.filter-section__header');
      const body = section.querySelector('.filter-section__body');
      
      if (header && body) {
        header.addEventListener('click', () => {
          section.classList.toggle('is-collapsed');
          
          // Update ARIA
          const isCollapsed = section.classList.contains('is-collapsed');
          header.setAttribute('aria-expanded', !isCollapsed);
        });
        
        // Initialize ARIA
        header.setAttribute('role', 'button');
        header.setAttribute('aria-expanded', 'true');
        header.setAttribute('tabindex', '0');
        
        // Keyboard support for section headers
        header.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            header.click();
          }
        });
      }
    });
  }

  // ========================================================================
  // Filter Inputs (Checkboxes, Range, Date)
  // ========================================================================
  
  setupFilterInputs() {
    // Checkbox filters
    this.filterInputs.forEach(input => {
      input.addEventListener('change', (e) => {
        this.handleFilterChange(e.target);
        
        // On desktop, apply immediately
        if (window.innerWidth >= 1024) {
          this.applyFilters();
        }
      });
    });
    
    // Capacity range inputs
    const capacityMin = document.querySelector('[data-capacity-min]');
    const capacityMax = document.querySelector('[data-capacity-max]');
    
    if (capacityMin) {
      capacityMin.addEventListener('change', () => {
        if (window.innerWidth >= 1024) this.applyFilters();
      });
    }
    
    if (capacityMax) {
      capacityMax.addEventListener('change', () => {
        if (window.innerWidth >= 1024) this.applyFilters();
      });
    }
    
    // Date range inputs
    const dateFrom = document.querySelector('[data-availability-from]');
    const dateTo = document.querySelector('[data-availability-to]');
    
    if (dateFrom) {
      dateFrom.addEventListener('change', () => {
        if (window.innerWidth >= 1024) this.applyFilters();
      });
    }
    
    if (dateTo) {
      dateTo.addEventListener('change', () => {
        if (window.innerWidth >= 1024) this.applyFilters();
      });
    }
    
    // Location search
    const locationSearch = document.querySelector('[data-location-search]');
    if (locationSearch) {
      locationSearch.addEventListener('input', (e) => {
        this.filterLocationList(e.target.value);
      });
    }
  }

  handleFilterChange(input) {
    const filterType = input.name;
    const filterValue = input.value;
    
    if (input.type === 'checkbox') {
      if (input.checked) {
        // Add to active filters
        if (!this.activeFilters.has(filterType)) {
          this.activeFilters.set(filterType, []);
        }
        this.activeFilters.get(filterType).push(filterValue);
      } else {
        // Remove from active filters
        if (this.activeFilters.has(filterType)) {
          const values = this.activeFilters.get(filterType);
          const index = values.indexOf(filterValue);
          if (index > -1) {
            values.splice(index, 1);
          }
          if (values.length === 0) {
            this.activeFilters.delete(filterType);
          }
        }
      }
    }
    
    this.updateActiveFiltersUI();
    this.updateFilterCount();
  }

  // ========================================================================
  // Apply Filters (Update URL and Reload)
  // ========================================================================
  
  applyFilters() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams();
    
    // Preserve search query
    const searchQuery = document.querySelector('[name="q"]');
    if (searchQuery && searchQuery.value) {
      params.set('q', searchQuery.value);
    }
    
    // Add checkbox filters
    this.filterInputs.forEach(input => {
      if (input.type === 'checkbox' && input.checked) {
        params.append(input.name, input.value);
      }
    });
    
    // Add capacity range
    const capacityMin = document.querySelector('[data-capacity-min]');
    const capacityMax = document.querySelector('[data-capacity-max]');
    if (capacityMin && capacityMin.value) {
      params.set('capacity_min', capacityMin.value);
    }
    if (capacityMax && capacityMax.value) {
      params.set('capacity_max', capacityMax.value);
    }
    
    // Add date range
    const dateFrom = document.querySelector('[data-availability-from]');
    const dateTo = document.querySelector('[data-availability-to]');
    if (dateFrom && dateFrom.value) {
      params.set('date_from', dateFrom.value);
    }
    if (dateTo && dateTo.value) {
      params.set('date_to', dateTo.value);
    }
    
    // Add sort parameter if present
    const sortParam = url.searchParams.get('sort');
    if (sortParam) {
      params.set('sort', sortParam);
    }
    
    // Update URL and reload
    url.search = params.toString();
    window.location.href = url.toString();
  }

  clearAllFilters() {
    // Uncheck all checkboxes
    this.filterInputs.forEach(input => {
      if (input.type === 'checkbox' && input.name !== 'status') {
        input.checked = false;
      }
    });
    
    // Clear capacity inputs
    const capacityMin = document.querySelector('[data-capacity-min]');
    const capacityMax = document.querySelector('[data-capacity-max]');
    if (capacityMin) capacityMin.value = '';
    if (capacityMax) capacityMax.value = '';
    
    // Clear date inputs
    const dateFrom = document.querySelector('[data-availability-from]');
    const dateTo = document.querySelector('[data-availability-to]');
    if (dateFrom) dateFrom.value = '';
    if (dateTo) dateTo.value = '';
    
    // Clear active filters
    this.activeFilters.clear();
    
    // Update UI
    this.updateActiveFiltersUI();
    this.updateFilterCount();
    
    // Apply (redirect to base URL)
    const url = new URL(window.location.href);
    url.search = '';
    window.location.href = url.toString();
  }

  // ========================================================================
  // Load Filters from URL
  // ========================================================================
  
  loadFiltersFromURL() {
    const params = new URLSearchParams(window.location.search);
    
    // Load checkbox filters
    params.forEach((value, key) => {
      const input = document.querySelector(`[name="${key}"][value="${value}"]`);
      if (input && input.type === 'checkbox') {
        input.checked = true;
        
        if (!this.activeFilters.has(key)) {
          this.activeFilters.set(key, []);
        }
        this.activeFilters.get(key).push(value);
      }
    });
    
    // Load capacity range
    const capacityMin = params.get('capacity_min');
    const capacityMax = params.get('capacity_max');
    if (capacityMin) {
      const input = document.querySelector('[data-capacity-min]');
      if (input) input.value = capacityMin;
    }
    if (capacityMax) {
      const input = document.querySelector('[data-capacity-max]');
      if (input) input.value = capacityMax;
    }
    
    // Load date range
    const dateFrom = params.get('date_from');
    const dateTo = params.get('date_to');
    if (dateFrom) {
      const input = document.querySelector('[data-availability-from]');
      if (input) input.value = dateFrom;
    }
    if (dateTo) {
      const input = document.querySelector('[data-availability-to]');
      if (input) input.value = dateTo;
    }
  }

  // ========================================================================
  // Active Filters UI (Chips)
  // ========================================================================
  
  updateActiveFiltersUI() {
    const container = document.querySelector('[data-active-filters]');
    const list = document.querySelector('.filter-active__list');
    
    if (!container || !list) return;
    
    // Clear existing chips
    list.innerHTML = '';
    
    // Count all active filters
    let totalFilters = 0;
    
    // Add chips for each active filter
    this.activeFilters.forEach((values, filterType) => {
      values.forEach(value => {
        totalFilters++;
        const chip = document.createElement('div');
        chip.className = 'filter-active__chip';
        chip.innerHTML = `
          ${this.getFilterLabel(filterType, value)}
          <button type="button" data-remove-filter="${filterType}:${value}">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path d="M1 1L9 9M1 9L9 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        `;
        
        // Add remove handler
        const removeBtn = chip.querySelector('button');
        removeBtn.addEventListener('click', () => {
          this.removeFilter(filterType, value);
        });
        
        list.appendChild(chip);
      });
    });
    
    // Show/hide container
    if (totalFilters > 0) {
      container.style.display = 'flex';
      this.clearBtn.disabled = false;
    } else {
      container.style.display = 'none';
      this.clearBtn.disabled = true;
    }
  }

  getFilterLabel(filterType, value) {
    const labels = {
      category: {
        'study_room': 'Study Room',
        'equipment': 'Equipment',
        'lab': 'Lab',
        'space': 'Event Space',
        'tutoring': 'Tutoring'
      },
      status: {
        'published': 'Published',
        'draft': 'Draft',
        'archived': 'Archived'
      }
    };
    
    if (labels[filterType] && labels[filterType][value]) {
      return labels[filterType][value];
    }
    
    return value.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  removeFilter(filterType, value) {
    // Update the checkbox
    const input = document.querySelector(`[name="${filterType}"][value="${value}"]`);
    if (input) {
      input.checked = false;
    }
    
    // Remove from active filters
    if (this.activeFilters.has(filterType)) {
      const values = this.activeFilters.get(filterType);
      const index = values.indexOf(value);
      if (index > -1) {
        values.splice(index, 1);
      }
      if (values.length === 0) {
        this.activeFilters.delete(filterType);
      }
    }
    
    // Update UI and apply
    this.updateActiveFiltersUI();
    this.updateFilterCount();
    this.applyFilters();
  }

  updateFilterCount() {
    const badge = document.querySelector('[data-filter-count]');
    if (!badge) return;
    
    let count = 0;
    this.activeFilters.forEach(values => {
      count += values.length;
    });
    
    if (count > 0) {
      badge.textContent = count;
      badge.style.display = 'flex';
    } else {
      badge.style.display = 'none';
    }
  }

  // ========================================================================
  // View Toggle (Grid / List)
  // ========================================================================
  
  setupViewToggle() {
    this.viewToggle.forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.dataset.view;
        
        // Update button states
        this.viewToggle.forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        
        // Update grid
        const grid = document.querySelector('.resources-grid');
        if (grid) {
          grid.dataset.viewMode = view;
        }
        
        // Save preference
        localStorage.setItem('resourceViewMode', view);
      });
    });
    
    // Load saved preference
    const savedView = localStorage.getItem('resourceViewMode');
    if (savedView) {
      const btn = document.querySelector(`[data-view="${savedView}"]`);
      if (btn) btn.click();
    }
  }

  // ========================================================================
  // Search Clear Button
  // ========================================================================
  
  setupSearchClear() {
    if (this.searchClear) {
      this.searchClear.addEventListener('click', () => {
        const searchInput = document.querySelector('[name="q"]');
        if (searchInput) {
          searchInput.value = '';
          searchInput.form.submit();
        }
      });
    }
  }

  // ========================================================================
  // Location List Filter
  // ========================================================================
  
  filterLocationList(query) {
    const list = document.querySelector('[data-location-list]');
    if (!list) return;
    
    const items = list.querySelectorAll('.filter-option');
    const lowerQuery = query.toLowerCase();
    
    items.forEach(item => {
      const label = item.querySelector('.filter-option__label');
      if (label) {
        const text = label.textContent.toLowerCase();
        item.style.display = text.includes(lowerQuery) ? 'flex' : 'none';
      }
    });
  }

  // ========================================================================
  // Keyboard Navigation & Accessibility
  // ========================================================================
  
  setupKeyboardNavigation() {
    // ESC to close drawer
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.closeDrawer();
      }
    });
  }

  trapFocus() {
    if (!this.drawer) return;
    
    const focusableElements = this.drawer.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    const handleTab = (e) => {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };
    
    this.drawer.addEventListener('keydown', handleTab);
    
    // Remove listener when drawer closes
    const originalClose = this.closeDrawer.bind(this);
    this.closeDrawer = () => {
      this.drawer.removeEventListener('keydown', handleTab);
      originalClose();
    };
  }
}

// =============================================================================
// Initialize on DOM Ready
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Only initialize on resources list page
  if (document.querySelector('.resources-browse-page')) {
    new ResourceFilters();
  }
});

// Export for module usage
export default ResourceFilters;
