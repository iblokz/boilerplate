// libs
import { init, dispatch } from 'iblokz-state';
import { patchStream } from 'iblokz-snabbdom-helpers';
import { toVNode } from 'snabbdom';
import { map, distinctUntilChanged } from 'rxjs';

// state
import { initial } from './state';
import { serializeTheme } from './util/theme';
// services
import viewport from './services/viewport';
// ui
import ui from './ui';

let state$ = init(initial);
viewport.start({ state$ });

state$
  .pipe(
    map(s => serializeTheme(s)),
    distinctUntilChanged()
  )
  .subscribe(theme => localStorage.setItem('boilerplate-theme', theme));

let vnode$ = state$.pipe(map(ui));
let patchSubscription = patchStream(vnode$, toVNode(document.body));

if (module.hot) {
  module.hot.dispose(function (data) {
    data.state = state$.getValue();
    viewport.stop();
    patchSubscription.unsubscribe();
    state$.complete();
    document.body.innerHTML = document.body.innerHTML;
  });
  module.hot.accept(function () {
    dispatch(() => module.hot.data.state);
    viewport.start({ state$ });
  });
}
