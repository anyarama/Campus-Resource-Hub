# Campus Resource Hub — Design Tokens

_Source seeds: `Campus_Resource_hub/src/styles/globals.css`, `Campus_Resource_hub_login/src/styles/globals.css`._

## Colors

### Brand & Neutrals
| Token | Value | Notes |
| --- | --- | --- |
| `--color-brand-crimson-600` | `#990000` | Primary IU crimson used for CTAs, indicators, and active nav items. |
| `--color-brand-crimson-700` | `#7A0000` | Darker crimson for hover/dark surfaces. |
| `--color-brand-crimson-500` | `#B71C1C` | Lighter crimson for light backgrounds and destructive focus. |
| `--color-brand-cream-200` | `#F9F7F6` | Canvas background. |
| `--color-brand-cream-100` | `#FBFAF9` | Card & panel surface. |
| `--color-brand-cream-300` | `#F5F3F0` | Hover/subtle fills. |
| `--color-brand-cream-400` | `#EEDEDB` | Accent cream + legacy surfaces. |
| `--color-brand-black` | `#000000` | True black for icons/logos. |
| `--color-brand-white` | `#FFFFFF` | Base white + text inverse. |

### Text & Border
| Token | Value | Notes |
| --- | --- | --- |
| `--color-text-primary` | `#1E1E1E` | Default body + heading color. |
| `--color-text-secondary` | `#6E6E6E` | Secondary labels and muted metadata. |
| `--color-text-tertiary` | `#9E9E9E` | Subtle helper text. |
| `--color-text-inverse` | `#FFFFFF` | Text on crimson/ink backgrounds. |
| `--color-border-default` | `#E9E4DD` | Standard card + input borders. |
| `--color-border-muted` | `#EEE9E3` | Dividers + subtle outlines. |
| `--color-border-strong` | `#D4CFC4` | Hover state + emphasis borders. |
| `--color-border-focus` | `rgba(153, 0, 0, 0.3)` | Halo applied on focus-visible. |

### Surfaces & Overlays
| Token | Value | Notes |
| --- | --- | --- |
| `--color-surface-canvas` | `var(--color-brand-cream-200)` | Application background. |
| `--color-surface-card` | `var(--color-brand-cream-100)` | Cards/forms. |
| `--color-surface-muted` | `#F1EFEC` | Muted blocks, filters, subtle tags. |
| `--color-surface-hover` | `var(--color-brand-cream-300)` | Hover states for cards/inputs. |
| `--color-surface-elevated` | `var(--color-brand-white)` | Modals, popovers. |
| `--color-surface-backdrop` | `rgba(0, 0, 0, 0.5)` | Modal scrim/overlay. |

### Semantic & Accent
| Token | Value | Notes |
| --- | --- | --- |
| `--color-success-600` | `#1B5E20` | Success text/icons. |
| `--color-success-400` | `#43A047` | Hover + emphasis success tone. |
| `--color-success-100` | `#E8F5E9` | Success background. |
| `--color-danger-600` | `#B71C1C` | Destructive text/icons. |
| `--color-danger-400` | `#EF5350` | Hover state for destructive actions. |
| `--color-danger-100` | `#FFEBEE` | Error background. |
| `--color-warning-600` | `#8A5A00` | Warnings/amber alerts. |
| `--color-warning-400` | `#E65100` | Toasts + info banners (auth seed). |
| `--color-warning-100` | `#FFF4E0` | Warning background. |
| `--color-info-600` | `#0B5CAD` | Informational pills + links. |
| `--color-info-100` | `#E3F2FD` | Info background + highlights. |

### Data Visualization Palette
| Token | Value |
| --- | --- |
| `--chart-color-1` | `#990000` |
| `--chart-color-2` | `#B53A3A` |
| `--chart-color-3` | `#D56A6A` |
| `--chart-color-4` | `#F0A5A5` |
| `--chart-color-5` | `#6B7280` |
| `--chart-color-6` | `#A1A1AA` |

### Dark Theme Overrides
| Token | Dark Value | Notes |
| --- | --- | --- |
| `--color-text-primary` | `#F5F5F5` | Light text. |
| `--color-text-secondary` | `#B8B8B8` | Secondary text. |
| `--color-surface-canvas` | `#0F0F0F` | App background. |
| `--color-surface-card` | `#1A1A1A` | Panels/cards. |
| `--color-surface-muted` | `#242424` | Muted modules. |
| `--color-border-default` | `#2F2F2F` | Standard border. |
| `--color-border-muted` | `#262626` | Subtle separators. |
| `--color-brand-crimson-600` | `#E63946` | Lighter crimson for contrast. |
| `--color-success-600` | `#4ADE80` | Bright success text. |
| `--color-success-100` | `#1A3A26` | Dark success fill. |
| `--color-danger-600` | `#EF4444` | Danger text. |
| `--color-danger-100` | `#3A1F1F` | Dark error fill. |
| `--color-warning-600` | `#FBBF24` | Warning text. |
| `--color-warning-100` | `#3A3020` | Warning fill. |
| `--color-info-600` | `#60A5FA` | Info text. |
| `--color-info-100` | `#1F2937` | Info fill. |
| `--shadow-sm/md/lg` | Higher opacity versions from admin seed for visibility. |

## Typography

### Families & Weights
- `--font-family-sans`: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- `--font-family-mono`: `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`
- Weights: `--font-weight-regular: 400`, `--font-weight-medium: 500`, `--font-weight-semibold: 600`

### Scale (px)
| Token | Size / Line Height | Weight | Letter Spacing | Usage |
| --- | --- | --- | --- | --- |
| `--font-size-display` | `40 / 48` | 600 | `-0.2px` | Hero metrics, dashboards. |
| `--font-size-h1` | `32 / 40` | 600 | `-0.2px` | Page titles. |
| `--font-size-h2` | `24 / 32` | 600 | `-0.2px` | Section headers. |
| `--font-size-h3` | `20 / 28` | 600 | `0px` | Card titles. |
| `--font-size-h4` | `18 / 24` | 600 | `0px` | Subheads + widget titles. |
| `--font-size-label` | `14 / 20` | 600 | `0px` | Form labels. |
| `--font-size-body` | `15 / 24` | 400 | `0px` | Default copy (admin seed). |
| `--font-size-body-strong` | `15 / 24` | 600 | `0px` | Emphasis text. |
| `--font-size-caption` | `13 / 18` | 400 | `0px` | Helper text + metadata. |
| `--font-size-caption-strong` | `13 / 18` | 600 | `0px` | Badge counters. |
| `--font-size-micro` | `12 / 16` | 400 | `0px` | Table footers, chips. |
| `--font-size-micro-strong` | `12 / 16` | 600 | `0px` | Micro labels. |

## Spacing & Density

### Core Scale (4pt grid)
| Token | Value |
| --- | --- |
| `--space-0` | `0px` |
| `--space-1` | `4px` |
| `--space-2` | `8px` |
| `--space-3` | `12px` |
| `--space-4` | `16px` |
| `--space-5` | `20px` |
| `--space-6` | `24px` |
| `--space-7` | `28px` |
| `--space-8` | `32px` |
| `--space-10` | `40px` |
| `--space-12` | `48px` |
| `--space-16` | `64px` |
| `--section-spacing` | `24px` | Default vertical rhythm between sections. |

### Component Density
| Token | Value | Notes |
| --- | --- | --- |
| `--control-height-sm` | `40px` | Form controls / buttons. |
| `--control-height-md` | `44px` | Default control height. |
| `--control-height-lg` | `48px` | Spacious controls. |
| `--table-row-height-comfortable` | `56px` | Admin table default. |
| `--table-row-height-compact` | `44px` | Dense data tables. |
| `--table-cell-padding-comfortable` | `16px` | Horizontal padding. |
| `--table-cell-padding-compact` | `12px` | Compact tables. |
| `--card-padding-comfortable` | `20px` | Card interior padding. |
| `--card-padding-compact` | `16px` | Dense cards. |

## Radii & Shadows

### Border Radius
| Token | Value | Usage |
| --- | --- | --- |
| `--radius-sm` | `8px` | Chips, inputs, compact buttons. |
| `--radius-md` | `12px` | Default control radius. |
| `--radius-lg` | `16px` | Cards, modals. |
| `--radius-xl` | `20px` | Large surfaces & pills. |
| `--radius-full` | `9999px` | Pills, avatars, toggles. |

### Elevation
| Token | Value |
| --- | --- |
| `--shadow-xs` | `0 1px 2px rgba(0, 0, 0, 0.04)` |
| `--shadow-sm` | `0 1px 0 rgba(0, 0, 0, 0.02), 0 1px 2px rgba(0, 0, 0, 0.06)` |
| `--shadow-md` | `0 2px 4px rgba(0, 0, 0, 0.08), 0 4px 8px rgba(0, 0, 0, 0.04)` |
| `--shadow-lg` | `0 4px 8px rgba(0, 0, 0, 0.10), 0 8px 16px rgba(0, 0, 0, 0.06)` |
| `--shadow-xl` | `0 20px 25px rgba(0, 0, 0, 0.08), 0 8px 10px rgba(0, 0, 0, 0.04)` |
| `--shadow-card` | `var(--shadow-sm)` |

## Layout Metrics

### Breakpoints & Containers
| Token | Value | Notes |
| --- | --- | --- |
| `--layout-breakpoint-xl` | `1440px` | Desktop frame width. |
| `--layout-breakpoint-lg` | `1280px` | Content max width. |
| `--layout-breakpoint-md` | `1024px` | Tablet frame. |
| `--layout-breakpoint-sm` | `768px` | Small tablet / large mobile. |
| `--layout-breakpoint-xs` | `480px` | Narrow mobile content. |
| `--layout-breakpoint-xxs` | `390px` | Seed mobile frame reference. |
| `--layout-max-width` | `1280px` | Page container width. |
| `--layout-content-width` | `min(100%, var(--layout-max-width))` | Standard container clamp. |

### Grid, Gutters & Navigation
| Token | Value | Notes |
| --- | --- | --- |
| `--layout-grid-columns` | `12` | Responsive grid. |
| `--layout-gutter-desktop` | `24px` | Default horizontal padding. |
| `--layout-gutter-tablet` | `16px` | Tablet padding. |
| `--layout-gutter-mobile` | `12px` | Mobile padding. |
| `--layout-page-margin-desktop` | `80px` | Space between shell + content. |
| `--layout-sidebar-expanded` | `240px` | Admin seed expanded width. |
| `--layout-sidebar-collapsed` | `72px` | Icon-only nav width. |
| `--layout-topbar-height` | `72px` | Approx. admin topbar block. |

## Motion & Focus

| Token | Value | Notes |
| --- | --- | --- |
| `--motion-duration-fast` | `150ms` | Quick hover states. |
| `--motion-duration-base` | `200ms` | Default transitions. |
| `--motion-duration-slow` | `300ms` | Modal overlays, drawers. |
| `--motion-duration-slower` | `400ms` | Auth seed staged transitions. |
| `--motion-ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | Shared easing curve. |
| `--focus-ring-width` | `2px` | Visible focus halo. |
| `--focus-ring-offset` | `2px` | Outer halo separation. |
| `--focus-ring-color` | `rgba(153, 0, 0, 0.8)` | Focus outline color. |
| `--focus-ring-outer` | `0 0 0 2px rgba(153, 0, 0, 0.18)` | Default box-shadow ring. |
| `--focus-ring-destructive` | `rgba(183, 28, 28, 0.2)` | Error focus ring base. |

These tokens should be mapped directly to CSS variables inside `ui-system/scss/_tokens.scss` so that the base reset, typography, and layout layers inherit a single source of truth used across the standardized UI.
