

import { body, div, h, h1, button, img, span } from 'iblokz-snabbdom-helpers';
import { dispatch } from 'iblokz-state';

export default state => body('.app', [
  h1('hello world!'),
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
  button('.arrow-down')
]);