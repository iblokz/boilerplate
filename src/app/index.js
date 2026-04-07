// libs
import { init, dispatch } from 'iblokz-state';
import { body, div, h, h1, button, patchStream, span } from 'iblokz-snabbdom-helpers';
import { toVNode } from 'snabbdom';
import { map } from 'rxjs';

// state
import { initial } from './state';
// services
import viewport from './services/viewport';
// ui
import ui from './ui';
// Initialize state (RxJS BehaviorSubject)
console.log(initial);
let state$ = init(initial);
// start services
viewport.start({ state$ });
// ui stream: state -> vnode
let vnode$ = state$.pipe(map(ui));
// patch vnode stream to dom
let patchSubscription = patchStream(vnode$, toVNode(document.body));

// state$.subscribe(console.log);

if (module.hot) {
  module.hot.dispose(function (data) {
    console.log('dispose');
    data.state = state$.getValue();
    // stop services
    viewport.stop();
    patchSubscription.unsubscribe();
    state$.complete();
    // clean up html structure from events
    document.body.innerHTML = document.body.innerHTML;
    console.log('dispose done');
  });
  module.hot.accept(function () {
    console.log('accept');
    // reload state
    dispatch(() => module.hot.data.state);
    // start services
    viewport.start({ state$ });
  });
}

