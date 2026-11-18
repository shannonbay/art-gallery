(() => {
  const works = [...document.querySelectorAll(".work")].map((work) => ({
    link: work.querySelector("a"),
    alt: work.querySelector("img").alt,
    caption: work.querySelector("figcaption").innerHTML,
  }));

  const viewer = document.querySelector(".viewer");
  const image = viewer.querySelector(".viewer-image");
  const caption = viewer.querySelector(".viewer-caption");
  let current = 0;
  let touchStartX = null;

  const wrap = (index) => (index + works.length) % works.length;

  function show(index) {
    current = wrap(index);
    const work = works[current];
    image.src = work.link.href;
    image.alt = work.alt;
    caption.innerHTML = work.caption;
    [current - 1, current + 1].forEach((near) => {
      new Image().src = works[wrap(near)].link.href;
    });
  }

  works.forEach((work, index) => {
    work.link.addEventListener("click", (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      show(index);
      viewer.showModal();
    });
  });

  viewer.querySelector(".viewer-close").addEventListener("click", () => viewer.close());
  viewer.querySelector(".viewer-prev").addEventListener("click", () => show(current - 1));
  viewer.querySelector(".viewer-next").addEventListener("click", () => show(current + 1));

  viewer.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") show(current - 1);
    if (event.key === "ArrowRight") show(current + 1);
  });

  viewer.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0].clientX;
  }, { passive: true });

  viewer.addEventListener("touchend", (event) => {
    if (touchStartX === null) return;
    const distance = event.changedTouches[0].clientX - touchStartX;
    touchStartX = null;
    if (Math.abs(distance) > 50) show(current + (distance < 0 ? 1 : -1));
  }, { passive: true });
})();
