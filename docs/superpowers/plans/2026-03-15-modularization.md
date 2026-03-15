# Portfolio Modularization — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `abdul-portfolio.html` (1319 lines) into `index.html` + `css/styles.css` + `js/script.js` + `data/data.json` — pixel-identical output, data-driven content rendering.

**Architecture:** JSON data file holds all content. HTML has empty containers. JS fetches JSON on load, renders all content into containers, then initializes interactive features. CSS is extracted verbatim. Old file kept as backup.

**Tech Stack:** Vanilla HTML/CSS/JS, JSON, `fetch` API, `defer` script loading

**Spec:** `docs/superpowers/specs/2026-03-15-modularization-design.md`

**Important:** All scripts use `defer` so DOM is ready. The `init()` function fetches data, renders, then initializes interactivity. No `DOMContentLoaded` wrappers needed.

---

## Chunk 1: Extract Data and CSS

### Task 1: Create `data/data.json`

**Files:**
- Create: `data/data.json`
- Reference: `abdul-portfolio.html` (source of all content)

- [ ] **Step 1: Create directory and write the complete JSON file**

Extract ALL content from `abdul-portfolio.html` into structured JSON. The JSON must contain every piece of text content currently hardcoded in the HTML. Use the schema from the spec exactly.

Key sections to extract:
- `meta`: title, description, ogTitle, ogDescription (from `<head>` meta tags, lines 6-9, 11)
- `hero`: name, accent, eyebrow, tagline, phone, email (split user/domain), linkedin, github (from lines 791-822)
- `chips`: array of `{label, hot}` objects (from lines 798-812)
- `timeline`: array of 5 entries, each with period, periodNow, title, org, client, currentBadge, bullets (array of HTML strings), tags (array of `{label, color}`) — from lines 843-956
- `impact`: array of 3 cards with icon, title, body (from lines 967-983)
- `skills`: array of 6 blocks with icon, name, badge (or null), desc (from lines 994-1028)
- `certs`: array of 6 rows with badge, name, year (from lines 1039-1084)
- `cta`: heading (HTML string with `<span>`), body text (from lines 1088-1089)
- `footer`: name, meta, year (from lines 1095-1098)

**CRITICAL:** Copy text content EXACTLY — do not paraphrase or modify any content. Bullet text contains inline HTML (`<strong>`, `&amp;`) — preserve it as-is in JSON strings.

For the email field, split into `{"user": "abdul219428", "domain": "gmail.com"}` for obfuscation.

SVG icons for contact links (email, linkedin, github, phone) should be stored as strings in the hero object or hardcoded in the render function since they're structural, not content. Recommendation: hardcode SVG paths in the render function — they're markup, not data.

- [ ] **Step 2: Validate JSON**

```bash
python -c "import json; json.load(open('data/data.json')); print('Valid JSON')"
```

- [ ] **Step 3: Commit**

```bash
git add data/data.json
git commit -m "feat: extract all portfolio content into data/data.json"
```

---

### Task 2: Create `css/styles.css`

**Files:**
- Create: `css/styles.css`
- Reference: `abdul-portfolio.html` lines 17-755 (everything inside `<style>` tags)

- [ ] **Step 1: Extract the entire CSS block**

Copy lines 17 through 755 of `abdul-portfolio.html` (everything between `<style>` and `</style>`) into `css/styles.css`. No modifications — verbatim extraction.

- [ ] **Step 2: Verify line count is approximately 740 lines**

```bash
wc -l css/styles.css
```

- [ ] **Step 3: Commit**

```bash
git add css/styles.css
git commit -m "feat: extract CSS into css/styles.css — verbatim, no changes"
```

---

## Chunk 2: Build HTML Skeleton and JS Renderer

### Task 3: Create `index.html`

**Files:**
- Create: `index.html`

- [ ] **Step 1: Write the complete HTML skeleton**

The file should contain:

**`<head>`:**
- Same meta charset, viewport
- Meta description, OG, Twitter with placeholder values (JS will update from data)
- `<title>` with placeholder (JS updates)
- Inline SVG favicon (same as current)
- Google Fonts preconnect + stylesheet link
- `<link rel="stylesheet" href="css/styles.css">`

**`<body>` — static structural elements (NOT rendered from data):**
- `<canvas id="particles" aria-hidden="true"></canvas>`
- `<a href="#main-content" class="skip-link">Skip to content</a>`
- `<nav class="nav-dots">` with 5 dots (same as current lines 764-770)
- `<nav class="mobile-nav">` with 5 pills (same as current lines 772-778)
- `<button class="theme-toggle">` with moon/sun SVGs (same as current lines 780-783)
- `<button class="back-to-top">` with chevron SVG (same as current lines 785-787)

**`<body>` — container elements (JS renders into these):**

```html
<header id="hero">
  <div id="hero-content"></div>
</header>

<div class="divider"></div>

<main id="main-content">

<section id="timeline">
  <div class="section-label">Career Timeline</div>
  <div class="timeline">
    <svg class="timeline-spine" aria-hidden="true"></svg>
    <div id="timeline-entries"></div>
  </div>
</section>

<div class="divider"></div>

<section id="impact">
  <div class="section-label">Strategic Impact</div>
  <div class="impact-grid-full" id="impact-cards"></div>
</section>

<div class="divider"></div>

<section id="skills">
  <div class="section-label">Core Capabilities</div>
  <div class="skills-grid" id="skills-grid"></div>
</section>

<div class="divider"></div>

<section id="certs">
  <div class="section-label">Certifications</div>
  <div class="certs-strip" id="certs-list"></div>
</section>

<div class="divider"></div>

<section id="cta" class="cta-section">
  <div class="cta-inner" id="cta-content"></div>
</section>

<footer id="footer-content"></footer>

</main>

<script src="js/script.js" defer></script>
```

Note: Section labels ("Career Timeline", "Strategic Impact", etc.) stay in HTML — they're structural, not content that changes. The `<div class="divider">` elements also stay.

- [ ] **Step 2: Verify the file is approximately 100-150 lines**

```bash
wc -l index.html
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: create index.html skeleton with container elements"
```

---

### Task 4: Create `js/script.js`

**Files:**
- Create: `js/script.js`
- Reference: `abdul-portfolio.html` lines 1102-1318 (all `<script>` content)
- Reference: `data/data.json` (schema for render functions)

- [ ] **Step 1: Write the main init function and all render functions**

```javascript
// ─── MAIN INIT ───
async function init() {
  const res = await fetch('data/data.json');
  const data = await res.json();

  renderMeta(data.meta);
  renderHero(data.hero, data.chips);
  renderTimeline(data.timeline);
  renderImpact(data.impact);
  renderSkills(data.skills);
  renderCerts(data.certs);
  renderCTA(data.cta, data.hero.email);
  renderFooter(data.footer);

  // Initialize interactive features AFTER content is rendered
  initNavigation();
  initThemeToggle();
  initBackToTop();
  initScrollReveal();
  initTimelineSpine();
  initParticles();
}
```

**Render functions — each populates a container element with HTML built from data:**

`renderMeta(meta)` — Updates `document.title` and meta tag content attributes.

`renderHero(hero, chips)` — Builds into `#hero-content`: eyebrow with status dot, h1 with accent span, tagline, chips (looping over chips array, applying `.hot` class), contact row with SVG icons (SVG paths hardcoded in this function — they're markup, not data), scroll hint. Assembles email from `hero.email.user` + `@` + `hero.email.domain` for the mailto link and display text. All elements get the same `fadeUp` animation CSS classes/styles as the current file.

`renderTimeline(entries)` — Builds into `#timeline-entries`: loops over entries array, creates `.tl-entry.reveal` for each. If `entry.currentBadge` is true, dot gets `.current` class. If `entry.periodNow` is true, wraps "Present" in `<span class="now">`. Renders bullets as `<li>` items (using `innerHTML` since bullets contain `<strong>` tags). Renders tech tags with color classes. Education entry (no bullets/tags) renders without a `.tl-card`.

`renderImpact(items)` — Builds into `#impact-cards`: loop over items, create `.impact-card.reveal` for each.

`renderSkills(items)` — Builds into `#skills-grid`: loop over items, create `.skill-block.reveal` for each. Badge is optional (rendered as `<span class="exp-badge">` if present).

`renderCerts(items)` — Builds into `#certs-list`: loop over items, create `.cert-row.reveal` for each.

`renderCTA(cta, email)` — Builds into `#cta-content`: section label (centered), h2 heading, paragraph, email button (assembled from email.user + email.domain) and LinkedIn button.

`renderFooter(footer)` — Builds into `#footer-content`: name div, meta div, year div. Note: the `<footer>` element itself exists in HTML — this function sets its `innerHTML`.

- [ ] **Step 2: Write all init functions (moved from current `<script>` block)**

Move each existing IIFE into a named function. The logic stays identical — just unwrapped from IIFEs since they'll be called by `init()` after rendering.

`initNavigation()` — Same as current lines 1232-1260. Click/keyboard handlers for `[data-target]` elements + IntersectionObserver for active section.

`initThemeToggle()` — Same as current lines 1262-1295. localStorage, prefers-color-scheme, toggle logic, aria-label sync.

`initBackToTop()` — Same as current lines 1297-1317. Scroll listener, scroll hint hide.

`initScrollReveal()` — Same as current lines 1113-1139. Staggered IntersectionObserver with `_staggerIndex`. Reduced motion check.

`initTimelineSpine()` — Same as current lines 1141-1180. SVG path draw on scroll. Reduced motion check.

`initParticles()` — Same as current lines 1182-1230. Canvas 2D, 35 particles, theme-aware, mobile-disabled.

- [ ] **Step 3: Add the boot call at the bottom**

```javascript
// ─── BOOT ───
init();
```

- [ ] **Step 4: Verify file is approximately 280 lines**

```bash
wc -l js/script.js
```

- [ ] **Step 5: Commit**

```bash
git add js/script.js
git commit -m "feat: create js/script.js — data rendering + all interactive features"
```

---

## Chunk 3: Verify and Clean Up

### Task 5: Test the modular version

**Files:**
- Reference: `index.html`, `css/styles.css`, `js/script.js`, `data/data.json`

- [ ] **Step 1: Start a local server and verify**

```bash
cd C:\Users\yoges\Downloads\Pervy-Resume && python -m http.server 8080
```

Open `http://localhost:8080` in browser. Verify:
- [ ] Dark mode renders correctly (default)
- [ ] All hero content displays (name, tagline, chips, contact links)
- [ ] Email link works (click opens mailto)
- [ ] All 5 timeline entries render with correct content
- [ ] Timeline dots are connected, current dot pulses
- [ ] 3 impact cards display
- [ ] 6 skill blocks display with correct badges
- [ ] 6 cert rows display
- [ ] CTA section renders with email/LinkedIn buttons
- [ ] Footer displays
- [ ] Theme toggle works (dark ↔ light, persists on reload)
- [ ] Nav dots highlight on scroll
- [ ] Mobile pill bar appears at narrow viewport
- [ ] Scroll reveal animations fire
- [ ] SVG timeline spine draws on scroll
- [ ] Particles visible on desktop
- [ ] Back-to-top button appears on scroll
- [ ] Print preview looks clean
- [ ] No console errors

- [ ] **Step 2: Compare with original**

Open `abdul-portfolio.html` side by side. Verify pixel-identical output. Check:
- Font rendering matches
- Colors match in both themes
- Spacing and layout match
- All animations match

- [ ] **Step 3: Commit verification note**

```bash
git add -A
git commit -m "feat: modularization complete — verified pixel-identical output"
```

---

### Task 6: Update .gitignore and clean up

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Ensure .gitignore is appropriate**

Should already have `.superpowers/`. No other changes needed — all new files should be tracked.

- [ ] **Step 2: Final commit if any cleanup**

```bash
git status
# If clean, nothing to do
# If changes, commit appropriately
```

---

## Summary

| Task | What it delivers | Files |
|------|-----------------|-------|
| 1 | All content extracted to JSON | `data/data.json` |
| 2 | CSS extracted verbatim | `css/styles.css` |
| 3 | HTML skeleton with containers | `index.html` |
| 4 | Render functions + interactive JS | `js/script.js` |
| 5 | Verification of pixel-identical output | — |
| 6 | Cleanup | `.gitignore` |

**Old file:** `abdul-portfolio.html` is kept as-is for backup/email use case.
