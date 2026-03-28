import { init, dispatch } from 'iblokz-state';
import { body, div, h, button, patchStream } from 'iblokz-snabbdom-helpers';
import { toVNode } from 'snabbdom';
import { map } from 'rxjs';

// Initialize state (RxJS BehaviorSubject)
const state$ = init({ count: 0 });

// View: state -> vnode
function view(state) {
  return body('.app', [
    h('h1', 'iBlokz Boilerplate'),
    h('p', `Count: ${state.count}`),
    button('.btn', {
      on: {
        click: () => dispatch(s => ({ ...s, count: s.count + 1 })),
      },
    }, 'Increment'),
  ]);
}

// console.log('state$', state$);

if (module.hot) {
  module.hot.dispose(function (data) {
     data.state = state$.getValue();
  });

  module.hot.accept(function () {
    state$.next(module.hot.data.state);
  });
}

// Stream of vnodes from state, patched to DOM
const vnode$ = state$.pipe(map(view));
patchStream(vnode$, toVNode(document.body));
