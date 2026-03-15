# Portfolio Modularization — Data-Driven Architecture

**Date:** 2026-03-15
**Status:** Approved
**Subject:** Split single-file portfolio into modular files with data-driven content rendering

## Overview

Refactor `abdul-portfolio.html` (1319 lines) from a single self-contained HTML file into a modular architecture with separated CSS, JS, and JSON data. The visual output, animations, accessibility, and all functionality remain identical — this is a structural refactor only.

## Motivation

- **Content edits without touching code** — update `data.json` to change bullets, add a cert, tweak a skill. Push. Done.
- **Cleaner version control** — content changes show as JSON diffs, not HTML diffs mixed with markup
- **Maintainability** — HTML drops from ~1200 lines to ~150 (structure only)
- **GitHub Pages hosting** — `fetch('data.json')` works over HTTPS; no build step needed

## File Structure

```
Pervy-Resume/
├── index.html          ← ~150 lines: semantic HTML skeleton + container elements
├── css/
│   └── styles.css      ← ~740 lines: extracted verbatim from <style> block
├── js/
│   └── script.js       ← ~280 lines: data rendering + all existing JS functionality
├── data/
│   └── data.json       ← ~300 lines: all content (experience, skills, certs, etc.)
├── .gitignore
└── docs/               ← specs & plans (existing, not served)
```

## `data.json` Schema

```json
{
  "meta": {
    "title": "Abdul Gaffar Shaikh — Senior Software Engineer",
    "description": "Senior Software Engineer with 7+ years...",
    "ogTitle": "Abdul Gaffar Shaikh — Senior Software Engineer",
    "ogDescription": "7+ years in .NET modernisation..."
  },
  "hero": {
    "name": "ABDUL GAFFAR",
    "accent": "SHAIKH",
    "eyebrow": "Senior Software Engineer · 7+ Years",
    "tagline": "Senior engineer at the intersection of...",
    "phone": "+91 88986 71746",
    "email": { "user": "abdul219428", "domain": "gmail.com" },
    "linkedin": {
      "url": "https://linkedin.com/in/abdul-gaffar-shaikh21/",
      "label": "linkedin.com/in/abdul-gaffar-shaikh21"
    },
    "github": {
      "url": "https://github.com/abdul219428",
      "label": "github.com/abdul219428"
    }
  },
  "chips": [
    { "label": ".NET Core / C#", "hot": false },
    { "label": "RAG / LangChain", "hot": true }
  ],
  "timeline": [
    {
      "period": "May 2023 —",
      "periodNow": true,
      "title": "Senior Software Engineer",
      "org": "Capgemini · Mumbai",
      "currentBadge": true,
      "client": "// Global Investment Bank",
      "bullets": [
        "Modernised <strong>legacy .NET applications</strong> into <strong>microservices</strong>..."
      ],
      "tags": [
        { "label": ".NET Core", "color": "mint" },
        { "label": "Kubernetes", "color": "amber" },
        { "label": "LangChain", "color": "violet" }
      ]
    }
  ],
  "impact": [
    {
      "icon": "📰",
      "title": "Corporate CIO Newsletter Feature",
      "body": "The RAG-powered Knowledge Management solution..."
    }
  ],
  "skills": [
    {
      "icon": "⚙️",
      "name": "Backend Engineering",
      "badge": "7+ yrs",
      "desc": "7+ years in .NET Core C#..."
    }
  ],
  "certs": [
    { "badge": "MICROSOFT", "name": "AZ-204: Azure Developer Associate", "year": "2020" }
  ],
  "cta": {
    "heading": "Let's build something <span class=\"accent\">meaningful</span> together.",
    "body": "Whether you're looking for a senior engineer..."
  },
  "footer": {
    "name": "Abdul Gaffar Shaikh",
    "meta": "Senior Software Engineer · Capgemini (May 2023–Present) · Mumbai, Maharashtra",
    "year": "2026"
  }
}
```

### Content markup in JSON

Bullet text in `timeline[].bullets` and `cta.heading` may contain inline HTML (`<strong>`, `<span>`, `&amp;`). This is intentional — these are rendered via `innerHTML`. No user-generated content is involved (the JSON is author-controlled), so XSS is not a concern.

## `index.html` — Semantic Skeleton

Contains only structural HTML — no content text. Key elements:

### Static elements (stay as HTML, not rendered from data):
- `<canvas id="particles">` — particle field
- `<a class="skip-link">` — skip to content
- `<nav class="nav-dots">` — desktop nav (5 dots with `data-target` attributes)
- `<nav class="mobile-nav">` — mobile pill bar (5 pills)
- `<button class="theme-toggle">` — with moon/sun SVG icons
- `<button class="back-to-top">` — with chevron SVG

### Container elements (JS renders into these):
- `<header id="hero">` — contains empty child containers:
  - `<div id="hero-content"></div>` — JS renders eyebrow, h1, tagline, chips, contact row, scroll hint
- `<main id="main-content">`:
  - `<section id="timeline">` → `<div id="timeline-entries"></div>`
  - `<section id="impact">` → `<div id="impact-cards"></div>`
  - `<section id="skills">` → `<div id="skills-grid"></div>`
  - `<section id="certs">` → `<div id="certs-list"></div>`
  - `<section id="cta">` → `<div id="cta-content"></div>`
- `<footer>` → `<div id="footer-content"></div>`

### Head:
- `<link rel="stylesheet" href="css/styles.css">`
- `<script src="js/script.js" defer></script>`
- Meta tags with placeholder values (JS updates `<title>` and meta content from data on load)
- Google Fonts preconnect + stylesheet link
- Inline SVG favicon (stays in HTML — not data-driven)

## `styles.css` — Extracted Verbatim

The entire `<style>` block from the current file, extracted with zero changes. No CSS modifications.

## `script.js` — Structure

```javascript
// 1. Data fetch and render
async function init() {
  const res = await fetch('data/data.json');
  const data = await res.json();

  renderMeta(data.meta);
  renderHero(data.hero, data.chips);
  renderTimeline(data.timeline);
  renderImpact(data.impact);
  renderSkills(data.skills);
  renderCerts(data.certs);
  renderCTA(data.cta);
  renderFooter(data.footer);

  // After all content is rendered, initialize interactive features
  initNavigation();
  initThemeToggle();
  initBackToTop();
  initScrollReveal();
  initTimelineSpine();
  initParticles();
}

// 2. Render functions — each takes a section of data and populates its container
function renderMeta(meta) { /* update <title> and meta tags */ }
function renderHero(hero, chips) { /* build eyebrow, h1, tagline, chips, contact row, scroll hint */ }
function renderTimeline(entries) { /* build all .tl-entry elements with dots, cards, tags */ }
function renderImpact(items) { /* build impact cards grid */ }
function renderSkills(items) { /* build skill blocks grid */ }
function renderCerts(items) { /* build cert rows */ }
function renderCTA(cta) { /* build CTA heading, body, email/linkedin buttons */ }
function renderFooter(footer) { /* build footer name, meta, year */ }

// 3. Interactive features — same logic as current file, wrapped in init functions
function initNavigation() { /* nav dots + pills click handlers + IntersectionObserver */ }
function initThemeToggle() { /* localStorage, prefers-color-scheme, toggle logic */ }
function initBackToTop() { /* scroll listener, scroll hint hide */ }
function initScrollReveal() { /* staggered IntersectionObserver for .reveal elements */ }
function initTimelineSpine() { /* SVG path draw on scroll */ }
function initParticles() { /* Canvas 2D particle field */ }

// 4. Boot
init();
```

### Email assembly

The email is stored split in `data.json` (`{ "user": "abdul219428", "domain": "gmail.com" }`). The render function concatenates them at runtime — same obfuscation approach as the current JS, but driven by data.

### Render timing

`<script src="js/script.js" defer></script>` ensures the script runs after the DOM is parsed. No `DOMContentLoaded` wrapper needed. The `init()` function fetches data and renders, then initializes interactive features. The scroll reveal observer is set up AFTER rendering so all `.reveal` elements exist.

## What Does NOT Change

- Visual design — pixel-identical output
- All animations (fadeUp, pulse, dotPulse, expandLine, scroll reveals, SVG spine draw)
- All hover states and transitions
- Theme toggle (dark/light with localStorage)
- Canvas particle field
- Desktop nav dots + mobile pill bar
- Back-to-top button
- Print stylesheet + reduced motion support
- Accessibility (skip link, ARIA, keyboard nav, focus-visible)
- Google Fonts loading strategy

## What the Old File Becomes

`abdul-portfolio.html` is kept as-is for reference / email-attachment use case. The new modular version lives at `index.html` + `css/` + `js/` + `data/`. Both coexist in the repo — GitHub Pages serves `index.html`.

## GitHub Pages Deployment

1. Push repo to GitHub
2. Settings → Pages → Source: `main` branch, `/ (root)`
3. Site serves at `https://<username>.github.io/<repo>/`
4. `index.html` at root is auto-detected
5. Optional: add `CNAME` file for custom domain

## Out of Scope

- Build tools, bundlers, or minification
- Framework migration (React, Vue, etc.)
- Content changes — this is a structural refactor only
- CSS changes — extracted verbatim
