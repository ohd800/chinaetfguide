/* ChinaETFGuide — lightweight feedback widget (email mode, no backend)
 * Visitor ratings + comments open their mail client pre-filled to the owner's address.
 * Swap EMAIL below to change the destination. */
(function () {
  "use strict";
  var EMAIL = "11587939@qq.com";

  // Floating action button
  var fab = document.createElement("button");
  fab.id = "feedback-fab";
  fab.setAttribute("aria-label", "Send feedback");
  fab.innerHTML = '💬<span>Feedback</span>';

  // Panel
  var panel = document.createElement("div");
  panel.id = "feedback-panel";
  panel.setAttribute("hidden", "");
  panel.innerHTML =
    '<div class="fb-head"><strong>Share your feedback</strong>' +
    '<button id="fb-close" aria-label="Close">×</button></div>' +
    '<p class="fb-sub">Help us improve ChinaETFGuide. Submitting opens your email app — your message goes straight to ' +
    EMAIL + '.</p>' +
    '<div class="fb-stars" id="fb-stars" role="radiogroup" aria-label="Rating">' +
    [1, 2, 3, 4, 5].map(function (i) {
      return '<span class="fb-star" data-v="' + i + '" role="radio" aria-checked="false" aria-label="' + i + ' star">★</span>';
    }).join("") +
    '</div>' +
    '<textarea id="fb-msg" rows="4" placeholder="What works? What is confusing? What tool do you want next?"></textarea>' +
    '<input id="fb-email" type="email" placeholder="Your email (optional, so we can reply)" />' +
    '<button id="fb-send" class="fb-send">Send feedback</button>' +
    '<p class="fb-note">We receive this via email. No account, no tracking.</p>';

  document.body.appendChild(fab);
  document.body.appendChild(panel);

  var rating = 0;
  var stars = panel.querySelectorAll(".fb-star");
  stars.forEach(function (s) {
    s.addEventListener("click", function () {
      rating = +s.getAttribute("data-v");
      stars.forEach(function (x) {
        var on = +x.getAttribute("data-v") <= rating;
        x.classList.toggle("on", on);
        x.setAttribute("aria-checked", on ? "true" : "false");
      });
    });
  });

  function open() { panel.removeAttribute("hidden"); fab.classList.add("active"); }
  function close() { panel.setAttribute("hidden", ""); fab.classList.remove("active"); }

  fab.addEventListener("click", function () {
    if (panel.hasAttribute("hidden")) open(); else close();
  });
  panel.querySelector("#fb-close").addEventListener("click", close);

  panel.querySelector("#fb-send").addEventListener("click", function () {
    var msg = panel.querySelector("#fb-msg").value.trim();
    var em = panel.querySelector("#fb-email").value.trim();
    if (!msg && !rating) {
      alert("Please add a comment or a star rating first.");
      return;
    }
    var subject = "ChinaETFGuide Feedback";
    var body = [
      "Page: " + location.href,
      "Rating: " + (rating ? rating + "/5" : "-"),
      "Visitor email: " + (em || "-"),
      "",
      "Message:",
      msg || "(no text)"
    ].join("\n");

    // Open mail client pre-filled. Falls back to copying if mailto is unavailable.
    var href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
    var win = window.open(href, "_blank");
    if (!win) { window.location.href = href; }

    // Friendly confirmation state
    panel.querySelector(".fb-head").innerHTML = "<strong>Thanks! ✅</strong>";
    panel.querySelector(".fb-sub").textContent =
      "Your email app should have opened with your message ready to send. If not, email " + EMAIL + " directly.";
    panel.querySelector("#fb-send").disabled = true;
    panel.querySelector("#fb-msg").disabled = true;
    panel.querySelector("#fb-email").disabled = true;
  });
})();
