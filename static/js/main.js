const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
if (burger) {
  burger.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
}
const copy = document.getElementById('copy');
if (copy) {
  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(copy.dataset.copy);
      copy.textContent = 'Email copied';
    } catch (e) {
      copy.textContent = 'Copy failed, select the email above';
    }
    setTimeout(() => (copy.textContent = 'Copy email address'), 2000);
  });
}
