// Upcoming classes and events. Add, edit, or remove entries here; dates that
// have passed drop off the site automatically. Leave a field as "" if it isn't
// known yet.
//
// honor: shown under the title, e.g. "Rosh Chodesh Shevat" -> "In honor of Rosh Chodesh Shevat".
//
// rsvp: the Google Form behind the RSVP button, so people can RSVP right on the
// page. "form" is the long id in the form's link; the entry numbers come from
// the form's pre-filled link. Without rsvp, the button opens "signup" instead.
var EVENTS = [
  { date: "2027-01-06", title: "The Moonlight Shift", honor: "Rosh Chodesh Shevat", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "",
    signup: "https://docs.google.com/forms/d/e/1FAIpQLSfNElEo0aXcuK4euMXVMAaMLesJJXpIqNvQEPLSXYO4Vs1Sdw/viewform",
    rsvp: { form: "1FAIpQLSfNElEo0aXcuK4euMXVMAaMLesJJXpIqNvQEPLSXYO4Vs1Sdw", name: "entry.1303972338", email: "entry.1117826406", first: "entry.2045363639", ideas: "entry.1792170449" } },
  { date: "2027-02-03", title: "The Moonlight Shift", honor: "Rosh Chodesh Adar I", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "",
    signup: "https://docs.google.com/forms/d/e/1FAIpQLSdroYDh65l5sYYlzgjzja9uuT6zIRcFZp5SdwzlmxNJdDXJtA/viewform",
    rsvp: { form: "1FAIpQLSdroYDh65l5sYYlzgjzja9uuT6zIRcFZp5SdwzlmxNJdDXJtA", name: "entry.1303972338", email: "entry.1117826406", first: "entry.2045363639", ideas: "entry.1792170449" } },
  { date: "2027-03-09", title: "The Moonlight Shift", honor: "Rosh Chodesh Adar II", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "",
    signup: "https://docs.google.com/forms/d/e/1FAIpQLSfjrwiLN5BxrI5WaneZUr41z2yXwZQ2zOM7t74SFUO3V0NeHw/viewform",
    rsvp: { form: "1FAIpQLSfjrwiLN5BxrI5WaneZUr41z2yXwZQ2zOM7t74SFUO3V0NeHw", name: "entry.1303972338", email: "entry.1117826406", first: "entry.2045363639", ideas: "entry.1792170449" } },
  { date: "2027-05-05", title: "The Moonlight Shift", honor: "Rosh Chodesh Iyar", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "",
    signup: "https://docs.google.com/forms/d/e/1FAIpQLSffME9RO_u529XfGFLcpwQI-F5alxdQpmwnQNYJUXDubCcEGQ/viewform" },
  { date: "2027-06-02", title: "The Moonlight Shift", honor: "Rosh Chodesh Sivan", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "",
    signup: "https://docs.google.com/forms/d/e/1FAIpQLSdRanKZAVebIeqGi52Hjha5AVwagm1NCZQG-h98IRyRJ7SaTg/viewform" }
];

var RSVP_THANKS = "You’re in! We’ll send location information closer to the date. After all, we’re always home by 9.";
var RSVP_IDEAS_QUESTION = "We are working hard to build programming that reflects what the women in Riverdale are craving. Tell us a little bit about the kind of Torah you enjoy learning and what kind of experiences you’d like to see more of in Riverdale. The sky is the limit!";

(function () {
  var MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function parse(iso) {
    var p = iso.split("-");
    return new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function upcoming() {
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    return EVENTS
      .filter(function (e) { return parse(e.date) >= today; })
      .sort(function (a, b) { return parse(a.date) - parse(b.date); });
  }

  function rsvpForm(e, id) {
    return '<div class="rsvp" id="' + id + '" hidden>' +
      '<form novalidate data-date="' + e.date + '">' +
        '<div class="field"><label class="q" for="' + id + '-name">Name (First and Last) <span class="req">*</span></label>' +
          '<input type="text" id="' + id + '-name" autocomplete="name"></div>' +
        '<div class="field"><label class="q" for="' + id + '-email">Email <span class="req">*</span></label>' +
          '<input type="email" id="' + id + '-email" autocomplete="email"></div>' +
        '<fieldset class="field"><legend class="q">Is this your first time participating in The After Hours Beit Midrash? <span class="req">*</span></legend>' +
          '<label class="choice"><input type="radio" name="' + id + '-first" value="Yes"> Yes</label>' +
          '<label class="choice"><input type="radio" name="' + id + '-first" value="No"> No</label></fieldset>' +
        '<div class="field"><label class="q" for="' + id + '-ideas">' + esc(RSVP_IDEAS_QUESTION) + "</label>" +
          '<textarea id="' + id + '-ideas"></textarea></div>' +
        '<button type="submit" class="btn">Send my RSVP</button>' +
        '<p class="err" role="alert"></p>' +
      "</form>" +
      '<div class="rsvp-done" hidden><p class="thanks">' + esc(RSVP_THANKS) + "</p></div>" +
    "</div>";
  }

  function card(e, where) {
    var d = parse(e.date);
    var id = "rsvp-" + where + "-" + e.date;
    // One detail per line, so phrases like "(home by 9!)" never split awkwardly.
    var lines = [DAYS[d.getDay()] + ", " + d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })];
    if (e.time) lines.push(e.time);
    if (e.place) lines.push(e.place);
    if (e.teacher) lines.push("With " + e.teacher);
    var missing = [];
    if (!e.time) missing.push("time");
    if (!e.place) missing.push("location");
    if (!e.teacher) missing.push("teacher");
    if (!e.topic) missing.push("topic");
    if (!e.signup && !e.rsvp) missing.push("RSVP link");
    var button = e.rsvp
      ? '<button type="button" class="btn rsvp-open" aria-expanded="false" aria-controls="' + id + '">RSVP</button>'
      : e.signup ? '<a class="btn" href="' + esc(e.signup) + '" target="_blank" rel="noopener">RSVP</a>' : "";
    return '<div class="card event">' +
      '<div class="date-badge"><span class="mon">' + MONTHS[d.getMonth()] + '</span><span class="day">' + d.getDate() + "</span></div>" +
      "<div>" +
        "<h3>" + esc(e.title) + (e.topic ? ": " + esc(e.topic) : "") + "</h3>" +
        (e.honor ? '<p class="honor">In honor of ' + esc(e.honor) + "</p>" : "") +
        '<p class="meta">' + lines.map(esc).join("<br>") + "</p>" +
        (e.kind ? '<p class="meta">' + esc(e.kind) + "</p>" : "") +
        (missing.length ? '<p class="todo">' + missing.join(", ") + "</p>" : "") +
        button +
      "</div>" +
      (e.rsvp ? rsvpForm(e, id) : "") +
    "</div>";
  }

  function byDate(date) {
    for (var i = 0; i < EVENTS.length; i++) if (EVENTS[i].date === date) return EVENTS[i];
  }

  // Opens the RSVP form inside the card, and sends it to the event's Google Form.
  function wire(root) {
    root.querySelectorAll(".rsvp-open").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var box = document.getElementById(btn.getAttribute("aria-controls"));
        box.hidden = !box.hidden;
        btn.setAttribute("aria-expanded", box.hidden ? "false" : "true");
        btn.textContent = box.hidden ? "RSVP" : "Close";
        if (!box.hidden) box.querySelector("input").focus();
      });
    });
    root.querySelectorAll(".rsvp form").forEach(function (form) {
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var e = byDate(form.getAttribute("data-date"));
        var box = form.parentNode, id = box.id;
        var err = form.querySelector(".err");
        var name = document.getElementById(id + "-name").value.trim();
        var email = document.getElementById(id + "-email").value.trim();
        var first = form.querySelector('input[name="' + id + '-first"]:checked');
        var ideas = document.getElementById(id + "-ideas").value.trim();
        var missing = [];
        if (!name) missing.push("your name");
        if (!/^\S+@\S+\.\S+$/.test(email)) missing.push("a valid email");
        if (!first) missing.push("whether this is your first time");
        if (missing.length) { err.textContent = "Please add " + missing.join(", ") + "."; return; }
        err.textContent = "";

        var data = new URLSearchParams();
        data.append(e.rsvp.name, name);
        data.append(e.rsvp.email, email);
        data.append(e.rsvp.first, first.value);
        data.append(e.rsvp.ideas, ideas);
        var send = form.querySelector('button[type="submit"]');
        send.disabled = true;
        send.textContent = "Sending…";
        fetch("https://docs.google.com/forms/d/e/" + e.rsvp.form + "/formResponse", { method: "POST", mode: "no-cors", body: data })
          .then(function () {
            form.hidden = true;
            box.querySelector(".rsvp-done").hidden = false;
            var opener = box.parentNode.querySelector(".rsvp-open");
            if (opener) { opener.textContent = "RSVP sent"; opener.disabled = true; }
          })
          .catch(function () {
            send.disabled = false;
            send.textContent = "Send my RSVP";
            err.textContent = "Your RSVP didn’t go through. Please try again, or email us at theafterhoursbeitmidrash@gmail.com.";
          });
      });
    });
  }

  var list = document.getElementById("events-list");
  if (list) {
    var all = upcoming();
    list.innerHTML = all.length ? all.map(function (e) { return card(e, "list"); }).join("")
      : '<p class="center muted">New dates are coming soon. Follow us on Instagram to hear first.</p>';
    wire(list);
  }
  var next = document.getElementById("next-event");
  if (next) {
    var n = upcoming()[0];
    next.innerHTML = n ? card(n, "next") : '<p class="center muted">New dates are coming soon.</p>';
    wire(next);
  }
})();
