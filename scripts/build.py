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
    'modernisation': '',
    'engineering-support': '<section class="delivery-changes" aria-labelledby="delivery-changes-title"><h4 id="delivery-changes-title">What changed</h4><dl><div><dt>Application engineering</dt><dd>Restructured the Python codebase and resolved application and Linux runtime issues.</dd></div><div><dt>Internal model delivery</dt><dd>Packaged the embedding model through the internal artifact repository to work within the firm’s network restrictions.</dd></div><div><dt>Production deployment</dt><dd>Adopted established GitLab CI builds, resolved deployment blockers, and brought the application into production on Rancher.</dd></div></dl></section>',

}

headings = {
    'mcp': 'A shared foundation<br>for enterprise knowledge.',
    'modernisation': 'Modernising an<br>infrastructure dashboard.',
    'engineering-support': 'AI adoption and<br>production delivery.'
}
stories = ''
project_summaries = {
    'mcp': ('Knowledge-management template', 'Document extraction, enterprise search, and controlled access for coding agents.'),
    'modernisation': ('Infrastructure dashboard', 'Leading the move from a coupled Python and React implementation to maintainable services.'),
    'engineering-support': ('AI clause extraction', 'Restructured the application and resolved the runtime and deployment issues blocking production.'),
}
project_summaries['delivery'] = ('Application modernisation', 'Service upgrades, backend APIs, and AI applications carried through to production.')
project_outcomes = {'mcp':'A shared foundation for enterprise knowledge', 'delivery':'Architecture, implementation & production delivery'}
figures['delivery'] = ''
for key in data['featuredWork']:
    p = by_id[key]
    title, overview = project_summaries[key]
    context = f'<p>{e(p["context"])}</p>' if p.get('context') else ''
    capabilities = '<div class="project-capabilities">' + ''.join(f'<div><h4>{e(c["title"])}</h4><p>{e(c["body"])}</p></div>' for c in p.get('capabilities', [])) + '</div>' if p.get('capabilities') else ''
    recognition = f'<p class="recognition">{e(p["recognition"])}</p>' if p.get('recognition') else ''
    result = f'<p class="story-result"><strong>Result</strong> {e(p["outcome"])}</p>'
    examples = ''
    if key == 'delivery':
        context = ''
        result = ''
        examples = '<div class="delivery-examples"><h4>Selected deliveries</h4>'
        for example_id in ['service-modernisation', 'modernisation', 'engineering-support']:
            example = by_id[example_id]
            evidence = '<p class="recognition">' + e(example['recognition']) + '</p>' if example.get('recognition') else ''
            examples += f'<article class="delivery-example" id="project-{example_id}"><header><h5>{e(example["shortTitle"])}</h5><p class="delivery-preview">{e(example["previewOutcome"])}</p></header><div><p>{e(example.get("context") or example["summary"])}</p>{figures.get(example_id, "")}{evidence}{tags(example["tags"])}{technical_notes(example)}</div></article>'
        examples += '<p class="delivery-links">Related backend work: <a href="#project-dotnet-api">.NET business-data API ↗</a> · <a href="#project-api">Python financial-data API ↗</a> · <a href="#project-api-performance">API memory optimisation ↗</a></p></div>'
    stories += f'''<section class="project-disclosure" id="project-{key}"><header class="project-summary"><div class="project-overview-title"><h3>{title}</h3><span class="project-outcome">{e(project_outcomes[key])}</span></div><p>{overview}</p></header><article class="work-story story-{key}"><div class="story-layout"><div class="story-copy">{context}<p>{e(p['summary'])}</p>{result}{recognition}{tags(p['tags'])}</div>{examples}{figures[key]}<div class="lead-details">{capabilities}{technical_notes(p)}</div></div></article></section>'''

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
        return_link = '<a class="return-to-deliveries" href="#project-delivery">Back to application modernisation ↑</a>' if key in ['dotnet-api', 'api', 'api-performance'] else ''
        supporting += f'<article class="supporting-project" id="project-{key}"><div class="supporting-title"><h4>{e(p["shortTitle"])}</h4>{badge}</div><p>{e(p["summary"])}</p>{tags(p["tags"])}{technical_notes(p)}{return_link}</article>'
    supporting += '</div></div>'

current = data['timeline'][0]
role_progression = '<div class="role-progression">'
for role in current['roles']:
    bullets = role['bullets']
    contributions = '<ul class="role-contributions">' + ''.join('<li>'+b+'</li>' for b in bullets) + '</ul>'
    role_progression += f'<article class="progression-role"><p class="role-date">{e(role["period"])}</p><h4>{e(role["title"])}</h4><p class="progression-title">{e(role["designation"])}</p><div class="progression-contributions">{contributions}</div></article>'
role_progression += '</div>'
earlier = ''
for role in data['timeline'][1:-1]:
    earlier += f'<div class="earlier-role"><h4>{e(role["title"])}</h4><p class="role-date">{e(role["period"])}</p><ul>'+''.join('<li>'+b+'</li>' for b in role['bullets'])+'</ul></div>'
career = f'''<article class="employer current-employer"><div class="employer-heading"><div><p class="role-date">May 2023 — Present</p><h3>Capgemini</h3><p>Mumbai, India</p></div><span class="current-label">Current</span></div>{role_progression}<p class="role-summary">Backend modernisation, production AI, and engineering automation for a global investment bank.</p></article><article class="employer"><div class="employer-heading"><div><p class="role-date">October 2018 — May 2023</p><h3>Associate to Senior Software Engineer</h3><p>Accenture · Mumbai</p></div></div><p class="role-summary">Progressed through three engineering roles in financial services, working on insurance platforms, API modernisation, Azure integrations, and document automation.</p><details class="career-details"><summary>Earlier roles & contributions <span aria-hidden="true">+</span></summary>{earlier}</details></article><div class="education"><span>Education</span><div><strong>{e(data['timeline'][-1]['title'])}</strong><p>{e(data['timeline'][-1]['org'])} · 2015–2018</p></div></div>'''

skills = ''.join(f'<article class="skill-item"><h3>{e(x["name"])}</h3><p>{e(x["desc"])}</p></article>' for x in data['skills'])
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
<section class="hero" id="hero"><div class="hero-inner wrap"><div class="hero-identity"><p class="intro">Lead Software Engineer</p><h1>Abdul Gaffar<br><em>Shaikh.</em></h1><p class="hero-stack">.NET · Python · Kubernetes</p><p class="hero-location">Capgemini · Mumbai, India</p></div><div class="hero-positioning"><p class="hero-statement">I lead application modernisation and build <em>backend and AI systems</em> for production.</p><p class="hero-bio">7.5+ years in financial services, combining hands-on engineering with architecture guidance and team mentoring.</p><div class="hero-links"><a class="button" href="{asset('output/pdf/resume-revised.pdf')}" target="_blank" rel="noopener">Resume PDF <span aria-hidden="true">↗</span></a><a href="#impact">Selected work ↓</a>{external(linkedin,'LinkedIn')}</div></div><ul class="hero-evidence" aria-label="Delivery highlights"><li><strong>Enterprise knowledge</strong><span>Built the knowledge-management foundation adopted across the client account.</span></li><li><strong>Application modernisation</strong><span>Moved .NET services from Windows hosting to Kubernetes and delivered production AI applications.</span></li></ul></div></section>
<section class="work-section wrap" id="impact"><div class="work-header"><h2>Selected work <span>/ 01—02</span></h2></div><div class="work-overview">{stories}</div></section>
<section class="supporting-section" id="work-index"><div class="wrap"><header class="supporting-heading"><h2>The rest of the workbench.</h2><span>Backend APIs / performance / runtimes / tooling</span></header><div class="supporting-content">{supporting}</div></div></section>
<section class="experience-section wrap" id="timeline"><div class="section-heading"><h2>Experience.</h2></div><div class="experience-layout"><div class="experience-intro"><p>Hands-on engineering, with growing responsibility for architecture and delivery.</p>{external(linkedin,'View career on LinkedIn')}</div><div class="career-list">{career}</div></div></section>
<section class="expertise-section" id="skills"><div class="wrap"><div class="section-heading"><h2>What I work with.</h2><p>Backend depth, with the cloud and AI experience to connect the wider system.</p></div><div class="skill-grid">{skills}</div><details class="credentials"><summary><span>Certifications <small>Azure · AI · Security · Duck Creek</small></span><span aria-hidden="true">+</span></summary><div class="cert-list">{certs}</div></details></div></section>
<section class="contact-section wrap" id="cta"><div class="contact-question"><p>Engineering roles &amp; collaboration.</p><h2>What are you trying<br>to make work<span>?</span></h2></div><div class="contact-brief"><p>Hiring for a lead engineering role, modernising an application, or working through a production challenge? Start with the problem.</p><ol class="contact-prompts" aria-label="A useful engineering brief"><li><span>Context</span><small>What exists today</small></li><li><span>Constraint</span><small>What is getting in the way</small></li><li><span>Outcome</span><small>What good looks like</small></li></ol><div class="contact-actions"><a class="button" href="mailto:{email}">Send me the context <span aria-hidden="true">↗</span></a><div class="email-row"><a href="mailto:{email}">{email}</a><button id="copy-email" class="icon-button" data-email="{email}" aria-label="Copy email address" title="Copy email address" hidden>⧉</button></div></div><span id="copy-status" role="status"></span></div></section>
</main>
<footer><div class="wrap footer-inner"><a class="footer-name" href="#hero">Abdul Gaffar Shaikh<span>Lead Software Engineer · Mumbai, India</span></a><div>{external(github,'GitHub')}{external(linkedin,'LinkedIn')}<a href="tel:{data['hero']['phone'].replace(' ','')}">Phone ↗</a></div><span>© {data['footer']['year']}</span></div></footer>
</body></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
print(f'Built index.html: {len(data["featuredWork"])} highlights with supporting delivery examples.')
