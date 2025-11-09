# Enterprise UI Build Instructions

## Files Created

### Build System
- ✅ `vite.config.js` - Updated to output enterprise.{css,js}
- ✅ `src/static/scss/enterprise.scss` - Master SCSS import
- ✅ `src/static/js/enterprise.js` - Main JS bundle

### Design System
- ✅ `src/static/scss/tokens.scss` - Design tokens (colors, spacing, typography, shadows, etc.)
- ✅ `src/static/scss/theme.light.scss` - Light theme CSS variables
- ✅ `src/static/scss/theme.dark.scss` - Dark theme CSS variables
- ✅ `src/static/scss/base.scss` - Base styles, resets, utilities

### Components
- ✅ `src/static/scss/components/input.scss` - Form inputs
- ✅ `src/static/scss/components/toast.scss` - Toast notifications

### Templates
- ✅ `src/templates/base.html` - New app shell with sidebar+topbar (replaces Bootstrap)
- ✅ `src/templates/_components.html` - Jinja macros for components

## Required Commands

### 1. Install Dependencies (if not already done)
```bash
npm install
```

### 2. Build Assets
```bash
# Development build (watch mode)
npm run dev

# Production build (one-time)
npm run build
```

This will generate:
- `src/static/dist/assets/enterprise.css` (compiled from enterprise.scss)
- `src/static/dist/assets/enterprise.js` (bundled from enterprise.js)

### 3. Run Flask App
```bash
# In a separate terminal
python src/app.py
# OR
make run
```

## What's Different

### Before (Bootstrap CDN)
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

### After (Enterprise UI)
```html
<link rel="stylesheet" href="{{ url_for('static', filename='dist/assets/enterprise.css') }}">
<script type="module" src="{{ url_for('static', filename='dist/assets/enterprise.js') }}"></script>
```

## Features Included

### Theme System
- Light/Dark themes with localStorage persistence
- CSS custom properties for easy theming
- Accessible color contrast in both themes

### Application Shell
- **Sidebar navigation** (collapsible on mobile, toggle on desktop)
- **Topbar** with theme toggle, user menu
- **Responsive** layout (mobile-first)
- **Skip link** for accessibility

### JavaScript Modules
- `ThemeManager` - Theme switching
- `SidebarManager` - Sidebar collapse/expand
- `ModalManager` - Modal dialogs
- `ToastManager` - Toast notifications
- `TabsManager` - Tab navigation with keyboard support
- `FilterDrawerManager` - Filter panel toggle
- `FormValidator` - Client-side validation

### Jinja Macros Available
- `button()` - Buttons and links
- `form_field()` - Form inputs with validation
- `card()` - Card component
- `table()` - Data tables
- `badge()` - Status badges
- `alert()` - Alert messages
- `modal()` - Modal dialogs
- `tabs()` - Tab interface
- `pagination()` - Page navigation
- `skeleton()` - Loading states
- `empty_state()` - Empty data state
- `breadcrumbs()` - Breadcrumb navigation

## Next Steps (Template Migration)

### Priority 1 - Core Pages
These pages need manual refactoring to use the new component system:
1. `src/templates/auth/login.html` - Remove Bootstrap classes, use form_field macro
2. `src/templates/resources/list.html` - Use card macro, filter drawer
3. `src/templates/resources/detail.html` - Two-column layout
4. `src/templates/admin/dashboard.html` - KPI tiles, tables

### Priority 2 - Remaining Pages
All other templates in:
- `src/templates/resources/` (create.html, edit.html, my_resources.html)
- `src/templates/bookings/` (all)
- `src/templates/messages/` (all)
- `src/templates/admin/` (users.html, analytics.html, etc.)
- `src/templates/concierge/` (all)

### Migration Pattern
```jinja
{# OLD Bootstrap #}
<div class="row">
  <div class="col-md-6">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Title</h5>
        <p class="card-text">Content</p>
        <a href="#" class="btn btn-primary">Action</a>
      </div>
    </div>
  </div>
</div>

{# NEW Enterprise Component #}
{% from '_components.html' import card, button %}
{{ card(
  title='Title',
  body='<p>Content</p>',
  actions=button('Action', href='#', kind='primary')
) }}
```

## Styles Already Exist

The following component SCSS files are already in the codebase (created in Phase 12):
- `src/static/scss/components/button.scss`
- `src/static/scss/components/alert.scss`
- `src/static/scss/components/modal.scss`
- `src/static/scss/components/tabs.scss`
- `src/static/scss/components/pagination.scss`
- `src/static/scss/components/skeleton.scss`
- `src/static/scss/components/sidebar.scss`
- `src/static/scss/components/navbar.scss`
- `src/static/scss/components/filter-drawer.scss`
- `src/static/scss/components/form.scss`
- `src/static/scss/components/card.scss`
- `src/static/scss/components/table.scss`
- `src/static/scss/components/badge.scss`

These are all imported in `enterprise.scss`.

## Troubleshooting

### Assets not loading?
- Ensure `npm run build` completed successfully
- Check `src/static/dist/` directory exists with assets
- Verify Flask static file serving is working

### Styles broken?
- Build may have failed due to SCSS syntax errors
- Check console for error messages
- Try `npm run build -- --force`

### JavaScript not working?
- Check browser console for errors
- Ensure `type="module"` is in script tag
- Verify enterprise.js was built correctly
