# Route Map (High Level)

| Blueprint | Route | Methods | Template / Response | Notes |
|-----------|-------|---------|---------------------|-------|
| auth | `/auth/login` | GET/POST | `auth/login.html` | Login form, flashes errors. |
| auth | `/auth/register` | GET/POST | `auth/register.html` | Registration w/ server-side validation. |
| auth | `/auth/logout` | POST | redirect | Requires CSRF + login. |
| auth | `/auth/profile` | GET | `auth/profile.html` | Protected profile summary. |
| resources | `/` | GET | redirect to `/resources/dashboard` | Entry point after login. |
| resources | `/resources` | GET | `resources/list.html` | Public browse w/ filter drawer & cards. |
| resources | `/resources/<int:resource_id>` | GET | `resources/detail.html` | Hero carousel, facts, reviews, booking button. |
| resources | `/resources/dashboard` | GET | `resources/dashboard.html` | Authenticated dashboard of KPIs. |
| resources | `/resources/create` | GET/POST | `resources/create.html` | Multistep form wizard (wizard partial). |
| resources | `/resources/<id>/edit` | GET/POST | `resources/edit.html` | Same wizard for editing. |
| resources | `/resources/my_resources` | GET | `resources/my_resources.html` | Owner list (extends base). |
| bookings | `/bookings/new` | GET/POST | `bookings/new.html` | Booking request wizard. |
| bookings | `/bookings/my_bookings` | GET | `bookings/my_bookings.html` | List + cards. |
| bookings | `/bookings/<id>` | GET | `bookings/detail.html` | Booking detail view. |
| messages | `/messages/inbox` | GET | `messages/inbox.html` | Split inbox/thread UI. |
| messages | `/messages/conversation/<int:user_id>` | GET | `messages/inbox.html` | Same template w/ active thread. |
| messages | `/messages/compose` | GET/POST | `messages/compose.html` | Compose drawer-style form. |
| reviews | `/reviews/<resource_id>/new` | POST | redirect | uses `_review_form.html`. |
| admin | `/admin/dashboard` | GET | `admin/dashboard.html` | KPI cards + flagged content. |
| admin | `/admin/users` | GET | `admin/users.html` | Table w/ role chips, bulk actions. |
| admin | `/admin/analytics` | GET | `admin/analytics.html` | Charts (line/bar/doughnut). |
| admin | `/admin/users/<id>` | GET | `admin/user_detail.html` | Detail view. |
| concierge | `/concierge` | GET | `concierge/index.html` | AI concierge landing. |
| concierge | `/concierge/help` | GET | `concierge/help.html` | FAQ style help. |
| concierge | `/concierge/api/query` | POST | JSON | AI response API (per plan). |
| misc | `/resources/availability/<id>` | GET (JSON) | JSON | Booking drawer availability feed. |
| misc | `/admin/ping` | GET | JSON | RBAC smoke test. |
