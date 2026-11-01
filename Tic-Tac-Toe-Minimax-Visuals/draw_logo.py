#!/usr/bin/env python3
"""Tic-Tac-Toe-Minimax logo: single abalone shell from above, holes arc, mother of pearl,
krill pink fleck, plankton green sheen; Anuphan wordmark beneath; 64px keeps shell only."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 900, 700
img = Image.new("RGB", (W, H), (6, 12, 24)); d = ImageDraw.Draw(img, "RGBA")
cx, cy, sx, sy = 450, 300, 300, 190
d.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=(18, 48, 92), outline=(110, 220, 225), width=8)
d.ellipse([cx - sx + 42, cy - sy + 36, cx + sx - 42, cy + sy - 36], fill=(96, 180, 196))
d.ellipse([cx - sx + 96, cy - sy + 72, cx + sx - 110, cy + sy - 72], fill=(178, 224, 214))
d.ellipse([cx - sx + 150, cy - sy + 104, cx + sx - 190, cy + sy - 104], fill=(214, 232, 222))
for k in range(6):  # breathing holes arc
    hx = cx - 190 + k * 62
    hy = cy - sy + 52 - (k * (5 - k)) * 3
    d.ellipse([hx - 13, hy - 10, hx + 13, hy + 10], fill=(4, 7, 12), outline=(200, 240, 235), width=2)
d.polygon([(cx + 120, cy + 60), (cx + 260, cy - 20), (cx + 270, cy + 10), (cx + 150, cy + 96)], fill=(110, 210, 140, 90))
d.ellipse([cx + 205, cy + 96, cx + 232, cy + 116], fill=(235, 150, 170))
try:
    f = ImageFont.truetype("fonts/Anuphan.ttf", 52)
except Exception:
    f = ImageFont.load_default()
txt = "Tic-Tac-Toe-Minimax"
bb = d.textbbox((0, 0), txt, font=f)
d.text(((W - (bb[2] - bb[0])) / 2, 560), txt, font=f, fill=(140, 230, 235))
out = "logo.png" if v == "ship" else f"scratch/logo-{v}.png"
img.save(out)
img.resize((64, 64)).save("scratch/logo64-ship.png" if v == "ship" else f"scratch/logo64-{v}.png")
print(out)
