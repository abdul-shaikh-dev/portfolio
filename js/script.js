/* Native links and disclosures keep the complete page usable without JavaScript. */
const themeToggle = document.getElementById('theme-toggle');
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeToggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
}
try {
  const saved = localStorage.getItem('theme');
  if (saved === 'light' || saved === 'dark') applyTheme(saved);
} catch { /* Storage is optional. */ }
themeToggle.hidden = false;
themeToggle.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  try { localStorage.setItem('theme', next); } catch { /* Keep the session preference. */ }
});

const copyButton = document.getElementById('copy-email');
const copyStatus = document.getElementById('copy-status');
let copyTimer;
copyButton.hidden = false;
copyButton.addEventListener('click', async () => {
  clearTimeout(copyTimer);
  try {
    await navigator.clipboard.writeText(copyButton.dataset.email);
    copyStatus.textContent = 'Email address copied.';
  } catch {
    copyStatus.textContent = 'Select the email address above to copy it.';
  }
  copyTimer = setTimeout(() => { copyStatus.textContent = ''; }, 5000);
});

// Use the section at the reading position, not a section entering the bottom of the screen.
const header = document.querySelector('.site-header');
const mainLinks = [...document.querySelectorAll('.header-inner nav a')];
const workLinks = [...document.querySelectorAll('.work-navigation nav a')];
const sections = [...document.querySelectorAll('main > section[id]')];
const stories = [...document.querySelectorAll('.work-story'), document.getElementById('work-index')];
let scrollPending = false;
function sectionAtReadingPosition(elements, offset) {
  let active = null;
  for (const element of elements) {
    if (element.getBoundingClientRect().top <= offset) active = element.id;
  }
  return active;
}
function markCurrent(links, id) {
  for (const link of links) {
    if (link.hash === `#${id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}
function updateNavigation() {
  scrollPending = false;
  const offset = header.getBoundingClientRect().bottom + 40;
  const section = sectionAtReadingPosition(sections, offset);
  markCurrent(mainLinks, section === 'work-index' ? 'impact' : section);
  markCurrent(workLinks, sectionAtReadingPosition(stories, offset));
}
function scheduleNavigation() {
  if (scrollPending) return;
  scrollPending = true;
  requestAnimationFrame(updateNavigation);
}
window.addEventListener('scroll', scheduleNavigation, { passive: true });
window.addEventListener('resize', scheduleNavigation);
window.addEventListener('load', scheduleNavigation);
if (document.fonts?.ready) document.fonts.ready.then(scheduleNavigation);
updateNavigation();

// Preserve project links from earlier versions without retaining their popup interface.
function followLegacyLink() {
  const match = location.hash.match(/^#work-(mcp|modernisation|engineering-support|onboarding|informatica|api|browser|platform|migrations)$/);
  if (!match) return;
  const target = document.getElementById(`project-${match[1]}`);
  if (!target) return;
  history.replaceState(null, '', `#${target.id}`);
  target.scrollIntoView({ behavior: 'auto', block: 'start' });
}
window.addEventListener('hashchange', followLegacyLink);
followLegacyLink();
