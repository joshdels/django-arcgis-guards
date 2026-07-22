function setActiveSidebar() {
  const currentPath = window.location.pathname;

  document.querySelectorAll(".sidebar-link").forEach((link) => {
    const path = new URL(link.getAttribute("hx-get"), window.location.origin)
      .pathname;

    link.classList.toggle("active", path === currentPath);
  });
}

document.addEventListener("DOMContentLoaded", setActiveSidebar);

// after HTMX updates the browser history
document.body.addEventListener("htmx:pushedIntoHistory", setActiveSidebar);
document.body.addEventListener("htmx:replacedInHistory", setActiveSidebar);

// browser back/forward
window.addEventListener("popstate", setActiveSidebar);
