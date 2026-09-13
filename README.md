# Portfolio

A static portfolio with three responsibility-led work highlights, eight supporting projects, career history and visible expertise. Native anchor links and optional technical notes keep the content accessible without JavaScript.

The design uses a cobalt introduction with direct links into the three main stories, light/dark reading surfaces, and a dashboard architecture figure that separates deployed components from planned work. Responsive navigation and native disclosures keep the content available on smaller screens and without JavaScript.

## Run locally

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173.

## Update content

Edit `data/data.json`, then regenerate the page:

```powershell
python scripts/build.py
```

- `data/data.json`: project descriptions, career history, expertise and credentials.
- `scripts/build.py`: page structure, project figures and concise career summaries.
- `css/styles.css`: responsive layout and light/dark themes.
- `js/script.js`: reading-position navigation, theme preference and email copying.
- `index.html`: generated static page; update its source data or generator.

Project links such as `#project-mcp` and `#project-modernisation` navigate directly to the inline stories. The three highlights are knowledge management, application modernisation and delivery, and AI adoption/runtime integration. Onboarding automation and Informatica migration tooling are supporting work. The main navigation tracks the section at the reading position; a desktop project rail offers direct jumps between the three highlights. Implementation notes and earlier-career detail use native disclosure controls. There are no filters or project popups.

The Vite hub remains a supporting prototype. Informatica includes Python/Prefect code generation; its adoption and completion of the Oracle API's authentication have not been confirmed, so the copy makes no claims about those details.

## Build the resume

The editable resume is `docs/resume.tex`. With MiKTeX installed, compile it from the project root:

```powershell
New-Item -ItemType Directory -Force tmp/pdfs,output/pdf | Out-Null
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error -output-directory=tmp/pdfs docs/resume.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error -output-directory=tmp/pdfs docs/resume.tex
Copy-Item tmp/pdfs/resume.pdf output/pdf/resume.pdf
```

Open a new terminal after installing MiKTeX so its executables are available on PATH. The first build can download missing LaTeX packages.
