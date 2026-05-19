import { header, nav, a, div, select, option } from 'iblokz-snabbdom-helpers';
import { scrollToSection } from '../util/scroll';

const onHomeClick = ev => {
  ev.preventDefault();
  scrollToSection('#hero', '#hero');
};

const headerProgress = scrollY => Math.min(1, scrollY / 120);

export default state => {
  const { scroll, size } = state.viewport.screen;
  const scrollY = scroll?.y ?? 0;
  const progress = headerProgress(scrollY);
  const paddingTop = (
    scrollY > 28 || ['xs', 'sm'].includes(size)
      ? 8
      : 28 - scrollY
  ) + 'px';

  return header('.site-header.fixed-top', {
    class: { 'is-formed': progress > 0.05 },
    style: {
      paddingTop,
      '--header-progress': progress,
    },
  }, [
    nav('.site-nav', [
      a('.site-title[href="#hero"]', {
        on: { click: onHomeClick },
      }, 'iBlokz Boilerplate'),
      div('.site-controls', [
        select('.control.lang-select', {
          props: { disabled: true },
        }, [
          option({ props: { value: 'en', selected: true } }, 'EN'),
          option({ props: { value: 'bg' } }, 'BG'),
        ]),
        select('.control.theme-select', {
          props: { disabled: true },
        }, [
          option({ props: { value: 'dark', selected: true } }, 'Dark'),
          option({ props: { value: 'light' } }, 'Light'),
        ]),
      ]),
    ]),
  ]);
};
