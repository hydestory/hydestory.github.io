const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

function setup({ reduce = false, blocked = false } = {}) {
  const handlers = {}, motion = { matches: reduce, addEventListener(_, fn) { this.change = fn; } };
  const video = { paused: true, controls: true, plays: 0, addEventListener(name, fn) { handlers[name] = fn; },
    play() { this.plays++; if (blocked) return Promise.reject(new Error('Autoplay blocked')); this.paused = false; handlers.play?.(); return Promise.resolve(); },
    pause() { this.paused = true; handlers.pause?.(); } };
  const button = { hidden: true, setAttribute(name, value) { this[name] = value; }, addEventListener(_, fn) { this.click = fn; } };
  const context = vm.createContext({ document: { getElementById: id => id === 'hourglass-video' ? video : button }, window: { matchMedia: () => motion } });
  vm.runInContext(readFileSync('static/js/hourglass.js', 'utf8'), context);
  return { video, button, motion };
}

test('autoplay stays muted and the visible button can pause and resume it', async () => {
  const { video, button } = setup();
  assert.equal(video.muted, true); assert.equal(video.paused, false); assert.equal(button.hidden, false);
  assert.equal(button.textContent, '暫停');
  await button.click(); assert.equal(video.paused, true); assert.equal(button.textContent, '播放');
  await button.click(); assert.equal(video.paused, false); assert.equal(button.textContent, '暫停');
});
test('reduced motion prevents autoplay but still allows explicit playback', async () => {
  const { video, button, motion } = setup({ reduce: true });
  assert.equal(video.plays, 0);
  await button.click(); assert.equal(video.paused, false);
  motion.change({ matches: true }); assert.equal(video.paused, true);
});
test('blocked autoplay leaves a working, correctly labelled play button', async () => {
  const { video, button } = setup({ blocked: true });
  await Promise.resolve(); await Promise.resolve();
  assert.equal(video.paused, true); assert.equal(button.textContent, '播放');
  await button.click(); assert.equal(video.plays, 2);
});
