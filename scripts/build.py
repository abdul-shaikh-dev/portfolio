"""Build the static portfolio from data/data.json. Run: python scripts/build.py."""
from pathlib import Path
from html import escape
import json
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/data.json').read_text(encoding='utf-8'))
e = escape
projects = [dict(item) for item in data['recentWork']]
projects.append({
    'id': 'migrations', 'shortTitle': 'Messaging service migrations',
    'group': 'platform', 'category': 'Production modernisation',
    'intro': 'AutoSys-triggered .NET workloads moved from Windows hosting to Kubernetes through Solace messaging.',
        'summary': 'Converted scheduled .NET console processes into long-running Solace subscribers, enabling AutoSys-triggered workloads to move from Windows servers to Kubernetes. Led three of seven migrations through production with no post-deployment defects.',
    'detail': 'Because AutoSys was not available in Rancher, a .NET bridge remained on Windows to receive command arguments from AutoSys jobs, construct messages, and publish them to Solace queues. Each former console process became a long-running Kubernetes subscriber using the in-house library built on the official Solace .NET packages. The migration covered application restructuring, message handling, AutoSys batch changes, end-to-end testing, and production release.',
    'outcome': 'Seven service migrations with zero post-deployment defects and zero business disruption.',
    'tags': ['.NET', 'AutoSys', 'Solace', 'Kubernetes'],
    'proof': 'Three migrations led · zero post-deployment defects',
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
    detail_ids = {'mcp', 'modernisation', 'engineering-support', 'service-estate', 'browser', 'migrations', 'informatica'}
    if not p.get('detail') or p.get('id') not in detail_ids:
        return ''
    extra = f'<p>{e(p["notes"])}</p>' if p.get('notes') else ''
    return f'<details class="technical-notes"><summary>Implementation notes <span aria-hidden="true">+</span></summary><div><p>{e(p["detail"])}</p>{extra}</div></details>'

def walkthrough(key, title, description):
    return f'<figure class="system-figure walkthrough" data-walkthrough="{key}"><figcaption>{e(title)}<span>{e(description)}</span></figcaption><div class="walkthrough-interactive" hidden></div><p class="walkthrough-fallback">{e(description)} Full architecture and implementation details are available in the accompanying notes.</p></figure>'

figures = {
    'mcp': walkthrough('extraction', 'From document to attributed fields.', 'Ingestion and adaptive extraction inside the knowledge template · fictional example.'),
    'modernisation': '',
    'engineering-support': '<section class="delivery-changes" aria-labelledby="delivery-changes-title"><h4 id="delivery-changes-title">What changed</h4><dl><div><dt>Application engineering</dt><dd>Restructured the Python service and adapted document processing for Linux.</dd></div><div><dt>Internal model delivery</dt><dd>Delivered the embedding model through the internal artifact repository when external model hubs were unavailable.</dd></div><div><dt>Release path</dt><dd>Moved builds to GitLab CI and resolved the blockers to deployment on Rancher.</dd></div></dl></section>',

}

stories = ''
project_summaries = {
    'mcp': ('Knowledge-management template', 'Multisource ingestion, RAG, adaptive extraction, and secured agent access.'),
}
project_outcomes = {'mcp':'A shared foundation for enterprise knowledge'}
for key in data['featuredWork']:
    p = by_id[key]
    title, overview = project_summaries[key]
    context = f'<p>{e(p["context"])}</p>' if p.get('context') else ''
    capabilities = '<div class="project-capabilities">' + ''.join(f'<div><h4>{e(c["title"])}</h4><p>{e(c["body"])}</p></div>' for c in p.get('capabilities', [])) + '</div>' if p.get('capabilities') else ''
    recognition = f'<p class="recognition">{e(p["recognition"])}</p>' if p.get('recognition') else ''
    result = f'<p class="story-result"><strong>Result</strong> {e(p["outcome"])}</p>'
    stories += f'''<section class="project-disclosure" id="project-{key}"><header class="project-summary"><div class="project-overview-title"><h3>{title}</h3><span class="project-outcome">{e(project_outcomes[key])}</span></div><p>{overview}</p></header><article class="work-story story-{key}"><div class="story-layout"><div class="story-copy">{context}<p>{e(p['summary'])}</p>{result}{recognition}{tags(p['tags'])}</div>{figures[key]}<div class="lead-details">{capabilities}{technical_notes(p)}</div></div></article></section>'''

service_estate = {
    'id': 'service-estate', 'shortTitle': 'Service estate modernisation',
    'summary': 'Modernised a large estate of .NET services, React microfrontends, and NestJS APIs for Kubernetes, covering framework upgrades, CI adoption, build remediation, and Rancher deployment.',
    'detail': by_id['service-modernisation']['detail'] + ' The recurring application-chart, infrastructure-chart, and Flux setup also became a guided workflow that creates, validates, and publishes the required repositories using the firm’s conventions.',
    'tags': ['.NET / React / NestJS', 'GitLab CI', 'Helm / Flux', 'Kubernetes'],
    'proof': 'Windows-hosted estate → repeatable Kubernetes delivery',
}
backend_apis = {
    'id': 'backend-apis', 'shortTitle': 'Backend API delivery',
    'summary': 'Built supported access paths for previously isolated business data: a .NET and EF Core API over legal data in SQL Server, and a maintainable FastAPI service over financial data in Oracle.',
    'tags': ['.NET / EF Core', 'Python / FastAPI', 'SQL Server / Oracle'],
    'proof': 'Two data domains → maintained team APIs',
}
delivery_groups = [
    ('delivery-applications', 'Applications & service modernisation', [service_estate, by_id['modernisation'], by_id['engineering-support']]),
    ('delivery-backend', 'Backend systems & performance', [backend_apis, by_id['api-performance']]),
    ('delivery-production', 'Production enablement & migration', [by_id['migrations'], by_id['browser'], by_id['informatica']]),
    ('delivery-tooling', 'Internal tooling & prototypes', [by_id['platform']]),
]
legacy_aliases = {
    'service-estate': ['project-delivery', 'project-service-modernisation', 'project-onboarding'],
    'backend-apis': ['supporting-backend', 'project-dotnet-api', 'project-api'],
    'migrations': ['supporting-runtime'], 'platform': ['supporting-tooling'],
}
engineering_delivery = ''
for group_id, label, items in delivery_groups:
    engineering_delivery += f'<section class="delivery-group" id="{group_id}"><h3>{e(label)}</h3><div class="delivery-grid">'
    for p in items:
        key = p['id']
        aliases = ''.join(f'<span class="anchor-alias" id="{alias}" aria-hidden="true"></span>' for alias in legacy_aliases.get(key, []))
        badge_text = p.get('statusLabel') or ('Prototype' if p.get('status') == 'prototype' else '')
        badge = f'<span class="prototype-badge">{e(badge_text)}</span>' if badge_text else ''
        proof = f'<p class="delivery-proof">{e(p["proof"])}</p>' if p.get('proof') else ''
        evidence = f'<p class="recognition">{e(p["recognition"])}</p>' if p.get('recognition') else ''
        engineering_delivery += f'<article class="delivery-project" id="project-{key}">{aliases}<div class="delivery-title"><h4>{e(p["shortTitle"])}</h4>{badge}</div>{proof}<p>{e(p["summary"])}</p>{figures.get(key, "")}{evidence}{technical_notes(p)}</article>'
    engineering_delivery += '</div></section>'

current = data['timeline'][0]
role_progression = '<div class="role-progression">'
for role in current['roles']:
    bullets = role['bullets']
    contributions = '<ul class="role-contributions">' + ''.join('<li>'+b+'</li>' for b in bullets) + '</ul>'
    role_progression += f'<article class="progression-role"><p class="role-date">{e(role["period"])}</p><h4>{e(role["title"])}</h4><div class="progression-contributions">{contributions}</div></article>'
role_progression += '</div>'
earlier = ''
for role in data['timeline'][1:-1]:
    earlier += f'<div class="earlier-role"><h4>{e(role["title"])}</h4><p class="role-date">{e(role["period"])}</p><ul>'+''.join('<li>'+b+'</li>' for b in role['bullets'])+'</ul></div>'
career = f'''<article class="employer current-employer"><div class="employer-heading"><div><p class="role-date">May 2023 — Present</p><h3>Capgemini</h3><p>Mumbai, India · Global investment bank</p></div><span class="current-label">Current</span></div>{role_progression}</article><article class="employer"><div class="employer-heading"><div><p class="role-date">October 2018 — May 2023</p><h3>Associate to Senior Software Engineer</h3><p>Accenture · Mumbai</p></div></div><p class="role-summary">Progressed through three engineering roles in financial services, working on insurance platforms, API modernisation, Azure integrations, and document automation.</p><details class="career-details"><summary>Earlier roles & contributions <span aria-hidden="true">+</span></summary>{earlier}</details></article><div class="education"><span>Education</span><div><strong>{e(data['timeline'][-1]['title'])}</strong><p>{e(data['timeline'][-1]['org'])} · 2015–2018</p></div></div>'''

skills = ''.join(f'<article class="skill-item"><h3><a href="{e(x["href"])}">{e(x["name"])} <span aria-hidden="true">↗</span></a></h3><p>{e(x["desc"])}</p></article>' for x in data['skills'])
certs = ''
for c in data['certs']:
    content = f'<span class="cert-code">{e(c["badge"])}</span><span>{e(c["name"].replace("Microsoft Certified: ",""))}</span><span class="cert-year">{e(c["year"])}</span>'
    certs += external(c['url'],content) if c.get('url') else '<div>'+content+'</div>'

def asset(path):
    version = sha256((ROOT / path).read_bytes()).hexdigest()[:10]
    return f'{path}?v={version}'

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(data['meta']['description'])}">
<meta property="og:title" content="{e(data['meta']['title'])}"><meta property="og:description" content="{e(data['meta']['description'])}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary">
<title>{e(data['meta']['title'])}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%231f5f4b' width='100' height='100' rx='16'/%3E%3Ctext x='50' y='69' text-anchor='middle' font-size='66' font-family='serif' font-style='italic' fill='%23d7ff63'%3Ea%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('css/styles.css')}"><link rel="stylesheet" href="{asset('css/landing.css')}"><script src="{asset('js/script.js')}" defer></script><script src="{asset('js/diagrams.js')}" defer></script>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><div class="header-inner wrap"><a class="wordmark" href="#hero" aria-label="Abdul Gaffar Shaikh, home">ags<span>/</span></a><nav aria-label="Main navigation"><a href="#impact">Work</a><a href="#timeline">Experience</a><a href="#skills">Expertise</a><a href="#cta">Contact</a></nav><button id="theme-toggle" class="icon-button" aria-label="Switch to dark mode" title="Change color theme" hidden><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor"/></svg></button></div></header>
<main id="main-content">
<section class="hero" id="hero"><div class="hero-inner wrap"><div class="hero-identity"><p class="intro">Lead Software Engineer</p><h1>Abdul Gaffar<br><em>Shaikh.</em></h1><p class="hero-stack">.NET · Python · Kubernetes</p><p class="hero-location">Capgemini · Mumbai, India</p></div><div class="hero-positioning"><p class="hero-statement">Modernising applications and building <em>backend and AI systems</em> for production.</p><p class="hero-bio">7.5+ years in financial services, combining hands-on engineering with architecture guidance and team mentoring.</p><div class="hero-links"><a class="button" href="{asset('output/pdf/resume.pdf')}" target="_blank" rel="noopener">Resume PDF <span aria-hidden="true">↗</span></a><a href="#impact">Work ↓</a>{external(linkedin,'LinkedIn')}</div></div></div></section>
<nav class="work-directory wrap" aria-label="Portfolio map"><a href="#project-mcp"><i aria-hidden="true">01</i><span>Knowledge & AI</span><small>Account knowledge foundation</small></a><a href="#engineering-delivery"><i aria-hidden="true">02</i><span>Engineering delivery</span><small>Modernisation through production</small></a><a href="#timeline"><i aria-hidden="true">03</i><span>Career progression</span><small>2018 engineer → 2026 lead</small></a></nav>
<section class="work-section wrap" id="impact" aria-label="Selected systems"><div class="work-overview">{stories}</div></section>
<section class="engineering-delivery" id="engineering-delivery"><span class="anchor-alias" id="work-index" aria-hidden="true"></span><div class="wrap"><header class="delivery-heading"><div><p class="eyebrow">Engineering practice</p><h2>Engineering delivery.</h2></div><p>Applications, APIs, and platforms carried from technical decisions through implementation and production.</p></header><p class="delivery-intro">Codebase reviews become practical delivery plans, with engineers guided through implementation and hands-on support focused on the changes and production blockers that decide whether a system succeeds.</p><div class="delivery-content">{engineering_delivery}</div></div></section>
<section class="experience-section wrap" id="timeline"><div class="section-heading"><h2>Experience.</h2></div><div class="experience-layout"><div class="experience-intro"><p>Hands-on engineering, with growing responsibility for architecture and delivery.</p>{external(linkedin,'View career on LinkedIn')}</div><div class="career-list">{career}</div></div></section>
<section class="expertise-section" id="skills"><div class="wrap"><div class="section-heading"><h2>Engineering range.</h2><p>Backend depth, with the cloud and AI experience to connect the wider system.</p></div><div class="skill-grid">{skills}</div><details class="credentials"><summary><span>Certifications <small>Azure · AI · Security · Duck Creek</small></span><span aria-hidden="true">+</span></summary><div class="cert-list">{certs}</div></details></div></section>
<section class="contact-section wrap" id="cta"><div class="contact-question"><p>Engineering roles &amp; collaboration.</p><h2>What are you trying<br>to make work<span>?</span></h2></div><div class="contact-brief"><p>Hiring for a lead engineering role or tackling a modernisation challenge? I’d be glad to compare notes.</p><div class="contact-actions"><a class="button" href="mailto:{email}">Start a conversation <span aria-hidden="true">↗</span></a><div class="email-row"><a href="mailto:{email}">{email}</a><button id="copy-email" class="icon-button" data-email="{email}" aria-label="Copy email address" title="Copy email address" hidden>⧉</button></div></div><span id="copy-status" role="status"></span></div></section>
</main>
<footer><div class="wrap footer-inner"><a class="footer-name" href="#hero">Abdul Gaffar Shaikh<span>Lead Software Engineer · Mumbai, India</span></a><div>{external(github,'GitHub')}{external(linkedin,'LinkedIn')}<a href="tel:{data['hero']['phone'].replace(' ','')}">Phone ↗</a></div><span>© {data['footer']['year']}</span></div></footer>
</body></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
print(f'Built index.html: {len(data["featuredWork"])} flagship and {sum(len(items) for _, _, items in delivery_groups)} engineering evidence rows.')
