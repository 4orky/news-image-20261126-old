#!/usr/bin/env python3
"""Render the entry image for news-image-20261126.

Draws a one-page newspaper front page summing up Thursday,
26 November 2026, as a 1024x1024 PNG. Every coordinate, colour
and string is fixed in this file, so the output is fully
deterministic: running it twice writes byte-identical files.

Editorial choices (researched 26 Nov 2026, Asia morning):
  LEAD  - the 100th Macy's Thanksgiving Day Parade marches
          through New York on Thanksgiving Day itself, with a
          record 100 balloons and a nor'easter threatening to
          ground them. The day's signature event.
  PANEL - Colombia: troops storm a Cartagena supermarket and
          free all 20 remaining hostages after a 17-hour siege.
  PANEL - Pacific: Australia and Solomon Islands sign a
          sweeping security treaty; Honiara bars foreign bases.
  PANEL - Ukraine war: leaked Rosstat records analysed by the
          BBC put Russian military deaths at 490,334, and about
          700,000 counting the missing.
  PANEL - Malaysia sues Google for $146m over harmful content
          on YouTube.
  STRIP - Bangladesh garment workers win a 36% pay rise;
          India marks Constitution Day.

Run:  python3 render.py   (writes entry.png next to this file)
Requires Pillow and the DejaVu fonts (render-time only; the
submitted entrypoint main.py is standard library only).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
SKY_TOP = (176, 214, 235)
SKY_BOT = (232, 240, 244)
GREY = (90, 86, 76)
LIGHT_RULE = (180, 172, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting `width`."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_skyline(draw, x0, y0, x1, y1):
    """Flat skyline silhouette with lit windows, inside a box."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY_BOT)
    for i in range(14):  # sky bands for a soft gradient
        t = i / 13.0
        col = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * t)
                    for c in range(3))
        draw.rectangle([x0, y0 + (y1 - y0) * i // 14,
                        x1, y0 + (y1 - y0) * (i + 1) // 14], fill=col)
    # sun, top left so it cannot collide with a balloon
    draw.ellipse([x0 + 16, y0 + 14, x0 + 58, y0 + 56], fill=(250, 204, 90))
    buildings = [(0, 150, 46), (52, 110, 40), (98, 170, 52), (156, 96, 44),
                 (206, 140, 48), (260, 84, 42), (308, 128, 46),
                 (360, 168, 40)]
    for bx, bh, bw in buildings:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1],
                       fill=(52, 68, 92))
        for wy in range(y1 - bh + 10, y1 - 8, 18):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 6, 14):
                if (wx + wy) % 29 < 15:
                    draw.rectangle([wx, wy, wx + 5, wy + 7],
                                   fill=(252, 220, 130))


def draw_balloon(draw, cx, cy, rx, ry, body, dark):
    """A parade balloon: round body, highlight, ropes, basket."""
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=body,
                 outline=dark, width=3)
    draw.ellipse([cx - rx + 12, cy - ry + 12, cx - rx + 34, cy - ry + 34],
                 fill=(255, 255, 255))
    draw.line([(cx - rx // 2, cy + ry - 4), (cx - 14, cy + ry + 26)],
              fill=dark, width=2)
    draw.line([(cx + rx // 2, cy + ry - 4), (cx + 14, cy + ry + 26)],
              fill=dark, width=2)
    draw.rectangle([cx - 15, cy + ry + 26, cx + 15, cy + ry + 40],
                   fill=(120, 72, 20), outline=dark, width=2)


def draw_parade(draw, x0, y0, x1, y1):
    """Lead illustration: balloons over the Manhattan skyline."""
    draw_skyline(draw, x0, y0, x1, y1)
    draw_balloon(draw, x0 + 105, y0 + 78, 62, 52, (46, 111, 197),
                 (18, 52, 96))
    draw_balloon(draw, x0 + 265, y0 + 52, 54, 46, (198, 44, 44),
                 (110, 16, 20))
    draw_balloon(draw, x0 + 320, y0 + 100, 42, 36, (240, 178, 44),
                 (140, 100, 10))
    # wind streaks (the nor'easter)
    for wy, wl in [(y0 + 30, 90), (y0 + 150, 70), (y0 + 190, 110)]:
        draw.line([(x0 + 12, wy), (x0 + 12 + wl, wy)], fill=(255, 255, 255),
                  width=3)
    # confetti
    confetti = [(40, 210, RED), (150, 235, BLUE), (230, 205, (34, 139, 90)),
                (320, 240, RED), (90, 260, (240, 178, 44)),
                (280, 265, BLUE), (380, 220, (34, 139, 90))]
    for cx, cy, col in confetti:
        draw.rectangle([x0 + cx, y0 + cy, x0 + cx + 9, y0 + cy + 5],
                       fill=col)


def draw_shop(draw, x0, y0, size):
    """Colombia panel: a supermarket front with a rescue shield."""
    draw.rectangle([x0, y0, x0 + size, y0 + size], fill=(214, 228, 240))
    draw.rectangle([x0 + 14, y0 + 52, x0 + size - 14, y0 + size - 10],
                   fill=(245, 245, 245), outline=INK, width=2)
    for i in range(6):  # striped awning
        col = RED if i % 2 == 0 else (255, 255, 255)
        draw.polygon([(x0 + 14 + i * 17, y0 + 26),
                      (x0 + 14 + (i + 1) * 17, y0 + 26),
                      (x0 + 14 + (i + 1) * 17, y0 + 52),
                      (x0 + 14 + i * 17, y0 + 52)], fill=col,
                     outline=INK)
    draw.rectangle([x0 + 46, y0 + 78, x0 + size - 46, y0 + size - 10],
                   fill=(120, 170, 210), outline=INK, width=2)
    draw.line([(x0 + size // 2, y0 + 78), (x0 + size // 2, y0 + size - 10)],
              fill=INK, width=2)
    # shield with a check mark
    sx, sy = x0 + size - 42, y0 + 8
    draw.polygon([(sx, sy), (sx + 34, sy), (sx + 34, sy + 24),
                  (sx + 17, sy + 38), (sx, sy + 24)], fill=BLUE,
                 outline=INK)
    draw.line([(sx + 8, sy + 17), (sx + 15, sy + 25), (sx + 27, sy + 10)],
              fill=(255, 255, 255), width=4)


def draw_island(draw, x0, y0, size):
    """Pacific panel: an island, palm and no-base shield."""
    draw.rectangle([x0, y0, x0 + size, y0 + size], fill=(176, 214, 235))
    for wy in range(3):  # sea waves
        yy = y0 + size - 34 + wy * 11
        draw.arc([x0 + 6, yy, x0 + size - 6, yy + 16], 0, 180,
                 fill=(255, 255, 255), width=3)
    draw.ellipse([x0 + 18, y0 + size - 52, x0 + size - 18, y0 + size - 8],
                 fill=(96, 160, 90), outline=(52, 100, 52), width=2)
    draw.line([(x0 + size // 2, y0 + 34), (x0 + size // 2, y0 + size - 44)],
              fill=(120, 72, 20), width=5)
    for dx, dy in [(-30, -14), (-12, -24), (12, -24), (30, -14)]:
        draw.line([(x0 + size // 2, y0 + 36),
                   (x0 + size // 2 + dx, y0 + 36 + dy)],
                  fill=(34, 139, 90), width=4)
    draw.ellipse([x0 + 12, y0 + 12, x0 + 34, y0 + 34], fill=(250, 204, 90))


def draw_chart(draw, x0, y0, size):
    """Ukraine panel: rising bars and the verified toll."""
    draw.rectangle([x0, y0, x0 + size, y0 + size], fill=(232, 228, 220))
    bars = [34, 58, 84]
    for i, bh in enumerate(bars):
        bx = x0 + 18 + i * 38
        draw.rectangle([bx, y0 + size - 22 - bh, bx + 26,
                        y0 + size - 22], fill=(70, 70, 78))
    draw.line([(x0 + 10, y0 + size - 22), (x0 + size - 8, y0 + size - 22)],
              fill=INK, width=2)
    draw.text((x0 + 10, y0 + 10), "490,334", font=font(SANS_BOLD, 21),
              fill=RED)


def draw_gavel(draw, x0, y0, size):
    """Malaysia panel: a judge's gavel over a courthouse."""
    draw.rectangle([x0, y0, x0 + size, y0 + size], fill=(214, 228, 240))
    draw.polygon([(x0 + 14, y0 + 108), (x0 + size - 14, y0 + 108),
                  (x0 + size // 2, y0 + 84)], fill=GREY, outline=INK)
    for i in range(3):
        cx = x0 + 30 + i * 36
        draw.rectangle([cx, y0 + 112, cx + 10, y0 + size - 14], fill=INK)
    draw.rectangle([x0 + 14, y0 + size - 12, x0 + size - 14, y0 + size - 8],
                   fill=INK)
    # gavel, upright: horizontal head, vertical handle, sound block
    draw.rectangle([x0 + 66, y0 + 10, x0 + 118, y0 + 30], fill=(150, 96, 40),
                   outline=INK, width=2)
    draw.line([(x0 + 92, y0 + 30), (x0 + 92, y0 + 66)], fill=(120, 72, 20),
              width=7)
    draw.rectangle([x0 + 68, y0 + 66, x0 + 116, y0 + 76], fill=(150, 96, 40),
                   outline=INK, width=2)


PANELS = [
    ("COLOMBIA", "All 20 hostages freed in Cartagena raid",
     "Troops storm an Exito supermarket after a 17-hour siege; "
     "one captor killed, four arrested.", draw_shop),
    ("THE PACIFIC", "Solomons choose Australia, shut door on bases",
     "Canberra becomes primary security partner in a treaty worth "
     "A$740m over 10 years.", draw_island),
    ("UKRAINE WAR", "Russia's own ledger: nearly 500,000 dead",
     "Leaked Rosstat records analysed by the BBC put the toll at "
     "490,334 - 700,000 with the missing.", draw_chart),
    ("MALAYSIA", "Kuala Lumpur sues Google for $146 million",
     "Regulator says YouTube failed to curb gambling, scams and "
     "harmful videos.", draw_gavel),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # ---- masthead ----
    title = font(SERIF, 66)
    d.text((W // 2, 30), "THE WORLD TODAY", font=title, fill=INK,
           anchor="ma")
    rule(d, mx, 108, W - mx, 3)
    rule(d, mx, 114, W - mx, 1)
    dateline = font(SANS_BOLD, 21)
    d.text((mx, 126), "THURSDAY, 26 NOVEMBER 2026", font=dateline, fill=RED)
    right = "NEW YORK  ·  LONDON  ·  SYDNEY"
    d.text((W - mx, 126), right, font=font(SANS, 18), fill=GREY, anchor="ra")

    # ---- lead story ----
    y = 168
    d.text((mx, y), "THANKSGIVING  ·  NEW YORK", font=font(SANS_BOLD, 19),
           fill=RED)
    y += 30
    y = para(d, mx, y, "A century of balloons over Manhattan",
             font(SERIF, 46), 520, leading=52)
    y += 6
    y = para(d, mx, y,
             "Macy's 100th Thanksgiving Day Parade fills the streets "
             "with a record 100 balloons - as a nor'easter's high "
             "winds threaten to keep them grounded.",
             font(SANS, 21), 520, leading=28)
    y += 10
    d.text((mx, y), "3 million spectators expected along the 2.5-mile "
           "route  ·  NBC, 8:30 a.m.", font=font(SANS, 16), fill=GREY)
    draw_parade(d, 580, 168, W - mx, 452)
    rule(d, mx, 472, W - mx, 2)

    # ---- 2 x 2 story grid ----
    gy = 492
    cell_w, cell_h = (W - 2 * mx - 24) // 2, 178
    for i, (kicker, head, body, drawer) in enumerate(PANELS):
        cx = mx + (i % 2) * (cell_w + 24)
        cy = gy + (i // 2) * (cell_h + 16)
        drawer(d, cx, cy + 8, 128)
        tx = cx + 144
        d.text((tx, cy + 6), kicker, font=font(SANS_BOLD, 16), fill=RED)
        ty = para(d, tx, cy + 30, head, font(SERIF, 25),
                  cell_w - 144, leading=29)
        para(d, tx, ty + 4, body, font(SANS, 16), cell_w - 144, leading=21)
        if i % 2 == 0:
            d.line([(cx + cell_w + 12, cy), (cx + cell_w + 12, cy + cell_h)],
                   fill=LIGHT_RULE, width=1)
    rule(d, mx, gy + 2 * cell_h + 16, W - mx, 2)

    # ---- bottom strip ----
    sy = gy + 2 * cell_h + 34
    d.text((mx, sy), "ALSO TODAY", font=font(SANS_BOLD, 16), fill=RED)
    sy += 26
    strip = font(SANS, 17)
    para(d, mx, sy,
         "DHAKA - Bangladesh garment workers win a 36% pay rise, "
         "to 17,000 taka a month.",
         strip, 460, leading=22)
    para(d, mx + 500, sy,
         "NEW DELHI - India marks Constitution Day and calls for "
         "human control over AI weapons.",
         strip, 460, leading=22)
    rule(d, mx, H - 34, W - mx, 1)
    d.text((W // 2, H - 26),
           "THE WORLD TODAY  ·  THURSDAY 26 NOVEMBER 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
