// Upcoming classes and events. Add, edit, or remove entries here; dates that
// have passed drop off the site automatically. Leave a field as "" if it isn't
// known yet.
var EVENTS = [
  { date: "2027-01-06", title: "The Moonlight Shift", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "", signup: "https://docs.google.com/forms/d/e/1FAIpQLSfNElEo0aXcuK4euMXVMAaMLesJJXpIqNvQEPLSXYO4Vs1Sdw/viewform" },
  { date: "2027-02-03", title: "The Moonlight Shift", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "", signup: "https://docs.google.com/forms/d/e/1FAIpQLSdroYDh65l5sYYlzgjzja9uuT6zIRcFZp5SdwzlmxNJdDXJtA/viewform" },
  { date: "2027-03-09", title: "The Moonlight Shift", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "", signup: "https://docs.google.com/forms/d/e/1FAIpQLSfjrwiLN5BxrI5WaneZUr41z2yXwZQ2zOM7t74SFUO3V0NeHw/viewform" },
  { date: "2027-05-05", title: "The Moonlight Shift", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "", signup: "https://docs.google.com/forms/d/e/1FAIpQLSffME9RO_u529XfGFLcpwQI-F5alxdQpmwnQNYJUXDubCcEGQ/viewform" },
  { date: "2027-06-02", title: "The Moonlight Shift", kind: "", time: "8:00pm-8:50pm (home by 9!)", place: "Address shared upon RSVP", teacher: "", topic: "", signup: "https://docs.google.com/forms/d/e/1FAIpQLSdRanKZAVebIeqGi52Hjha5AVwagm1NCZQG-h98IRyRJ7SaTg/viewform" }
];

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

  function card(e) {
    var d = parse(e.date);
    var meta = [DAYS[d.getDay()] + ", " + d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })];
    if (e.time) meta.push(e.time);
    if (e.place) meta.push(e.place);
    var missing = [];
    if (!e.time) missing.push("time");
    if (!e.place) missing.push("location");
    if (!e.teacher) missing.push("teacher");
    if (!e.topic) missing.push("topic");
    if (!e.signup) missing.push("RSVP link");
    return '<div class="card event">' +
      '<div class="date-badge"><span class="mon">' + MONTHS[d.getMonth()] + '</span><span class="day">' + d.getDate() + "</span></div>" +
      "<div>" +
        "<h3>" + esc(e.title) + (e.topic ? ": " + esc(e.topic) : "") + "</h3>" +
        '<p class="meta">' + esc(meta.join(" · ")) + "</p>" +
        (e.teacher ? '<p class="meta">With ' + esc(e.teacher) + "</p>" : "") +
        (e.kind ? '<p class="meta">' + esc(e.kind) + "</p>" : "") +
        (missing.length ? '<p class="todo">' + missing.join(", ") + "</p>" : "") +
        (e.signup ? '<a class="btn" href="' + esc(e.signup) + '" target="_blank" rel="noopener">RSVP</a>' : "") +
      "</div></div>";
  }

  var list = document.getElementById("events-list");
  if (list) {
    var all = upcoming();
    list.innerHTML = all.length ? all.map(card).join("")
      : '<p class="center muted">New dates are coming soon. Follow us on Instagram to hear first.</p>';
  }
  var next = document.getElementById("next-event");
  if (next) {
    var n = upcoming()[0];
    next.innerHTML = n ? card(n) : '<p class="center muted">New dates are coming soon.</p>';
  }
})();
