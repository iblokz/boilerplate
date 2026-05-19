import { body } from 'iblokz-snabbdom-helpers';
import header from './header';
import hero from './sections/hero';
import examples from './sections/examples';

export default state => body('.app', [
  header(state),
  hero(state),
  examples(state),
]);
