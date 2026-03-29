import { obj } from 'iblokz-data';

export const initial = {
  count: 0,
  viewport: {
    mouse: {
      x: 0,
      y: 0,
      down: false,
    },
    screen: {
      width: 0,
      height: 0,
    },
  },
}


export const patch = (path, value) => state => obj.patch(state, path, value);


export default {
  initial,
  patch,
}