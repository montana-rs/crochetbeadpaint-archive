# CrochetBeadPaint — Digital Preservation Archive & Offline Rebuild

> **⚠️ This is a preservation project, not a claim of ownership.**
> `crochetbeadpaint.info` shut down permanently. This repository exists solely to keep a
> historically/functionally useful tool from disappearing entirely, for personal and
> educational reference. It is **not** a fork, a competing product, or a redistribution of
> anyone's paid/private content. See [`NOTICE.md`](./NOTICE.md) for the full provenance and
> takedown statement.

## What this is

`crochetbeadpaint.info` was a free web app (Rails backend) for designing bead-crochet rope
patterns: paint a repeating bead pattern on a grid, see it simulated as a spiral/corrected
view, export to PNG/PDF/DBB/JBB, calculate bead counts, and browse a community gallery of
patterns. This repo is a recovery of what could be salvaged from the Internet Archive Wayback
Machine, plus a working **offline rebuild of the pattern editor** assembled from the recovered
client-side code — runs standalone in a browser, no server, no account, no tracking.

**Live demo (GitHub Pages):** `https://<owner>.github.io/<repo>/` (fill in once Pages is
enabled — see below).

## What was and wasn't recoverable

- **The editor's client-side application logic — fully recovered.** The site's asset pipeline
  (Sprockets/Rails) bundled the entire front-end into one static, fingerprinted JS file per
  deploy. Static assets aren't behind auth, so the Wayback Machine has clean captures of them
  going back to 2014. The last capture (Oct 7 2022) contains the full `RaportDraw` editor class
  and its supporting classes (`RaportRender`, `RaportPaintTool`, `RaportFillTool`,
  `RaportLineTool`, `RaportRectangleTool`, `RaportSelectTool`, `RaportPickTool`,
  `RaportElement`, `RaportColor`, `RaportLocalStore`, `RaportSoundPlayer`, PNG/PDF export,
  bead-count calculator, undo/redo, mirror/rotate/clone tools) — bundled together with jQuery
  1.12.4, Bootstrap's modal JS, Raphael.js (+ colorwheel plugin), jsPDF, FileSaver.js, and
  CreateJS/SoundJS. This is `assets/application-latest.js` (~1.3MB minified, unmodified from
  the archive) and `assets/application-latest.css`.
- **Actual saved user patterns — NOT recoverable.** Every pattern-editing page
  (`/raports/:id`) lived behind a login wall for its entire history — every Wayback capture,
  even from 2014, is a 302 redirect to `/users/sign_in`. Pattern data lived server-side in the
  Rails DB and was never crawlable. Nobody's private/community pattern content is in this repo.
- **Static/login shell pages — recovered where they existed.** `archive/mirror/` contains 77
  raw Wayback captures (about page in 3 locales, sign-in/sign-up/password-reset shells,
  robots.txt, fonts/icons/images referenced by the CSS). Historical reference only, not needed
  to run the offline editor.
- **Server-only features — inherently NOT recoverable**: community gallery, comments, likes,
  sharing, account sync, and the sound-pack `.wav` files (referenced in code but never linked
  from any crawled page, so Wayback never captured them).

## The offline rebuild

`index.html` (repo root, so GitHub Pages can serve it directly) calls the site's own real
bootstrap function, `load_raport()`, instead of reimplementing the editor's wiring:

1. Loads the recovered `assets/application-latest.js` / `.css` as-is (unmodified, byte-for-byte
   from the 2022-10-07 Wayback capture). `load_raport()` — the ~500-line function the Rails view
   called on every editor page load — is a genuine top-level function in that bundle, not scoped
   inside anything, so it's callable directly. It's also saved standalone, extracted verbatim and
   beautified, at `archive/load_raport_extracted{,.beautified}.js` for anyone auditing this repo.
2. Provides every DOM element ID the bundled JS queries via jQuery selectors (`#main_field`,
   `#colors`, all toolbar buttons, all modals) — reverse-engineered by grepping the minified JS
   for every `$("#...")` reference (129 distinct IDs) plus tracing `load_raport()`'s full body
   line by line for every selector, `.data()` call, and event binding it makes.
3. Uses the bundle's own **real, complete i18n-js library and translation tables** — confirmed
   present in `application-latest.js` (`I18n.translations`, multiple locales including the
   Russian strings visible in archived tutorial screenshots, e.g. "Название" for "Name"). No
   hand-typed translation shim; whatever the original site really said is what displays here.
4. Calls `load_raport('/raports/offline', ..., i=true, ...)` — offline mode, a real feature the
   original app already shipped (see `RaportLocalStore` in the bundle) for exactly this case, not
   a reimplementation. `local_store` (a `new RaportLocalStore()`) is declared as a page-global
   here because the original Rails layout partial did that for every page — that one line is
   the only piece of "glue" standing in for missing server-rendered markup.
5. Serves FontAwesome 5 / LigatureSymbols / summernote webfonts from `webfonts/` and `font/` at
   the repo root, matching the CSS's own absolute `/webfonts/...` and `/font/...` references
   (recovered files, just needed to sit where the stylesheet already expects them).

**Toolbar icons**: the archived CSS defines every FontAwesome glyph but the `<i class="fa fa-*">`
markup itself lived in server-rendered Rails view templates that were never captured (only static
assets were crawlable — see above). Icon choices in `index.html` are FontAwesome classes matched
to each button's confirmed function from tracing `load_raport()`'s own code (e.g. `#set_paint` →
paint brush, `#mirror_horizontal` → horizontal arrows) and cross-checked against two 2017–2020
Russian-language tutorial videos of the live site
([lD3hYiHTNI8](https://www.youtube.com/watch?v=lD3hYiHTNI8),
[qB9c3ZqkLyo](https://www.youtube.com/watch?v=qB9c3ZqkLyo)) whose transcripts were reviewed in
full. **This is a disclosed best-match reconstruction, not a captured fact** — video *frames*
showing the literal pixel icons could not be extracted (see Research notes below), so treat icon
choices as informed but unverified against a direct screenshot.

One small piece of markup was added beyond what `load_raport()` itself provides: `data-dismiss=
"modal"` on the color-picker's OK button. Tracing the code shows `#choose_color`'s own click
handler updates the color but never calls `.modal("hide")` — the original Rails-rendered button
must have carried a dismiss attribute we don't have captured, since the dialog obviously has to
close after choosing a color. Documented here rather than left silent.

**Verified working end-to-end** (real Chromium via CDP, Sep 2026 — not guessed):
- Canvas renders with pattern/corrected/simulation panels at correct proportions (this needed
  the original's Bootstrap `.row-fluid` container present — `RaportRender`'s own sizing function
  measures it — omitting it was the earlier build's main cause of the "too zoomed out" layout).
- Painting on the canvas places beads; pattern/corrected views update live; color-repeat table
  and disc stats (`Repeat:`, `Used rows:`, `Elements:`) recompute correctly and show real numbers
  once anything is painted (an all-blank canvas legitimately shows "NaN" for repeat length —
  traced into `RaportElement.repeat_length()`/`get_last_not_empty_index()`, this is the real
  app's own behavior on an empty pattern, not a rebuild bug).
- **Double-click a palette swatch → real Raphael colorwheel modal opens pre-loaded with that
  color, with a Delete button → pick a new hue → OK → modal closes → palette and canvas both
  update.** This is the exact "click into a color and change it with the wheel" behavior
  requested — confirmed by direct interaction, not inferred.
- Save persists the pattern (including edited colors) to `localStorage.raports` in the app's own
  JSON format; reloading the page restores it correctly.
- FontAwesome/LigatureSymbols/summernote webfonts load without 404s.

**Known limitations of the rebuild:**
- No account system, no sharing/gallery/comments — inherent, server-gone.
- Image-to-pattern import is genuinely unrecoverable, not just unwired: it ran in a Web Worker
  script loaded from a URL the Rails view injected at render time, which was never linked from
  any crawled page, so the Wayback Machine never captured it. The toolbar button and its modal
  are present (for layout fidelity) but explain this instead of silently doing nothing.
- Sound-on-paint (`RaportColorSound`) silently no-ops — the WAV files were never archived.
- 3D bead-rope preview (`/raports/model`, a popup in the original) is NOT rebuilt — that was a
  separate server-rendered page.
- Toolbar icon glyph choices are a disclosed reconstruction (see above), not a captured fact.

## Directory layout

```
.
├── README.md              this file
├── LICENSE                MIT license for the rebuild/glue code (see NOTICE.md for scope)
├── NOTICE.md               provenance, ownership, and takedown statement
├── index.html              the offline editor — GitHub Pages entry point
├── assets/
│   ├── application-latest.js   2022-10-07 Wayback capture — original app bundle
│   └── application-latest.css  2022-10-07 Wayback capture — original stylesheet
├── webfonts/               FontAwesome 5 / summernote font files (recovered), served from repo
│                           root because application-latest.css references them at /webfonts/...
├── font/                   LigatureSymbols font files (recovered), served at /font/... likewise
└── archive/                 raw recovery artifacts, not needed to run the editor
    ├── mirror/                 77 raw Wayback captures of static/shell pages
    ├── cdx_full.json           CDX index of every 200-status capture Wayback has
    ├── download_manifest.json  url -> local path mapping used to build mirror/
    ├── download_assets.py      script used to fetch the mirror
    ├── retry_failed.py         retry pass for rate-limited (503) fetches
    ├── load_raport_extracted.js             verbatim extraction of the real bootstrap function
    └── load_raport_extracted.beautified.js  same, pretty-printed for readability
```

## Running it locally

```
git clone https://github.com/<owner>/<repo>.git
cd <repo>
python3 -m http.server 8765
# open http://localhost:8765/
```

No build step, no server-side code, no dependencies beyond a modern browser.

## Recovery process notes (for anyone re-doing / extending this)

- Wayback Machine's CDX API (`web.archive.org/cdx/search/cdx?url=...&output=json`) enumerates
  every URL/timestamp ever captured for a domain — used to find all 96 `statuscode:200`
  captures across the site's lifetime (52,833 total captured URL variants once you include the
  endless 302-redirect noise from crawled dynamic pages).
- `web.archive.org/web/<timestamp>id_/<original_url>` (note the `id_` suffix) returns the RAW
  captured bytes with Wayback's toolbar/banner stripped — use this form for asset downloads,
  not the normal `/web/<timestamp>/<url>` viewer form.
- Wayback aggressively rate-limits (429/503) under burst traffic; back off to ~1.5–2s between
  requests and retry 503s with a short backoff.

## Where the original was hosted

`crochetbeadpaint.info`'s DNS **A record is still live** as of this recovery pass and resolves to
`89.188.171.6`, but nothing answers on port 80/443 (connection refused/timeout) — the server
process is down, not the domain. This means the site could theoretically come back at the same
IP without warning; it also means the shutdown is a hosting/server decision, not a domain
expiry, consistent with "going down permanently" being an intentional choice by whoever ran it
rather than a lapsed registration. `whois` on the IP was attempted for hosting-provider attribution
but returned no useful registrant data beyond the IP block owner — insufficient to name a specific
host or operator here, and not pursued further since it's not needed to complete the recovery.

## Video research notes

Two tutorial videos were identified and their transcripts reviewed in full to verify UI behavior
against the recovered code (both linked above). Confirmed from transcript content, independent of
any screenshot: the presenter narrates double-clicking a palette color to bring up "the same color
wheel used to add colors" for editing an existing one — this matches, word for word, the behavior
this rebuild now reproduces via `load_raport()`'s real double-click handler. **Frame-level images
from these videos could not be extracted in this pass** — both direct download (yt-dlp) and
in-browser playback hit persistent network failures (SSL handshake timeouts to `googlevideo.com`,
and the YouTube player never progressing past `readyState 0`) in this environment. Icon and layout
details in this rebuild are therefore sourced from the transcripts' verbal descriptions and from
tracing the actual code paths, not from viewing the tutorials' pixels directly — treat any visual
claim (icon shapes, exact colors, spacing) as the best available reconstruction, not a verified
screenshot match, until someone with working video access can confirm it.
