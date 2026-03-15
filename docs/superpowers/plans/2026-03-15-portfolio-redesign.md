# Portfolio Redesign — Bold Technical: Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Abdul Gaffar Shaikh's portfolio from editorial-minimal to Bold Technical — dark-first, neon accents, scroll animations, theme toggle, in a single HTML file.

**Architecture:** Single self-contained HTML file with inline `<style>` and `<script>`. CSS custom properties for theming (dark default, `[data-theme="light"]` overrides). Vanilla JS for scroll animations, theme toggle, particle field, and navigation. No build tools, no frameworks.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox, `@keyframes`, `@media print`), Vanilla JS (Intersection Observer, Canvas 2D, localStorage), Google Fonts (Space Grotesk, Inter, JetBrains Mono)

**Spec:** `docs/superpowers/specs/2026-03-15-portfolio-redesign-design.md`

**Important: Script placement** — All `<script>` blocks must be placed at the end of `<body>`, after all HTML content. This ensures DOM elements exist when JS runs. No `DOMContentLoaded` wrappers needed if scripts are at the bottom.

---

## Chunk 1: Foundation & Hero

### Task 1: Head, CSS Custom Properties, and Base Styles

**Files:**
- Modify: `abdul-portfolio.html` (complete rewrite of `<head>` and `<style>` block)

- [ ] **Step 1: Rewrite `<head>` section**

Replace the existing `<head>` with new meta tags, font imports, and favicon:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Abdul Gaffar Shaikh — Senior Software Engineer with 7+ years in .NET modernisation, Kubernetes, and production AI systems. Currently at Capgemini, Mumbai.">
<meta property="og:title" content="Abdul Gaffar Shaikh — Senior Software Engineer">
<meta property="og:description" content="7+ years in .NET modernisation, Kubernetes infrastructure, and production AI. Building intelligent systems at scale.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<title>Abdul Gaffar Shaikh — Senior Software Engineer</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%230a0f1a' width='100' height='100' rx='12'/><text x='50' y='68' text-anchor='middle' font-size='52' font-family='system-ui' font-weight='700' fill='%2363e6be'>A</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Write CSS custom properties (dark mode defaults)**

```css
:root {
  --bg:      #0a0f1a;
  --surface: #0e1424;
  --ink:     #e8edf5;
  --ink2:    #8a9bb0;
  --border:  #1a2235;
  --mint:    #63e6be;
  --mint-bg: rgba(99,230,190,0.08);
  --mint-bd: rgba(99,230,190,0.3);
  --amber:   #fbbf24;
  --amber-bg: rgba(251,191,36,0.08);
  --amber-bd: rgba(251,191,36,0.3);
  --violet:  #a78bfa;
  --violet-bg: rgba(167,139,250,0.08);
  --violet-bd: rgba(167,139,250,0.3);
  --grid:    rgba(99,230,190,0.04);
  --glow:    rgba(99,230,190,0.07);
  --surface2: #121a2e; /* skills section background */
}

[data-theme="light"] {
  --bg:      #f4f7fa;
  --surface: #ffffff;
  --ink:     #0a0f1a;
  --ink2:    #5a6b7a;
  --border:  #dde3ea;
  --mint:    #0d9373;
  --mint-bg: rgba(13,147,115,0.06);
  --mint-bd: rgba(13,147,115,0.3);
  --amber:   #a07008;
  --amber-bg: rgba(180,120,10,0.06);
  --amber-bd: rgba(180,120,10,0.3);
  --violet:  #6d4bc8;
  --violet-bg: rgba(109,75,200,0.06);
  --violet-bd: rgba(109,75,200,0.3);
  --grid:    rgba(10,15,26,0.04);
  --glow:    transparent;
  --surface2: #edf1f5; /* skills section background */
}
```

- [ ] **Step 3: Write base/reset styles**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--ink);
  font-family: 'Inter', system-ui, sans-serif;
  overflow-x: hidden;
}

/* Grid background */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(var(--grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
  z-index: 0;
}

/* Skip to content */
.skip-link {
  position: absolute;
  top: -100%;
  left: 16px;
  background: var(--mint);
  color: var(--bg);
  padding: 8px 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  border-radius: 0 0 4px 4px;
  z-index: 200;
  text-decoration: none;
}
.skip-link:focus { top: 0; }

/* Shared keyframes */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 4px var(--mint-bg); }
  50%      { box-shadow: 0 0 0 8px var(--mint-bg), 0 0 16px var(--glow); }
}
@keyframes dotPulse {
  0%, 100% { opacity: 0.7; }
  50%      { opacity: 1; }
}
@keyframes expandLine {
  0%, 100% { width: 20px; opacity: 0.4; }
  50%      { width: 50px; opacity: 1; }
}

/* Scroll reveal (JS adds .visible) */
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Theme transition (toggled briefly via JS) */
.theme-transitioning,
.theme-transitioning *,
.theme-transitioning *::before,
.theme-transitioning *::after {
  transition: background-color 0.3s, color 0.3s, border-color 0.3s !important;
}
```

- [ ] **Step 4: Open file in browser to verify dark background, grid pattern, no content yet**

Open `abdul-portfolio.html` in a browser. Verify: deep navy background, grid-line pattern visible, no errors in console.

- [ ] **Step 5: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: foundation — head, CSS custom properties, base styles, dark/light tokens"
```

---

### Task 2: Hero Section HTML & CSS

**Files:**
- Modify: `abdul-portfolio.html` (add hero HTML after `<body>`, add hero CSS)

- [ ] **Step 1: Add skip link and hero HTML**

Insert after `<body>`:

```html
<a href="#main-content" class="skip-link">Skip to content</a>

<header id="hero">
  <div class="eyebrow">
    <span class="status-dot"></span>
    Senior Software Engineer · 7+ Years
  </div>
  <h1>ABDUL GAFFAR <span class="accent">SHAIKH</span></h1>
  <p class="tagline">Senior engineer at the intersection of .NET modernisation, Kubernetes infrastructure, and production AI — turning legacy systems into cloud-native platforms and unstructured data into intelligent, searchable knowledge. Based in Mumbai.</p>
  <div class="chips">
    <span class="chip">.NET Core / C#</span>
    <span class="chip">Python</span>
    <span class="chip">Kubernetes</span>
    <span class="chip">Rancher</span>
    <span class="chip">FastAPI</span>
    <span class="chip hot">RAG / LangChain</span>
    <span class="chip hot">MCP Development</span>
    <span class="chip hot">Agentic AI Dev</span>
    <span class="chip">Azure</span>
    <span class="chip">Solace Messaging</span>
    <span class="chip">Helm Charts</span>
    <span class="chip">Docker</span>
    <span class="chip">AWS / EKS</span>
    <span class="chip">OCR / pytesseract</span>
  </div>
  <div class="contact-row">
    <a class="contact-link" id="email-link">
      <svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
      <span id="email-text"></span>
    </a>
    <a class="contact-link" href="https://linkedin.com/in/abdul-gaffar-shaikh21/" target="_blank" rel="noopener">
      <svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14m-.5 15.5v-5.3a3.26 3.26 0 00-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 011.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 001.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 00-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
      linkedin.com/in/abdul-gaffar-shaikh21
    </a>
    <a class="contact-link" href="https://github.com/abdul219428" target="_blank" rel="noopener">
      <svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
      github.com/abdul219428
    </a>
    <span class="contact-link">
      <svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
      +91 88986 71746
    </span>
  </div>
  <div class="scroll-hint">SCROLL TO EXPLORE</div>
</header>
```

- [ ] **Step 2: Write hero CSS**

All hero-related CSS — header layout, eyebrow with status dot, h1 styling, tagline, chips, contact row, scroll hint. Copy exact CSS from spec (font families, sizes, colors all use custom properties). Include all `fadeUp` animation delays. Include hero radial glow via `header::after` pseudo-element.

Key styles to include:
- `header`: `min-height: 100vh`, flex column, centered, `padding: 80px 10vw`, `background: var(--bg)`
- `header::after`: radial glow, positioned top-right, mint-tinted
- `.eyebrow`: JetBrains Mono, 11px, `--mint` color, flex with status dot
- `.status-dot`: 6px circle, `--mint` background, `animation: dotPulse 2s ease-in-out infinite`
- `h1`: Space Grotesk, `clamp(2.8rem, 7.5vw, 6rem)`, weight 700, uppercase, `-0.04em` spacing
- `.accent`: `color: var(--mint)`
- `header::after`: radial glow positioned top-right corner (dark mode only):
  ```css
  header::after {
    content: '';
    position: absolute;
    top: -20%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--glow) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }
  ```
- `.tagline`: Inter 300, no italic, `--ink2` color
- `.chip`: JetBrains Mono 10.5px, `--border` border, `--surface` bg
- `.chip.hot`: `--amber-bd` border, `--amber` color, `--amber-bg` bg
- `.contact-link`: JetBrains Mono 11.5px, `--ink2` color, hover → `--mint`
- `.scroll-hint`: JetBrains Mono 9.5px, `--ink2`, absolute bottom, with `expandLine` animation on `::after`

- [ ] **Step 3: Add email assembly JS**

```html
<script>
(function() {
  var u = 'abdul219428', d = 'gmail.com';
  var link = document.getElementById('email-link');
  var text = document.getElementById('email-text');
  if (link) link.href = 'mailto:' + u + '@' + d;
  if (text) text.textContent = u + '@' + d;
})();
</script>
```

- [ ] **Step 4: Verify hero renders correctly in browser**

Open in browser. Verify: dark background, grid lines, name in large Space Grotesk, mint accent on "SHAIKH", status dot pulsing, chips render, contact links visible, scroll hint at bottom.

- [ ] **Step 5: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: hero section — name, eyebrow, chips, contact, scroll hint"
```

---

## Chunk 2: Content Sections

### Task 3: Career Timeline Section

**Files:**
- Modify: `abdul-portfolio.html` (add timeline HTML + CSS)

- [ ] **Step 1: Add `<main>` wrapper and divider after hero**

```html
<div class="divider"></div>
<main id="main-content">
```

- [ ] **Step 2: Add timeline section HTML**

Insert the full timeline section with all 5 entries (Capgemini, Accenture Senior SE, Accenture SE, Accenture Associate, Education). Content text is identical to current site. Structure per entry:

```html
<section id="timeline">
  <div class="section-label">Career Timeline</div>
  <div class="timeline">
    <svg class="timeline-spine" aria-hidden="true"></svg>
    <!-- Each .tl-entry with .tl-dot, .tl-period, .tl-title, .tl-org, .tl-card -->
    <!-- Education entry has no .tl-card -->
  </div>
</section>
```

Each `.tl-entry` gets `class="reveal"` for scroll animation. The current role's dot gets `class="tl-dot current"`. Tech tags use color classes: default (mint), `.amber`, `.violet` (replaces old `.green` for AI tags).

**Migration: rename `.green` to `.violet`** on these tags in the Capgemini entry:
- `LangChain` → `class="tech-tag violet"`
- `LangGraph` → `class="tech-tag violet"`
- `ChromaDB` → `class="tech-tag violet"`
- `MCP` → `class="tech-tag violet"`

**Migration: `.tl-period .now`** — use `color: var(--mint)` (replaces old `var(--now)`).

- [ ] **Step 3: Write timeline CSS**

Key styles:
- `.divider`: `height: 1px`, `background: var(--border)`, `z-index: 10`
- `.section-label`: JetBrains Mono, 10px, `--mint`, uppercase, flex with `::after` line
- `.timeline`: relative container
- `.timeline-spine`: absolute SVG, `left: 20px`, `top: 8px` to `bottom: 0`, stroke color `var(--mint-bd)` fading to `var(--border)`
- `.tl-entry`: `padding-left: 64px`, `padding-bottom: 64px`, `class="reveal"`
- `.tl-dot`: 18px circle, `--border` border, `--surface` bg, centered inner dot
- `.tl-dot.current`: `--mint` border, `animation: pulse 3s ease-in-out infinite`
- `.tl-card`: `--surface` bg, `--border` border, 6px radius, `::before` left accent bar (transparent → mint on hover)
- `.tl-items li::before`: `▸` marker in `--mint`
- `.tech-tag`: JetBrains Mono 10px, mint default
- `.tech-tag.amber`: amber variant
- `.tech-tag.violet`: violet variant (new, replaces `.green`)

- [ ] **Step 4: Verify timeline renders in browser**

Verify: timeline spine visible, 5 entries with correct content, current role has glowing dot, tech tags color-coded, cards have hover effects.

- [ ] **Step 5: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: career timeline — 5 entries, SVG spine, tech tags, hover states"
```

---

### Task 4: Impact, Skills, Certifications, CTA, and Footer

**Files:**
- Modify: `abdul-portfolio.html` (add remaining content sections + CSS)

- [ ] **Step 1: Add Strategic Impact section HTML**

3 impact cards (CIO Newsletter, Zero-Defect K8s, Enterprise RAG). Each card gets `class="reveal"`. Content identical to current site.

- [ ] **Step 2: Add Core Capabilities section HTML**

6 skill blocks. Section gets `background: var(--surface2)` for visual separation (replaces old `var(--faint)`). Each block gets `class="reveal"`. Content identical to current site.

- [ ] **Step 3: Add Certifications section HTML**

5 cert rows. Each row gets `class="reveal"`. Content identical to current site.

- [ ] **Step 4: Add CTA section HTML (no inline styles)**

Centered layout with proper CSS classes instead of inline styles. JS email assembly for the email button (same pattern as hero).

```html
<section id="cta" class="cta-section">
  <div class="cta-inner">
    <div class="section-label section-label-centered">Get In Touch</div>
    <h2 class="cta-heading">Let's build something <span class="accent">meaningful</span> together.</h2>
    <p class="cta-body">Whether you're looking for a senior engineer to lead backend modernisation, build AI-powered systems, or strengthen your team's technical foundations — I'd love to connect.</p>
    <div class="cta-buttons">
      <a id="cta-email" class="btn-primary">EMAIL ME</a>
      <a href="https://linkedin.com/in/abdul-gaffar-shaikh21/" target="_blank" rel="noopener" class="btn-outline">LINKEDIN</a>
    </div>
  </div>
</section>
```

- [ ] **Step 5: Add Footer HTML and close `</main>`**

```html
<footer>
  <div>
    <div class="footer-name">Abdul Gaffar Shaikh</div>
    <div class="footer-meta">Senior Software Engineer · Capgemini (May 2023–Present) · Mumbai, Maharashtra</div>
  </div>
  <div class="footer-meta">2026</div>
</footer>
</main>
```

Note: `<main>` wraps from timeline through footer (opened in Task 3, closed here after footer). `<header>` stays outside `<main>` as a sibling.

- [ ] **Step 6: Write CSS for all four sections**

Impact: `.impact-grid-full` grid, `.impact-card` with mint border, hover lift.
Skills: `.skills-grid` grid, `.skill-block` with hover, `.skill-icon`, `.skill-name` with experience badge span.
Certs: `.certs-strip` flex column, `.cert-row` with amber hover.
CTA: `.cta-section` with gradient background, `.cta-heading` (Space Grotesk), `.btn-primary` (solid mint), `.btn-outline` (mint border), `.section-label-centered` (`justify-content: center`).
Footer: flex row, `--surface` bg, top border.

- [ ] **Step 7: Add CTA email JS**

```javascript
(function() {
  var u = 'abdul219428', d = 'gmail.com';
  var el = document.getElementById('cta-email');
  if (el) el.href = 'mailto:' + u + '@' + d;
})();
```

- [ ] **Step 8: Verify all sections render correctly**

Scroll through entire page. Verify: impact cards, skill blocks, cert rows, CTA buttons, footer all display with correct colors and hover states.

- [ ] **Step 9: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: impact, skills, certs, CTA, footer sections"
```

---

## Chunk 3: Navigation & Theme Toggle

### Task 5: Desktop Nav Dots and Mobile Pill Bar

**Files:**
- Modify: `abdul-portfolio.html` (add nav HTML + CSS + JS)

- [ ] **Step 1: Add desktop nav dots HTML**

Insert after `<body>` / skip-link:

```html
<nav class="nav-dots" aria-label="Page sections">
  <div class="nav-dot active" role="button" tabindex="0" aria-label="Navigate to Introduction" data-label="INTRO" data-target="hero"></div>
  <div class="nav-dot" role="button" tabindex="0" aria-label="Navigate to Timeline" data-label="TIMELINE" data-target="timeline"></div>
  <div class="nav-dot" role="button" tabindex="0" aria-label="Navigate to Impact" data-label="IMPACT" data-target="impact"></div>
  <div class="nav-dot" role="button" tabindex="0" aria-label="Navigate to Skills" data-label="SKILLS" data-target="skills"></div>
  <div class="nav-dot" role="button" tabindex="0" aria-label="Navigate to Certifications" data-label="CERTS" data-target="certs"></div>
</nav>
```

- [ ] **Step 2: Add mobile nav HTML**

```html
<nav class="mobile-nav" aria-label="Page sections">
  <div class="pill active" role="button" tabindex="0" data-target="hero">Intro</div>
  <div class="pill" role="button" tabindex="0" data-target="timeline">Timeline</div>
  <div class="pill" role="button" tabindex="0" data-target="impact">Impact</div>
  <div class="pill" role="button" tabindex="0" data-target="skills">Skills</div>
  <div class="pill" role="button" tabindex="0" data-target="certs">Certs</div>
</nav>
```

- [ ] **Step 3: Write nav CSS**

Desktop `.nav-dots`: fixed right 28px, vertical, z-index 100, dot with `::before` label tooltip. Hidden below 768px.
Mobile `.mobile-nav`: fixed bottom 16px, centered, horizontal, `backdrop-filter: blur(12px)`, semi-transparent `--surface` bg, rounded pill shape, z-index 100. Hidden above 768px.
`.pill.active` and `.nav-dot.active`: mint accent.

- [ ] **Step 4: Write nav JS — click handlers and Intersection Observer**

```javascript
// Navigation click handlers (works for both dot and pill nav)
function setupNav() {
  document.querySelectorAll('[data-target]').forEach(function(el) {
    function navigate() {
      document.getElementById(el.dataset.target).scrollIntoView({ behavior: 'smooth' });
    }
    el.addEventListener('click', navigate);
    el.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); navigate(); }
    });
  });

  // Intersection Observer for active section
  var sections = ['hero','timeline','impact','skills','certs'];
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var id = entry.target.id;
        document.querySelectorAll('.nav-dot, .pill').forEach(function(n) {
          n.classList.toggle('active', n.dataset.target === id);
        });
      }
    });
  }, { threshold: 0.3 });

  sections.forEach(function(id) {
    var el = document.getElementById(id);
    if (el) observer.observe(el);
  });
}
setupNav();
```

- [ ] **Step 5: Verify navigation works**

Desktop: nav dots visible on right, clicking scrolls to section, active dot updates on scroll. Resize to mobile: nav dots hidden, pill bar appears at bottom, same behavior.

- [ ] **Step 6: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: desktop nav dots + mobile pill bar with Intersection Observer"
```

---

### Task 6: Theme Toggle and Back-to-Top

**Files:**
- Modify: `abdul-portfolio.html` (add toggle + back-to-top HTML/CSS/JS)

- [ ] **Step 1: Add theme toggle HTML**

Insert after nav dots:

```html
<button class="theme-toggle" role="button" tabindex="0" aria-label="Switch to light mode" id="theme-toggle">
  <!-- Moon icon (shown in dark mode) -->
  <svg class="icon-moon" aria-hidden="true" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
  <!-- Sun icon (shown in light mode) -->
  <svg class="icon-sun" aria-hidden="true" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
</button>
```

- [ ] **Step 2: Add back-to-top HTML**

```html
<button class="back-to-top" id="back-to-top" role="button" tabindex="0" aria-label="Back to top">
  <svg aria-hidden="true" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/></svg>
</button>
```

- [ ] **Step 3: Write theme toggle + back-to-top CSS**

```css
.theme-toggle {
  position: fixed;
  top: 24px;
  right: 28px;
  z-index: 100;
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s, color 0.2s;
}
.theme-toggle:hover { border-color: var(--mint); color: var(--mint); }
.theme-toggle:focus-visible { outline: 2px solid var(--mint); outline-offset: 2px; }
/* Show/hide icons based on theme */
.icon-sun { display: none; }
[data-theme="light"] .icon-moon { display: none; }
[data-theme="light"] .icon-sun { display: block; }

.back-to-top {
  position: fixed;
  bottom: 24px;
  right: 28px;
  z-index: 100;
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s, border-color 0.2s, color 0.2s;
}
.back-to-top.visible { opacity: 1; pointer-events: auto; }
.back-to-top:hover { border-color: var(--mint); color: var(--mint); }
.back-to-top:focus-visible { outline: 2px solid var(--mint); outline-offset: 2px; }

@media (max-width: 768px) {
  .theme-toggle { top: 16px; right: 16px; }
  .back-to-top { bottom: 72px; right: 16px; } /* above mobile nav */
}
```

- [ ] **Step 4: Write theme toggle JS**

```javascript
(function() {
  var toggle = document.getElementById('theme-toggle');
  var html = document.documentElement;

  // Init: check localStorage, then prefers-color-scheme
  function getInitialTheme() {
    try {
      var saved = localStorage.getItem('theme');
      if (saved) return saved;
    } catch(e) {}
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  var theme = getInitialTheme();
  if (theme === 'light') html.setAttribute('data-theme', 'light');

  toggle.addEventListener('click', function() {
    html.classList.add('theme-transitioning');
    var isLight = html.getAttribute('data-theme') === 'light';
    if (isLight) {
      html.removeAttribute('data-theme');
      toggle.setAttribute('aria-label', 'Switch to light mode');
    } else {
      html.setAttribute('data-theme', 'light');
      toggle.setAttribute('aria-label', 'Switch to dark mode');
    }
    try { localStorage.setItem('theme', isLight ? 'dark' : 'light'); } catch(e) {}
    setTimeout(function() { html.classList.remove('theme-transitioning'); }, 350);
  });

  toggle.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle.click(); }
  });
})();
```

- [ ] **Step 5: Write back-to-top + scroll-hint-hide JS**

```javascript
(function() {
  var btn = document.getElementById('back-to-top');
  var scrollHint = document.querySelector('.scroll-hint');
  var hintHidden = false;

  btn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  btn.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); btn.click(); }
  });

  window.addEventListener('scroll', function() {
    // Back to top visibility
    btn.classList.toggle('visible', window.scrollY > window.innerHeight);
    // Scroll hint auto-hide (one-time)
    if (!hintHidden && window.scrollY > 50 && scrollHint) {
      scrollHint.style.opacity = '0';
      hintHidden = true;
    }
  }, { passive: true });
})();
```

- [ ] **Step 6: Verify toggle and back-to-top work**

Toggle: click switches dark↔light smoothly, persists on reload. Back-to-top: appears when scrolled past hero, click scrolls to top. Scroll hint hides on first scroll.

- [ ] **Step 7: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: theme toggle (dark/light) + back-to-top button"
```

---

## Chunk 4: Animations, Particles, Print, and Polish

### Task 7: Scroll Reveal Animations and SVG Timeline Draw

**Files:**
- Modify: `abdul-portfolio.html` (add scroll animation JS, update SVG spine)

- [ ] **Step 1: Write scroll reveal Intersection Observer JS**

```javascript
(function() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.reveal').forEach(function(el) { el.classList.add('visible'); });
    return;
  }

  // Pre-compute stagger index for each .reveal within its parent
  var parents = new Map();
  document.querySelectorAll('.reveal').forEach(function(el) {
    var parent = el.parentElement;
    if (!parents.has(parent)) parents.set(parent, 0);
    el._staggerIndex = parents.get(parent);
    parents.set(parent, parents.get(parent) + 1);
  });

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.style.transitionDelay = (entry.target._staggerIndex * 100) + 'ms';
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal').forEach(function(el) {
    observer.observe(el);
  });
})();
```

- [ ] **Step 2: Write SVG timeline spine draw-on-scroll JS**

```javascript
(function() {
  var timeline = document.querySelector('.timeline');
  var svg = document.querySelector('.timeline-spine');
  if (!timeline || !svg || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function initSpine() {
    var h = timeline.offsetHeight;
    svg.setAttribute('viewBox', '0 0 2 ' + h);
    svg.setAttribute('height', h);
    svg.innerHTML = '<path d="M1 0 V' + h + '" stroke="url(#spineGrad)" stroke-width="1" fill="none" id="spine-path"/>' +
      '<defs><linearGradient id="spineGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--mint-bd)"/><stop offset="70%" stop-color="var(--border)"/><stop offset="100%" stop-color="transparent"/></linearGradient></defs>';
    var path = document.getElementById('spine-path');
    var len = path.getTotalLength();
    path.style.strokeDasharray = len;
    path.style.strokeDashoffset = len;
    path.style.transition = 'stroke-dashoffset 0.15s ease';
  }

  function onScroll() {
    var path = document.getElementById('spine-path');
    if (!path) return;
    var rect = timeline.getBoundingClientRect();
    var viewH = window.innerHeight;
    var total = rect.height + viewH;
    var scrolled = viewH - rect.top;
    var progress = Math.max(0, Math.min(1, scrolled / total));
    var len = path.getTotalLength();
    path.style.strokeDashoffset = len * (1 - progress);
  }

  initSpine();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', initSpine);
})();
```

- [ ] **Step 3: Update `.timeline-spine` CSS**

```css
.timeline-spine {
  position: absolute;
  left: 20px;
  top: 8px;
  width: 2px;
  z-index: 1;
  overflow: visible;
}
```

- [ ] **Step 4: Verify scroll animations**

Scroll down the page. Verify: timeline entries fade in as they enter viewport, timeline spine draws progressively, no jank.

- [ ] **Step 5: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: scroll reveal animations + SVG timeline spine draw-on-scroll"
```

---

### Task 8: Canvas 2D Particle Field

**Files:**
- Modify: `abdul-portfolio.html` (add canvas + particle JS + CSS)

- [ ] **Step 1: Add canvas element**

Insert after `<body>` opening (before skip-link):

```html
<canvas id="particles" aria-hidden="true"></canvas>
```

- [ ] **Step 2: Write particle canvas CSS**

```css
#particles {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}
```

- [ ] **Step 3: Write particle field JS**

```javascript
(function() {
  var canvas = document.getElementById('particles');
  if (!canvas) return;
  // Disable on mobile or reduced motion
  if (window.innerWidth < 768 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    canvas.style.display = 'none';
    return;
  }

  var ctx = canvas.getContext('2d');
  var particles = [];
  var count = 35;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  for (var i = 0; i < count; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      r: Math.random() * 1.5 + 0.5,
      o: Math.random() * 0.05 + 0.03
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var isLight = document.documentElement.getAttribute('data-theme') === 'light';
    var color = isLight ? '10,15,26' : '99,230,190';
    particles.forEach(function(p) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + color + ',' + p.o + ')';
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
```

- [ ] **Step 4: Verify particles**

On desktop: subtle floating particles visible behind content. On mobile (resize narrow): particles hidden. Toggle theme: particle color adapts.

- [ ] **Step 5: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: canvas 2D particle field — desktop only, theme-aware"
```

---

### Task 9: Print Stylesheet and Reduced Motion

**Files:**
- Modify: `abdul-portfolio.html` (add print + reduced-motion CSS)

- [ ] **Step 1: Add print stylesheet**

```css
@media print {
  .nav-dots, .mobile-nav, .scroll-hint, .theme-toggle,
  .back-to-top, #cta, #particles { display: none !important; }
  body { background: white; color: black; }
  body::before { display: none; }
  * { animation: none !important; transition: none !important; }
  header, section { padding: 24px 0; min-height: auto; }
  h1, .tl-title, .skill-name, .impact-card-title, .cta-heading { color: black; }
  .tl-items li, .skill-desc, .impact-card-body, .tagline, .cert-name { color: #333; }
  .eyebrow, .section-label, .tl-period, .tl-org { color: #555; }
  .tl-card, .impact-card, .skill-block, .cert-row { border-color: #ccc; background: white; box-shadow: none; }
  .chip, .tech-tag, .cert-badge { border-color: #ccc; color: #333; background: #f5f5f5; }
  footer { background: white; border-top-color: #ccc; }
  .footer-name { color: black; }
  .footer-meta { color: #555; }
}
```

- [ ] **Step 2: Add reduced motion styles**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .reveal { opacity: 1; transform: none; }
  html { scroll-behavior: auto; }
}
```

- [ ] **Step 3: Test print preview**

Browser → Print Preview. Verify: nav/CTA/particles hidden, black text on white, no animations, compact spacing.

- [ ] **Step 4: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: print stylesheet + prefers-reduced-motion support"
```

---

### Task 10: Final Polish and Responsive Tweaks

**Files:**
- Modify: `abdul-portfolio.html` (responsive CSS, final cleanup)

- [ ] **Step 1: Write responsive breakpoint styles**

```css
@media (max-width: 768px) {
  header, section { padding: 60px 6vw; }
  .nav-dots { display: none; }
  footer { padding: 36px 6vw; }
  h1 { letter-spacing: -0.03em; }
  .contact-row { flex-direction: column; gap: 12px; }
  .chips { gap: 6px; }
  .impact-grid-full { grid-template-columns: 1fr; }
  .skills-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 2: Verify mobile layout**

Resize browser to ~375px width. Verify: hero stacks correctly, chips wrap, contact links stack vertically, timeline is readable, pill bar visible at bottom, all sections look good.

- [ ] **Step 3: Verify desktop layout**

Full-width browser. Verify: nav dots on right, grids fill properly, no overflow, hover states work.

- [ ] **Step 4: Run through full checklist**

- [ ] Dark mode renders correctly (default)
- [ ] Light mode renders correctly (toggle)
- [ ] Theme persists on reload
- [ ] All 5 nav sections navigate correctly
- [ ] Mobile pill bar works
- [ ] Scroll reveal animations fire
- [ ] Timeline spine draws on scroll
- [ ] Particles visible on desktop, hidden on mobile
- [ ] Print preview looks clean
- [ ] Skip-to-content link works (Tab → Enter)
- [ ] All keyboard navigation works
- [ ] No console errors
- [ ] Email links assemble correctly

- [ ] **Step 5: Commit**

```bash
git add abdul-portfolio.html
git commit -m "feat: responsive styles, final polish, complete redesign"
```

---

## Summary

| Task | What it delivers | Commit |
|------|-----------------|--------|
| 1 | Head, CSS tokens, base styles | Foundation |
| 2 | Hero section | Hero |
| 3 | Career timeline | Timeline |
| 4 | Impact + Skills + Certs + CTA + Footer | Content sections |
| 5 | Nav dots + Mobile pill bar | Navigation |
| 6 | Theme toggle + Back-to-top | Interactive controls |
| 7 | Scroll reveals + SVG spine draw | Animations |
| 8 | Canvas particle field | Background depth |
| 9 | Print stylesheet + Reduced motion | Accessibility |
| 10 | Responsive + Final polish | Ship it |
