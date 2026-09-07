"""Build the static portfolio from data/data.json. Run: python scripts/build.py."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/data.json').read_text(encoding='utf-8'))
e = escape
projects = [dict(item) for item in data['recentWork']]
projects.append({
    'id': 'migrations', 'shortTitle': 'Messaging service migrations',
    'group': 'platform', 'category': 'Production modernisation',
    'intro': 'Seven Solace services migrated to Kubernetes, with zero post-deployment defects.',
    'summary': 'Migrated seven Solace messaging services to Kubernetes, independently leading three migrations. Resolved messaging reliability and deployment issues.',
    'detail': 'The work involved moving existing messaging services into the Kubernetes environment while maintaining business continuity. The migration pattern established during this work became the approach for subsequent service migrations across the account.',
    'outcome': 'Seven service migrations with zero post-deployment defects and zero business disruption.',
    'tags': ['Solace', 'Kubernetes', 'Rancher'],
})
by_id = {item['id']: item for item in projects}
email = data['hero']['email']['user'] + '@' + data['hero']['email']['domain']
linkedin = data['hero']['linkedin']['url']
github = data['hero']['github']['url']

def tags(items):
    return '<ul class="tags" aria-label="Technologies">' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'

def external(url, label):
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>'

def technical_notes(p):
    if not p.get('detail'):
        return ''
    extra = f'<p>{e(p["notes"])}</p>' if p.get('notes') else ''
    return f'<details class="technical-notes"><summary>Implementation notes <span aria-hidden="true">+</span></summary><div><p>{e(p["detail"])}</p>{extra}</div></details>'

def walkthrough(key, title, description):
    return f'<figure class="system-figure walkthrough" data-walkthrough="{key}"><figcaption>{e(title)}<span>{e(description)}</span></figcaption><div class="walkthrough-interactive" hidden></div><p class="walkthrough-fallback">{e(description)} Full architecture and implementation details are available in the accompanying notes.</p></figure>'

figures = {
    'mcp': walkthrough('extraction', 'Find what’s missing.', 'Adaptive extraction inside the knowledge template · fictional example.'),
    'modernisation': '''<figure class="system-figure architecture-sketch"><figcaption>A clearer separation of responsibilities.</figcaption><div class="architecture-before"><span class="diagram-label">Before · coupled implementation</span><p>Python script <span aria-hidden="true">→</span> Generated JSON files <span aria-hidden="true">→</span> React dashboard</p><small>Spreadsheet dependencies and application logic intertwined.</small></div><div class="architecture-now"><span class="diagram-label">Current · deployed on Rancher</span><div class="service-pair"><div><span class="sketch-symbol" aria-hidden="true">▤</span><strong>React</strong><small>Present the dashboard</small></div><span class="service-link">REST API <span aria-hidden="true">↔</span></span><div><span class="sketch-symbol" aria-hidden="true">{ }</span><strong>Python</strong><small>Serve application data</small></div></div></div><div class="architecture-next"><span class="diagram-label">Next · planned data pipeline</span><ol class="pipeline-line"><li><strong>ServiceNow</strong><small>Source</small></li><li><strong>Prefect</strong><small>Collect</small></li><li><strong>SQL</strong><small>Store</small></li><li><strong>Python API</strong><small>Serve data</small></li><li><strong>React</strong><small>Display dashboard</small></li></ol></div></figure>''',
    'engineering-support': '<section class="delivery-changes" aria-labelledby="delivery-changes-title"><h4 id="delivery-changes-title">What changed</h4><dl><div><dt>Application engineering</dt><dd>Restructured the Python codebase and resolved application and Linux runtime issues.</dd></div><div><dt>Internal model delivery</dt><dd>Packaged the embedding model through the internal artifact repository to work within the firm’s network restrictions.</dd></div><div><dt>Production deployment</dt><dd>Adopted established GitLab CI builds, resolved deployment blockers, and brought the application into production on Rancher.</dd></div></dl></section>',

}

headings = {
    'mcp': 'A shared foundation<br>for enterprise knowledge.',
    'modernisation': 'Modernising an<br>infrastructure dashboard.',
    'engineering-support': 'AI adoption and<br>production delivery.'
}
stories = ''
for key in data['featuredWork']:
    p = by_id[key]
    context = f'<p>{e(p["context"])}</p>' if p.get('context') else ''
    capabilities = '<div class="project-capabilities">' + ''.join(f'<div><h4>{e(c["title"])}</h4><p>{e(c["body"])}</p></div>' for c in p['capabilities']) + '</div>' if p.get('capabilities') else ''
    recognition = f'<p class="recognition">{e(p["recognition"])}</p>' if p.get('recognition') else ''
    stories += f'''<article class="work-story story-{key}" id="project-{key}"><div class="story-heading"><p class="project-category">{e(p['category'])}</p><h3>{headings[key]}</h3></div><div class="story-layout"><div class="story-copy">{context}<p>{e(p['summary'])}</p>{tags(p['tags'])}{technical_notes(p)}{capabilities}</div>{figures[key]}</div>{recognition}</article>'''

supporting = ''
supporting_groups = [
    ('Backend services & performance', ['dotnet-api', 'api', 'api-performance']),
    ('Deployment & runtime engineering', ['onboarding', 'browser', 'migrations']),
    ('Migration tooling & prototypes', ['informatica', 'platform']),
]
for label, keys in supporting_groups:
    supporting += f'<div class="supporting-group"><h3 class="supporting-group-heading">{e(label)}</h3><div class="supporting-grid">'
    for key in keys:
        p = by_id[key]
        badge = '<span class="prototype-badge">Prototype</span>' if p.get('status') == 'prototype' else ''
        supporting += f'<article class="supporting-project" id="project-{key}"><div class="supporting-title"><h4>{e(p["shortTitle"])}</h4>{badge}</div><p>{e(p["summary"])}</p>{tags(p["tags"])}{technical_notes(p)}</article>'
    supporting += '</div></div>'

current = data['timeline'][0]
current_details = '<details class="career-details"><summary>Full responsibilities & contributions <span aria-hidden="true">+</span></summary><ul>' + ''.join('<li>'+b+'</li>' for b in current['bullets']) + '</ul></details>'
earlier = ''
for role in data['timeline'][1:-1]:
    earlier += f'<div class="earlier-role"><h4>{e(role["title"])}</h4><p class="role-date">{e(role["period"])}</p><ul>'+''.join('<li>'+b+'</li>' for b in role['bullets'])+'</ul></div>'
career = f'''<article class="employer current-employer"><div class="employer-heading"><div><p class="role-date">May 2023 — Present</p><h3>Senior Software Engineer</h3><p>Capgemini · Mumbai</p></div><span class="current-label">Current</span></div><p class="role-summary">Backend modernisation, production AI, and engineering automation for a global investment bank.</p><ul class="career-highlights"><li>Developed the knowledge-management template as a shared foundation for enterprise AI use cases.</li><li>Modernised a PDF clause-extraction application and delivered it into production.</li><li>Lead phased architecture improvements for a Python and React dashboard, with both applications now deployed on Rancher.</li><li>Built and deployed a .NET business-data API and reduced financial API memory use through query optimisation.</li><li>Guide teammates delivering modernisation work and adoption of established CI and deployment practices.</li></ul>{current_details}</article><article class="employer"><div class="employer-heading"><div><p class="role-date">October 2018 — May 2023</p><h3>Associate to Senior Software Engineer</h3><p>Accenture · Mumbai</p></div></div><p class="role-summary">Progressed through three engineering roles in financial services, working on insurance platforms, API modernisation, Azure integrations, and document automation.</p><details class="career-details"><summary>Earlier roles & contributions <span aria-hidden="true">+</span></summary>{earlier}</details></article><div class="education"><span>Education</span><div><strong>{e(data['timeline'][-1]['title'])}</strong><p>{e(data['timeline'][-1]['org'])} · 2015–2018</p></div></div>'''

skills = ''.join(f'<article class="skill-item"><h3>{e(x["name"])}</h3><p>{e(x["desc"])}</p></article>' for x in data['skills'])
certs = ''
for c in data['certs']:
    content = f'<span class="cert-code">{e(c["badge"])}</span><span>{e(c["name"].replace("Microsoft Certified: ",""))}</span><span class="cert-year">{e(c["year"])}</span>'
    certs += external(c['url'],content) if c.get('url') else '<div>'+content+'</div>'

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(data['meta']['description'])}">
<meta property="og:title" content="{e(data['meta']['title'])}"><meta property="og:description" content="{e(data['meta']['description'])}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary">
<title>{e(data['meta']['title'])}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%232434ad' width='100' height='100' rx='16'/%3E%3Ctext x='50' y='69' text-anchor='middle' font-size='66' font-family='sans-serif' fill='%23ffffff'%3Ea%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css"><script src="js/script.js" defer></script><script src="js/diagrams.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><div class="header-inner wrap"><a class="wordmark" href="#hero" aria-label="Abdul Gaffar Shaikh, home">ags<span>/</span></a><nav aria-label="Main navigation"><a href="#impact">Work</a><a href="#timeline">Experience</a><a href="#skills">Expertise</a><a href="#cta">Contact</a></nav><button id="theme-toggle" class="icon-button" aria-label="Switch to dark mode" title="Change color theme" hidden><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor"/></svg></button></div></header>
<main id="main-content">
<section class="hero" id="hero"><div class="hero-inner wrap"><div class="hero-identity"><p class="intro">Senior software engineer <span>/</span> Mumbai, India</p><h1>Abdul Gaffar<br>Shaikh<span>.</span></h1><p class="hero-statement">I build backend systems and modernise applications for production.</p><p class="hero-bio">7.5+ years in financial services. Enterprise knowledge, application modernisation, and the work that takes an idea into production.</p><div class="hero-links"><a class="button" href="#project-mcp">Explore my work <span aria-hidden="true">↘</span></a>{external(linkedin,'LinkedIn')}{external(github,'GitHub')}</div></div><nav class="hero-directory" aria-label="Explore my work"><p class="directory-title">A few ways into my work</p><a href="#project-mcp"><span><strong>Knowledge systems</strong><small>A shared foundation for enterprise AI.</small></span><span class="directory-arrow" aria-hidden="true">↗</span></a><a href="#project-modernisation"><span><strong>Modernisation</strong><small>Architecture, implementation, deployment.</small></span><span class="directory-arrow" aria-hidden="true">↗</span></a><a href="#project-engineering-support"><span><strong>AI production delivery</strong><small>Clause extraction, from application to production.</small></span><span class="directory-arrow" aria-hidden="true">↗</span></a><div class="directory-footer"><span>Design decisions.<br>Working implementations.</span><a href="#timeline">My experience <span aria-hidden="true">↓</span></a></div></nav></div></section>
<section class="work-section wrap" id="impact"><div class="work-header"><h2>The work behind the experience<span>.</span></h2><p>The knowledge platform and the engineering work behind teams’ modernisation, AI adoption, and production delivery.</p></div><div class="work-layout"><aside class="work-navigation"><p>In this section</p><nav aria-label="Selected projects"><a href="#project-mcp">Knowledge template</a><a href="#project-modernisation">Dashboard modernisation</a><a href="#project-engineering-support">AI production delivery</a><a href="#work-index">Supporting work <span aria-hidden="true">↓</span></a></nav></aside><div class="work-stories">{stories}</div></div></section>
<section class="supporting-section" id="work-index"><div class="wrap"><div class="section-heading"><h2>More from the workbench.</h2><p>Supporting implementations and tools: APIs, deployment automation, migration workflows, and experiments.</p></div>{supporting}</div></section>
<section class="experience-section wrap" id="timeline"><div class="section-heading"><h2>Experience.</h2><p>Increasing ownership across backend architecture, enterprise AI, and platform modernisation.</p></div><div class="experience-layout"><div class="experience-intro"><p>My work combines system design with hands-on delivery: writing the implementation, resolving production issues, and making the design understandable to the team.</p>{external(linkedin,'View career on LinkedIn')}</div><div class="career-list">{career}</div></div></section>
<section class="expertise-section" id="skills"><div class="wrap"><div class="section-heading"><h2>What I work with.</h2><p>Backend depth, with the cloud and AI experience to connect the wider system.</p></div><div class="skill-grid">{skills}</div><details class="credentials"><summary><span>Certifications <small>Azure · AI · Security · Duck Creek</small></span><span aria-hidden="true">+</span></summary><div class="cert-list">{certs}</div></details></div></section>
<section class="contact-section wrap" id="cta"><div><p>Let’s compare notes.</p><h2>Good work starts<br>with a conversation<span>.</span></h2></div><div><p>Building something complex, exploring an idea, or just want to talk engineering? I’d like to hear about it.</p><a class="button" href="mailto:{email}">Start a conversation <span aria-hidden="true">↗</span></a><div class="email-row"><a href="mailto:{email}">{email}</a><button id="copy-email" class="icon-button" data-email="{email}" aria-label="Copy email address" title="Copy email address" hidden>⧉</button></div><span id="copy-status" role="status"></span></div></section>
</main>
<footer><div class="wrap footer-inner"><a class="footer-name" href="#hero">Abdul Gaffar Shaikh<span>Senior Software Engineer · Mumbai, India</span></a><div>{external(github,'GitHub')}{external(linkedin,'LinkedIn')}<a href="tel:{data['hero']['phone'].replace(' ','')}">Phone ↗</a></div><span>© {data['footer']['year']}</span></div></footer>
</body></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
print(f'Built index.html: 3 responsibility-led highlights, 8 supporting projects, {len(data["skills"])} visible expertise areas.')
