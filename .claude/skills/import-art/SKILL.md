---
name: import-art
description: This skill should be used when the user asks to "import my art", "add new pictures to the gallery", "add art from my Pictures folder", "put my new drawings on the site", "publish new artwork", or otherwise wants photos of their drawings and paintings from ~/Pictures/my art cropped, named, described and published on the art-gallery GitHub Pages site.
---

# Import art into the gallery

Turn phone photos of artworks in `~/Pictures/my art` into finished pieces on
https://shannonbay.github.io/art-gallery/ (repo `shannonbay/art-gallery`, branch `main`, Pages serves `/`).
Never modify or delete the original photos.

Scripts live in this skill's `scripts/` folder; run them with plain `python` (Pillow and numpy are installed,
but `python -I` hides numpy). Put spec files, grids and contact sheets in the session scratchpad, not the repo.

## 1. Find new photos

List `~/Pictures/my art` and compare against `references/imported.md`. Only photos not listed there are new.
If there are none, say so and stop.

## 2. Look at every new photo, then ask before publishing

Read each new photo. For each one decide what it is: an artwork, or something else (a screenshot,
a photo of a website). The site is public, so ask the user (AskUserQuestion, one batch) before going further when a piece:

- **uses someone else's line art** (colouring pages, printouts). Look for a book title or URL in the photo.
  Ask whether to include it and how to credit it. If the source is unknown, say so; captions then say
  "line art by an unknown artist". Some artists, like Johanna Basford, invite sharing on their own site:
  see `references/gallery-format.md` for the linked-piece format used for those.
- **shows a recognisable real person**, especially a child. Ask; never guess names.
- **is a duplicate or an unfinished version** of something already on the site.

Leaving a piece out is always fine: log it in `imported.md` as "left out", without the reason.

## 3. Crop each artwork

Run `python scripts/grid.py <scratch>/grid <photo> ...` and Read each grid image. Lines are every 100 px,
labelled every 200 px, in the photo's own pixel coordinates. Pick one treatment per piece:

- **As is**: the photo is already just the artwork.
- **crop** `[left, top, right, bottom]`: the paper is square-on to the camera.
- **quad** `[[nw],[sw],[se],[ne]]` + `size [w,h]`: the paper is photographed at an angle. Give the four corners
  of the artwork in source coordinates, anticlockwise from top-left, and an output size with the artwork's
  real proportions. This straightens it.
- **paper_patches**: polygons (in coordinates after crop/quad) painted over with paper colour, for a sofa
  corner, a finger, a clip or a shadow that can't be cropped away without cutting the art. The paper colour
  is the median of the cropped image's edges unless `paper` `[r,g,b]` is given.
- **square: true**: pads to a square with paper-coloured, feathered margins, so nothing is cut off where a
  square is required (artists' sharing sites, Instagram).

Crop tight to the artwork, keeping a little paper margin and none of the background. Write all pieces into one
spec (format in the docstring of `scripts/process_art.py`) and run:

```
python scripts/process_art.py <scratch>/spec.json C:/Users/layen/GitHub/art-gallery/images <scratch>/sheet.jpg
```

This writes `images/full/<slug>.jpg` (≤2000 px) and `images/thumb/<slug>.jpg` (720 px). Read the contact sheet
and look at each edge. If any background, sofa, carpet or fingers show, or art is cut off, nudge the coordinates
by 5–15 px and rerun. Repeat until every edge is clean.

## 4. Name and describe each piece

Look closely at each finished image and write:

- **Title**: short and evocative, two or three words, in the style of the existing ones ("Golden Afternoon",
  "Lion in the Wind", "Downcast Smile"). Use te reo Māori names with macrons for native subjects ("Kākāriki",
  "Kererū and Nīkau"). The slug is the title in kebab-case without macrons.
- **Medium**: what it was made with, as seen in the image ("Pencil", "Charcoal", "Watercolour",
  "Coloured pencil on notepaper", "Paint on paper"). Add the line-art credit for colourings.
- **Alt text**: one plain sentence describing what's depicted, its colours and its medium, for screen readers.

Show the user the titles and media in a short list with the contact sheet before publishing, and take their changes.

## 5. Add to the page and publish

Add a `<figure class="work">` block per piece to `index.html` as described in `references/gallery-format.md`.
Use the thumbnail's real width and height. Keep the first piece as is unless the user asks; it's the link-preview
image (`og:image`), and changing it means updating the `og:image*` meta tags too.

Commit to `main` in the art-gallery repo with a message like "Add <Title> to the gallery" and push. Then poll the live
site with a cache-busting query (`?v=<random>`) every 10 s for up to 3 minutes until the new `<cite>` titles appear
and each new `images/full` and `images/thumb` URL returns 200. Report what's live, with the link.

## 6. Log it

Add a row to `references/imported.md` for every photo handled this time, including those left out or not artwork,
and commit that with the gallery change.
