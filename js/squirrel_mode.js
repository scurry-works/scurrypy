(function () {
  // Load saved preference or default to human
  const savedMode = localStorage.getItem("scurrypy_font_mode") || "human";
  if (savedMode === "squirrel") {
    document.body.setAttribute("data-font-mode", "squirrel");
  }

  function injectSquirrelToggle() {
    // Avoid double injection
    if (document.getElementById("squirrel-toggle-btn")) return;

    // Find the header options / palette toggle container
    const paletteForm = document.querySelector(".md-header__option");
    if (!paletteForm) return;

    const btn = document.createElement("button");
    btn.id = "squirrel-toggle-btn";
    btn.type = "button";
    btn.className = "md-header__button md-icon md-header__squirrel-toggle";
    
    const isSquirrel = document.body.getAttribute("data-font-mode") === "squirrel";
    btn.title = isSquirrel ? "Switch to Human Font" : "Switch to Squirrel Font";
    btn.setAttribute("aria-label", btn.title);
    btn.textContent = isSquirrel ? "🐿️" : "🌰";

    btn.addEventListener("click", () => {
      const current = document.body.getAttribute("data-font-mode");
      const next = current === "squirrel" ? "human" : "squirrel";

      if (next === "squirrel") {
        document.body.setAttribute("data-font-mode", "squirrel");
        localStorage.setItem("scurrypy_font_mode", "squirrel");
        btn.textContent = "🐿️";
        btn.title = "Switch to Human Font";
      } else {
        document.body.removeAttribute("data-font-mode");
        localStorage.setItem("scurrypy_font_mode", "human");
        btn.textContent = "🌰";
        btn.title = "Switch to Squirrel Font";
      }
      btn.setAttribute("aria-label", btn.title);
    });

    // Place it right next to the palette toggle
    paletteForm.parentNode.insertBefore(btn, paletteForm.nextSibling);
  }

  // Handle initial load and client-side instant navigation
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectSquirrelToggle);
  } else {
    injectSquirrelToggle();
  }

  // MkDocs Material instant loading support
  if (typeof document$ !== "undefined") {
    document$.subscribe(() => {
      injectSquirrelToggle();
      // Re-apply attribute if body was refreshed
      if (localStorage.getItem("scurrypy_font_mode") === "squirrel") {
        document.body.setAttribute("data-font-mode", "squirrel");
      }
    });
  }
})();
