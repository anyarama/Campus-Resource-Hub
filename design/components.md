# Campus Resource Hub — Component Patterns

Each component summary captures variants, interaction states, sizing, and icon usage observed in both design seeds.

## Button

### Admin seed (`src/components/IUButton.tsx`)
- Variants: `primary`, `secondary`, `ghost`, `destructive`; all lean on IU token classes (`bg-iu-crimson`, `border-iu`, `bg-[var(--iu-danger)]`).
- Sizes: `sm` (36px min height, `px-3 py-1.5`), `md` (44px, `px-4 py-2.5`), `lg` (48px, `px-6 py-3`).
- States: loading state injects `Loader2` spinner; `disabled` applies `opacity-50` and prevents pointer events; `focus-visible` outlines use `var(--iu-focus)`.
- Icon treatment: inline icons share `gap-2`; spinner inherits `w-4 h-4`.

### Auth seed (`src/components/ui/button.tsx`)
- Built with `class-variance-authority`; variants include `default`, `destructive`, `outline`, `secondary`, `ghost`, `link`.
- Sizes: `sm`, `default`, `lg`, `icon`; padding adjusts (`px-3`, `px-4`, `px-6`) with height tokens (32–40px) and icon-specific square layout.
- States: `aria-invalid` drives red ring, `disabled` sets opacity/pointer rules, focus-visible ring inherits `--ring` token; hover states lighten/darken backgrounds per variant.
- Icons: any nested `svg` auto-size to `1rem` unless overridden, ensuring alignment.

## Input

### Admin seed (`src/components/IUInput.tsx`, `FormControls.tsx`)
- Text input/textarea/select share wrapper with `gap-1.5` between label and control, helper text sits at `mt-1.5`.
- Controls default to `min-h-[44px]`, `px-3`, `rounded-[var(--radius-md)]`, and toggle between focus border `var(--iu-focus)` or error border `var(--iu-danger)`; helper/error IDs for accessibility.
- `FormControls` extends patterns with `size` prop (`sm`=40px, `md`=44px, `lg`=48px), `helperText`, `disabled` styling, icon affordances (embedded `Calendar`, `Clock`, `Search`).
- Error state applies `focus:ring` tinted at 20%, disabled state swaps to muted surface.

### Auth seed (`src/components/ui/input.tsx`)
- Single input primitive with consistent `h-9`, `rounded-md`, `border-input`; uses CSS vars `bg-input-background`, `--ring` for focus.
- File inputs share styling through `::file-selector-button` rules; `aria-invalid` toggles destructive border/ring automatically.
- Paired with `Form` primitives for labels/messages.

## Select

### Admin seed (`IUSelect`, `Combobox` in `FormControls.tsx`)
- Native `<select>` shares same styling as text inputs; options array passed via props.
- Combobox pattern uses custom popover: search input with `Search` icon, scrollable option list with selected state (accent background + `text-role-accent`).
- States: `disabled`, `error`, focus ring, and helper messaging use same wrappers as inputs.

### Auth seed (`src/components/ui/select.tsx`)
- Radix Select with `Trigger`, `Content`, `Item`, `Group`; sizes `default`/`sm` adjust heights.
- Icons: `ChevronDownIcon`, `ChevronUpIcon`, `CheckIcon` signal open state and selection.
- States: `data-[placeholder]` styling for muted text, `aria-invalid` reuses destructive border/ring, disabled prevents pointer events, focus-visible ring uses `--ring`.
- Content uses popper positioning with animated entrance/exit tokens.

## Card

### Admin seed (`IUCard.tsx`)
- Base card uses `bg-iu-surface`, `rounded-[var(--radius-lg)]`, `shadow-iu-sm`, `border-iu`.
- Padding options `none`, `sm (16px)`, `md (24px)`, `lg (32px)`; header/content subcomponents manage spacing (`mb-4`).

### Auth seed (`src/components/ui/card.tsx`)
- Card is flex column with `gap-6`, `rounded-xl`, `border`, `bg-card`; header uses CSS container queries to align action slots, padding standardized to `px-6 pt-6` with optional `.border-b` support.
- Footer + content add `px-6` + `pb-6`, ensuring consistent vertical rhythm.

## Navbar

### Admin seed (`Topbar.tsx`)
- Combines breadcrumbs, page title, search input (320px default), notification menu, theme toggle, avatar dropdown.
- Spacing: `px-5 py-4`, `gap-4`; breadcrumbs `admin-small` typography with `ChevronRight` separators.
- States: sticky top with `border-b`, search focus uses `var(--iu-focus)` ring, notifications render dropdowns with read/unread styling, toggles rely on `focus-visible` outlines.

### Auth seed (`components/ui/navigation-menu.tsx`)
- Radix Navigation Menu supporting triggers, dropdown content, viewport animations.
- Trigger states respond to `data-[state=open]`, focus-visible ring `--ring`; icons (`ChevronDownIcon`) rotate on open.
- Menu links are rounded, gap-based, allow description + icon stacking.

## Sidebar / Topbar Framework

### Admin seed (`Sidebar.tsx`)
- Widths: expanded `240px`, collapsed `72px`; `density` prop toggles padding/gap (`py-2.5` vs `py-2`).
- Features multi-level nav with collapsible Admin section, tooltip support when collapsed, `ChevronRight` rotation for nested lists.
- States: active item displays crimson pill indicator + `bg-[var(--iu-crimson)]/5`, tooltips track pointer position, keyboard `Escape` closes tooltip.

### Auth seed (`components/ui/sidebar.tsx`)
- Context provider manages expanded/collapsed/off-canvas states, storing preference via cookie and keyboard shortcut (`⌘/Ctrl + B`).
- Breakpoints: mobile variant renders within `Sheet`; widths `--sidebar-width` (16rem) and icon rail `3rem` tokens.
- Includes subcomponents (`SidebarHeader`, `SidebarGroup`, `SidebarTrigger`, `SidebarRail`) with tooltip support for icon mode, form search slot, skeleton placeholders.

## Modal

### Admin seed (`Modal.tsx` + `ConfirmationModal`)
- Sizes: `sm` (480px), `md` (640px), `lg` (800px) via utility map; includes focus trap, ESC + backdrop dismissal toggles, body scroll lock.
- Header with title + `X` icon button, body `p-6`, optional footer for actions; `ConfirmationModal` maps action types to icons (`CheckCircle`, `AlertCircle`, etc.) and semantic colors.
- Backdrop uses `bg-black/50`; content inherits `rounded-token-lg`, `shadow-iu-xl`.

### Auth seed (`components/ui/dialog.tsx`, `alert-dialog.tsx`)
- Radix Dialog with overlay fade/zoom animations, content centered with max width `calc(100% - 2rem)` and default `sm:max-w-lg`.
- Close button sits `top-4 right-4` and uses focus ring tokens; `DialogHeader/Footer` provide standard stacking.
- Alert dialog variant includes destructive emphasis and action stack for confirmations.

## Table

### Admin seed (`AdminTable.tsx`)
- Composition: `AdminTable`, `AdminTableHeader/Body/Row/Cell`; density prop toggles row heights (comfortable 56px, compact 44px) and padding (16px vs 12px).
- Rows highlight on hover, `TableDensityToggle` component allows user switching with pill buttons.
- Typography uses `admin-small`/`admin-caption` tokens for cells.

### Auth seed (`components/ui/table.tsx`)
- Lightweight wrappers: `Table`, `TableHeader`, `TableBody`, etc. with utility classes for hover/selected states.
- `TableRow` uses `data-[state=selected]` to apply muted background; supports checkboxes via `[role=checkbox]` selectors for padding adjustments.
- `TableFooter` adds `bg-muted/50` and `font-medium` to summary rows.

## Tabs

### Admin seed (`components/ui/ch-tabs.tsx` & usage in pages)
- Tab list renders inline buttons with `border-b-2`; active tab uses crimson border + text, optional `CHBadge` count chips.
- Supports controlled/uncontrolled state; content wrapper only renders matching value with fade-in animation.
- Sticky implementations (e.g., MyBookings) pair tabs with counts for statuses (Upcoming, Pending, Past, Cancelled) and incorporate horizontal scroll on mobile.

### Auth seed (`components/ui/tabs.tsx`)
- Radix Tabs with `.TabsList` pill rail, `.TabsTrigger` toggles `data-[state=active]` backgrounds, `.TabsContent` becomes flex child.
- Focus-visible ring and disabled states handled automatically; triggers support inline icons (`svg` sized to `1rem`).

## Toast

### Admin seed (`components/ui/ch-toast.tsx`)
- Variants: `success`, `error`, `info`, `warning`; each displays leading icon (`CheckCircle2`, `AlertCircle`, `Info`, `AlertTriangle`) tinted via semantic tokens.
- Layout: border-left accent, `p-4`, `gap-3`, `rounded-md`, optional close button with `X` icon.
- `CHToastContainer` anchors stack at `top-4 right-4 z-50` with `gap-2`.

### Auth seed (`components/ui/sonner.tsx`)
- Wraps `sonner` Toaster, piping theme from `next-themes`; CSS vars map to popover/background tokens so toast colors auto-sync with light/dark mode.
- Supports `toast.success/error/info` APIs with progress + action slots out of the box.

## FormGroup / Form System

### Admin seed (`FieldWrapper` + `FormControls.tsx`)
- `FieldWrapper` standardizes label, helper/error text spacing (`gap-2`, helper at `mt-1.5`), and required asterisk styling.
- Complex controls (date picker, time picker, multi-select, combobox) reuse base class generator ensuring consistent border, focus rings, disabled opacity, and icon padding.
- Accessibility: each helper/error message receives `aria-describedby` IDs and error `role="alert"`.

### Auth seed (`components/ui/form.tsx`)
- React Hook Form helpers: `Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormDescription`, `FormMessage` manage context/IDs.
- `useFormField` wires `aria` attributes automatically, `FormLabel` toggles destructive color when `error` exists.
- Grid-based form rows (`FormItem` uses `display: grid; gap: 0.5rem`) keep spacing consistent across inputs, selects, checkboxes.

These patterns should guide the consolidated UI system so tokens, layout primitives, and new SCSS layers can faithfully represent how each component is already implemented in both source applications.
