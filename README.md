# Abdul Gaffar Shaikh — Portfolio

A static portfolio covering enterprise knowledge systems, application modernisation, backend engineering, and production delivery in financial services.

The site is generated from structured JSON and served as plain HTML, CSS, and JavaScript. It does not require a frontend framework or runtime build step in production.

## Local development

Generate the website and start a local server:

```powershell
python scripts/build.py
python -m http.server 4173 --bind 127.0.0.1
```

Open [http://127.0.0.1:4173](http://127.0.0.1:4173).

## Content sources

- `data/data.json` contains portfolio copy, work history, expertise, links, and credentials.
- `data/resume.json` contains the resume profile, experience, skills, certifications, and education.
- `scripts/build.py` generates `index.html` from the portfolio data.
- `scripts/build_resume.py` generates `docs/resume.tex` from the resume data.

`index.html` and `docs/resume.tex` are generated files. Edit their JSON sources or templates rather than changing them directly.

## Resume generation

The resume pipeline has one editable source and two generated outputs:

```text
data/resume.json
        │
        ▼
scripts/build_resume.py
        │
        ├── docs/resume.tex        reviewable LaTeX
        │
        ▼
      LaTeX
        │
        └── output/pdf/resume.pdf  portfolio download
```

Generate the LaTeX locally:

```powershell
python scripts/build_resume.py
```

With MiKTeX installed, compile the PDF from the repository root:

```powershell
New-Item -ItemType Directory -Force tmp/pdfs,output/pdf | Out-Null
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error -output-directory=tmp/pdfs docs/resume.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error -output-directory=tmp/pdfs docs/resume.tex
Copy-Item tmp/pdfs/resume.pdf output/pdf/resume.pdf
python scripts/build.py
```

The second LaTeX pass resolves document references. Rebuilding the website refreshes the cache-busting hash on the resume link.

## Resume CI

`.github/workflows/resume.yml` runs when resume data, its generator, or its template changes. It can also be started manually from the GitHub Actions page.

For pull requests, the workflow:

1. Generates `docs/resume.tex` from `data/resume.json`.
2. Fails if the committed LaTeX is stale.
3. Compiles the PDF with TeX Live.
4. Uploads `Abdul-Gaffar-Shaikh-resume` as a workflow artifact for review.

For pushes to `main`, it also updates the canonical PDF and the website’s cache-busted link, then commits generated files with `[skip ci]` to avoid a workflow loop.

## Repository structure

```text
.
├── .github/workflows/    GitHub Actions
├── css/                  responsive layout and themes
├── data/                 portfolio and resume sources
├── docs/                 resume template and generated LaTeX
├── js/                   navigation and interactive diagrams
├── output/pdf/           published resume PDF
├── scripts/              site and resume generators
└── index.html            generated static site
```

## Useful checks

```powershell
python -m json.tool data/data.json > $null
python -m json.tool data/resume.json > $null
python -m py_compile scripts/build.py scripts/build_resume.py
python scripts/build_resume.py
python scripts/build.py
node --check js/script.js
node --check js/diagrams.js
git diff --check
```
