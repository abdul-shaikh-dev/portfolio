"""Build the static portfolio from data/data.json. Run: python scripts/build.py."""
from pathlib import Path
from html import escape
import json
from hashlib import sha256
from datetime import date, datetime

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/data.json').read_text(encoding='utf-8'))
e = escape
projects = [dict(item) for item in data['recentWork']]
by_id = {item['id']: item for item in projects}

def validate_content():
    if len(by_id) != len(projects):
        raise ValueError('recentWork contains duplicate project IDs')
    for key in data['featuredWork']:
        if key not in by_id:
            raise ValueError(f'featuredWork references unknown project: {key}')
        if not by_id[key].get('feature'):
            raise ValueError(f'Featured project has no feature presentation: {key}')
    delivery_ids = []
    for group in data['engineeringDelivery']['groups']:
        for key in group['projectIds']:
            if key not in by_id:
                raise ValueError(f'Engineering delivery references unknown project: {key}')
            if not by_id[key].get('transformation'):
                raise ValueError(f'Engineering project has no transformation narrative: {key}')
            delivery_ids.append(key)
    if len(delivery_ids) != len(set(delivery_ids)):
        raise ValueError('A project appears more than once in engineeringDelivery')

validate_content()
email = data['hero']['email']['user'] + '@' + data['hero']['email']['domain']
linkedin = data['hero']['linkedin']['url']
github = data['hero']['github']['url']

def career_start_date():
    starts = []
    for employer in data['career']['employers']:
        for role in employer['roles']:
            value = role['period'].split('—', 1)[0].strip()
            for pattern in ('%b %Y', '%B %Y'):
                try:
                    starts.append(datetime.strptime(value, pattern).date())
                    break
                except ValueError:
                    continue
    if not starts:
        raise ValueError('No parseable career start date found')
    return min(starts)

def experience_phrase(start, as_of=None):
    as_of = as_of or date.today()
    elapsed_months = max(0, (as_of.year - start.year) * 12 + as_of.month - start.month)
    full_years, remaining_months = divmod(elapsed_months, 12)
    if remaining_months >= 10:
        return f'nearly {full_years + 1} years'
    if remaining_months >= 3:
        return f'more than {full_years} years'
    return f'{full_years}+ years'

career_started = career_start_date()
experience_label = experience_phrase(career_started)
hero_bio = e(data['hero']['bio']).replace(
    e('{experience}'),
    f'<span data-experience-start="{career_started:%Y-%m}">{experience_label}</span>'
)

def tags(items):
    return '<ul class="tags" aria-label="Technologies">' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'

def external(url, label):
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>'

def technical_notes(p):
    if not p.get('detail') or p.get('showDetail') is False:
        return ''
    extra = f'<p>{e(p["notes"])}</p>' if p.get('notes') else ''
    label = p.get('detailLabel', 'Implementation notes')
    return f'<details class="technical-notes"><summary>{e(label)} <span aria-hidden="true">+</span></summary><div><p>{e(p["detail"])}</p>{extra}</div></details>'

def feature_details(p, narrative, capabilities):
    if not narrative:
        return capabilities + technical_notes(p)
    notes = f'<p>{e(p["notes"])}</p>' if p.get('notes') else ''
    implementation = f'<div class="feature-implementation"><p>{e(p["detail"])}</p>{notes}</div>' if p.get('detail') else ''
    return f'''<details class="feature-details"><summary>Platform scope &amp; implementation <span aria-hidden="true">+</span></summary><div><p class="feature-context">{e(narrative)}</p>{capabilities}{implementation}</div></details>'''

def walkthrough(figure):
    key = figure['key']
    title = figure['title']
    description = figure['description']
    return f'<figure class="system-figure walkthrough" data-walkthrough="{key}"><figcaption>{e(title)}<span>{e(description)}</span></figcaption><div class="walkthrough-interactive" hidden></div><p class="walkthrough-fallback">{e(description)} Full architecture and implementation details are available in the accompanying notes.</p></figure>'

def project_figure(p):
    figure = p.get('feature', {}).get('figure')
    if not figure:
        return ''
    if figure['type'] == 'walkthrough':
        return walkthrough(figure)
    raise ValueError(f'Unknown figure type: {figure["type"]}')

stories = ''
for key in data['featuredWork']:
    p = by_id[key]
    feature = p['feature']
    narrative = feature.get('narrative')
    context = '' if narrative else (f'<p>{e(p["context"])}</p>' if p.get('context') else '')
    story_summary = '' if narrative else f'<p>{e(p["summary"])}</p>'
    capabilities = '<div class="project-capabilities">' + ''.join(f'<div><h4>{e(c["title"])}</h4><p>{e(c["body"])}</p></div>' for c in p.get('capabilities', [])) + '</div>' if p.get('capabilities') else ''
    recognition = f'<p class="recognition">{e(p["recognition"])}</p>' if p.get('recognition') else ''
    result = f'<p class="story-result"><strong>Result</strong> {e(p["outcome"])}</p>'
    stories += f'''<section class="project-disclosure" id="project-{key}"><header class="project-summary"><div class="project-overview-title"><h3>{e(feature['displayTitle'])}</h3><span class="project-outcome">{e(feature['headlineOutcome'])}</span></div><p>{e(feature['overview'])}</p></header><article class="work-story story-{key}"><div class="story-layout">{project_figure(p)}<div class="story-copy">{context}{story_summary}{result}{recognition}{tags(p['tags'])}</div><div class="lead-details">{feature_details(p, narrative, capabilities)}</div></div></article></section>'''

delivery = data['engineeringDelivery']
delivery_columns = ''.join(f'<span>{e(label)}</span>' for label in delivery['columns'])
engineering_delivery = f'<div class="ledger-columns" aria-hidden="true">{delivery_columns}</div><div class="delivery-ledger">'
delivery_index = 0
for group in delivery['groups']:
    group_title_id = f'{group["id"]}-title'
    engineering_delivery += f'<section class="delivery-group" id="{e(group["id"])}" aria-labelledby="{e(group_title_id)}"><h3 class="delivery-group-title" id="{e(group_title_id)}">{e(group["label"])}</h3>'
    for item_index, key in enumerate(group['projectIds']):
        delivery_index += 1
        p = by_id[key]
        transformation = p['transformation']
        aliases = ''.join(f'<span class="anchor-alias" id="{e(alias)}" aria-hidden="true"></span>' for alias in p.get('aliases', []))
        badge_text = p.get('statusLabel') or ('Prototype' if p.get('status') == 'prototype' else '')
        badge = f'<span class="prototype-badge">{e(badge_text)}</span>' if badge_text else ''
        evidence = f'<p class="ledger-recognition">{e(p["recognition"])}</p>' if p.get('recognition') else ''
        prominence = p.get('prominence', '')
        project_class = f' delivery-project--{e(prominence)}' if prominence else ''
        prominence_label = f'<p class="delivery-scope">{e(p["prominenceLabel"])}</p>' if p.get('prominenceLabel') else ''
        delivery_status = e(p.get('deliveryStatus', 'Current state'))
        cells = ''.join(
            f'<div class="ledger-cell ledger-{name.lower()}"><span class="ledger-stage"><b>{stage_index:02}</b>{e(name)}</span><p>{e(transformation[name.lower()])}</p>{f"<span class=\"delivery-status\">{delivery_status}</span>" if name == "Running" else ""}</div>'
            for stage_index, name in enumerate(delivery['columns'][1:], start=1)
        )
        engineering_delivery += f'''<article class="delivery-project{project_class}" id="project-{key}">{aliases}<div class="ledger-identity"><span class="ledger-number">{delivery_index:02}</span>{prominence_label}<div class="delivery-title"><h4>{e(p["shortTitle"])}</h4>{badge}</div></div>{cells}{evidence}{technical_notes(p)}</article>'''
    engineering_delivery += '</section>'
engineering_delivery += '</div>'

portfolio_map = ''.join(
    f'<a href="{e(item["href"])}" aria-label="{e(item["title"])} — {e(item["subtitle"])}">'
    f'<span data-mobile-label="{e(item.get("mobileTitle", item["title"]))}">{e(item["title"])}</span></a>'
    for item in data['portfolioMap']
)

career_data = data['career']
career = '<div class="career-timeline">'
for employer_index, employer in enumerate(career_data['employers']):
    role_class = 'role-progression' if employer_index == 0 else 'earlier-progression'
    item_class = 'progression-role' if employer_index == 0 else 'earlier-role'
    contribution_class = 'role-contributions' if employer_index == 0 else 'earlier-contributions'
    roles = f'<div class="{role_class}">'
    for role in employer['roles']:
        highlighted = set(role.get('highlightBullets', []))
        contributions = f'<ul class="{contribution_class}">' + ''.join(
            f'<li{" class=\"role-highlight\"" if index in highlighted else ""}>{bullet}</li>'
            for index, bullet in enumerate(role['bullets'])
        ) + '</ul>'
        role_body = f'<h4>{e(role["title"])}</h4><div class="progression-contributions">{contributions}</div>' if employer_index == 0 else f'<div><h4>{e(role["title"])}</h4>{contributions}</div>'
        roles += f'<article class="{item_class}"><p class="role-date">{e(role["period"])}</p>{role_body}</article>'
    roles += '</div>'
    current_label = f'<span class="current-label">{e(employer["currentLabel"])}</span>' if employer.get('currentLabel') else ''
    employer_class = 'current-employer' if employer_index == 0 else 'earlier-employer'
    career += f'''<article class="employer {employer_class}"><header class="employer-heading"><p class="role-date">{e(employer['period'])}</p><div><h3>{e(employer['name'])}</h3><p class="employer-meta"><span>{e(employer['location'])}</span><span>{e(employer['context'])}</span></p></div>{current_label}</header>{roles}</article>'''
career += '</div>'
education = career_data['education']
career += f'''<div class="education"><span>{e(education['label'])}</span><div><strong>{e(education['title'])}</strong><p>{e(education['organisation'])} · {e(education['period'])}</p></div></div>'''

skills = ''.join(f'<article class="skill-item"><h3><a href="{e(x["href"])}">{e(x["name"])} <span aria-hidden="true">↗</span></a></h3><p>{e(x["desc"])}</p></article>' for x in data['skills'])
certs = ''
for c in data['certs']:
    content = f'<span class="cert-code">{e(c["badge"])}</span><span>{e(c["name"].replace("Microsoft Certified: ",""))}</span><span class="cert-year">{e(c["year"])}</span>'
    certs += external(c['url'],content) if c.get('url') else '<div>'+content+'</div>'

navigation = ''.join(f'<a href="{e(item["href"])}">{e(item["label"])}</a>' for item in data['navigation'])
hero = data['hero']
expertise = data['expertiseSection']
contact = data['contactSection']
contact_title = '<br>'.join(e(line) for line in contact['title'])

def asset(path):
    resource = ROOT / path
    content = resource.read_bytes()
    if resource.suffix in {'.css', '.js'}:
        content = content.replace(b'\r\n', b'\n')
    version = sha256(content).hexdigest()[:10]
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
<header class="site-header"><div class="header-inner wrap"><a class="wordmark" href="#hero" aria-label="{e(data['footer']['name'])}, home">ags<span>/</span></a><nav aria-label="Main navigation">{navigation}</nav><button id="theme-toggle" class="icon-button" aria-label="Switch to dark mode" title="Change color theme" hidden><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor"/></svg></button></div></header>
<main id="main-content">
<section class="hero" id="hero"><div class="hero-inner wrap"><div class="hero-identity"><p class="intro">{e(hero['role'])}</p><h1>{e(hero['nameLine'])}<br><em>{e(hero['accentLine'])}</em></h1><p class="hero-stack">{e(hero['stack'])}</p><p class="hero-location">{e(hero['location'])}</p></div><div class="hero-positioning"><p class="hero-statement">{e(hero['statement']['before'])} <em>{e(hero['statement']['emphasis'])}</em> {e(hero['statement']['after'])}</p><p class="hero-bio">{hero_bio}</p><div class="hero-links"><a class="button" href="{asset('output/pdf/resume.pdf')}" target="_blank" rel="noopener">{e(hero['resumeLabel'])} <span aria-hidden="true">↗</span></a><a href="#impact">{e(hero['workLabel'])}</a>{external(linkedin,e(hero['linkedinLabel']))}</div></div></div></section>
<nav class="chapter-nav" aria-label="Portfolio chapters"><div class="wrap">{portfolio_map}</div></nav>
<section class="work-section wrap" id="impact" aria-label="Selected systems"><div class="work-overview">{stories}</div></section>
<section class="engineering-delivery" id="engineering-delivery"><span class="anchor-alias" id="work-index" aria-hidden="true"></span><div class="wrap"><header class="delivery-heading"><div><p class="eyebrow">{e(delivery['eyebrow'])}</p><h2>{e(delivery['title']).replace(chr(10), '<br>')}</h2></div><p>{e(delivery['intro'])}</p></header><div class="delivery-content">{engineering_delivery}</div></div></section>
<section class="experience-section wrap" id="timeline"><div class="section-heading"><h2>{e(career_data['title'])}</h2></div><div class="experience-layout"><div class="experience-intro"><p>{e(career_data['intro'])}</p>{external(linkedin,e(career_data['linkLabel']))}</div><div class="career-list">{career}</div></div></section>
<section class="expertise-section" id="skills"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">{e(expertise['eyebrow'])}</p><h2>{e(expertise['title'])}</h2></div><p>{e(expertise['intro'])}</p></div><div class="skill-grid">{skills}</div><details class="credentials"><summary><span>{e(expertise['credentialsLabel'])} <small>{e(expertise['credentialsSummary'])}</small></span><span aria-hidden="true">+</span></summary><div class="cert-list">{certs}</div></details></div></section>
<section class="contact-section wrap" id="cta"><div class="contact-question"><p>{e(contact['eyebrow'])}</p><h2>{contact_title}<span>?</span></h2></div><div class="contact-brief"><p>{e(contact['body'])}</p><div class="contact-actions"><a class="button" href="mailto:{email}">{e(contact['buttonLabel'])} <span aria-hidden="true">↗</span></a><div class="email-row"><a href="mailto:{email}">{email}</a><button id="copy-email" class="icon-button" data-email="{email}" aria-label="Copy email address" title="Copy email address" hidden>⧉</button></div></div><span id="copy-status" role="status"></span></div></section>
</main>
<footer><div class="wrap footer-inner"><a class="footer-name" href="#hero">{e(data['footer']['name'])}<span>{e(data['footer']['meta'])}</span></a><div>{external(github,'GitHub')}{external(linkedin,'LinkedIn')}<a href="tel:{data['hero']['phone'].replace(' ','')}">Phone ↗</a></div><span>© {data['footer']['year']}</span></div></footer>
</body></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
print(f'Built index.html: {len(data["featuredWork"])} flagship and {sum(len(group["projectIds"]) for group in delivery["groups"])} engineering evidence rows.')
