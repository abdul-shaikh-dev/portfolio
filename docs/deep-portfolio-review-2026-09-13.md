# Deep portfolio review — 13 September 2026

## Verdict

The portfolio now reads as the work of a lead engineer with substantial production experience. The first screen establishes role, seniority, core stack, financial-services context, architecture responsibility, and hands-on delivery. The strongest projects show difficult constraints rather than generic technology usage.

The largest remaining issue is editorial hierarchy. The site has enough strong material, but it explains some of it more than once and gives too many sections similar visual importance. A recruiter can understand the profile in the first 5–10 seconds; reaching the best proof still takes longer than it should.

The audited desktop page is about 10,900 px tall and the 390 px mobile page about 15,300 px tall. The two work sections contain roughly 1,480 words before Experience, and the page contains 14 expandable implementation sections. These figures do not make the page inherently unusable, but they confirm the visible sense of density.

## Audit walkthrough

### 1. First screen — strong, with one repeated layer

**Health: Strong**

The hero answers the main recruiter questions quickly:

- Lead Software Engineer
- .NET, Python, and Kubernetes
- application modernisation, backend systems, and production AI
- 7.5+ years in financial services
- architecture guidance, mentoring, and hands-on engineering

The serif typography, restrained palette, and system orbit give the page a recognisable identity. The résumé and LinkedIn are easy to find.

The `At a glance` row repeats the hero and the two projects immediately below it. On mobile it adds another block before any project evidence appears. Remove it. Let the hero statement lead directly into the work.

`WORK / 01—02` is visually interesting but cryptic. Replace it with `Selected systems`, `Selected work`, or simply remove the section label and let project 01 begin.

### 2. Knowledge-management template — the signature case study

**Health: Strong, slightly overlong on mobile**

This is the clearest expression of the profile: enterprise need, system ownership, AI/RAG context, modular architecture, adoption, recognition, and a technical demonstration. The adaptive-extraction walkthrough is distinctive because it explains an actual system behaviour rather than adding decorative motion.

The first mobile viewport of this project is almost entirely introductory copy. Compress the opening to one context sentence, one ownership sentence, and the result. Keep the interactive walkthrough and the short `From source to useful answer` / `Composable for each team` explanations.

The diagram should remain the site's signature interaction. On mobile, fit its stages into one stable visual area instead of making the reader move between several tall panels. Keep the visible play/pause and step controls, and do not make progress depend on waiting for animation.

### 3. Application modernisation — the main duplicated section

**Health: Needs restructuring**

The section currently has three layers that communicate the same material:

1. the application-modernisation introduction;
2. the `Delivery paths` interactive diagram;
3. the three `Selected deliveries` stories.

The diagram does not add a decision, architecture, or process that the delivery stories do not already explain. It is also the largest block in this section and gives the ongoing dashboard the same visual weight as the service-estate and production-AI work. Remove the diagram.

Keep the section introduction, then move directly into the three deliveries. Use each row to show a different kind of ownership:

- estate modernisation: framework, CI, and Kubernetes delivery at scale;
- dashboard: architecture review and phased rescue of an existing codebase;
- clause extraction: code, model, OCR, pipeline, and runtime work that reached production.

This gives the section a clear purpose: several examples of taking constrained applications toward a maintainable production state.

### 4. Supporting work — useful breadth, too much equal weight

**Health: Good content, heavy presentation**

The categories are useful and the summaries are much stronger than earlier versions. The section proves breadth across APIs, runtime engineering, messaging, migration tooling, and prototypes.

Every item currently follows the same title–paragraph–tags–accordion pattern. That makes a production migration, a measured performance result, and a prototype feel equally important. Introduce hierarchy without creating more hidden content:

- surface the performance result as a compact metric line: `6–7 GB → ~1 GB` and `5 min → 40 sec`;
- keep the Solace migration outcome visible;
- keep `Prototype` visible on the tools hub;
- use a short outcome or status line for the remaining items;
- retain expandable notes only where the implementation materially strengthens the story.

A small, always-visible work index can reduce navigation effort: `Knowledge · Modernisation · APIs · Runtime & migration · Experience`. These should be direct anchors, not filters or modal views.

### 5. Experience — clear progression

**Health: Strong**

The April 2026 promotion to Manager / Lead Software Engineer is now immediately understandable, and the earlier Senior Consultant / Senior Software Engineer period remains visible. This section successfully shows growing responsibility while preserving hands-on engineering.

Some Senior Consultant bullets repeat projects already described above. That repetition is defensible because it places the work in time, but the bullets should stay at role level. Avoid adding more project mechanics here.

### 6. Expertise and contact — clean but partly repetitive

**Health: Needs light editing**

The expertise grid restates themes already evident in the hero, projects, and experience. Keep it as a compact recruiter reference, but connect each capability to proof or shorten the descriptions further. A capability without evidence is less useful than a link to the relevant work.

The contact headline has personality and the call to action is clear. The `Context / Constraint / Outcome` mini-framework repeats the storytelling structure used throughout the site and adds visual length without increasing confidence. Remove it, leaving the short invitation, button, and email.

### 7. Responsive behaviour and accessibility

**Health: Good foundation, a few refinements**

The audited layouts had no horizontal overflow or browser-console warnings. Mobile navigation links are 45 px tall, primary controls are clearly labelled, keyboard focus is visible, the theme toggle has an accessible name, and native disclosure elements provide usable keyboard behaviour. Reduced-motion handling is present.

Refinements:

- increase the Reset control from 39 × 44 px to at least 44 × 44 px;
- keep the adaptive-extraction state understandable without animation;
- verify the complete diagram with a screen reader, especially the stage controls exposed as pressed/toggle controls;
- preserve stable figure height while scripts initialise so deep links do not visibly reposition;
- retest every direct project anchor after layout consolidation.

This was a code, keyboard, responsive, and visual audit. It was not a full assistive-technology or formal WCAG conformance test.

### 8. Source structure — visible quality is ahead of maintainability

**Health: Needs cleanup**

`css/landing.css` contains several generations of overrides. Examples include nine definitions affecting `.hero h1`, seven for `.hero-inner`, seven for `.hero-statement`, and seven for project-summary layout. Conflicting scroll-margin rules also remain. Consolidating the final design into one rule set will make spacing and breakpoints predictable.

The content source also has drift:

- `chips`, `impact`, and `cta` data are not used by the current build;
- a dormant impact entry still contains the old `4,000+ documents` claim;
- the build script hardcodes project summaries, outcomes, delivery copy, experience framing, and the contact section while related content also exists in JSON;
- the Informatica record says `Not yet confirmed` for maturity, but that state is not rendered;
- older unused headings and summaries remain in the builder.

Move all editorial content into one active data model, delete dormant claims, and make the build script responsible only for presentation. This reduces the chance that the website and résumé diverge during the next update.

## Project context check

| Work item | Context health | Recommendation |
|---|---|---|
| Knowledge-management template | Complete | Keep as the flagship; tighten only the mobile introduction. |
| Service modernisation | Complete enough | The business reason, estate types, ownership, and destination are clear. Add no more implementation detail to the visible copy. |
| Infrastructure dashboard | Complete | Value, initial condition, current work, and unfinished data layer are clear. |
| AI clause extraction | Complete | The legal-document use case, OCR/RAG context, blockers, production result, and recognition are clear. |
| Business data API | Complete | It states the data domain, prior access problem, implementation, consumers, and deployment. |
| Financial data API | Missing one reason | Explain why the API was needed without exposing business specifics: for example, `Built a maintainable FastAPI service to give teams a supported way to consume financial data held in Oracle, with a reference structure they could extend.` Use only if that accurately describes the need. |
| Financial API performance | Complete | Keep the measured before/after values visible. They are among the strongest proof on the page. |
| Rancher onboarding automation | Missing the former workflow | Add the concise before state: it replaced manual cloning and placeholder edits across application, infrastructure, and Flux repositories. |
| Browser automation | Complete | The blocked Chromium runtime, Playwright service, Crawl4AI connection, and Kubernetes setting are clear. |
| Messaging migrations | Complete | The AutoSys constraint, Solace bridge/subscriber pattern, ownership, and result are all present. |
| Informatica migration plugin | Missing maturity/outcome | The capability is clear, but readers cannot tell whether it is a prototype, internal tool in use, or completed delivery. Confirm its status before changing the public label. Do not invent adoption. |
| Internal tools hub | Complete | It is clearly labelled as a prototype and states what was built and what others extended. |

## Recommended next design pass

### Priority 0 — reduce diversion

1. Remove `At a glance`.
2. Replace or remove `WORK / 01—02`.
3. Remove the application-modernisation `Delivery paths` diagram.
4. Remove the contact `Context / Constraint / Outcome` strip.
5. Tighten the knowledge-project opening on mobile.

### Priority 1 — make evidence easier to scan

1. Add a slim direct-anchor work index.
2. Give the measured performance result a typographic metric treatment.
3. Reduce low-value implementation accordions; keep important evidence visible.
4. Give supporting items explicit outcome or status lines so production work and prototypes do not look equivalent.
5. Shorten expertise descriptions or link each capability to its evidence.

### Priority 2 — preserve personality with less motion

1. Keep adaptive extraction as the signature interactive system demonstration.
2. Use editorial numbering, scale, rule lines, and controlled accent changes to create rhythm elsewhere.
3. Add motion only where it reveals system state or causality.
4. Avoid more boxed diagrams. A single precise interaction will feel more authored than several generic process graphics.

### Engineering cleanup

1. Consolidate `landing.css` into one final cascade.
2. Remove unused JSON sections and stale claims.
3. Move hardcoded editorial copy from the builder into the content data.
4. Add a small build check for required fields, duplicate project IDs, missing maturity/status, and broken internal anchors.
5. Re-run desktop, mobile, keyboard, reduced-motion, and direct-link checks after the cleanup.

## Reference review

- [Figma recruiter guidance](https://www.figma.com/blog/product-design-portfolio-tips-from-a-figma-recruiter/) reinforces designing for the actual audience and making the intended capabilities explicit.
- [Nielsen Norman Group portfolio guidance](https://www.nngroup.com/articles/ux-design-portfolios/?lm=maintain-ux-portfolio&pt=article) stresses clear capability selection and case studies that are easy to scan and follow.
- [Josh W. Comeau's developer-portfolio guide](https://storage.googleapis.com/joshwcomeau/building-an-effective-dev-portfolio.pdf) is a useful reference for project detail, accessibility, and intentional interaction.
- [Josh W. Comeau's site](https://www.joshwcomeau.com/) shows how bespoke interactions can support the subject matter instead of decorating every section.
- [Bruno Simon's portfolio](https://bruno-simon.com/) is a useful extreme: the interaction is the proof because he is a creative developer. For this portfolio, the equivalent is the adaptive-extraction demonstration, not a site-wide game or animation layer.
- [Recent senior software-engineer portfolio examples](https://www.sitebuilderreport.com/inspiration/software-engineer-portfolios) repeatedly favour clear navigation, strong typography, and scroll-friendly project stories even when the visual identity is distinctive.

## Proposed final page rhythm

1. Hero
2. Slim work index
3. Knowledge-management flagship + adaptive-extraction interaction
4. Application modernisation + three concise delivery stories
5. Supporting engineering evidence, grouped and outcome-led
6. Experience and promotion progression
7. Compact capability reference
8. Direct contact invitation

This keeps the portfolio's depth while making the strongest evidence appear sooner and only once.
