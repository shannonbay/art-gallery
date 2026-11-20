"""Draw a labelled coordinate grid over source photos so crop boxes and corners can be read off.

Usage: python grid.py OUT_DIR PHOTO [PHOTO ...]
Writes OUT_DIR/<photo-stem>-grid.jpg for each photo, in the photo's own pixel coordinates
(after EXIF rotation), with a line every 100 px and a label every 200 px.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

out_dir = sys.argv[1]
os.makedirs(out_dir, exist_ok=True)
for path in sys.argv[2:]:
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=max(20, img.width // 30))
    except TypeError:  # Pillow < 10.1
        font = ImageFont.load_default()
    w, h = img.size
    for x in range(0, w, 100):
        draw.line([(x, 0), (x, h)], fill=(255, 0, 255) if x % 200 == 0 else (0, 200, 255), width=1)
        if x % 200 == 0:
            draw.text((x + 3, 3), str(x), fill=(255, 0, 255), font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    for y in range(0, h, 100):
        draw.line([(0, y), (w, y)], fill=(255, 0, 255) if y % 200 == 0 else (0, 200, 255), width=1)
        if y % 200 == 0:
            draw.text((3, y + 3), str(y), fill=(255, 0, 255), font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    stem = os.path.splitext(os.path.basename(path))[0]
    dest = os.path.join(out_dir, f"{stem}-grid.jpg")
    img.save(dest, quality=85)
    print(dest, img.size)
