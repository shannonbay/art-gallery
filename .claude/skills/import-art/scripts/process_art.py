"""Turn photos of artworks into gallery images: crop or straighten, patch, pad to square, resize.

Usage: python process_art.py SPEC.json IMAGES_DIR SHEET.jpg

SPEC.json is a list of pieces. Every coordinate is in pixels.
  {
    "slug": "kakariki",                      # output filename, kebab-case
    "source": "C:/Users/.../photo.jpg",      # original photo (never modified)
    "crop": [left, top, right, bottom],      # optional: rectangle in source coordinates
    "quad": [[nw], [sw], [se], [ne]],        # optional instead of crop: the artwork's four corners
    "size": [w, h],                          #   in the source, and the straightened output size
    "paper_patches": [[[x, y], ...], ...],   # optional: polygons, in coordinates AFTER crop/quad,
                                             #   painted over with paper colour (sofa, fingers, clips)
    "paper": [r, g, b],                      # optional: paper colour; default = median of the edges
    "square": true                           # optional: pad to a square with paper-coloured margins
  }

Writes IMAGES_DIR/full/<slug>.jpg (longest side at most 2000 px), IMAGES_DIR/thumb/<slug>.jpg
(longest side 720 px) and a contact sheet of every result at SHEET.jpg for checking.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

FULL_MAX = 2000
THUMB_MAX = 720
FEATHER = 10


def edge_paper(img):
    """Median colour of an 8 px band round the edge: the paper, once the photo is cropped to the art."""
    a = np.asarray(img)
    band = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3),
                           a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(band, axis=0))


def patch(img, polygons, paper):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    for poly in polygons:
        draw.polygon([tuple(p) for p in poly], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(5))
    out = img.copy()
    out.paste(Image.new("RGB", img.size, paper), (0, 0), mask)
    return out


def squared(img, paper):
    side = max(img.size)
    square = Image.new("RGB", (side, side), paper)
    mask = Image.new("L", img.size, 0)
    mask.paste(255, (FEATHER, FEATHER, img.width - FEATHER, img.height - FEATHER))
    mask = mask.filter(ImageFilter.GaussianBlur(FEATHER / 2))
    square.paste(img, ((side - img.width) // 2, (side - img.height) // 2), mask)
    return square


def build(piece):
    img = ImageOps.exif_transpose(Image.open(piece["source"])).convert("RGB")
    if "quad" in piece:
        nw, sw, se, ne = piece["quad"]
        img = img.transform(tuple(piece["size"]), Image.QUAD, (*nw, *sw, *se, *ne), Image.BICUBIC)
    elif "crop" in piece:
        img = img.crop(tuple(piece["crop"]))
    paper = tuple(piece["paper"]) if "paper" in piece else edge_paper(img)
    if piece.get("paper_patches"):
        img = patch(img, piece["paper_patches"], paper)
    if piece.get("square"):
        img = squared(img, paper)
    return img, paper


def main():
    spec_path, images_dir, sheet_path = sys.argv[1:4]
    with open(spec_path, encoding="utf-8") as f:
        pieces = json.load(f)
    os.makedirs(os.path.join(images_dir, "full"), exist_ok=True)
    os.makedirs(os.path.join(images_dir, "thumb"), exist_ok=True)
    results = []
    for piece in pieces:
        art, paper = build(piece)
        full = art.copy()
        full.thumbnail((FULL_MAX, FULL_MAX), Image.LANCZOS)
        full.save(os.path.join(images_dir, "full", f"{piece['slug']}.jpg"), quality=88, optimize=True, progressive=True)
        thumb = art.copy()
        thumb.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
        thumb.save(os.path.join(images_dir, "thumb", f"{piece['slug']}.jpg"), quality=82, optimize=True, progressive=True)
        results.append(full)
        print(f"{piece['slug']}: full {full.size[0]}x{full.size[1]}, thumb {thumb.size[0]}x{thumb.size[1]}, paper {paper}")

    cell, cols = 420, min(5, len(results))
    rows = -(-len(results) // cols)
    sheet = Image.new("RGB", (cell * cols, cell * rows), (90, 90, 90))
    for n, art in enumerate(results):
        t = art.copy()
        t.thumbnail((cell - 12, cell - 12))
        sheet.paste(t, ((n % cols) * cell + 6, (n // cols) * cell + 6))
    sheet.save(sheet_path, quality=85)
    print("sheet:", sheet_path)


if __name__ == "__main__":
    main()
