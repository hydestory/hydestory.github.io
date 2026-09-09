const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

// The mail service and DOM are boundary doubles; execute the real submit handler.
function formHarness(send, values = { from_name: 'Test', from_email: 'test@example.com', subject: '技術交流', message: 'A test message' }) {
  let submit, resets = 0;
  const button = { disabled: false, textContent: '送出訊息' };
  const status = { dataset: {}, textContent: '' };
  const form = { reportValidity: () => true, addEventListener: (_, handler) => { submit = handler; }, reset: () => { resets++; } };
  const elements = { 'contact-form': form, 'submit-btn': button, 'form-status': status };
  const context = vm.createContext({
    document: { documentElement: { classList: { add() {} } }, querySelector: () => null,
      querySelectorAll: () => [], getElementById: id => elements[id] },
    window: { emailjs: { init() {}, send } },
    FormData: class { [Symbol.iterator]() { return Object.entries(values)[Symbol.iterator](); } },
    setTimeout, clearTimeout,
  });
  vm.runInContext(readFileSync('static/js/site.js', 'utf8'), context);
  return { submit: () => submit({ preventDefault() {} }), status, button, resets: () => resets };
}

test('failed sends preserve entered text, show an error, and allow retry', async () => {
  const form = formHarness(async () => { throw new Error('offline'); });
  await form.submit();
  assert.equal(form.resets(), 0);
  assert.equal(form.status.dataset.state, 'error');
  assert.equal(form.button.disabled, false);
});

test('the form clears only after the mail service confirms success', async () => {
  let confirm;
  const form = formHarness(() => new Promise(resolve => { confirm = resolve; }));
  const pending = form.submit();
  await Promise.resolve();
  assert.equal(form.resets(), 0);
  assert.equal(form.button.disabled, true);
  confirm({ status: 200 });
  await pending;
  assert.equal(form.resets(), 1);
  assert.equal(form.status.dataset.state, 'success');
  assert.equal(form.button.disabled, false);
});

test('repeated submits cannot send a second message while one is pending', async () => {
  let sends = 0, confirm;
  const form = formHarness(() => { sends++; return new Promise(resolve => { confirm = resolve; }); });
  const pending = form.submit();
  await form.submit();
  assert.equal(sends, 1);
  confirm({ status: 200 });
  await pending;
});

test('whitespace-only names or messages never reach the mail service', async () => {
  let sends = 0;
  const form = formHarness(async () => { sends++; }, { from_name: ' ', message: ' ' });
  await form.submit();
  assert.equal(sends, 0);
  assert.equal(form.status.dataset.state, 'error');
  assert.equal(form.resets(), 0);
});
