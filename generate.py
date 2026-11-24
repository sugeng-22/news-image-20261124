#!/usr/bin/env python3
"""Render the news infographic for Tuesday 24 November 2026.

Deterministic, standard library + Pillow only, no network. Reads the
bundled hero illustration (hero.png, an AI-generated flat illustration
with no text) and composes the full 1024x1024 infographic: header with
the date, the hero banner, six story rows with drawn pictograms, and an
"Also today" footer. Run: python3 generate.py -> writes entry.png next
to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

NAVY = (11, 26, 48)
NAVY_DARK = (8, 19, 36)
GOLD = (232, 185, 74)
TEAL = (31, 168, 160)
WHITE = (245, 247, 250)
GREY = (199, 210, 224)
INK = (11, 26, 48)


def font(name, size):
    """Resolve a TrueType font, trying DejaVu then Liberation then Noto."""
    bases = [
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/truetype/liberation/",
        "/usr/share/fonts/truetype/noto/",
    ]
    for base in bases:
        path = os.path.join(base, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_KICKER = lambda s: font("DejaVuSans-Bold.ttf", s)
F_TITLE = lambda s: font("DejaVuSans-Bold.ttf", s)
F_TAG = lambda s: font("DejaVuSans-Bold.ttf", s)
F_HEAD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_BODY = lambda s: font("DejaVuSans.ttf", s)

STORIES = [
    {
        "tag": "RIYADH  ·  MIDDLE EAST",
        "head": "Houthis strike Riyadh's tallest tower",
        "body": "Second attack on the tower in five days; 11 people injured.",
        "icon": "tower",
        "accent": GOLD,
    },
    {
        "tag": "TALLINN  ·  EUROPE",
        "head": "Russia warns Estonia of 'open war'",
        "body": "Moscow reacts to Estonia's plan to close border crossings on 1 December.",
        "icon": "warn",
        "accent": TEAL,
    },
    {
        "tag": "SPORT  ·  AFRICA",
        "head": "Senegal crowned AFCON champions",
        "body": "Top court reinstates Senegal as winners of the 2025 Africa Cup of Nations.",
        "icon": "trophy",
        "accent": GOLD,
    },
    {
        "tag": "TECH  ·  MARKETS",
        "head": "Nvidia chief Jensen Huang returns",
        "body": "Reinstated as CEO under two weeks after resigning; shares jump.",
        "icon": "chip",
        "accent": TEAL,
    },
    {
        "tag": "SPACE  ·  DEFENCE",
        "head": "NATO vows to defend space",
        "body": "Chief Mark Rutte answers reports of a Russian nuclear-armed satellite.",
        "icon": "sat",
        "accent": GOLD,
    },
    {
        "tag": "SEOUL  ·  AI",
        "head": "South Korea pays to catch AI cheats",
        "body": "Rewards up to $375,000 for tips on AI cheating in the national college exam.",
        "icon": "cap",
        "accent": TEAL,
    },
]

ALSO_TODAY = [
    "Israeli strikes kill Hamas security chief in Gaza  ·  Zaporizhzhia strike kills 2, wounds 40",
    "Spain's top court amnesties Catalan leader Puigdemont  ·  S&P 500 slips 0.95%",
]


def draw_spaced(draw, xy, text, fnt, fill, spacing=4):
    """Draw text with letter spacing (for the kicker line)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def truncate(draw, text, fnt, max_w):
    """Shorten text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        text = text[:-1]
    return text + "…"


def icon_tower(d, x, y, s, fg):
    d.rectangle([x + 22, y + 16, x + 38, y + 52], fill=fg)
    d.polygon([(x + 30, y + 4), (x + 22, y + 16), (x + 38, y + 16)], fill=fg)
    d.rectangle([x + 18, y + 52, x + 42, y + 56], fill=fg)
    for wy in (22, 30, 38, 46):
        d.rectangle([x + 27, y + wy, x + 33, y + wy + 3], fill=NAVY_DARK)


def icon_warn(d, x, y, s, fg):
    d.polygon([(x + 30, y + 6), (x + 54, y + 52), (x + 6, y + 52)], fill=fg)
    d.polygon([(x + 30, y + 14), (x + 48, y + 46), (x + 12, y + 46)], fill=NAVY_DARK)
    d.rectangle([x + 28, y + 20, x + 32, y + 36], fill=fg)
    d.rectangle([x + 28, y + 40, x + 32, y + 44], fill=fg)


def icon_trophy(d, x, y, s, fg):
    d.pieslice([x + 14, y + 8, x + 46, y + 38], 0, 180, fill=fg)
    d.rectangle([x + 14, y + 8, x + 46, y + 20], fill=fg)
    d.arc([x + 6, y + 12, x + 18, y + 30], 90, 270, fill=fg, width=4)
    d.arc([x + 42, y + 12, x + 54, y + 30], 270, 90, fill=fg, width=4)
    d.rectangle([x + 27, y + 38, x + 33, y + 48], fill=fg)
    d.rectangle([x + 20, y + 48, x + 40, y + 54], fill=fg)


def icon_chip(d, x, y, s, fg):
    d.rounded_rectangle([x + 14, y + 14, x + 46, y + 46], radius=6, fill=fg)
    d.rounded_rectangle([x + 22, y + 22, x + 38, y + 38], radius=3, fill=NAVY_DARK)
    for px in (20, 30, 40):
        d.line([(x + px, y + 8), (x + px, y + 14)], fill=fg, width=3)
        d.line([(x + px, y + 46), (x + px, y + 52)], fill=fg, width=3)
    for py in (20, 30, 40):
        d.line([(x + 8, y + py), (x + 14, y + py)], fill=fg, width=3)
        d.line([(x + 46, y + py), (x + 52, y + py)], fill=fg, width=3)


def icon_sat(d, x, y, s, fg):
    d.polygon([(x + 26, y + 22), (x + 34, y + 22), (x + 38, y + 38),
               (x + 22, y + 38)], fill=fg)
    d.rectangle([x + 10, y + 26, x + 24, y + 34], fill=fg)
    d.rectangle([x + 36, y + 26, x + 50, y + 34], fill=fg)
    d.line([(x + 24, y + 30), (x + 26, y + 30)], fill=fg, width=2)
    d.line([(x + 34, y + 30), (x + 36, y + 30)], fill=fg, width=2)
    d.ellipse([x + 40, y + 40, x + 48, y + 48], outline=fg, width=3)


def icon_cap(d, x, y, s, fg):
    d.polygon([(x + 30, y + 12), (x + 54, y + 24), (x + 30, y + 36),
               (x + 6, y + 24)], fill=fg)
    d.polygon([(x + 20, y + 30), (x + 40, y + 30), (x + 40, y + 46),
               (x + 20, y + 46)], fill=fg)
    d.line([(x + 52, y + 26), (x + 52, y + 46)], fill=fg, width=3)
    d.ellipse([x + 49, y + 46, x + 55, y + 52], fill=fg)


ICONS = {
    "tower": icon_tower,
    "warn": icon_warn,
    "trophy": icon_trophy,
    "chip": icon_chip,
    "sat": icon_sat,
    "cap": icon_cap,
}


def hero_band(img, x, y, w, h):
    """Centre-crop the hero art to the banner box, keeping the globe."""
    art = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
    # Scale so the width matches, then take a band centred on the globe.
    scaled = art.resize((w, int(art.height * w / art.width)), Image.LANCZOS)
    globe_cy = int(scaled.height * 0.48)
    top = max(0, min(scaled.height - h, globe_cy - h // 2))
    band = scaled.crop((0, top, w, top + h))
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w, h], radius=18, fill=255)
    img.paste(band, (x, y), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + w, y + h], radius=18,
                        outline=GOLD, width=2)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Header
    draw_spaced(d, (48, 26), "THE WORLD IN ONE DAY", F_KICKER(27), GOLD, 5)
    d.text((48, 58), "Tuesday, 24 November 2026",
           font=F_TITLE(50), fill=WHITE)
    d.line([(48, 122), (976, 122)], fill=GOLD, width=3)

    # Hero banner
    hero_band(img, 48, 136, 928, 272)
    d = ImageDraw.Draw(img)

    # Story rows
    y = 428
    row_h, gap = 74, 6
    for story in STORIES:
        # Icon chip
        d.rounded_rectangle([48, y, 108, y + 60], radius=14,
                            fill=story["accent"])
        ICONS[story["icon"]](d, 48, y, 60, INK)
        tx = 128
        d.text((tx, y - 1), story["tag"], font=F_TAG(19), fill=GOLD)
        d.text((tx, y + 21), story["head"], font=F_HEAD(29), fill=WHITE)
        body = truncate(d, story["body"], F_BODY(21), 976 - tx)
        d.text((tx, y + 51), body, font=F_BODY(21), fill=GREY)
        y += row_h + gap

    # Footer
    d.line([(48, 916), (976, 916)], fill=(38, 58, 86), width=2)
    d.text((48, 928), "ALSO TODAY", font=F_TAG(19), fill=GOLD)
    d.text((48, 952), truncate(d, ALSO_TODAY[0], F_BODY(20), 928),
           font=F_BODY(20), fill=GREY)
    d.text((48, 978), truncate(d, ALSO_TODAY[1], F_BODY(20), 928),
           font=F_BODY(20), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
