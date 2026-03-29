import { fromEvent, filter, startWith } from "rxjs";

import { patch, zoom } from "../state";
import { dispatch } from 'iblokz-state';

export let stop = () => {};
export const start = ({state$}) => {
	let subs = [];
	// mouse movement
	subs.push(
		fromEvent(document, 'mousemove')
			.subscribe(ev => dispatch(patch(['viewport', 'mouse'], {
				x: ev.pageX,
				y: ev.pageY
			}))));

	subs.push(
		fromEvent(document, 'mousedown')
			.pipe(
        filter(ev => ev.target.tagName === 'CANVAS')
      )
			.subscribe(ev => dispatch(patch(['viewport', 'mouse'], {
				down: true
			}))));

	subs.push(
		fromEvent(document, 'mouseup')
			.subscribe(ev => dispatch(patch(['viewport', 'mouse'], {
				down: false
			}))));

	subs.push(
		fromEvent(window, 'resize')
			.pipe(
        startWith({})
      )
			.subscribe(ev => dispatch(patch(['viewport', 'screen'], {
				width: window.innerWidth,
				height: window.innerHeight,
				size: window.innerWidth >= 1200
					? 'xl'
					: window.innerWidth >= 992
						? 'lg'
						: window.innerWidth >= 768
							? 'md'
							: window.innerWidth >= 576
								? 'sm'
								: 'xs'
			}))));

	stop = () => subs.forEach(sub => sub.dispose());
};

export default {
  start,
  stop,
}