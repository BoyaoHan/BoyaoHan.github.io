/* A native range selects a task, scrolls its card into view, and plays it. */
document.querySelectorAll('.simulation-gallery').forEach((gallery) => {
  const track = gallery.querySelector('.sim-demo-grid');
  const cards = Array.from(track.querySelectorAll('figure'));
  const videos = cards.map((card) => card.querySelector('video'));
  const axis = gallery.querySelector('.simulation-axis');
  const status = gallery.querySelector('.simulation-selected');
  if (!cards.length) return;
  axis.max = String(cards.length - 1);

  function selectTask(value, scroll, play) {
    const index = Math.min(cards.length - 1, Math.max(0, Math.round(Number(value) || 0)));
    const label = `${index + 1} / ${cards.length} — ${cards[index].dataset.title}`;
    cards.forEach((card, position) => {
      card.classList.toggle('is-selected', position === index);
      if (position !== index) videos[position].pause();
    });
    axis.value = String(index);
    axis.setAttribute('aria-valuetext', label);
    status.textContent = label;
    if (scroll) {
      track.scrollTo({
        left: cards[index].offsetLeft - cards[0].offsetLeft,
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
      });
    }
    if (play) {
      videos[index].play().catch(() => {
        if (Number(axis.value) === index && videos[index].paused) {
          status.textContent = `${label} — press Play to start.`;
        }
      });
    }
  }

  axis.addEventListener('input', () => selectTask(axis.value, true, true));
  axis.addEventListener('pointerup', () => selectTask(axis.value, true, true));
  window.addEventListener('resize', () => selectTask(axis.value, true, false));
  videos.forEach((video, index) => {
    video.addEventListener('play', () => {
      if (!video.paused) selectTask(index, false, false);
    });
  });
  gallery.querySelector('.simulation-controls').hidden = false;
  gallery.classList.add('has-video-axis');
  selectTask(0, false, false);
});

/* Each camera-count stop shows all four configurations of one task. */
document.querySelectorAll('.camera-count-gallery').forEach((gallery) => {
  const groups = Array.from(gallery.querySelectorAll('.camera-count-grid'));
  const axis = gallery.querySelector('.simulation-axis');
  const status = gallery.querySelector('.simulation-selected');
  if (!groups.length) return;

  function selectTask(play) {
    const index = Number(axis.value);
    const label = `${index + 1} / ${groups.length} — ${groups[index].dataset.title}`;
    status.textContent = label;
    axis.setAttribute('aria-valuetext', label);
    groups.forEach((group, position) => {
      group.hidden = position !== index;
      group.querySelectorAll('video').forEach((video) => {
        if (group.hidden) video.pause();
        else if (play) video.play().catch(() => {
          if (Number(axis.value) === index && video.paused) {
            status.textContent = `${label} — press Play to start.`;
          }
        });
      });
    });
  }

  axis.addEventListener('input', () => selectTask(true));
  axis.addEventListener('pointerup', () => selectTask(true));
  gallery.querySelector('.simulation-controls').hidden = false;
  selectTask(false);
});
