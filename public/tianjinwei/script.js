(function () {
  const body = document.body;
  const mobileMenu = document.querySelector("[data-mobile-menu]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const menuClose = document.querySelector("[data-menu-close]");

  function setMenu(open) {
    if (!mobileMenu || !menuToggle) return;
    mobileMenu.classList.toggle("open", open);
    mobileMenu.setAttribute("aria-hidden", String(!open));
    menuToggle.setAttribute("aria-expanded", String(open));
    body.classList.toggle("menu-open", open);
  }

  menuToggle?.addEventListener("click", () => setMenu(true));
  menuClose?.addEventListener("click", () => setMenu(false));
  mobileMenu?.addEventListener("click", (event) => {
    if (event.target === mobileMenu || event.target.closest("a")) {
      setMenu(false);
    }
  });

  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach((tab) => {
        tab.classList.toggle("active", tab === button);
      });

      document.querySelectorAll("[data-menu-list] .menu-group").forEach((group) => {
        group.hidden = filter !== "all" && group.dataset.category !== filter;
      });
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setMenu(false);
    }
  });
})();
