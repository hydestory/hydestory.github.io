(() => {
  const video = document.getElementById('hourglass-video');
  const toggle = document.getElementById('hourglass-toggle');
  if (!video || !toggle) return;

  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const sync = () => {
    toggle.textContent = video.paused ? '播放' : '暫停';
    toggle.setAttribute('aria-label', video.paused ? '播放沙漏動畫' : '暫停沙漏動畫');
  };
  const play = async () => {
    try { await video.play(); } catch { /* Autoplay may require a user gesture. */ }
    sync();
  };

  video.muted = true;
  video.controls = false;
  toggle.hidden = false;
  video.addEventListener('play', sync);
  video.addEventListener('pause', sync);
  toggle.addEventListener('click', () => {
    if (video.paused) return play();
    video.pause();
  });
  motion.addEventListener('change', event => { if (event.matches) video.pause(); });
  sync();
  if (!motion.matches) play();
})();
