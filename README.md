# The After Hours Beit Midrash: website

Live site: https://www.theafterhoursbeitmidrash.com (published from `main`)

## Where things live

- `index.html`: home
- `about/`, `team/`, `programs/`, `events/`, `contact/`
- `support/`: donation overview, linking to the sponsorship forms
- `moonlight/`, `cohort/`, `partner/`: sponsorship forms (save to Google Forms, then offer Venmo or Zelle)
- `assets/events.js`: upcoming events and their RSVP forms
- `assets/site.css`, `assets/chrome.css`: styles (chrome.css is the shared menu and footer)
- `assets/img/`: photos
- `tools/build_site.py`: builds the pages from one template; `tools/our_story.txt` holds the founders' story

## Making changes

Edit `tools/build_site.py` (or `tools/our_story.txt`), then run `python3 tools/build_site.py`.
Events are edited directly in `assets/events.js`.
