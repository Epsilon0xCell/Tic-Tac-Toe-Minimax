#!/usr/bin/env python3
"""Tic-Tac-Toe-Minimax intro banner: moonless reef, wordless. Reef ledge with abalone,
tube worms, sonar rings in a channel, coral, sparse bubbles, black surface skin with a
boat shadow, one distant warden light. No text, numerals, insignia, or human figure."""
import sys, random, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
random.seed(71)
W, H = 1600, 900
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
CYAN = (110, 220, 225); GREEN = (110, 210, 140); PINK = (235, 150, 170); DEEP = (8, 22, 48)
img = Image.new("RGB", (W, H), DEEP); d = ImageDraw.Draw(img, "RGBA")
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(6 + 6 * t), int(16 + 14 * t), int(38 + 26 * t)))
# surface skin at top, black, faint cyan smear, boat shadow crossing
d.rectangle([0, 0, W, 86], fill=(3, 5, 10))
d.polygon([(180, 30), (1180, 22), (1310, 52), (260, 62)], fill=(10, 14, 20))
for x in range(120, 1450, 7):
    d.line([(x, 84 + int(4 * math.sin(x / 90.0))), (x + 4, 84 + int(4 * math.sin(x / 90.0)))], fill=(60, 160, 175, 90), width=2)
# warden light, far right, steady
for r, a in ((46, 26), (26, 60), (12, 130)):
    d.ellipse([1470 - r, 150 - r, 1470 + r, 150 + r], fill=(240, 244, 220, a))
d.ellipse([1464, 144, 1476, 156], fill=(250, 252, 235))
# sonar rings in channel
for cx, cy in ((800, 330), (800, 330), (800, 330)):
    pass
for rad, alpha in ((90, 120), (190, 80), (300, 50), (420, 30)):
    d.ellipse([800 - rad, 330 - rad // 2, 800 + rad, 330 + rad // 2], outline=(140, 225, 235, alpha), width=3)
# coral fingers far side
for bx in (1180, 1260, 1350, 1420):
    for k in range(4):
        x0 = bx + k * 18
        tip = 560 - random.randint(90, 170)
        d.line([(x0, 560), (x0 + random.randint(-14, 14), tip)], fill=(30, 44, 70), width=9)
        d.ellipse([x0 - 8, tip - 8, x0 + 8, tip + 8], fill=(44, 70, 100))
# reef ledge lower third, basalt dark pitted
d.polygon([(0, 620), (420, 580), (900, 610), (1600, 570), (1600, 900), (0, 900)], fill=(16, 20, 28))
for _ in range(500):
    x, y = random.randint(0, W - 4), random.randint(580, H - 4)
    d.ellipse([x, y, x + random.randint(2, 7), y + 2], fill=(8, 10, 14))
for x in range(0, W, 26):  # short algae fringe
    d.line([(x, 612 + int(10 * math.sin(x / 70.0))), (x + 3, 596 + int(10 * math.sin(x / 70.0)))], fill=(40, 110, 80), width=2)
def abalone(cx, cy, s, glow):
    d.ellipse([cx - s, cy - int(s * 0.55), cx + s, cy + int(s * 0.55)], fill=(26, 52, 84), outline=CYAN if glow else (70, 140, 150), width=3)
    d.ellipse([cx - int(s * 0.7), cy - int(s * 0.36), cx + int(s * 0.7), cy + int(s * 0.36)], fill=(120, 190, 200))
    d.ellipse([cx - int(s * 0.45), cy - int(s * 0.2), cx + int(s * 0.45), cy + int(s * 0.2)], fill=(190, 220, 215))
    for k in range(5):
        hx = cx - int(s * 0.5) + k * int(s * 0.24)
        d.ellipse([hx - 4, cy - int(s * 0.42), hx + 4, cy - int(s * 0.42) + 8], fill=(5, 8, 12))
    d.ellipse([cx + int(s * 0.55), cy + 2, cx + int(s * 0.55) + 9, cy + 9], fill=PINK)
for cx, cy, s in ((220, 680, 74), (520, 716, 62), (860, 690, 82), (1180, 724, 58), (1420, 676, 66)):
    abalone(cx, cy, s, glow=(cx in (860, 220)))
# overturned loose shells showing nacre
for cx, cy in ((390, 790), (1020, 800)):
    d.ellipse([cx - 44, cy - 20, cx + 44, cy + 20], fill=(225, 175, 190), outline=(150, 200, 190), width=2)
# tube worm clusters
for wx, wy in ((330, 640), (680, 650), (1080, 648), (1330, 640)):
    for k in range(6):
        x0 = wx + k * 12
        d.line([(x0, wy + 60), (x0, wy + 18)], fill=(180, 175, 150), width=3)
        for ang in range(0, 360, 45):
            d.line([(x0, wy + 16), (x0 + int(11 * math.cos(math.radians(ang))), wy + 16 + int(8 * math.sin(math.radians(ang))))], fill=(170, 230, 185), width=2)
# sparse bubbles bending sideways
for bx, by in ((620, 560), (648, 500), (676, 446), (700, 398)):
    d.ellipse([bx, by, bx + 10, by + 10], outline=(180, 235, 240), width=2)
# bioluminescent specks
for _ in range(140):
    x, y = random.randint(0, W), random.randint(100, 860)
    d.ellipse([x, y, x + 3, y + 3], fill=(140, 235, 225, 160))
img = img.filter(ImageFilter.GaussianBlur(0.6))
rng = np.random.default_rng(4); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "intro-banner.png" if v == "ship" else f"scratch/intro-{v}.png"
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
img.save(out); print(out)
