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

`index.html` (repo root, so GitHub Pages can serve it directly) is a hand-built HTML shell that:

1. Loads the recovered `assets/application-latest.js` / `.css` as-is (unmodified, byte-for-byte
   from the 2022-10-07 Wayback capture).
2. Provides every DOM element ID the bundled JS queries via jQuery selectors (`#main_field`,
   `#colors`, all toolbar buttons, all modals) — reverse-engineered by grepping the minified JS
   for every `$("#...")` reference (129 distinct IDs).
3. Supplies a minimal `I18n.t()` shim with the ~30 translation keys the JS calls, in English
   (the original used server-rendered i18n-js; that pipeline is gone).
4. Boots a blank `RaportDraw` instance directly against `#main_field`, bypassing the
   Rails-only `load_raport()` bootstrap (which needed server-provided JSON + save URLs).
   Toolbar buttons call straight into the `RaportDraw` public API (`zoom_in`, `step_back`,
   `set_current_tool`, `get_png_bytes`, `to_json`, etc.).
5. Persists patterns to `localStorage` via the app's own first-party `RaportLocalStore` class
   (the original app already shipped an offline mode for exactly this — `/raports/offline` —
   so this reuses first-party code, not a reimplementation).

**Verified working** (tested in a real Chromium instance, Sep 2026):
- Canvas renders with pattern/corrected/simulation panels, matching the original 3-panel layout.
- Painting on the canvas places beads and both linked views update live.
- Color palette add/select works; Raphael colorwheel picker renders.
- `raport.to_json()` produces valid serialized pattern data.
- Zoom, undo/redo, mirror, width/height resize are wired to the underlying class API.

**Known limitations of the rebuild:**
- No account system, no sharing/gallery/comments — inherent, server-gone.
- Bead-count calculator's material presets (Czech/Delica/Toho) UI is present but untested
  end-to-end.
- Sound-on-paint (`RaportColorSound`) silently no-ops — the WAV files were never archived.
- 3D bead-rope preview (`/raports/model`, a popup in the original) is NOT rebuilt — that was a
  separate server-rendered page.
- I18n strings are English-only (originals also had DE/RU).

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
└── archive/                 raw recovery artifacts, not needed to run the editor
    ├── mirror/                 77 raw Wayback captures of static/shell pages
    ├── cdx_full.json           CDX index of every 200-status capture Wayback has
    ├── download_manifest.json  url -> local path mapping used to build mirror/
    ├── download_assets.py      script used to fetch the mirror
    └── retry_failed.py         retry pass for rate-limited (503) fetches
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
