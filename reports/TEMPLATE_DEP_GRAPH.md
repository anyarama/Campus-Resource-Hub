# Template Dependency Graph

```
base.html
├── includes components/booking_drawer.html (authenticated only)
├── yields blocks: breadcrumbs, page_header, main_content, extra_css, extra_js
├── references macros in templates/_components.html
└── loaded by every page template: auth/login, auth/register, resources/*, bookings/*, admin/*, messages/*, concierge/*
```

## Component & Partial Usage
- `templates/components/*.html` host macros for button, card, table, badge, etc. Page templates `{% from %}` these macros.
- `_resource_card.html`, `_booking_card.html`, `_review_list.html`, `_review_form.html` supply reusable chunks included via `{% include %}`.
- Layout helpers (e.g., `app.html`, `layouts/app.html`) exist for legacy references but new IU UI funnels through `base.html`.

## Notable Relationships
- `resources/_form_wizard.html` consumed by both `create.html` and `edit.html`.
- `messages/inbox.html` renders both conversation list + detail; includes `_review_*` components for rating display.
- `admin` templates share macros for tables (role chips, status badges) and rely on `admin.js` bundle for chart hydration.
