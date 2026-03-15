# Portfolio Redesign — Bold Technical

**Date:** 2026-03-15
**Status:** Approved
**Subject:** Complete redesign of Abdul Gaffar Shaikh's portfolio website

## Overview

Rebuild the existing single-page portfolio HTML from an editorial-minimal warm design to a **Bold Technical** aesthetic — dark-first, high-contrast, with neon accent colors on deep navy. The site remains a single self-contained HTML file with no build tools or framework dependencies.

## Design Direction

**Bold Technical** — dark mode as the default experience, with a polished light mode alternate. Terminal-meets-design-studio aesthetic. Grid-line background pattern. Glowing accents. The content (career achievements, quantified impact) stays front and center — the design amplifies it without distracting.

## Color System

### Dark Mode (Default)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0a0f1a` | Page background |
| `--surface` | `#0e1424` | Cards, elevated surfaces |
| `--ink` | `#e8edf5` | Primary text |
| `--ink2` | `#8a9bb0` | Secondary/body text (bumped from `#7b8da4` for better WCAG AA contrast) |
| `--border` | `#1a2235` | Card borders, dividers |
| `--mint` | `#63e6be` | Primary accent — nav, headings, links, active timeline |
| `--amber` | `#fbbf24` | Secondary accent — org names, certs, "hot" tags |
| `--violet` | `#a78bfa` | Tertiary accent — AI/MCP highlights, CTA hover |

### Light Mode (Alternate)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#f4f7fa` | Page background |
| `--surface` | `#ffffff` | Cards, elevated surfaces |
| `--ink` | `#0a0f1a` | Primary text |
| `--ink2` | `#5a6b7a` | Secondary/body text |
| `--border` | `#dde3ea` | Card borders, dividers |
| `--mint` | `#0d9373` | Primary accent (darker for contrast on white) |
| `--amber` | `#a07008` | Secondary accent |
| `--violet` | `#6d4bc8` | Tertiary accent |

### Background Treatment

- Grid-line pattern: `linear-gradient` creating a subtle grid overlay
  - Dark: `rgba(99,230,190,0.04)` grid lines
  - Light: `rgba(10,15,26,0.04)` grid lines
  - Grid size: `32px × 32px`
- Hero section: subtle radial glow in top-right corner (dark mode only), mint-tinted

## Typography

All fonts loaded from Google Fonts with `display=swap` to avoid FOIT.

**Migration from current site:** Syne (headings) → Space Grotesk; Lora (body) → Inter. JetBrains Mono retained. Syne and Lora removed from Google Fonts import.

| Role | Font Family | Weights | Usage |
|------|-------------|---------|-------|
| Headings | Space Grotesk | 700 | h1, h2, section titles, card titles, timeline titles |
| Body | Inter | 300, 400, 500 | Paragraphs, tagline, bullet items, descriptions |
| Code/Labels | JetBrains Mono | 300, 400, 500 | Eyebrows, tech tags, cert badges, contact links, nav labels, period dates |

### Type Scale

- Hero name: `clamp(2.8rem, 7.5vw, 6rem)`, weight 700, uppercase, letter-spacing `-0.04em` (tightened from current `-0.03em` to suit Space Grotesk's geometry)
- Section labels: `10px`, weight 500, letter-spacing `0.28em`, uppercase
- Timeline title: `1.3rem`, weight 700
- Body text: `0.93rem`, line-height `1.7`
- Tags/badges: `10px`, letter-spacing `0.04em`

## Page Sections

### 1. Hero (full viewport)

- Eyebrow: monospace label with glowing status dot (pulsing animation). **Migration note:** replaces the current `::before` horizontal line decoration with a dot to match the technical aesthetic.
- Name: large uppercase Space Grotesk, accent color on last name
- Tagline: Inter light weight, italic style removed (doesn't fit the technical vibe)
- Tech chips: monospace tags with colored borders — mint for standard, amber for "hot" (AI-related)
- Contact row: email (JS-assembled, no Cloudflare dependency), LinkedIn, GitHub, phone
- Scroll hint: auto-hides after first scroll event, does not reappear on scroll-back-to-top

### 2. Career Timeline

- Vertical spine: SVG `<path>` absolutely positioned inside `.timeline` container. Height matches container height via JS on load/resize. Uses `stroke-dasharray` equal to path length, with `stroke-dashoffset` driven by scroll position (calculated from timeline container's top/bottom viewport intersection). On fast scroll, the draw catches up smoothly via CSS `transition: stroke-dashoffset 0.15s`.
- Timeline dots: circular, `18px`, current role has glowing mint ring (`box-shadow` + `@keyframes` pulse). **Note:** CSS `@property` was considered for the pulse but dropped in favor of a standard `@keyframes box-shadow` animation for broader browser compatibility (Firefox < 128 lacks `@property` support).
- Each entry: period (monospace) → title (Space Grotesk) → org (monospace, amber) → card
- Cards: surface background, border, left accent bar on hover (3px mint), hover lifts with subtle shadow
- Tech tags inside each card, color-coded: mint (default), amber (infra/devops), violet (AI/ML). **Migration note:** current site's `.green` / `--sage` tags (LangChain, LangGraph, ChromaDB, MCP) map to violet in the new scheme.
- Education entry (B.E., VESIT) is a card-less terminal node — period, title, org only, no card or bullet points
- Entries animate in on scroll: fade + translateY, staggered timing

### 3. Strategic Impact

- Grid: `repeat(auto-fill, minmax(300px, 1fr))`
- Impact cards: icon + title + body, mint border, hover lifts with shadow
- Animate in on scroll

### 4. Core Capabilities

- Grid: `repeat(auto-fill, minmax(280px, 1fr))`
- Skill blocks: icon → name (with experience badge in monospace) → description
- Hover: border shifts to mint, subtle lift
- Background: slightly different surface tone for visual separation
- Animate in on scroll

### 5. Certifications

- Vertical stack of cert rows
- Each row: badge (monospace, amber background tint) → cert name → year
- Hover: amber border highlight

### 6. CTA (Call to Action)

- Centered layout, max-width `560px`
- Section eyebrow + heading with accent color on key word
- Email button: solid mint background, white text
- LinkedIn button: outlined, mint border
- All inline styles from current site extracted into proper CSS classes

### 7. Footer

- Flex row: name + meta info on left, year on right
- Surface background, top border

## Animations & Interactions

### Scroll-Driven

| Element | Animation | Trigger |
|---------|-----------|---------|
| Timeline spine | SVG path draws downward | Scroll position via Intersection Observer |
| Timeline entries | `fadeUp` (opacity 0→1, translateY 20px→0) | Entry enters viewport, staggered 100ms per entry |
| Impact cards | `fadeUp` | Card enters viewport |
| Skill blocks | `fadeUp` | Block enters viewport |
| Cert rows | `fadeUp` | Row enters viewport |

### CSS Animations

| Element | Animation | Implementation |
|---------|-----------|----------------|
| Current timeline dot | Pulsing glow ring | `@keyframes` with `box-shadow` oscillation |
| Status dot (hero eyebrow) | Subtle pulse | Same approach, smaller scale |
| Scroll hint | Auto-hide on first scroll | JS `scroll` event listener, `opacity` transition |
| Hero elements | Staggered fadeUp on load | Same as current site, adapted timing |

### Hover States

- Cards: `translateY(-2px)`, `box-shadow` increase, border-color shift to accent
- Timeline entries: left accent bar appears on card, dot shifts to mint
- Chips/tags: border-color and text-color shift to accent
- Contact links: color shift to mint
- CTA buttons: opacity shift (solid), background tint (outline)

### Canvas 2D Particle Field

- Lightweight floating particles in background for depth
- ~30-40 particles, slow drift, very low opacity (`0.03-0.08`)
- Responds to dark/light mode (mint-tinted in dark, neutral in light)
- Renders on a fixed-position canvas behind all content
- ~50 lines of JS, zero dependencies
- Disabled on `prefers-reduced-motion: reduce`
- Also disabled on viewports below `768px` to preserve mobile battery life

## New Features

### Dark/Light Mode Toggle

- Small toggle button, top-right corner (fixed position)
- Icon switches between sun/moon SVG
- On click: toggles `data-theme="light"` attribute on `<html>`
- CSS uses `[data-theme="light"]` selectors to override custom properties
- Respects `prefers-color-scheme` on first load
- Persists user choice in `localStorage` (wrapped in `try/catch` for private browsing compatibility)
- Transition: `*, *::before, *::after { transition: background-color 0.3s, color 0.3s, border-color 0.3s; }` applied briefly during toggle, then removed to avoid interfering with hover transitions
- **Accessibility:** `aria-label="Switch to light mode"` / `"Switch to dark mode"` (updates on toggle), `role="button"`, `tabindex="0"`, keyboard support (`Enter`/`Space`)

### Mobile Navigation

- Nav dots hidden on mobile (existing behavior)
- Replaced with a floating bottom pill bar
- Shows section names in abbreviated form
- Fixed position, `bottom: 16px`, centered
- Semi-transparent background with backdrop blur
- Active section highlighted
- Class name: `.mobile-nav`
- Same Intersection Observer drives both nav dots (desktop) and pill bar (mobile)
- Breakpoint: `768px`
- **Accessibility:** wrapped in `<nav aria-label="Page sections">` (shared with desktop nav dots — only one renders per viewport), pills have `role="button"`, `tabindex="0"`, keyboard support

### Print Stylesheet

```css
@media print {
  /* Hide non-essential elements */
  .nav-dots, .mobile-nav, .scroll-hint, .theme-toggle,
  #cta, canvas, .nav-dot { display: none; }

  /* Reset to printable styles */
  body { background: white; color: black; }
  * { animation: none !important; transition: none !important; }

  /* Tighten spacing */
  header, section { padding: 24px 0; min-height: auto; }

  /* Force readable colors */
  h1, .tl-title, .skill-name, .impact-card-title { color: black; }
  .tl-items li, .skill-desc, .impact-card-body { color: #333; }
}
```

### Back to Top

- Appears after scrolling past hero section
- Small fixed button, bottom-right (above mobile nav on small screens)
- Smooth scroll to top on click
- Fade in/out based on scroll position
- **Accessibility:** `aria-label="Back to top"`, `role="button"`, `tabindex="0"`, keyboard support (`Enter`/`Space`)

## Semantic HTML

- Wrap all content sections (timeline through footer) in `<main id="main-content">`
- Retain `<html lang="en">`
- `<header>` for hero, `<section>` for each content section, `<footer>` for footer (matches current structure)

## Accessibility

- `<nav aria-label="Page sections">` wrapping nav dots (desktop) and mobile pill bar (only one rendered per viewport)
- Each nav dot / pill: `role="button"`, `tabindex="0"`, `aria-label="Navigate to [section]"`
- Keyboard handler: `Enter` and `Space` trigger navigation on all interactive elements (nav dots, pills, theme toggle, back-to-top)
- `aria-hidden="true"` on all decorative SVGs (contact icons, etc.)
- Skip-to-content link: visually hidden, visible on focus, links to `#main-content`
- Visible focus outlines on all interactive elements (`:focus-visible`)
- `prefers-reduced-motion: reduce` — disables all scroll animations, particle field, and pulsing effects
- All text meets WCAG AA contrast ratios against their backgrounds
- Theme toggle and back-to-top button accessibility detailed in their respective feature sections above

## Fixes from Current Site

1. **Remove Cloudflare dependency** — replace `email-decode.min.js` and `__cf_email__` with consistent JS email assembly (as CTA already does)
2. **Fix truncated script** — rewrite the Intersection Observer for nav dot highlighting (currently cut off mid-string)
3. **Remove dead CSS** — delete `impact-strip`, `impact-grid`, `impact-item`, `impact-label` styles (~50 lines marked "legacy, unused")
4. **Extract inline styles** — CTA section (lines 890-898) has heavy inline styles; move to CSS classes
5. **Add meta tags** — `<meta name="description">`, Open Graph (`og:title`, `og:description`, `og:type`), Twitter card
6. **Add favicon** — inline SVG favicon in `<head>` (single `<link>` tag)
7. **Add `rel="noopener"`** — to all external links (LinkedIn, GitHub). Using `noopener` only (not `noreferrer`) to preserve referrer for LinkedIn analytics.
8. **Fix email link** — header email should use same JS assembly pattern as CTA

## File Structure

Single file: `abdul-portfolio.html` — all CSS inline in `<style>`, all JS inline in `<script>`. No external dependencies beyond Google Fonts CDN.

## Out of Scope

- Three.js or any WebGL — decided against during brainstorming (payload, mobile, accessibility concerns)
- React or any framework — single HTML file approach is a feature
- Backend/hosting infrastructure — this is a static file
- Text content changes — all text content remains identical to current site. Visual styling changes (font swap, italic removal, letter-spacing adjustments) are in scope and documented above.
- Navigation does not include a CTA dot/pill — CTA is a destination section but not a navigation target (it's always visible by scrolling past certs)
