/* ─── RENDER FUNCTIONS ─── */

function renderMeta(meta) {
  document.title = meta.title;
  var desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute('content', meta.description);
  var ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) ogTitle.setAttribute('content', meta.ogTitle);
  var ogDesc = document.querySelector('meta[property="og:description"]');
  if (ogDesc) ogDesc.setAttribute('content', meta.ogDescription);
}

function renderHero(hero, chips) {
  var addr = hero.email.user + '@' + hero.email.domain;
  var chipsHtml = chips.map(function(c) {
    return '<span class="chip' + (c.hot ? ' hot' : '') + '">' + c.label + '</span>';
  }).join('');

  var html =
    '<div class="eyebrow">' +
      '<span class="status-dot"></span>' +
      hero.eyebrow +
    '</div>' +
    '<h1>' + hero.name + ' <span class="accent">' + hero.accent + '</span></h1>' +
    '<p class="tagline">' + hero.tagline + '</p>' +
    '<div class="chips">' + chipsHtml + '</div>' +
    '<div class="contact-row">' +
      '<a class="contact-link" href="mailto:' + addr + '">' +
        '<svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>' +
        addr +
      '</a>' +
      '<a class="contact-link" href="' + hero.linkedin.url + '" target="_blank" rel="noopener">' +
        '<svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14m-.5 15.5v-5.3a3.26 3.26 0 00-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 011.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 001.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 00-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>' +
        hero.linkedin.label +
      '</a>' +
      '<a class="contact-link" href="' + hero.github.url + '" target="_blank" rel="noopener">' +
        '<svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>' +
        hero.github.label +
      '</a>' +
      '<a class="contact-link" href="tel:' + hero.phone.replace(/\s/g, '') + '">' +
        '<svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>' +
        hero.phone +
      '</a>' +
    '</div>' +
    '<div class="scroll-hint" style="opacity:0; animation: fadeUp 0.7s ease forwards 1.1s;">SCROLL TO EXPLORE</div>';

  document.getElementById('hero-content').innerHTML = html;
}

function renderTimeline(entries) {
  var html = '';
  entries.forEach(function(entry) {
    var dotClass = 'tl-dot' + (entry.currentBadge ? ' current' : '');
    var periodHtml = entry.period;
    if (entry.periodNow) {
      periodHtml += ' <span class="now">Present</span>';
    }
    var orgHtml = entry.org;
    if (entry.currentBadge) {
      orgHtml += ' <span class="current-badge">CURRENT</span>';
    }
    if (entry.client) {
      orgHtml += ' <span class="client-tag">' + entry.client + '</span>';
    }

    html += '<div class="tl-entry reveal">';
    html += '<div class="' + dotClass + '"></div>';
    html += '<div class="tl-period">' + periodHtml + '</div>';
    html += '<div class="tl-title">' + entry.title + '</div>';
    html += '<div class="tl-org">' + orgHtml + '</div>';

    if (entry.bullets && entry.bullets.length > 0) {
      html += '<div class="tl-card"><ul class="tl-items">';
      entry.bullets.forEach(function(bullet) {
        html += '<li>' + bullet + '</li>';
      });
      html += '</ul>';

      if (entry.tags && entry.tags.length > 0) {
        html += '<div class="tech-tags">';
        entry.tags.forEach(function(tag) {
          var colorClass = tag.color === 'mint' ? '' : ' ' + tag.color;
          html += '<span class="tech-tag' + colorClass + '">' + tag.label + '</span>';
        });
        html += '</div>';
      }

      html += '</div>';
    }

    html += '</div>';
  });

  document.getElementById('timeline-entries').innerHTML = html;
}

function renderImpact(items) {
  var html = '';
  items.forEach(function(item) {
    html += '<div class="impact-card reveal">' +
      '<span class="impact-card-icon" aria-hidden="true">' + item.icon + '</span>' +
      '<div class="impact-card-title">' + item.title + '</div>' +
      '<div class="impact-card-body">' + item.body + '</div>' +
    '</div>';
  });
  document.getElementById('impact-cards').innerHTML = html;
}

function renderSkills(items) {
  var html = '';
  items.forEach(function(item) {
    var badgeHtml = item.badge ? ' <span class="exp-badge">' + item.badge + '</span>' : '';
    html += '<div class="skill-block reveal">' +
      '<span class="skill-icon" aria-hidden="true">' + item.icon + '</span>' +
      '<div class="skill-name">' + item.name + badgeHtml + '</div>' +
      '<div class="skill-desc">' + item.desc + '</div>' +
    '</div>';
  });
  document.getElementById('skills-grid').innerHTML = html;
}

function renderCerts(items) {
  var html = '';
  items.forEach(function(item) {
    var nameHtml = item.url
      ? '<a class="cert-name cert-link" href="' + item.url + '" target="_blank" rel="noopener">' + item.name + ' <span class="cert-verify">↗ verify</span></a>'
      : '<span class="cert-name">' + item.name + '</span>';
    html += '<div class="cert-row reveal">' +
      '<span class="cert-badge">' + item.badge + '</span>' +
      nameHtml +
      '<span class="cert-year">' + item.year + '</span>' +
    '</div>';
  });
  document.getElementById('certs-list').innerHTML = html;
}

function renderCTA(cta, email, linkedin) {
  var addr = email.user + '@' + email.domain;
  var html =
    '<div class="section-label section-label-centered">Get In Touch</div>' +
    '<h2 class="cta-heading">' + cta.heading + '</h2>' +
    '<p class="cta-body">' + cta.body + '</p>' +
    '<div class="cta-buttons">' +
      '<a href="mailto:' + addr + '" class="btn-primary">EMAIL ME</a>' +
      '<a href="' + linkedin.url + '" target="_blank" rel="noopener" class="btn-outline">LINKEDIN</a>' +
    '</div>';
  document.getElementById('cta-content').innerHTML = html;
}

function renderFooter(footer) {
  var html =
    '<div>' +
      '<div class="footer-name">' + footer.name + '</div>' +
      '<div class="footer-meta">' + footer.meta + '</div>' +
    '</div>' +
    '<div class="footer-meta">' + footer.year + '</div>';
  document.getElementById('footer-content').innerHTML = html;
}

/* ─── INTERACTIVE INIT FUNCTIONS ─── */

function initNavigation() {
  document.querySelectorAll('[data-target]').forEach(function(el) {
    function navigate() {
      document.getElementById(el.dataset.target).scrollIntoView({ behavior: 'smooth' });
    }
    el.addEventListener('click', navigate);
    el.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); navigate(); }
    });
  });

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
  }, { threshold: 0, rootMargin: '0px 0px -50% 0px' });

  sections.forEach(function(id) {
    var el = document.getElementById(id);
    if (el) observer.observe(el);
  });
}

function initThemeToggle() {
  var toggle = document.getElementById('theme-toggle');
  var html = document.documentElement;

  function getInitialTheme() {
    try { var saved = localStorage.getItem('theme'); if (saved) return saved; } catch(e) {}
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  var theme = getInitialTheme();
  if (theme === 'light') {
    html.setAttribute('data-theme', 'light');
    toggle.setAttribute('aria-label', 'Switch to dark mode');
  }

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
}

function initBackToTop() {
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
    btn.classList.toggle('visible', window.scrollY > window.innerHeight);
    if (!hintHidden && window.scrollY > 50 && scrollHint) {
      scrollHint.style.opacity = '0';
      hintHidden = true;
    }
  }, { passive: true });
}

function initScrollReveal() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.reveal').forEach(function(el) { el.classList.add('visible'); });
    return;
  }

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

  document.querySelectorAll('.reveal').forEach(function(el) { observer.observe(el); });
}

function initTimelineSpine() {
  var timeline = document.querySelector('.timeline');
  var svg = document.querySelector('.timeline-spine');
  if (!timeline || !svg || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function initSpine() {
    var h = timeline.offsetHeight;
    svg.setAttribute('viewBox', '0 0 2 ' + h);
    svg.setAttribute('height', h);
    svg.setAttribute('width', '2');
    svg.innerHTML = '<defs><linearGradient id="spineGrad" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0%" stop-color="var(--mint-bd)"/>' +
      '<stop offset="70%" stop-color="var(--border)"/>' +
      '<stop offset="100%" stop-color="transparent"/>' +
      '</linearGradient></defs>' +
      '<path d="M1 0 V' + h + '" stroke="url(#spineGrad)" stroke-width="1" fill="none" id="spine-path"/>';
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
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function() { initSpine(); onScroll(); });
}

function initParticles() {
  var canvas = document.getElementById('particles');
  if (!canvas) return;
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
}

/* ─── MAIN INIT ─── */

async function init() {
  try {
    var response = await fetch('data/data.json');
    if (!response.ok) throw new Error('HTTP ' + response.status);
    var data = await response.json();

    renderMeta(data.meta);
    renderHero(data.hero, data.chips);
    renderTimeline(data.timeline);
    renderImpact(data.impact);
    renderSkills(data.skills);
    renderCerts(data.certs);
    renderCTA(data.cta, data.hero.email, data.hero.linkedin);
    renderFooter(data.footer);

    initNavigation();
    initThemeToggle();
    initBackToTop();
    initScrollReveal();
    initTimelineSpine();
    initParticles();
  } catch (err) {
    console.error('Portfolio failed to load:', err);
    var hero = document.getElementById('hero-content');
    if (hero) {
      hero.innerHTML =
        '<div class="eyebrow"><span class="status-dot"></span>Senior Software Engineer &middot; 7+ Years</div>' +
        '<h1>ABDUL GAFFAR <span class="accent">SHAIKH</span></h1>' +
        '<p class="tagline" style="margin-top:28px">Portfolio data failed to load. ' +
        'Please serve this project via a local HTTP server (e.g. <code>npx serve .</code>) rather than opening the HTML file directly.</p>';
    }
    initThemeToggle();
  }
}

init();