(function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("#site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  var shop = document.querySelector("[data-shop]");
  if (!shop) return;

  var buttons = Array.prototype.slice.call(shop.querySelectorAll("[data-filter]"));
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-product]"));
  var sections = Array.prototype.slice.call(document.querySelectorAll("[data-category-section]"));
  var search = shop.querySelector("[data-search]");
  var count = shop.querySelector("[data-count]");
  var empty = document.querySelector("[data-empty]");

  function normalize(value) {
    return (value || "").toLowerCase().trim();
  }

  function setPressed(active) {
    buttons.forEach(function (button) {
      var on = button === active;
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function apply() {
    var active = buttons.find(function (button) {
      return button.getAttribute("aria-pressed") === "true";
    });
    var filter = active ? active.getAttribute("data-filter") : "all";
    var query = search ? normalize(search.value) : "";
    var visible = 0;

    cards.forEach(function (card) {
      var category = card.getAttribute("data-category");
      var haystack = normalize(card.getAttribute("data-search"));
      var show = (filter === "all" || category === filter) && (!query || haystack.indexOf(query) !== -1);
      card.hidden = !show;
      if (show) visible += 1;
    });

    sections.forEach(function (section) {
      var any = Array.prototype.some.call(section.querySelectorAll("[data-product]"), function (card) {
        return !card.hidden;
      });
      section.hidden = !any;
    });

    if (count) {
      count.textContent = visible + (visible === 1 ? " listing" : " listings");
    }
    if (empty) empty.hidden = visible !== 0;
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      setPressed(button);
      var slug = button.getAttribute("data-slug") || "all";
      if (window.history && window.history.replaceState) {
        var next = window.location.pathname + window.location.search;
        if (slug !== "all") next += "#" + slug;
        window.history.replaceState(null, "", next);
      }
      apply();
    });
  });

  if (search) {
    search.addEventListener("input", apply);
    var form = search.closest("form");
    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var url = new URL(window.location.href);
        var value = search.value.trim();
        if (value) url.searchParams.set("q", value);
        else url.searchParams.delete("q");
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, "", url.pathname + url.search + url.hash);
        }
        apply();
      });
    }
  }

  var params = new URLSearchParams(window.location.search);
  var requested = params.get("category");
  if (requested) {
    var match = buttons.find(function (button) {
      return button.getAttribute("data-filter") === requested || button.getAttribute("data-slug") === requested;
    });
    if (match) setPressed(match);
  } else if (window.location.hash) {
    var hash = window.location.hash.replace("#", "");
    var hashed = buttons.find(function (button) {
      return button.getAttribute("data-slug") === hash;
    });
    if (hashed) setPressed(hashed);
  }

  if (params.get("q") && search) search.value = params.get("q");
  apply();
})();
