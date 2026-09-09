document.documentElement.classList.add('js');

const menu = document.querySelector('.menu-toggle');
const nav = document.getElementById('site-nav');
if (menu && nav) {
  const closeMenu = () => { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); }
  });
}
document.querySelectorAll('[data-current-year]').forEach(element => { element.textContent = new Date().getFullYear(); });

// Load the mail SDK only when the visitor uses the contact form.
let mailSdkPromise;
function loadMailSdk() {
  if (window.emailjs) return Promise.resolve(window.emailjs);
  if (!mailSdkPromise) {
    mailSdkPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      let timer;
      const fail = () => { clearTimeout(timer); script.remove(); mailSdkPromise = null; reject(new Error('Mail service unavailable')); };
      script.src = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js';
      script.onload = () => { clearTimeout(timer); if (window.emailjs) resolve(window.emailjs); else fail(); };
      script.onerror = fail;
      timer = setTimeout(fail, 10000);
      document.head.append(script);
    });
  }
  return mailSdkPromise;
}

const contactForm = document.getElementById('contact-form');
if (contactForm) contactForm.addEventListener('submit', async event => {
  event.preventDefault();
  const button = document.getElementById('submit-btn');
  if (button.disabled || !contactForm.reportValidity()) return;
  const status = document.getElementById('form-status');
  const fields = new FormData(contactForm);
  const values = Object.fromEntries([...fields].map(([key, value]) => [key, String(value).trim()]));
  if (!values.from_name || !values.message) {
    status.dataset.state = 'error'; status.textContent = '請填寫名字與訊息，不能只有空白。'; return;
  }
  button.disabled = true;
  button.textContent = '傳送中…';
  status.dataset.state = 'pending';
  status.textContent = '正在連線郵件服務，請稍候。';
  let timeout;
  try {
    const emailjs = await loadMailSdk();
    // Existing public EmailJS configuration.
    emailjs.init('iVqyhJ2_yWdZLbdl7');
    await Promise.race([
      emailjs.send('service_8seq3kh', 'template_i2e7ga7', { ...values, company: '', to_email: 'roger042897@gmail.com' }),
      new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('timeout')), 15000); })
    ]);
    status.dataset.state = 'success';
    status.textContent = '訊息已送出，謝謝你的來信！';
    contactForm.reset();
  } catch (error) {
    status.dataset.state = 'error';
    status.textContent = error.message === 'timeout'
      ? '尚未收到寄送結果；訊息可能已送出。內容已保留，也可以直接寄信至 roger042897@gmail.com。'
      : '目前無法送出，內容已保留。請稍後重試，或直接寄信至 roger042897@gmail.com。';
  } finally {
    clearTimeout(timeout);
    button.disabled = false;
    button.textContent = '送出訊息 ↗';
  }
});
