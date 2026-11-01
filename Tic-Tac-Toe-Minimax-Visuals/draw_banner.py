#!/usr/bin/env python3
"""Tic-Tac-Toe-Minimax wordmark banner: night water over a closed reef, unlit boat with the
title painted in dull Anuphan along its hull, rope and sack over the far side, distant
warden launch with one shielded light, abalone on rocks, tube worm fans, pearl grit."""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont
random.seed(19)
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 1600, 560
img = Image.new("RGB", (W, H), (7, 18, 40)); d = ImageDraw.Draw(img, "RGBA")
for y in range(H):
    t = y / H; d.line([(0, y), (W, y)], fill=(int(5 + 5 * t), int(14 + 12 * t), int(34 + 22 * t)))
# rocks and abalone low in frame
for rx, ry, rw in ((120, 430, 420), (620, 452, 460), (1180, 438, 380)):
    d.polygon([(rx, ry + 90), (rx + 40, ry), (rx + rw - 30, ry - 14), (rx + rw, ry + 90)], fill=(15, 19, 27))
    for k in range(3):
        ax, ay = rx + 90 + k * 110, ry + 26
        d.ellipse([ax - 42, ay - 20, ax + 42, ay + 20], fill=(30, 58, 96), outline=(110, 220, 225), width=2)
        d.ellipse([ax - 24, ay - 11, ax + 24, ay + 11], fill=(170, 218, 208))
        d.ellipse([ax + 26, ay, ax + 34, ay + 7], fill=(235, 150, 170))
for _ in range(220):  # pearl grit
    x, y = random.randint(0, W), random.randint(430, 545)
    d.ellipse([x, y, x + 4, y + 3], fill=(205, 215, 205, 170))
for wx in (480, 1020):  # worm fans opening
    for k in range(5):
        x0 = wx + k * 13
        d.line([(x0, 500), (x0, 462)], fill=(175, 170, 145), width=3)
        d.ellipse([x0 - 9, 448, x0 + 9, 462], outline=(150, 225, 175), width=2)
# boat hull, black cut, title painted along hull
d.polygon([(260, 210), (1080, 210), (1000, 292), (340, 292)], fill=(4, 6, 10), outline=(40, 60, 80), width=2)
d.rectangle([640, 148, 760, 210], fill=(4, 6, 10))
d.line([(1080, 226), (1120, 330)], fill=(150, 140, 110), width=4)
d.polygon([(1102, 330), (1146, 330), (1138, 392), (1110, 392)], fill=(30, 30, 26), outline=(90, 84, 60), width=2)
# warden launch at right margin
d.polygon([(1330, 236), (1540, 236), (1500, 272), (1360, 272)], fill=(10, 16, 26), outline=(60, 80, 100), width=2)
for r, a in ((34, 30), (18, 70), (8, 150)):
    d.ellipse([1436 - r, 196 - r, 1436 + r, 196 + r], fill=(245, 248, 230, a))
try:
    f = ImageFont.truetype("fonts/Anuphan.ttf", 54)
except Exception:
    f = ImageFont.load_default()
txt = "Tic-Tac-Toe-Minimax"
bb = d.textbbox((0, 0), txt, font=f)
d.text(((670 - (bb[2] - bb[0]) / 2), 226), txt, font=f, fill=(168, 196, 198))
out = "banner.png" if v == "ship" else f"scratch/banner-{v}.png"
img.save(out); print(out)
