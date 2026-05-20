import {
  section, h2, h3, p, div, span, ul, li, button,
  fieldset, legend, form, label, input, table, tr, td, th,
} from 'iblokz-snabbdom-helpers';
import { toData } from '../../util/form';
import { getThemeMeta } from '../../util/theme-meta';
import { themeClass } from '../../util/theme';

const exampleBlock = (title, children) =>
  div('.example-block', [
    h2(title),
    ...children,
  ]);

export default state => {
  const meta = getThemeMeta(state.themeFamily);
  const activeClass = themeClass(state);

  return section('#examples', [
    h2('Component examples'),
    p('.examples-lead', [
      'Switch theme family and mode in the header. Styles below use the active class ',
      span('.code', activeClass),
      ' on ',
      span('.code', '.app'),
      '.',
    ]),
    div('.example-block.theme-guide', [
      h2(`Theme: ${meta.label} (${state.themeMode})`),
      p('.theme-summary', meta.summary),
      h3('What changes in this family'),
      ul('.trait-list', meta.traits.map(trait => li(trait))),
      div('.token-preview', [
        span('.swatch', { attrs: { title: 'text' } }),
        span('.swatch.swatch-muted', { attrs: { title: 'muted' } }),
        span('.swatch.swatch-accent', { attrs: { title: 'accent / border' } }),
        span('.swatch.swatch-panel', { attrs: { title: 'panel bg' } }),
        span('.swatch.swatch-primary', { attrs: { title: 'primary btn' } }),
      ]),
    ]),
    exampleBlock('Typography', [
      p('.type-sample', [
        'The quick brown fox — ',
        span('.type-mono-hint', 'font comes from the active theme family.'),
      ]),
      p('.type-muted', 'Muted secondary line (labels, hints).'),
    ]),
    exampleBlock('Panels & depth', [
      p('.example-note', 'Panel shadow and border differ per family (offset vs inset vs flat).'),
      div('.panel-compare', [
        div('.mini-panel', [span('Panel A')]),
        div('.mini-panel', [span('Panel B')]),
      ]),
    ]),
    exampleBlock('Buttons', [
      div('.btn-row', [
        button('.btn.btn-primary', 'Primary'),
        button('.btn.btn-secondary', 'Secondary'),
        button('.btn.btn-primary[disabled]', { props: { disabled: true } }, 'Disabled'),
      ]),
    ]),
    exampleBlock('Form', [
      fieldset('.demo-form', [
        legend('Contact'),
        form('.form', {
          on: {
            submit: ev => {
              ev.preventDefault();
              console.log('form submit:', toData(ev.target));
            },
          },
        }, [
          div('.field', [
            label('Name'),
            input('[name="name"][type="text"][placeholder="Jane Doe"]'),
          ]),
          div('.field', [
            label('Email'),
            input('[name="email"][type="email"][placeholder="jane@example.com"]'),
          ]),
          div('.field', [
            button('.btn.btn-primary[type="submit"]', 'Submit'),
          ]),
        ]),
      ]),
    ]),
    exampleBlock('Table & tags', [
      p('.example-note', 'Row states and compact tags — common in inventory and thriftify-style apps.'),
      table('.demo-grid', [
        tr([
          th('Item'),
          th('Qty'),
          th('Status'),
        ]),
        tr([
          td('Widget A'),
          td('12'),
          td(span('.tag.tag-ok', 'OK')),
        ]),
        tr([
          td('Widget B'),
          td('3'),
          td(span('.tag.tag-warn', 'Low')),
        ]),
      ]),
    ]),
    exampleBlock('Toolbar', [
      p('.example-note', 'Inset controls like header search and tool rows.'),
      div('.demo-toolbar', [
        input('[type="search"][placeholder="Search…"]'),
        button('.btn.btn-secondary', 'Open'),
        button('.btn.btn-primary', 'Add'),
      ]),
    ]),
  ]);
};
