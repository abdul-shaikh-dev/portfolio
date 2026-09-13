# Portfolio structure review — 13 September 2026

## Conclusion

The current page has one real flagship system and two overlapping presentations of the rest of the work.

- `Knowledge-management template` is a discrete system and works as a full case study.
- `Application modernisation` is a professional practice containing several deliveries.
- `More engineering work` contains more examples of that same practice: backend delivery, performance, Kubernetes enablement, runtime problem-solving, and migration engineering.

The problem is therefore the taxonomy, not the quality or quantity of the content. `Application modernisation` and `More engineering work` should become one continuous delivery portfolio.

## What the current structure communicates

### Knowledge-management template

This reads as a flagship project. It has a defined need, an owned system, architecture, adoption, recognition, and a distinctive interaction. Its scale and treatment are justified.

### Application modernisation

The heading presents this as project 02, equal in type to the knowledge-management system. It is not one project. The copy describes a way of operating:

> review codebases, define phased delivery plans, guide engineers, remain hands-on, and resolve production blockers

The three examples then demonstrate that practice.

### More engineering work

The dark section appears to begin a separate class of work, but its contents are further examples of the same practice. Backend APIs, performance optimisation, Rancher onboarding, browser-runtime work, messaging migrations, and Informatica migration tooling all belong within architecture-to-production engineering delivery.

The `Related backend work` links at the end of Application modernisation expose the problem: the page asks the visitor to leave one modernisation section for another section containing related modernisation work.

## Why the split feels wrong

### 1. A practice is presented as a project

Numbering Application modernisation as `02` makes it look like a single case study. Its content is actually a portfolio theme.

### 2. The categories are not mutually exclusive

The work directory separates `Modernisation`, `APIs`, and `Runtime & migration`, even though many projects belong to two or three of those categories. The service-estate work includes APIs, CI, Kubernetes, and migration. The AI clause application includes modernisation, runtime integration, and production delivery. The messaging work is both migration and application modernisation.

### 3. The visual hierarchy contradicts the labels

The dark `More engineering work` section has the strongest contrast and most prominent quantified result. It can feel more important than the supposedly primary Application modernisation section.

### 4. The transition adds orientation cost

On mobile, Application modernisation occupies about 2,560 px and More engineering work another 3,380 px. Together they contain roughly 640 words. The reader crosses a large visual boundary, learns a new section title, and then continues reading the same kind of evidence.

## Recommended structure

### 1. Hero

Keep the current hero. Its positioning remains accurate:

> application modernisation, backend systems, AI systems, and production delivery

### 2. Compact directory

Reduce the five work-directory entries to three:

1. `Knowledge & AI` — flagship knowledge-management system
2. `Engineering delivery` — modernisation, APIs, runtime, and migration work
3. `Experience` — career progression

The detailed groups can have local anchors inside Engineering delivery. They do not need equal prominence in the page-level directory.

### 3. Flagship system

Keep Knowledge-management template as the only full case study with a large interactive explanation.

Use a small plain-language label such as `Flagship system` if orientation is needed. Remove numerical project markers; a numbered pair implies two equivalent project case studies.

### 4. Engineering delivery

Replace both Application modernisation and More engineering work with one section:

**Engineering delivery**  
`Architecture, implementation, and production ownership across applications, APIs, and platforms.`

The opening should state the operating model once:

> I review constrained codebases, define phased delivery plans, guide engineers through implementation, and stay hands-on through deployment and production blockers.

Then present all supporting evidence in grouped editorial rows.

#### Applications and service modernisation

- **Service estate and Kubernetes onboarding** — combine the estate migration and onboarding automation. The skill becomes evidence of making repeated delivery easier, rather than a separate project competing for attention.
- **Infrastructure dashboard** — retain the stakeholder value, phased restructuring, Rancher deployment, and ongoing data-layer status.
- **AI clause extraction** — retain the legal-document context, production result, and CIO recognition.

#### Backend systems and performance

- **Backend API delivery** — pair the .NET legal-data API and Python financial-data API in one row. This shows range across stacks without presenting two similarly shaped small API cards.
- **Financial API performance** — keep the measured `6–7 GB → ~1 GB` and `5 min → 40 sec` treatment as the strongest quantified proof.

#### Production enablement and migration

- **Messaging migrations** — keep the AutoSys/Solace constraint and production outcome.
- **Browser runtime on Rancher** — retain as a concise example of removing an environment blocker for an AI use case.
- **Informatica migration plugin** — retain the internal-plugin label, application-scale assessment, state, reporting, and Python/Prefect generation.
- **Internal tools hub** — retain as the final, visibly secondary prototype item.

This reduces eleven separate project treatments to nine clearer evidence rows, while preserving every substantive accomplishment.

### 5. Experience, expertise, and contact

Keep the current order and overall treatment. Expertise should continue linking back to evidence within the unified Engineering delivery section.

## Visual direction for the merged section

Use one continuous dark surface for Engineering delivery. The dark treatment already works well for concise evidence and measured outcomes; extending it upward removes the false boundary.

Inside that surface:

- place the Engineering delivery thesis at the top;
- use category names in the left column and evidence rows in the right;
- keep project titles, one context/result line, technology tags, and selected implementation notes visible;
- give the performance figures additional scale;
- use thin rules and spacing to distinguish groups;
- avoid cards and additional diagrams;
- keep the prototype visually quieter than production deliveries.

The reader should experience one coherent sequence:

`how I work → where I applied it → what changed`

## Content edits

### Remove

- the `02` marker from Application modernisation;
- the heading `More engineering work.`;
- `Backend APIs / performance / runtimes / tooling` beneath that heading;
- `Related backend work` and its three links;
- the standalone Rancher onboarding item after its substance is incorporated into service-estate delivery;
- the two separate small API items after they are combined as Backend API delivery.

### Rename

- `Application modernisation` → `Engineering delivery`
- `Architecture, implementation & production delivery` → `Applications, APIs, and platforms carried through to production`
- `Service modernisation & Kubernetes onboarding` → `Service estate modernisation`

### Retain

- every measured result;
- production and ongoing status language;
- CIO recognition;
- the knowledge-management walkthrough;
- implementation notes where they explain a non-obvious constraint.

## Expected result

The page will have two clear work ideas instead of three competing sections:

1. a flagship enterprise knowledge and AI system;
2. a broad engineering-delivery portfolio showing lead-level ownership across applications, APIs, platforms, and production.

That structure matches the hero, removes the artificial boundary, and makes the breadth feel like one senior engineering practice rather than a collection of unrelated projects.
