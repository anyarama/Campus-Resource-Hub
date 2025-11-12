# Templates Inventory

_Scanned `src/templates` (vendor directories, virtualenv, and the seed apps under `/Campus_Resource_hub*` were excluded)._  Each entry notes whether the template itself defines actionable forms or server-bound links.

| Template | Purpose | Actionable Elements |
| --- | --- | --- |
| `src/templates/_components.html` | Shared macro definitions for form fields, buttons, cards. | None (helpers only). |
| `src/templates/admin/analytics.html` | Analytics dashboard with charts and period selector. | GET `<form class="analytics-period">` submits `period` query param on change. |
| `src/templates/admin/dashboard.html` | Admin overview of KPIs, pending approvals, flagged reviews. | POST bulk approvals form (`admin.bulk_booking_approvals`), POST review unhide form (`reviews.unhide`), link to `resources.detail` for review context. |
| `src/templates/admin/user_detail.html` | Detailed profile for a single user with moderation actions. | Back link to `admin.users`; POST forms for activate (`admin.activate_user`), suspend (`admin.suspend_user`), delete (`admin.delete_user`). |
| `src/templates/admin/users.html` | User management table with filters and bulk actions. | GET filter form; POST bulk update form (`admin.bulk_update_users`); per-row POST forms for suspend/activate; per-row link to `admin.user_detail`; header link to `admin.dashboard`. |
| `src/templates/auth/login.html` | Login screen using `_components` macros. | POST login form (`auth.login`); link to registration. |
| `src/templates/auth/profile.html` | Displays current user profile, stats, admin shortcut. | Link to `resources.dashboard`; admin-only link to `admin.dashboard`. |
| `src/templates/auth/register.html` | Registration form with role selection. | POST register form (`auth.register`); link to login. |
| `src/templates/base.html` | Global layout, sidebar, header, booking drawer include. | Sidebar nav links (dashboard/resources/my resources/my bookings/messages/concierge); admin nav links; guest header links (`auth.login`/`auth.register`); user dropdown link (`auth.profile`); two POST logout forms (`auth.logout`). |
| `src/templates/bookings/_booking_card.html` | Macro rendering booking cards with contextual actions. | Links to `resources.detail`/`bookings.detail`/`resources.detail#reviews`; POST forms for approve (`bookings.approve`), cancel (`bookings.cancel`), complete (`bookings.complete`). |
| `src/templates/bookings/detail.html` | Booking detail view with action buttons and reject modal. | POST forms for approve/cancel/complete/reject; links to leave review, back to `bookings.my_bookings`, and `messages.compose`. |
| `src/templates/bookings/my_bookings.html` | My bookings overview with sections. | CTA links to `resources.index` and `resources.create`; booking cards inherit actions from `_booking_card`. |
| `src/templates/bookings/new.html` | Booking request form for a resource. | POST booking creation form (`bookings.create`); cancel link back to `resources.detail`. |
| `src/templates/components/alert.html` | Visual alert snippet. | None. |
| `src/templates/components/avatar.html` | Avatar UI partial. | None. |
| `src/templates/components/badge.html` | Badge UI partial. | None. |
| `src/templates/components/booking_drawer.html` | Client-side booking drawer used in base layout. | JS-driven `<form data-booking-form>` (no direct action attribute; JS reads `data-booking-url` / `data-availability-url`). |
| `src/templates/components/breadcrumbs.html` | Breadcrumb component. | Anchor placeholders only. |
| `src/templates/components/button.html` | Button tokens demo. | None. |
| `src/templates/components/card.html` | Card component demo. | None. |
| `src/templates/components/checkbox.html` | Checkbox component markup. | None server-bound. |
| `src/templates/components/empty_state.html` | Empty state partial. | None. |
| `src/templates/components/input.html` | Input component markup. | None server-bound. |
| `src/templates/components/loading_skeleton.html` | Skeleton loader markup. | None. |
| `src/templates/components/modal.html` | Modal component markup. | None (no submission). |
| `src/templates/components/pagination.html` | Pagination macro generating `href`s from a URL pattern. | Links resolved via provided `url_pattern`. |
| `src/templates/components/select.html` | Select component markup. | None. |
| `src/templates/components/skeleton.html` | Additional skeleton states. | None. |
| `src/templates/components/table.html` | Table component markup. | None. |
| `src/templates/components/tabs.html` | Tabs component markup. | None. |
| `src/templates/components/textarea.html` | Textarea component markup. | None. |
| `src/templates/concierge/help.html` | Static help content for AI concierge. | Footer CTAs (broken markup) intended for `concierge.index` / `resources.index`. |
| `src/templates/concierge/index.html` | AI concierge landing with JS form. | `<form id="concierge-form">` handled via fetch to `concierge.query`; fallback link to `resources.index`. |
| `src/templates/errors/401.html` | Unauthorized page. | Link back to `resources.dashboard`. |
| `src/templates/errors/403.html` | Forbidden page. | Link back to `resources.dashboard`. |
| `src/templates/errors/404.html` | Not-found page. | Link back to `resources.dashboard`. |
| `src/templates/errors/500.html` | Server-error page. | Link back to `resources.dashboard`. |
| `src/templates/messages/compose.html` | Compose new direct message. | POST compose form (`messages.compose`, param `user_id`); cancel link to inbox. |
| `src/templates/messages/conversation.html` | Conversation thread view. | POST delete form per message (`messages.delete`); reply form (`messages.send`). |
| `src/templates/messages/inbox.html` | Inbox with conversation list and composer. | Conversation links (`messages.inbox`, param `user_id`); CTA to `resources.index`; POST composer form (`messages.send`). |
| `src/templates/resources/_form_wizard.html` | Core form partial for resource create/edit. | Multipart POST form (`form_action` from parent) with visibility radios, file uploads, availability checkboxes; cancel/back links (`resources.detail` or `resources.index`). |
| `src/templates/resources/_resource_card.html` | Card used in "My resources" with admin actions. | Links to `resources.detail`/`resources.edit`; POST forms for publish (`resources.publish`) or archive (`resources.archive`). |
| `src/templates/resources/create.html` | Wrapper configuring `_form_wizard` for creation. | Sets `form_action` = `resources.create`. |
| `src/templates/resources/dashboard.html` | User dashboard KPI view. | None beyond chart JS. |
| `src/templates/resources/detail.html` | Resource detail page with booking CTA and review drawer. | Booking button (JS) referencing `bookings.new` and `resources.availability`; fallback link to `bookings.new`; POST review form (`reviews.create`). |
| `src/templates/resources/edit.html` | Wrapper configuring `_form_wizard` for editing. | Sets `form_action` = `resources.edit(resource_id)` and adds back link to detail view. |
| `src/templates/resources/list.html` | Public resource browse with filters and toolbar. | GET search form (`resources.index` with preserved filter params); header links to `resources.my_resources` and `resources.create`; sort dropdown links (`resources.index` + `sort` param). |
| `src/templates/resources/my_resources.html` | Owner dashboard listing their resources. | CTA to `resources.create`; cards reuse `_resource_card` actions. |
| `src/templates/reviews/_review_form.html` | Macro for review create/edit UI. | POST form to `reviews.submit`/`reviews.update` depending on mode; cancel link back to `resources.detail#reviews`. |
| `src/templates/reviews/_review_list.html` | Renders list of reviews. | None. |
| `src/templates/reviews/_star_rating.html` | Star rating widget. | None. |
