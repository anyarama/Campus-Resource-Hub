# Reconcile Plan — UX vs Backend
_Current routes already satisfy UX requirements; we can stay within the existing contract._

## Option A – Template-Level Alignment (Preferred)
1. **Dashboard CTA alignment**
   - Template: `src/templates/resources/dashboard.html`
   - Elements: “Book this resource”, “View booking options”, recent activity links
   - Action: ensure these buttons continue pointing to the original endpoints listed in `design/bindings_map.md` (`bookings.new`, `resources.availability`, `messages.compose`). No backend change needed.
   - File updates: only adjust template labels/btn styles; no route edits.

2. **Resources list filters and CTAs**
   - Template: `src/templates/resources/list.html`
   - Elements: search form, “My Resources”, “Create Resource”, filter drawer links
   - Action: confirm form `action` stays `resources.index` and CTA `href`s remain `resources.my_resources` / `resources.create`. If any UX copy needs to change, do so without altering endpoints.
   - Files: `resources/list.html`, optional SCSS tweaks under `ui-system/pages/resources-list.scss`.

3. **Admin users table actions**
   - Template: `src/templates/admin/users.html`
   - Elements: bulk action form, per-row suspend/activate forms, detail links
   - Action: keep form `action`s (`admin.bulk_update_users`, `admin.suspend_user`, `admin.activate_user`) as-is; simply update button classes/labels.
   - Files: `admin/users.html`, `ui-system/pages/admin-users.scss`.

No discrepancies require new routes, so Option B (adapter routes) is unnecessary at this stage.

## File Diff Summary (Option A)
1. `src/templates/resources/dashboard.html`
   - Replace inline-styled cards/tables with UI-system components while keeping existing `url_for` calls intact.
   - Remove hard-coded colors, move layout to `ui-system/pages/resources-dashboard.scss`.

2. `src/templates/resources/list.html`
   - Wrap header + toolbar with UI-system markup; ensure `form action` and CTA `href`s remain unchanged.
   - Introduce `ui-system/pages/resources-list.scss` for any layout adjustments.

3. `src/templates/admin/users.html`
   - Swap legacy class soup for UI-system cards/buttons/tables but keep all `url_for` references and form names untouched.
   - Style with `ui-system/pages/admin-users.scss`.

4. `src/app.py`
   - Ensure Flask’s Jinja loader includes the `ui-system` templates so `base.html` imports succeed (already done; retain).

5. `src/static/scss/pages/*.scss`
   - Add `@use` lines to pull in new UI-system page styles created above.

This plan preserves all backend routes/params while delivering the UX fidelity requested.
