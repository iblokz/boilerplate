import {
  section, h2, div, button,
  fieldset, legend, form, label, input,
} from 'iblokz-snabbdom-helpers';
import { toData } from '../../util/form';

export default () => section('#examples', [
  h2('Examples'),
  div('.example-block', [
    h2('Buttons'),
    div('.btn-row', [
      button('.btn.btn-primary', 'Primary'),
      button('.btn.btn-secondary', 'Secondary'),
      button('.btn.btn-primary[disabled]', { props: { disabled: true } }, 'Disabled'),
    ]),
  ]),
  div('.example-block', [
    h2('Form'),
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
          input('[name="name"][type="text"]'),
        ]),
        div('.field', [
          label('Email'),
          input('[name="email"][type="email"]'),
        ]),
        div('.field', [
          button('.btn.btn-primary[type="submit"]', 'Submit'),
        ]),
      ]),
    ]),
  ]),
]);
