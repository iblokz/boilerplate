import { init, dispatch } from 'iblokz-state';
import { body, div, h, h1, button, patchStream, span } from 'iblokz-snabbdom-helpers';
import { toVNode } from 'snabbdom';
import { map } from 'rxjs';

// Initialize state (RxJS BehaviorSubject)
let state$ = init({ count: 0 });


// View: state -> vnode
let view = (state) => {
  return body('.app', [
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
  ]);
}

// console.log('state$', state$);

let vnode$ = state$.pipe(map(view));
let patchSubscription = patchStream(vnode$, toVNode(document.body));

if (module.hot) {
  module.hot.dispose(function (data) {
    console.log('dispose');
    data.state = state$.getValue();
    patchSubscription.unsubscribe();
    state$.complete();
    // clean up html structure from events
    document.body.innerHTML = document.body.innerHTML;
    console.log('dispose done');
  });
  module.hot.accept(function () {
    console.log('accept');
    dispatch(() => module.hot.data.state);
  });
}
