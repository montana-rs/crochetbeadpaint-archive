# Notice: Provenance, Ownership & Takedown

## What this repository is

This repository preserves and rebuilds public functionality of `crochetbeadpaint.info`, a
bead-crochet pattern design tool that has shut down permanently. It exists to prevent a useful,
free community tool from disappearing entirely, for personal, educational, and archival
purposes — in the spirit of digital preservation projects like the Internet Archive itself.

**This is not:**
- A claim of authorship or ownership over the original application, its design, its brand, or
  its name.
- A commercial product, a monetized fork, or a competitor to any successor site.
- A redistribution of any user's private data, saved patterns, account information, or
  community content. **None of that exists in this repository** — it was never accessible to
  the Wayback Machine (every pattern-editing page required login for its entire history) and
  was not obtained from any other source.
- An attempt to misrepresent the origin of this code as original work by the repository owner.

## What's actually in this repository

- The client-side JavaScript/CSS bundle (`assets/application-latest.js`,
  `assets/application-latest.css`) as captured by the Internet Archive's Wayback Machine on
  2022-10-07, unmodified. This bundle was served publicly and without authentication by the
  original site to every visitor's browser (it is, by nature, distributed to any HTTP client
  that requests it — this is how client-side web applications work). Wayback Machine capture
  is a matter of public record, freely queryable via `web.archive.org`.
- A small amount of original "glue" HTML/JS (`index.html`) written from scratch to host the
  above bundle standalone, by mapping the DOM element IDs the bundle's minified code queries.
  This glue code is original work and is MIT-licensed (see `LICENSE`).
- Static assets (fonts, icons, locale shell pages) similarly captured from public,
  unauthenticated URLs, archived by Wayback Machine.

## Why this is reasonable to publish

- The recovered JavaScript/CSS was never gated — it was served to every anonymous visitor of
  the original site as a normal part of loading the page, exactly as it's served here.
- No account data, saved user patterns, private messages, or any other non-public content is
  present or reproduced.
- The original site and service are permanently discontinued; this project does not compete
  with, divert users from, or cause any commercial harm to an active service.
- This mirrors common, widely-accepted practice for preserving discontinued web tools (e.g.
  Flash game preservation projects, abandoned freeware mirrors, archive.org's own hosted
  copies of dead software) — recovery for continuity of access, not appropriation.

## If you are the original developer/rights-holder

If you are affiliated with `crochetbeadpaint.info` and have any concern about this repository
— whether about the code, the name, or anything else — please open an issue on this repository
or contact the repository owner directly. This project will be taken down, renamed, relicensed,
or amended promptly on request. The intent here is purely preservation of a tool that would
otherwise be lost, with full respect for the original creator's work.

## License scope

See `LICENSE` for the license terms. It applies **only** to the original glue code written for
this repository (`index.html` and any other files explicitly marked as original work). It does
NOT purport to grant any license over `assets/application-latest.js` /
`assets/application-latest.css`, which remain the intellectual property of their original
author(s) and are included here solely under the preservation/fair-use rationale above.
