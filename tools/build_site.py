"""Builds the site's pages. Run from anywhere: python3 tools/build_site.py

Edit the content here (or tools/our_story.txt, or assets/events.js for events), then rebuild.
The sponsorship pages (moonlight/, cohort/, partner/) keep their own form code; this only
refreshes their menu, footer and page titles."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.join(HERE, "..") + "/"
DRAFT = True  # shows the "Draft preview" banner; set False at launch

LAMP = '''<svg class="{cls}" viewBox="0 0 160 150" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {aria}>
      <line x1="80" y1="0" x2="80" y2="50"/>
      <path d="M73 50h14v10H73z"/>
      <path d="M80 60C52 60 40 94 22 118h116C120 94 108 60 80 60Z"/>
      <path d="M22 118Q80 132 138 118"/>
      <path d="M68 123Q80 140 92 123"/>
    </svg>'''

MOON = '''<svg class="moon card-icon" viewBox="0 0 120 120" aria-hidden="true">
      <defs>
        <radialGradient id="mg" cx="65%" cy="40%" r="80%"><stop offset="0" stop-color="#f3e9d3"/><stop offset="1" stop-color="#a99a7b"/></radialGradient>
        <mask id="mm"><rect width="120" height="120" fill="#fff"/><circle cx="44" cy="50" r="46" fill="#000"/></mask>
      </defs>
      <circle cx="68" cy="62" r="46" fill="url(#mg)" mask="url(#mm)"/>
    </svg>'''

NAV = [
    ("index.html", "Home"),
    ("about/index.html", "About"),
    ("team/index.html", "Our Team"),
    ("programs/index.html", "Programs"),
    ("events/index.html", "Upcoming"),
    ("contact/index.html", "Contact"),
]


SITE_URL = "https://www.theafterhoursbeitmidrash.com/"
SUPPORT_PAGES = {"support/index.html", "moonlight/index.html", "cohort/index.html", "partner/index.html"}


def head_extras(path, title, description, up):
    """Icon, shared menu styles, and the preview card shown when the link is shared."""
    url = SITE_URL + path.replace("index.html", "")
    return f"""<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="stylesheet" href="{up}assets/chrome.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The After Hours Beit Midrash">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}assets/img/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="628">
<meta name="twitter:card" content="summary_large_image">"""


def nav_html(path, up):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == path else ""
        links.append(f'<li><a href="{up}{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if path in SUPPORT_PAGES else ""
    links.append(f'<li><a class="nav-cta" href="{up}support/index.html"{cur}>Support us</a></li>')
    banner = '<div class="draft-banner">Draft preview: not yet published</div>\n' if DRAFT else ""
    joined = "\n      ".join(links)
    return f"""{banner}<nav class="nav" aria-label="Main">
  <div class="nav-inner">
    <a class="brand" href="{up}index.html">
      {LAMP.format(cls="", w="5", aria='aria-hidden="true"')}
      <span>The After Hours<br>Beit Midrash</span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-links">Menu</button>
    <ul class="nav-links" id="nav-links">
      {joined}
    </ul>
  </div>
</nav>"""


FOOTER = """<footer>
  <p class="tag">Meaningful Torah learning, after hours.</p>
  <p>Riverdale, NY · Questions? Reach out any time.</p>
  <div class="reach">
    <a href="https://www.instagram.com/theafterhoursbeitmidrash/" target="_blank" rel="noopener">Instagram</a>
    <a href="mailto:theafterhoursbeitmidrash@gmail.com">Email us</a>
  </div>
  <p class="small">The After Hours Beit Midrash is an independently operated educational initiative and is not a registered 501(c)(3) nonprofit.</p>
</footer>

<script>
var nav = document.querySelector(".nav"), menuBtn = document.querySelector(".menu-btn");
menuBtn.addEventListener("click", function () {
  var open = nav.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
});
// Start at the top after following a link (Back still returns to where you were).
(function () {
  var navType = performance.getEntriesByType && performance.getEntriesByType("navigation")[0];
  if (!location.hash && navType && navType.type === "navigate") {
    window.scrollTo(0, 0);
    try { document.documentElement.scrollIntoView({ block: "start" }); } catch (e) {}
  }
})();
</script>"""


def page(path, title, body, description):
    up = "../" * path.count("/")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css">
{head_extras(path, title, description, up)}
</head>
<body>
{nav_html(path, up)}

{body.replace("{up}", up)}

{FOOTER}
</body>
</html>
"""
    os.makedirs(os.path.dirname(ROOT + path) or ROOT, exist_ok=True)
    with open(ROOT + path, "w") as f:
        f.write(html)


def between(html, start, end, content, anchor, before=True):
    """Replace the block between two marker comments, or insert it next to anchor the first time."""
    block = f"{start}\n{content}\n{end}"
    if start in html:
        a = html.index(start); b = html.index(end) + len(end)
        return html[:a] + block + html[b:]
    i = html.index(anchor)
    return html[:i] + block + "\n" + html[i:] if before else html[:i + len(anchor)] + "\n" + block + html[i + len(anchor):]


def sponsor_page(path, title, description):
    """The sponsorship pages keep their own form code and styles; add the shared menu, footer and head extras."""
    up = "../" * path.count("/")
    with open(ROOT + path) as f:
        html = f.read()
    import re
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1)
    html = between(html, "<!-- site-head -->", "<!-- /site-head -->",
                   f'<meta name="description" content="{description}">\n' + head_extras(path, title, description, up), "</head>")
    html = between(html, "<!-- site-nav -->", "<!-- /site-nav -->", nav_html(path, up), "<body>", before=False)
    html = between(html, "<!-- site-footer -->", "<!-- /site-footer -->", FOOTER, "</body>")
    with open(ROOT + path, "w") as f:
        f.write(html)


def page_hero(eyebrow, heading, lede="", cls=""):
    lede_html = f'\n    <p class="lede">{lede}</p>' if lede else ""
    return f'''<header class="hero page-hero{" " + cls if cls else ""}">
  <div class="hero-inner">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{heading}</h1>{lede_html}
  </div>
</header>'''


# ---------------- Home ----------------
page("index.html", "The After Hours Beit Midrash", f'''<header class="hero">
  <div class="hero-inner">
    {LAMP.format(cls="lamp", w="1.3", aria='role="img" aria-label="Hanging pendant lamp"')}
    <div class="lockup">
      <span class="the">The</span>
      <span class="big">AFTER HOURS</span>
      <span class="small">BEIT MIDRASH</span>
    </div>
    <hr class="rule">
    <figure class="arch-photo">
      <img src="{{up}}assets/img/around-the-table.jpg" width="360" height="480" alt="Women learning together around a dining room table under a chandelier, seen through an arched doorway.">
    </figure>
    <h1>Turns out, you still have time for this type of learning.</h1>
    <p class="lede">The texts you love didn’t go anywhere.<br>We’re making it easier to find your way back.</p>
    <p class="place">Riverdale, NY</p>
    <div class="btn-row">
      <a class="btn" href="{{up}}events/index.html">See what’s coming up</a>
      <a class="btn ghost" href="{{up}}support/index.html">Support us</a>
    </div>
  </div>
</header>

<main>
  <section class="block">
    <div class="narrow prose center">
      <p class="lead">Serious learning for full adult lives.</p>
      <p>The magic of fifty minutes is that it asks for so little of your week, but gives you enough time to do something substantial. Week after week, those fifty minutes add up to serious, sustained Torah learning that actually fits into your life.</p>
      <div class="btn-row"><a class="btn ghost" href="{{up}}about/index.html">More about us</a></div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2 class="center">Our programs</h2>
      <div class="grid">
        <div class="card center">
          {LAMP.format(cls="minilamp card-icon", w="1.6", aria='aria-hidden="true"')}
          <h3>The Cohort Series</h3>
          <p class="kicker">Serious, text-based learning over four to six weeks.</p>
          <p class="muted">A small group, a substantial topic, and a commitment that actually feels manageable.</p>
          <a class="btn ghost" href="{{up}}programs/index.html#cohort">Learn more</a>
        </div>
        <div class="card center">
          {MOON}
          <h3>The Moonlight Shift</h3>
          <p class="kicker">A monthly evening of Torah in honor of Rosh Chodesh.</p>
          <p class="muted">Fifty minutes on a weeknight, free and open to all who are interested.</p>
          <a class="btn ghost" href="{{up}}programs/index.html#moonlight">Learn more</a>
        </div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="narrow">
      <h2 class="center">Coming up</h2>
      <div class="events-list" id="next-event"></div>
      <script src="{{up}}assets/events.js"></script>
      <div class="btn-row"><a class="btn ghost" href="{{up}}events/index.html">All upcoming events</a></div>
    </div>
  </section>

  <section class="block">
    <div class="narrow prose center">
      <h2>Help keep the door open</h2>
      <p class="muted">Your gift keeps the learning exceptional, the commitment manageable, and the Moonlight Shift free for everyone.</p>
      <div class="btn-row"><a class="btn" href="{{up}}support/index.html">Sponsor or give</a></div>
    </div>
  </section>
</main>''', "Serious Torah learning for women in Riverdale, NY: the Cohort Series and the Moonlight Shift.")

# ---------------- About ----------------
STORY = [l.strip() for l in open(os.path.join(HERE, "our_story.txt")) if l.strip()]
PULL = {"So we decided to create one.", "So we started with a dining room table in Riverdale, some source sheets, and an invitation to come learn."}
LAST = "There's a place for you at this table."
def story_html():
    out = []
    for line in STORY:
        text = line.replace("'", "’")
        if line == LAST:
            out.append(f'      <p class="pull closing-line">{text}</p>')
        elif line in PULL:
            out.append(f'      <p class="pull">{text}</p>')
            if line.startswith("So we started with a dining room table"):
                out.append('      <figure class="story-photo"><img src="{up}assets/img/our-story-source-sheet.jpg" width="1086" height="1448" loading="lazy" alt="A hand holding a printed source sheet on Eliyahu HaNavi above a wooden table, with a pen nearby."></figure>')
        else:
            if line.startswith("Of course, there are already wonderful shiurim"):
                out.append('      <figure class="story-photo left"><img src="{up}assets/img/our-story-listening.jpg" width="720" height="960" loading="lazy" alt="A woman in a baseball cap listening closely at the table, chin resting on her hand, pen in hand."></figure>')
            out.append(f'      <p>{text}</p>')
    return "\n".join(out)

page("about/index.html", "Our Story | The After Hours Beit Midrash", page_hero("About us", "Our story", cls="photo-hero") + f'''

<main>
  <section class="block">
    <div class="narrow prose story">
{story_html()}
      <p class="signoff"><span class="names">Racheli &amp; Shuli</span><span class="title">Founders, The After Hours Beit Midrash</span></p>
      <div class="btn-row"><a class="btn" href="{{up}}events/index.html">Join us</a><a class="btn ghost" href="{{up}}team/index.html">Meet the team</a></div>
    </div>
  </section>
</main>''', "How two high school Torah teachers started The After Hours Beit Midrash around a dining room table in Riverdale.")

# ---------------- Team ----------------
def person(initials, name, bio=None, photo=None):
    # photo: an image in assets/img/ (e.g. "racheli.jpg"); no photo shows no circle at all
    photo_html = (f'          <img class="photo" src="{{up}}assets/img/{photo}" alt="{name}">\n' if photo else "")
    # bio: list of paragraphs; cards without one show just the name and role
    paras = "\n".join(f"          <p>{p}</p>" for p in bio) if bio else ""
    return f'''        <div class="card person">
{photo_html}          <h3>{name}</h3>
          <p class="role">Co-founder · Judaic Studies Teacher at SAR High School</p>
{paras}
        </div>'''

RACHELI_BIO = [
    "Racheli Barris is a Tanakh educator at SAR High School, where she spends her days helping teenagers discover that Torah texts are far more interesting, complicated, and relevant than they might have expected. She studied at Yeshiva University’s Graduate Program in Advanced Talmudic Studies (GPATS) and Bernard Revel Graduate School, and brings years of serious Torah learning and classroom experience to her teaching.",
    "In addition to teaching in high school, Racheli frequently teaches adult classes and has been invited to speak at synagogues and community learning programs. She loves to share her love of Torah with learners well beyond the high school classroom. Racheli believes that excellent Torah learning should be intellectually challenging, genuinely enjoyable, and full of opportunities for people to bring their own ideas and experiences into the room.",
    "Outside the classroom, Racheli is a wife, mom, and Riverdale resident who knows firsthand how quickly adult life can crowd out the things we always meant to make time for. She co-founded The After Hours Beit Midrash because she believes that meaningful Torah learning shouldn’t be something we have to leave behind when life gets busy.",
]

SHULI_BIO = [
    "Shuli Taubes chairs the Jewish Philosophy Department at SAR High School in Riverdale, where she also teaches Tanakh and Jewish Identity and has developed curricula in comparative religion and Jewish sexual ethics for Modern Orthodox high school students. She holds a Master of Divinity from Harvard Divinity School and a BA in History from Barnard College, and brings both serious Torah learning and genuine curiosity about the wider world into her teaching. Shuli lectures in synagogues and adult education programs throughout North America.",
    "Shuli believes that everyone should have the opportunity to find their own chelek in Torah, to discover the ideas, questions, and sources that speak to them and become part of their lives. She co-founded The After Hours Beit Midrash because she believes that Torah learning shouldn’t be confined to a particular stage of life. Its wisdom can meet us wherever we are, offering new ways to think, grow, and connect. Shuli lives with her family in Riverdale.",
]

page("team/index.html", "Our Team | The After Hours Beit Midrash", page_hero("Our team", "The people behind the Beit Midrash") + f'''

<main>
  <section class="block">
    <div class="wrap">
      <div class="grid">
{person("RB", "Racheli Barris", RACHELI_BIO)}
{person("ST", "Shuli Taubes", SHULI_BIO)}
      </div>
    </div>
  </section>
</main>''', "Meet the team behind The After Hours Beit Midrash.")

# ---------------- Teachers ----------------
def teacher(n):
    return f'''        <div class="card person">
          <div class="photo" aria-hidden="true">?</div>
          <h3>Teacher {n}</h3>
          <p class="role todo">name and what they teach</p>
          <p class="todo">short bio and a photo</p>
        </div>'''

SHOW_TEACHERS = False  # turn on once there are teacher bios
if SHOW_TEACHERS: page("teachers/index.html", "Teachers | The After Hours Beit Midrash", page_hero("Our teachers", "Exceptional teachers, thoughtfully chosen texts") + f'''

<main>
  <section class="block">
    <div class="wrap">
      <div class="grid">
{teacher(1)}
{teacher(2)}
{teacher(3)}
      </div>
    </div>
  </section>
</main>''', "The teachers of The After Hours Beit Midrash.")

# ---------------- Programs ----------------
page("programs/index.html", "Programs | The After Hours Beit Midrash", page_hero("Our programs", "Two ways to learn with us") + f'''

<main>
  <section class="block" id="cohort">
    <div class="narrow prose">
      {LAMP.format(cls="minilamp card-icon", w="1.6", aria='aria-hidden="true"')}
      <h2 class="center">The Cohort Series</h2>
      <p class="kicker center">Serious, text-based learning over four to six weeks.</p>
      <p>The cohort learning experience we offer is truly unique. It gives busy women the opportunity to engage in serious, text-based Torah learning over an extended period of time, in a way that actually feels manageable to commit to. Each series runs about four to six weeks, long enough to really get into a topic and cover meaningful ground. And because the group is small, the experience feels personal. We plan to offer a new cohort each season.</p>
      <div class="btn-row"><a class="btn ghost" href="{{up}}cohort/index.html">Sponsor a cohort</a></div>
    </div>
  </section>

  <section class="block" id="moonlight">
    <div class="narrow prose">
      {MOON}
      <h2 class="center">The Moonlight Shift</h2>
      <p class="kicker center">A monthly evening of Torah in honor of Rosh Chodesh.</p>
      <p>We designed The Moonlight Shift for women who want more Torah in their lives but can’t realistically commit to a full six-week cohort. Once a month, in honor of Rosh Chodesh, it offers a way to make Torah learning a regular part of life without adding another major commitment to the calendar. The teachers are incredible and the topics are carefully chosen. We know that fifty minutes on a weeknight is precious. We always make it worth it.</p>
      <p>The Moonlight Shift is free and open to all who are interested.</p>
      <p><strong>Time:</strong> 8:00pm-8:50pm (home by 9!)<br><strong>Where:</strong> Address shared upon RSVP</p>
      <div class="btn-row"><a class="btn" href="{{up}}events/index.html">Next Moonlight Shift</a><a class="btn ghost" href="{{up}}moonlight/index.html">Sponsor an evening</a></div>
    </div>
  </section>
</main>''', "The Cohort Series and The Moonlight Shift at The After Hours Beit Midrash.")

# ---------------- Upcoming ----------------
page("events/index.html", "Upcoming | The After Hours Beit Midrash", page_hero("Upcoming", "Classes and events") + '''

<main>
  <section class="block">
    <div class="narrow">
      <div class="events-list" id="events-list"></div>
      <script src="{up}assets/events.js"></script>
    </div>
  </section>
</main>''', "Upcoming classes and events at The After Hours Beit Midrash.")

# ---------------- Contact ----------------
page("contact/index.html", "Contact | The After Hours Beit Midrash", page_hero("Contact", "We’d love to hear from you") + '''

<main>
  <section class="block">
    <div class="narrow prose center">
      <p>Questions about a class, sponsoring an evening, or getting involved? Reach out any time.</p>
      <div class="btn-row">
        <a class="btn" href="mailto:theafterhoursbeitmidrash@gmail.com">theafterhoursbeitmidrash@gmail.com</a>
      </div>
      <div class="btn-row">
        <a class="btn ghost" href="https://www.instagram.com/theafterhoursbeitmidrash/" target="_blank" rel="noopener">@theafterhoursbeitmidrash on Instagram</a>
      </div>
    </div>
  </section>
</main>''', "Contact The After Hours Beit Midrash.")

# ---------------- Support (the live donation page, in the new layout) ----------------
page("support/index.html", "Support | The After Hours Beit Midrash", page_hero("Support us", "Your gift is how we keep the standard high.") + f'''

<main>
  <section class="block">
    <div class="narrow prose center">
      <p>It allows us to keep the learning exceptional, the commitment manageable, and the door open for the next woman who’s been looking for a way back in.</p>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <h2 class="center">What you can support</h2>
      <div class="grid">
        <div class="card center">
          {LAMP.format(cls="minilamp card-icon", w="1.6", aria='aria-hidden="true"')}
          <h3>The Cohort Series</h3>
          <p class="kicker">Serious, text-based learning over four to six weeks.</p>
          <p class="muted">A small group, a substantial topic, and a commitment that actually feels manageable. We plan to offer a new cohort each season.</p>
          <a class="btn" href="{{up}}cohort/index.html">Sponsor a cohort</a>
        </div>
        <div class="card center">
          {MOON}
          <h3>The Moonlight Shift</h3>
          <p class="kicker">A monthly evening of Torah in honor of Rosh Chodesh.</p>
          <p class="muted">For women who want more Torah in their lives but can’t commit to a full cohort. Help us keep this experience free and open to all who are interested.</p>
          <a class="btn" href="{{up}}moonlight/index.html">Sponsor a Moonlight Shift</a>
        </div>
        <div class="card center">
          <h3>After Hours Partner</h3>
          <p class="kicker">A general gift to the cause.</p>
          <p class="muted">Not tied to a single evening. It supports the whole of what we are building: the cohorts, the Moonlight Shift, and the learning still to come.</p>
          <a class="btn" href="{{up}}partner/index.html">Become a partner</a>
        </div>
      </div>
      <p class="center muted" style="margin-top:28px">If you’re sponsoring a cohort or a Moonlight Shift, we’ll be in touch to confirm your date once we receive your gift.</p>
    </div>
  </section>
</main>''', "Sponsor a cohort or a Moonlight Shift, or become an After Hours Partner.")

# ---------------- Sponsorship pages (forms stay as they are) ----------------
sponsor_page("moonlight/index.html", "Sponsor a Moonlight Shift | The After Hours Beit Midrash", "Sponsor a Moonlight Shift: a monthly evening of Torah in honor of Rosh Chodesh.")
sponsor_page("cohort/index.html", "Sponsor the Cohort Series | The After Hours Beit Midrash", "Sponsor the Cohort Series: serious, text-based learning over four to six weeks.")
sponsor_page("partner/index.html", "Become an After Hours Partner | The After Hours Beit Midrash", "Become an After Hours Partner with a general gift to The After Hours Beit Midrash.")

print("built")
