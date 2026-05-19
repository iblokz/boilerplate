export const scrollToSection = (selector, hash) => {
  const target = document.querySelector(selector);
  if (!target) return;
  target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  if (hash) history.pushState(null, '', hash);
};
