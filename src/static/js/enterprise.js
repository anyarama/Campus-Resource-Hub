import Chart from 'chart.js/auto';

// ============================================
// ENTERPRISE UI - Main JavaScript Bundle
// ============================================

// --- THEME TOGGLE ---
class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'light';
    this.init();
  }
  
  init() {
    document.documentElement.setAttribute('data-theme', this.theme);
    this.updateToggleButtons();
    this.attachListeners();
    this.emitThemeChange();
  }
  
  toggle() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    document.documentElement.setAttribute('data-theme', this.theme);
    this.updateToggleButtons();
    this.emitThemeChange();
  }
  
  updateToggleButtons() {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      const icon = btn.querySelector('.theme-icon');
      if (icon) {
        // Update Bootstrap icon classes or text
        if (icon.classList.contains('bi')) {
          icon.className = this.theme === 'light' ? 'bi bi-moon-fill theme-icon' : 'bi bi-sun-fill theme-icon';
        } else {
          icon.textContent = this.theme === 'light' ? '🌙' : '☀️';
        }
      }
    });
    
    // Update body theme attribute
    document.body.dataset.theme = this.theme;
  }
  
  attachListeners() {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.addEventListener('click', () => this.toggle());
    });
  }

  emitThemeChange() {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('crh-theme-change', { detail: { theme: this.theme } }));
    }
  }
}

// --- SIDEBAR MANAGER (Icon-Only with Mobile Toggle) ---
class SidebarManager {
  constructor() {
    this.sidebar = document.querySelector('.app-sidebar');
    this.overlay = document.querySelector('.sidebar-overlay');
    this.toggleBtn = document.querySelector('[data-sidebar-toggle]');
    this.expanded = false;  // Desktop: icon-only by default
    this.init();
  }
  
  init() {
    if (!this.sidebar) return;
    
    // Desktop: always start icon-only (collapsed)
    // Mobile: hidden by default
    if (window.innerWidth < 768) {
      this.sidebar.classList.remove('open');
    }
    
    this.attachListeners();
  }
  
  toggle() {
    if (window.innerWidth < 768) {
      // Mobile: slide in/out overlay
      this.sidebar.classList.toggle('open');
      this.overlay?.classList.toggle('active');
      document.body.style.overflow = this.sidebar.classList.contains('open') ? 'hidden' : '';
    } else {
      // Desktop: optional expand (keep icon-only as default)
      this.expanded = !this.expanded;
      this.sidebar.classList.toggle('expanded');
    }
  }
  
  close() {
    this.sidebar?.classList.remove('open');
    this.overlay?.classList.remove('active');
    document.body.style.overflow = '';
  }
  
  attachListeners() {
    this.toggleBtn?.addEventListener('click', () => this.toggle());
    this.overlay?.addEventListener('click', () => this.close());
    
    // Close on mobile nav link click
    if (window.innerWidth < 768) {
      document.querySelectorAll('.app-sidebar a').forEach(link => {
        link.addEventListener('click', () => this.close());
      });
    }
    
    // Handle window resize
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 768) {
        this.close();
      }
    });
  }
}

// --- MODAL MANAGER ---
class ModalManager {
  constructor() {
    this.activeModal = null;
    this.attachListeners();
  }
  
  open(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    
    this.activeModal = modal;
    modal.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
    
    // Focus first focusable element
    const focusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    focusable?.focus();
  }
  
  close(modal = this.activeModal) {
    if (!modal) return;
    
    modal.classList.remove('modal-open');
    document.body.style.overflow = '';
    this.activeModal = null;
  }
  
  attachListeners() {
    // Open modal triggers
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-modal-open]');
      if (trigger) {
        e.preventDefault();
        this.open(trigger.dataset.modalOpen);
      }
    });
    
    // Close modal triggers
    document.addEventListener('click', (e) => {
      const closer = e.target.closest('[data-modal-close]');
      if (closer) {
        e.preventDefault();
        const modal = closer.closest('.modal');
        this.close(modal);
      }
    });
    
    // Close on backdrop click
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal')) {
        this.close(e.target);
      }
    });
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.activeModal) {
        this.close();
      }
    });
  }
}

// --- TOAST NOTIFICATIONS ---
class ToastManager {
  constructor() {
    this.container = this.getOrCreateContainer();
  }
  
  getOrCreateContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  }
  
  show(message, type = 'info', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ℹ'
    };
    
    toast.innerHTML = `
      <div class="toast-icon">${icons[type] || icons.info}</div>
      <div class="toast-content">
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close" aria-label="Close">×</button>
    `;
    
    this.container.appendChild(toast);
    
    // Close button
    toast.querySelector('.toast-close').addEventListener('click', () => {
      this.hide(toast);
    });
    
    // Auto-hide
    if (duration > 0) {
      setTimeout(() => this.hide(toast), duration);
    }
    
    return toast;
  }
  
  hide(toast) {
    toast.classList.add('toast-hiding');
    setTimeout(() => toast.remove(), 300);
  }
  
  success(message, duration) {
    return this.show(message, 'success', duration);
  }
  
  error(message, duration) {
    return this.show(message, 'error', duration);
  }
  
  warning(message, duration) {
    return this.show(message, 'warning', duration);
  }
  
  info(message, duration) {
    return this.show(message, 'info', duration);
  }
}

// --- TABS MANAGER ---
class TabsManager {
  constructor() {
    this.attachListeners();
  }
  
  switchTab(trigger) {
    const tabContainer = trigger.closest('[data-tabs]');
    if (!tabContainer) return;
    
    const targetId = trigger.dataset.tabTrigger;
    const targetPanel = document.getElementById(targetId);
    if (!targetPanel) return;
    
    // Update triggers
    tabContainer.querySelectorAll('[data-tab-trigger]').forEach(t => {
      t.classList.remove('active');
      t.setAttribute('aria-selected', 'false');
    });
    trigger.classList.add('active');
    trigger.setAttribute('aria-selected', 'true');
    
    // Update panels
    tabContainer.querySelectorAll('[role="tabpanel"]').forEach(p => {
      p.classList.remove('active');
      p.hidden = true;
    });
    targetPanel.classList.add('active');
    targetPanel.hidden = false;
  }
  
  attachListeners() {
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-tab-trigger]');
      if (trigger) {
        e.preventDefault();
        this.switchTab(trigger);
      }
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      const trigger = e.target.closest('[data-tab-trigger]');
      if (!trigger) return;
      
      const tabList = trigger.parentElement;
      const triggers = Array.from(tabList.querySelectorAll('[data-tab-trigger]'));
      const currentIndex = triggers.indexOf(trigger);
      
      let nextIndex = currentIndex;
      
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        nextIndex = (currentIndex + 1) % triggers.length;
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        nextIndex = (currentIndex - 1 + triggers.length) % triggers.length;
      } else if (e.key === 'Home') {
        e.preventDefault();
        nextIndex = 0;
      } else if (e.key === 'End') {
        e.preventDefault();
        nextIndex = triggers.length - 1;
      } else {
        return;
      }
      
      triggers[nextIndex].focus();
      this.switchTab(triggers[nextIndex]);
    });
  }
}

// --- DRAWER MANAGER (Generic slide-out drawer) ---
class DrawerManager {
  constructor() {
    this.activeDrawer = null;
    this.backdrop = null;
    this.attachListeners();
  }
  
  open(drawerId) {
    const drawer = document.getElementById(drawerId);
    if (!drawer) return;

    this.activeDrawer = drawer;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');

    // Create backdrop
    if (!this.backdrop) {
      this.backdrop = document.createElement('div');
      this.backdrop.className = 'drawer-backdrop';
      this.backdrop.addEventListener('click', () => this.close());
      document.body.appendChild(this.backdrop);
    }
    
    this.backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Focus first focusable element
    const focusable = drawer.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    focusable?.focus();
  }
  
  close(drawer = this.activeDrawer) {
    if (!drawer) return;

    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    this.backdrop?.classList.remove('active');
    document.body.style.overflow = '';
    this.activeDrawer = null;
  }
  
  attachListeners() {
    // Open drawer triggers
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-drawer-open]');
      if (trigger) {
        e.preventDefault();
        this.open(trigger.dataset.drawerOpen);
      }
    });
    
    // Close drawer triggers
    document.addEventListener('click', (e) => {
      const closer = e.target.closest('[data-drawer-close], .drawer-close');
      if (closer) {
        e.preventDefault();
        const drawer = closer.closest('.drawer');
        this.close(drawer);
      }
    });
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.activeDrawer) {
        this.close();
      }
    });
  }
}

// --- FILTER DRAWER (Legacy support) ---
class FilterDrawerManager {
  constructor() {
    this.drawer = document.querySelector('.filter-drawer');
    this.attachListeners();
  }
  
  toggle() {
    this.drawer?.classList.toggle('filter-drawer-open');
  }
  
  close() {
    this.drawer?.classList.remove('filter-drawer-open');
  }
  
  attachListeners() {
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-filter-toggle]');
      if (trigger) {
        e.preventDefault();
        this.toggle();
      }
      
      const closer = e.target.closest('[data-filter-close]');
      if (closer) {
        e.preventDefault();
        this.close();
      }
    });
  }
}

// --- DROPDOWN MENU MANAGER ---
class DropdownManager {
  constructor() {
    this.activeDropdown = null;
    this.attachListeners();
  }
  
  toggle(triggerId) {
    const trigger = document.querySelector(`[data-dropdown-toggle="${triggerId}"]`);
    const dropdown = document.getElementById(triggerId);
    
    if (!dropdown) return;
    
    const isOpen = dropdown.classList.contains('active');
    
    // Close any open dropdowns
    this.closeAll();
    
    if (!isOpen) {
      dropdown.classList.add('active');
      trigger?.setAttribute('aria-expanded', 'true');
      this.activeDropdown = dropdown;
    }
  }
  
  close(dropdown = this.activeDropdown) {
    if (!dropdown) return;
    
    dropdown.classList.remove('active');
    const trigger = document.querySelector(`[data-dropdown-toggle="${dropdown.id}"]`);
    trigger?.setAttribute('aria-expanded', 'false');
    this.activeDropdown = null;
  }
  
  closeAll() {
    document.querySelectorAll('.dropdown-menu.active').forEach(dd => {
      this.close(dd);
    });
  }
  
  attachListeners() {
    // Toggle dropdown
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-dropdown-toggle]');
      if (trigger) {
        e.preventDefault();
        e.stopPropagation();
        this.toggle(trigger.dataset.dropdownToggle);
      }
    });
    
    // Close on outside click
    document.addEventListener('click', (e) => {
      if (this.activeDropdown && !e.target.closest('.dropdown-menu')) {
        this.closeAll();
      }
    });
    
    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.activeDropdown) {
        this.closeAll();
      }
    });
  }
}

// --- FORM VALIDATION ---
class FormValidator {
  constructor() {
    this.attachListeners();
  }
  
  validateField(field) {
    const value = field.value.trim();
    const required = field.hasAttribute('required');
    const pattern = field.pattern;
    const type = field.type;
    
    let isValid = true;
    let errorMessage = '';
    
    if (required && !value) {
      isValid = false;
      errorMessage = 'This field is required';
    } else if (value && pattern) {
      const regex = new RegExp(pattern);
      if (!regex.test(value)) {
        isValid = false;
        errorMessage = field.title || 'Invalid format';
      }
    } else if (type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        isValid = false;
        errorMessage = 'Invalid email address';
      }
    }
    
    this.setFieldState(field, isValid, errorMessage);
    return isValid;
  }
  
  setFieldState(field, isValid, errorMessage) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;
    
    field.classList.toggle('is-invalid', !isValid);
    field.classList.toggle('is-valid', isValid && field.value.trim());
    
    let errorEl = formGroup.querySelector('.form-error');
    if (!isValid && errorMessage) {
      if (!errorEl) {
        errorEl = document.createElement('span');
        errorEl.className = 'form-error';
        field.parentNode.appendChild(errorEl);
      }
      errorEl.textContent = errorMessage;
    } else if (errorEl) {
      errorEl.remove();
    }
  }
  
  attachListeners() {
    document.addEventListener('blur', (e) => {
      const field = e.target;
      if (field.matches('input, textarea, select')) {
        this.validateField(field);
      }
    }, true);
    
    document.addEventListener('submit', (e) => {
      const form = e.target;
      if (!form.matches('form')) return;
      
      let isValid = true;
      form.querySelectorAll('input, textarea, select').forEach(field => {
        if (!this.validateField(field)) {
          isValid = false;
        }
      });
      
      if (!isValid) {
        e.preventDefault();
        const firstInvalid = form.querySelector('.is-invalid');
        firstInvalid?.focus();
      }
    });
  }
}

// --- DASHBOARD CHARTS -------------------------------------------------------
const DASHBOARD_CHART_PALETTE = ['#990000', '#B91C1C', '#D97706', '#2563EB', '#10B981', '#9333EA'];
const dashboardCharts = {
  bookings: null,
  categories: null
};
let dashboardChartConfig = null;

function cloneConfig(config) {
  if (!config) return null;
  if (typeof structuredClone === 'function') {
    return structuredClone(config);
  }
  return JSON.parse(JSON.stringify(config));
}

function getThemeColors() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {
    text: isDark ? '#E5E7EB' : '#1F2937',
    grid: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(17,24,39,0.08)',
    border: isDark ? 'rgba(255,255,255,0.25)' : 'rgba(17,24,39,0.15)',
    tooltipBg: isDark ? '#111827' : '#ffffff'
  };
}

function buildLineOptions(theme) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: theme.tooltipBg,
        titleColor: theme.text,
        bodyColor: theme.text,
        borderColor: theme.border,
        borderWidth: 1
      }
    },
    interaction: {
      mode: 'index',
      intersect: false
    },
    scales: {
      x: {
        ticks: { color: theme.text },
        grid: { display: false },
        border: { color: theme.border }
      },
      y: {
        beginAtZero: true,
        ticks: { color: theme.text },
        grid: { color: theme.grid },
        border: { color: theme.border }
      }
    }
  };
}

function buildDoughnutOptions(theme) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '65%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: { color: theme.text, usePointStyle: true }
      },
      tooltip: {
        backgroundColor: theme.tooltipBg,
        titleColor: theme.text,
        bodyColor: theme.text,
        borderColor: theme.border,
        borderWidth: 1
      }
    }
  };
}

function buildCategoryPalette(length) {
  if (!length) return DASHBOARD_CHART_PALETTE;
  const colors = [];
  for (let i = 0; i < length; i += 1) {
    colors.push(DASHBOARD_CHART_PALETTE[i % DASHBOARD_CHART_PALETTE.length]);
  }
  return colors;
}

function renderDashboardCharts() {
  if (!dashboardChartConfig) return;
  const theme = getThemeColors();

  if (dashboardChartConfig.bookings) {
    const canvas = document.getElementById('chart-bookings');
    if (canvas) {
      dashboardCharts.bookings?.destroy();
      const lineData = cloneConfig(dashboardChartConfig.bookings);
      if (lineData?.datasets?.length) {
        lineData.datasets = lineData.datasets.map(dataset => ({
          borderColor: dataset.borderColor || '#990000',
          backgroundColor: dataset.backgroundColor || 'rgba(153, 0, 0, 0.15)',
          borderWidth: dataset.borderWidth ?? 2,
          tension: dataset.tension ?? 0.4,
          fill: dataset.fill ?? true,
          pointRadius: dataset.pointRadius ?? 4,
          pointHoverRadius: dataset.pointHoverRadius ?? 6,
          ...dataset
        }));
      }
      dashboardCharts.bookings = new Chart(canvas, {
        type: 'line',
        data: lineData,
        options: buildLineOptions(theme)
      });
    }
  }

  if (dashboardChartConfig.categories) {
    const canvas = document.getElementById('chart-categories');
    if (canvas) {
      dashboardCharts.categories?.destroy();
      const doughnutData = cloneConfig(dashboardChartConfig.categories);
      if (doughnutData?.datasets?.length) {
        doughnutData.datasets = doughnutData.datasets.map(dataset => ({
          backgroundColor: dataset.backgroundColor || buildCategoryPalette(dataset.data?.length || 0),
          borderWidth: dataset.borderWidth ?? 0,
          ...dataset
        }));
      }
      dashboardCharts.categories = new Chart(canvas, {
        type: 'doughnut',
        data: doughnutData,
        options: buildDoughnutOptions(theme)
      });
    }
  }
}

export function initDashboardCharts(config = {}) {
  dashboardChartConfig = config;
  renderDashboardCharts();
}

if (typeof window !== 'undefined') {
  window.initDashboardCharts = initDashboardCharts;
  window.addEventListener('crh-theme-change', () => {
    if (dashboardChartConfig) {
      renderDashboardCharts();
    }
  });
  window.dispatchEvent(new Event('dashboard-charts-ready'));
}

// --- INITIALIZE ALL ---
document.addEventListener('DOMContentLoaded', () => {
  window.theme = new ThemeManager();
  window.sidebar = new SidebarManager();
  window.modal = new ModalManager();
  window.toast = new ToastManager();
  window.tabs = new TabsManager();
  window.drawer = new DrawerManager();
  window.dropdown = new DropdownManager();
  window.filterDrawer = new FilterDrawerManager();
  window.formValidator = new FormValidator();
  
  // Show flash messages as toasts
  document.querySelectorAll('.flash-message').forEach(flash => {
    const type = flash.dataset.type || 'info';
    const message = flash.textContent.trim();
    if (message) {
      window.toast.show(message, type);
    }
    flash.remove();
  });
  
  console.log('✅ Enterprise UI initialized');
});

// Global utility functions
window.showToast = (message, type, duration) => {
  return window.toast?.show(message, type, duration);
};

window.openModal = (modalId) => {
  window.modal?.open(modalId);
};

window.closeModal = () => {
  window.modal?.close();
};
