const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function events(object = {}) {
  object.handlers = {};
  object.addEventListener = (name, callback) => { (object.handlers[name] ||= []).push(callback); };
  object.emit = (name) => { (object.handlers[name] || []).forEach((callback) => callback()); };
  return object;
}
function fixture(titles) {
  const videos = titles.map(() => events({
    paused: true, reject: false,
    pause() { this.paused = true; },
    play() {
      if (this.reject) return Promise.reject(new Error('Playback blocked'));
      this.paused = false; this.emit('play'); return Promise.resolve();
    }
  }));
  const cards = titles.map((title, index) => ({
    dataset: { title }, offsetLeft: 40 + index * 302, selected: false,
    classList: { toggle(name, value) { assert.equal(name, 'is-selected'); cards[index].selected = value; } },
    querySelector() { return videos[index]; }
  }));
  const axis = events({ value: '0', attributes: {}, setAttribute(name, value) { this.attributes[name] = value; } });
  const status = {};
  const controls = { hidden: true };
  const track = { querySelectorAll: () => cards, scrollTo(options) { this.lastScroll = options; } };
  const nodes = { '.sim-demo-grid': track, '.simulation-axis': axis, '.simulation-selected': status, '.simulation-controls': controls };
  return { videos, cards, axis, status, controls, track, gallery: { querySelector: (selector) => nodes[selector], classList: { add() {} } } };
}
const a = fixture(['Stack', 'Sort', 'Open']);
const b = fixture(['3 cameras', '4 cameras', '5 cameras', '6 cameras']);
let reducedMotion = false;
const browserWindow = events({ matchMedia: () => ({ matches: reducedMotion }) });
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../assets/js/versacam-gallery.js'), 'utf8'), {
  document: { querySelectorAll: (selector) => selector === '.simulation-gallery' ? [a.gallery, b.gallery] : [] }, window: browserWindow
});
(async () => {
  assert.equal(a.controls.hidden, false); assert.equal(b.controls.hidden, false);
  assert.equal(a.axis.max, '2'); assert.equal(b.axis.max, '3');
  assert.ok([...a.videos, ...b.videos].every((video) => video.paused));
  a.axis.value = '2'; a.axis.emit('input');
  assert.deepEqual(a.videos.map((video) => video.paused), [true, true, false]);
  assert.deepEqual(a.cards.map((card) => card.selected), [false, false, true]);
  assert.equal(a.track.lastScroll.left, 604); assert.equal(a.status.textContent, '3 / 3 — Open');
  b.axis.value = '1'; b.axis.emit('input');
  assert.equal(b.status.textContent, '2 / 4 — 4 cameras');
  assert.equal(a.axis.value, '2', 'Galleries must retain independent selections');
  a.videos[0].play(); assert.equal(a.axis.value, '0'); assert.ok(a.videos[2].paused);
  reducedMotion = true;
  a.axis.value = '1'; a.videos[1].reject = true; a.axis.emit('input');
  assert.equal(a.track.lastScroll.behavior, 'auto'); await new Promise(setImmediate);
  assert.match(a.status.textContent, /press Play/);
  a.axis.value = '1'; a.axis.emit('pointerup'); a.axis.value = '2'; a.axis.emit('input');
  await new Promise(setImmediate); assert.equal(a.status.textContent, '3 / 3 — Open');
  a.videos[0].emit('play'); assert.equal(a.axis.value, '2'); assert.equal(a.videos[2].paused, false);
  a.cards.forEach((card, index) => { card.offsetLeft = 40 + index * 175; });
  browserWindow.emit('resize'); assert.equal(a.track.lastScroll.left, 350);
  assert.equal(a.videos[2].paused, false); assert.equal(b.axis.value, '1');
  console.log('Gallery checks passed: two independent axes, playback isolation, resize, reduced motion, and stale playback events.');
})().catch((error) => { console.error(error); process.exitCode = 1; });
