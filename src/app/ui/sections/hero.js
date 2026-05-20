import { section, h2, div, button, span, img, p } from 'iblokz-snabbdom-helpers';
import { dispatch } from 'iblokz-state';
import { scrollToSection } from '../../util/scroll';

export default state => {
  const { height, scroll } = state.viewport.screen;
  const scrollY = scroll?.y ?? 0;
  const minHeight = Math.max(height - 28, 0);

  return section('#hero', {
    style: { minHeight: `${minHeight}px` },
  }, [
    // h1({
    //   style: {
    //     transform: `translate(-50%, calc(-50% + ${scrollY * 0.15}px))`,
    //     opacity: Math.max(0.3, 1 - scrollY / (height * 0.6 || 1)),
    //   },
    // }, 'hello world!'),
    div('.counter', [
      button('.btn', {
        on: {
          click: () => dispatch(s => ({ ...s, count: s.count - 1 })),
        },
      }, '-'),
      span('.counter-value', `${state.count}`),
      button('.btn', {
        on: {
          click: () => dispatch(s => ({ ...s, count: s.count + 1 })),
        },
      }, '+'),
    ]),
    button('.arrow-down', {
      attrs: { 'aria-label': 'Scroll to examples' },
      on: {
        click: ev => {
          ev.preventDefault();
          scrollToSection('#examples', '#examples');
        },
      },
    }),
  ]);
};
