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
  }
  
  toggle() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    document.documentElement.setAttribute('data-theme', this.theme);
    this.updateToggleButtons();
  }
  
  updateToggleButtons() {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      const icon = btn.querySelector('.theme-icon');
      if (icon) {
        icon.textContent = this.theme === 'light' ? '🌙' : '☀️';
      }
    });
  }
  
  attachListeners() {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.addEventListener('click', () => this.toggle());
    });
  }
}

// --- SIDEBAR TOGGLE ---
class SidebarManager {
  constructor() {
    this.sidebar = document.querySelector('.app-sidebar');
    this.overlay = document.querySelector('.sidebar-overlay');
    this.toggleBtn = document.querySelector('[data-sidebar-toggle]');
    this.collapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    this.init();
  }
  
  init() {
    if (!this.sidebar) return;
    
    if (window.innerWidth >= 1024 && this.collapsed) {
      this.sidebar.classList.add('sidebar-collapsed');
    }
    
    this.attachListeners();
  }
  
  toggle() {
    if (window.innerWidth < 1024) {
      // Mobile: slide in/out
      this.sidebar.classList.toggle('sidebar-collapsed');
      this.overlay?.classList.toggle('active');
    } else {
      // Desktop: collapse/expand
      this.collapsed = !this.collapsed;
      this.sidebar.classList.toggle('sidebar-collapsed');
      localStorage.setItem('sidebar-collapsed', this.collapsed);
    }
  }
  
  close() {
    this.sidebar?.classList.add('sidebar-collapsed');
    this.overlay?.classList.remove('active');
  }
  
  attachListeners() {
    this.toggleBtn?.addEventListener('click', () => this.toggle());
    this.overlay?.addEventListener('click', () => this.close());
    
    // Close on mobile nav link click
    if (window.innerWidth < 1024) {
      document.querySelectorAll('.app-sidebar a').forEach(link => {
        link.addEventListener('click', () => this.close());
      });
    }
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

// --- FILTER DRAWER ---
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

// --- INITIALIZE ALL ---
document.addEventListener('DOMContentLoaded', () => {
  window.theme = new ThemeManager();
  window.sidebar = new SidebarManager();
  window.modal = new ModalManager();
  window.toast = new ToastManager();
  window.tabs = new TabsManager();
  window.filterDrawer = new FilterDrawerManager();
  window.formValidator = new FormValidator();
  
  // Show flash messages as toasts
  document.querySelectorAll('.flash-message').forEach(flash => {
    const type = flash.dataset.type || 'info';
    const message = flash.textContent.trim();
    window.toast.show(message, type);
    flash.remove();
  });
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
