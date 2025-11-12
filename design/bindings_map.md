# Template → Action Bindings Map

| Template | Element Label / Selector | Current Target | Method | Params | Notes |
| --- | --- | --- | --- | --- | --- |
| base.html | Sidebar nav “Dashboard” | `url_for('resources.dashboard')` | GET | — | Primary navigation entry. |
| base.html | Sidebar nav “Browse Resources” | `url_for('resources.index')` | GET | Optional `q`, filter args preserved by view | Visible to all authenticated users. |
| base.html | Sidebar nav “My Resources” | `url_for('resources.my_resources')` | GET | — | Owners manage listings. |
| base.html | Sidebar nav “My Bookings” | `url_for('bookings.my_bookings')` | GET | — | User booking overview. |
| base.html | Sidebar nav “Messages” | `url_for('messages.inbox')` | GET | `user_id` optional query for active conversation | Badge updates unread count via JS. |
| base.html | Sidebar nav “AI Concierge” | `url_for('concierge.index')` | GET | — | Launches AI assistant. |
| base.html | Admin nav “Dashboard” | `url_for('admin.dashboard')` | GET | — | Rendered only for `role == 'admin'`. |
| base.html | Admin nav “Users” | `url_for('admin.users')` | GET | — | User management entry. |
| base.html | Admin nav “Analytics” | `url_for('admin.analytics')` | GET | `period` query optional | Stats workspace. |
| base.html | Topbar dropdown “Profile” | `url_for('auth.profile')` | GET | — | Opens account profile view. |
| base.html | Guest CTA “Login” | `url_for('auth.login')` | GET | — | Visible when unauthenticated. |
| base.html | Guest CTA “Register” | `url_for('auth.register')` | GET | — | Visible when unauthenticated. |
| base.html | Sidebar logout form (`.sidebar-logout`) | `url_for('auth.logout')` | POST | CSRF token | Signs user out from sidebar footer. |
| base.html | User menu logout form | `url_for('auth.logout')` | POST | CSRF token | Dropdown action under avatar. |
| messages/compose.html | “Send Message” form | `url_for('messages.compose', user_id=recipient.user_id)` | POST | CSRF token, `content` textarea | Creates a new direct message to the selected user. |
| messages/compose.html | “Cancel” button | `url_for('messages.inbox')` | GET | — | Returns to inbox without sending. |
| messages/conversation.html | Delete message form (`.message-delete`) | `url_for('messages.delete', message_id=message.message_id)` | POST | CSRF token | Sender-only option; confirm prompt in template. |
| messages/conversation.html | Reply form (`#replyForm`) | `url_for('messages.send')` | POST | CSRF token, `receiver_id`, `content` | Sends follow-up message in thread. |
| messages/inbox.html | Conversation list link | `url_for('messages.inbox', user_id=other.user_id)` | GET | `user_id` query selects conversation | Highlights active thread, loads messages server-side. |
| messages/inbox.html | Empty-state CTA “Browse resources” | `url_for('resources.index')` | GET | — | Encourages starting a conversation via resource owners. |
| messages/inbox.html | Composer form (`.conversation-view__form`) | `url_for('messages.send')` | POST | CSRF token, `receiver_id`, `content` | Same endpoint as reply form. |
| bookings/detail.html | Approve booking form | `url_for('bookings.approve', booking_id=booking.booking_id)` | POST | CSRF token | Restricted to owners/admins. |
| bookings/detail.html | Cancel booking form | `url_for('bookings.cancel', booking_id=booking.booking_id)` | POST | CSRF token | Requester or owner depending on state. |
| bookings/detail.html | Complete booking form | `url_for('bookings.complete', booking_id=booking.booking_id)` | POST | CSRF token | Admin-only action when status approved. |
| bookings/detail.html | Reject modal form | `url_for('bookings.reject', booking_id=booking.booking_id)` | POST | CSRF token, `rejection_reason` | Modal collects reason text. |
| bookings/detail.html | “Leave a review” link | `url_for('resources.detail', resource_id=resource.resource_id) + '#reviews'` | GET | `resource_id` | Exposed after completion. |
| bookings/detail.html | “Back to My Bookings” link | `url_for('bookings.my_bookings')` | GET | — | Standard back navigation. |
| bookings/detail.html | “Message owner” link | `url_for('messages.compose', user_id=resource.owner_id)` | GET | `user_id` | Opens compose page addressed to owner. |
| bookings/_booking_card.html | Card title link | `url_for('resources.detail', resource_id=resource.resource_id)` | GET | `resource_id` | Navigates to resource detail. |
| bookings/_booking_card.html | “View Details” button | `url_for('bookings.detail', booking_id=booking.booking_id)` | GET | `booking_id` | Deep link into booking detail page. |
| bookings/_booking_card.html | Approve button form | `url_for('bookings.approve', booking_id=booking.booking_id)` | POST | CSRF token | Same as detail form; rendered when status pending & owner/admin. |
| bookings/_booking_card.html | Cancel button form | `url_for('bookings.cancel', booking_id=booking.booking_id)` | POST | CSRF token | Requester self-cancel. |
| bookings/_booking_card.html | Complete button form | `url_for('bookings.complete', booking_id=booking.booking_id)` | POST | CSRF token | Admin-only when status approved. |
| bookings/_booking_card.html | “Leave Review” button | `url_for('resources.detail', resource_id=resource.resource_id) + '#reviews'` | GET | `resource_id` | Shows when booking completed. |
| bookings/new.html | “Submit request” form | `url_for('bookings.create')` | POST | CSRF token, `resource_id`, start/end date & time, notes | Creates a new booking request. |
| bookings/new.html | “Cancel” link | `url_for('resources.detail', resource_id=resource.resource_id)` | GET | `resource_id` | Returns to resource detail without submitting. |
| bookings/my_bookings.html | CTA “Browse catalog” | `url_for('resources.index')` | GET | — | Encourages exploring new resources. |
| bookings/my_bookings.html | CTA “List a resource” | `url_for('resources.create')` | GET | — | Shortcut for owners to add listings. |
| resources/list.html | Search form (`.resources-search`) | `url_for('resources.index')` | GET | `q` plus preserved filter inputs (`category`, `location`, `status`, etc.) | Primary search across catalog. |
| resources/list.html | Header action “My Resources” | `url_for('resources.my_resources')` | GET | — | Visible to authenticated users. |
| resources/list.html | Header action “Create Resource” | `url_for('resources.create')` | GET | — | Launch resource wizard. |
| resources/list.html | Sort dropdown options | `url_for('resources.index', sort=value, ...)` | GET | `sort` value + active filters | Links generated via `sort_url` macro. |
| resources/create.html | Resource wizard form | `url_for('resources.create')` | POST | CSRF token, multipart fields defined in `_form_wizard` | Supplies `form_action` for wizard include. |
| resources/edit.html | Resource wizard form (edit) | `url_for('resources.edit', resource_id=resource.resource_id)` | POST | CSRF token, multipart fields | Saves updates to existing resource. |
| resources/_form_wizard.html | Cancel link (create mode) | `url_for('resources.index')` | GET | — | Only shown when `is_edit` is false. |
| resources/_form_wizard.html | Cancel link (edit mode) | `url_for('resources.detail', resource_id=resource.resource_id)` | GET | `resource_id` | Provides return path when editing. |
| resources/_resource_card.html | “View” button | `url_for('resources.detail', resource_id=resource.resource_id)` | GET | `resource_id` | Displays resource in public detail page. |
| resources/_resource_card.html | “Edit” button | `url_for('resources.edit', resource_id=resource.resource_id)` | GET | `resource_id` | Opens wizard pre-filled. |
| resources/_resource_card.html | “Publish” form | `url_for('resources.publish', resource_id=resource.resource_id)` | POST | CSRF token | Available when status is `draft`. |
| resources/_resource_card.html | “Archive” form | `url_for('resources.archive', resource_id=resource.resource_id)` | POST | CSRF token | Available when status is `published`. |
| resources/detail.html | “Book this resource” button | Data attrs: `data-booking-url="{{ url_for('bookings.new', resource_id=resource.resource_id) }}"`, `data-availability-url="{{ url_for('resources.availability', resource_id=resource.resource_id) }}"` | JS fetch + redirect | `resource_id` | JS opens booking drawer, fetches availability, then redirects to bookings form. |
| resources/detail.html | “View booking options” link (guest) | `url_for('bookings.new', resource_id=resource.resource_id)` | GET | `resource_id` | Fallback CTA when not authenticated. |
| resources/detail.html | Review drawer form | `url_for('reviews.create', resource_id=resource.resource_id)` | POST | CSRF token, `rating`, `comment` | Shown when `can_review` true. |
| reviews/_review_form.html | Review form (create mode) | `url_for('reviews.submit', resource_id=resource.resource_id)` | POST | CSRF token, rating/comment | Macro used outside detail; button copy configurable. |
| reviews/_review_form.html | Review form (edit mode) | `url_for('reviews.update', review_id=existing_review.review_id)` | POST (with `_method='PUT'`) | CSRF token, `_method`, rating/comment | Provides Cancel link to `resources.detail#reviews`. |
| admin/dashboard.html | Bulk booking approvals toolbar | `url_for('admin.bulk_booking_approvals')` | POST | CSRF token, `booking_ids[]`, hidden `action` (`approve`/`reject`) | Buttons set `data-bulk-action`. |
| admin/dashboard.html | Flagged review “Unhide” | `url_for('reviews.unhide', review_id=review.review_id)` | POST | CSRF token | Restores visibility. |
| admin/dashboard.html | “View” flagged resource link | `url_for('resources.detail', resource_id=review.resource_id)` | GET | `resource_id` | Opens offending resource in new tab. |
| admin/users.html | User filter form | `url_for('admin.users')` | GET | `search`, `role`, `status` | Applies query parameters for filtering table. |
| admin/users.html | Bulk user update form | `url_for('admin.bulk_update_users')` | POST | CSRF token, `user_ids[]`, hidden `action` (`activate`/`suspend`) | Buttons set action before submit. |
| admin/users.html | Inline “Suspend” form | `url_for('admin.suspend_user', user_id=user.user_id)` | POST | CSRF token | Includes confirm prompt in template. |
| admin/users.html | Inline “Activate” form | `url_for('admin.activate_user', user_id=user.user_id)` | POST | CSRF token | For previously suspended users. |
| admin/users.html | “View details” icon | `url_for('admin.user_detail', user_id=user.user_id)` | GET | `user_id` | Navigates to detail page. |
| admin/user_detail.html | “Back to Users” link | `url_for('admin.users')` | GET | — | Returns to listing. |
| admin/user_detail.html | Activate user form | `url_for('admin.activate_user', user_id=user.user_id)` | POST | CSRF token | Rendered when account inactive. |
| admin/user_detail.html | Suspend user form (modal) | `url_for('admin.suspend_user', user_id=user.user_id)` | POST | CSRF token | Triggered from suspend modal. |
| admin/user_detail.html | Delete user form (modal) | `url_for('admin.delete_user', user_id=user.user_id)` | POST | CSRF token | Permanently removes account. |
| admin/analytics.html | Reporting period selector | `url_for('admin.analytics')` | GET | `period` (7/30/90) | `<select>` auto-submits on change. |
| concierge/index.html | Concierge query form (`#concierge-form`) | Fetch to `url_for('concierge.query')` | POST (AJAX, JSON) | Body `{ query }`, header `X-CSRFToken` | JS intercepts submit; no traditional action attribute. |
| concierge/index.html | “Browse all resources” link | `url_for('resources.index')` | GET | — | Appears when no AI matches. |
| components/booking_drawer.html | Quick booking form (`data-booking-form`) | JS uses `data-booking-url` / `data-availability-url` from triggering button | POST (AJAX) then redirect | Resource + slot metadata | Drawer orchestrates slot selection before redirecting to `bookings.new`. |
| messages/inbox.html | Attachment trigger (`data-attach-trigger`) | — | — | — | Client-side only (no server call). |
| components/pagination.html | Generated page links | `url_pattern.format(page)` | GET | `page` placeholder | Macro consumers supply pattern (e.g., `/resources?page={}`). |
| errors/401/403/404/500.html | “Go to Dashboard” buttons | `url_for('resources.dashboard')` | GET | — | Provides escape hatch from error views. |
