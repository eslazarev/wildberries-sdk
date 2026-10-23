// Material renders nav links as-is, so an absolute URL in SUMMARY.md would
// navigate away from the reference. Send every off-site nav link to a new tab.
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".md-nav a[href^='http']").forEach(function (link) {
    if (link.host !== location.host) {
      link.target = "_blank";
      link.rel = "noopener";
    }
  });
});
