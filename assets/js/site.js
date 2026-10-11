(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Scroll reveal
  var els = [].slice.call(document.querySelectorAll(".reveal"));
  if (reduce || !("IntersectionObserver" in window)) els.forEach(function (e) { e.classList.add("in"); });
  else {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
  }
  // Hero carousel
  var root = document.getElementById("hero-carousel"); if (!root) return;
  var slides = [].slice.call(root.querySelectorAll(".slide")), dotsEl = document.getElementById("car-dots");
  var i = 0, timer = null, paused = false, hover = false, userPaused = false, DELAY = 6500;
  var dots = slides.map(function (s, n) {
    var b = document.createElement("button"); b.type = "button"; b.className = "dot"; b.setAttribute("role", "tab"); b.setAttribute("aria-label", "Slide " + (n + 1));
    b.addEventListener("click", function () { go(n, true); }); dotsEl.appendChild(b); return b;
  });
  function show(n) {
    slides.forEach(function (s, k) {
      var on = k === n; s.classList.toggle("is-active", on); s.classList.toggle("is-prev", k < n);
      s.setAttribute("aria-hidden", on ? "false" : "true");
      [].forEach.call(s.querySelectorAll("a,button"), function (x) { x.tabIndex = on ? 0 : -1; });
      dots[k].setAttribute("aria-selected", on ? "true" : "false");
    });
    i = n;
  }
  function go(n, user) { show((n + slides.length) % slides.length); if (user) restart(); }
  function tick() { if (!paused && !hover && !userPaused && !document.hidden) go(i + 1); }
  function restart() { clearInterval(timer); if (!reduce) timer = setInterval(tick, DELAY); }
  document.getElementById("car-prev").addEventListener("click", function () { go(i - 1, true); });
  document.getElementById("car-next").addEventListener("click", function () { go(i + 1, true); });
  var pb = document.getElementById("car-pause");
  pb.addEventListener("click", function () { userPaused = !userPaused; pb.setAttribute("aria-pressed", userPaused); pb.setAttribute("aria-label", userPaused ? "Play slideshow" : "Pause slideshow"); pb.innerHTML = userPaused ? '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>' : '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>'; });
  root.addEventListener("mouseenter", function () { hover = true; }); root.addEventListener("mouseleave", function () { hover = false; });
  root.addEventListener("focusin", function () { paused = true; }); root.addEventListener("focusout", function () { paused = false; });
  root.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") go(i - 1, true); else if (e.key === "ArrowRight") go(i + 1, true); });
  var x0 = null, y0 = null;
  root.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; paused = true; }, { passive: true });
  root.addEventListener("touchend", function (e) {
    paused = false; if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.3) go(i + (dx < 0 ? 1 : -1), true);
  }, { passive: true });
  show(0); restart();
  if (reduce) { userPaused = true; pb.setAttribute("aria-pressed", "true"); pb.setAttribute("aria-label", "Play slideshow"); }
})();
