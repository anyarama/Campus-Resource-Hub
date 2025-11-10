# UI Consistency – Phase D

The codemod (`scripts/codemods/normalize_templates.py`) was executed across the page templates to enforce the agreed enterprise UI conventions. The table below captures the verification snapshot for the highest-traffic templates.

| Page | base.html | tokens only | macros used | grid ok | icons ok | dark ok | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `resources/list.html` | Yes | Yes | Yes (`_resource_card`) | Yes (`layout-col` w/ `data-col`) | Yes (Lucide) | Yes | Aligned |
| `resources/detail.html` | Yes | Yes | Partial (hero + review partials) | Yes | Yes | Yes | Minor polish (hero CTA macro gap) |
| `bookings/new.html` | Yes | Yes | Yes (form macros) | Yes | Yes | Yes | Aligned |
| `bookings/detail.html` | Yes | Yes | Partial (card + action buttons) | Yes | Yes | Yes | Needs follow-up on legacy `block content` |
| `admin/dashboard.html` | Yes | Yes | Yes (kpi/card macros) | Yes | Yes | Yes | Aligned |
| `admin/users.html` | Yes | Yes | Yes (bulk toolbar buttons) | Yes | Yes | Yes | Aligned |
| `messages/inbox.html` | Yes | Yes | Partial (message snippet include) | Yes | Yes | Yes | Needs follow-up for toast macro |
| `auth/login.html` | Yes | Yes | Yes (`form_field`, `button`) | Yes | Yes | Yes | Aligned |
| `concierge/index.html` | Yes | Yes | Partial (card grid) | Yes | Yes | Yes | Needs follow-up (drawer macro) |
| `errors/404.html` | Yes | Yes | N/A (static) | Yes | Yes | Yes | Aligned |

**Notes**
- “Tokens only” reflects the absence of raw hex color usage; the codemod replaced inline colors with IU design tokens.
- “Macros used” flags whether the template leverages the shared button/form/card/table helpers. “Partial” indicates further refactors are desirable but not blocking.
- “Grid ok” ensures `.layout-col` wrappers now expose the `data-col*` hints required by the responsive grid.
- “Icons ok” confirms every `<i>` element now uses either Lucide (`data-lucide`) or Bootstrap Icons (`bi`) with normalized sizing classes.
- Dark-mode parity relies on tokens/macros; templates listed as “Needs follow-up” still render correctly but would benefit from deeper macro adoption in a future sweep.
