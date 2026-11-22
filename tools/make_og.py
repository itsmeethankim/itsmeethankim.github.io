"""Render Brillion link-preview images (1200x630) in pixel-art style.

Base canvas is 400x210 "art pixels", upscaled 3x with nearest-neighbour.
Inputs: the app's splash-icon.png (brain sprite, 12px grid) and paywall-bg.webp (ocean).
"""
import sys, math, random
from PIL import Image, ImageDraw

ASSETS = sys.argv[1]
OUT = sys.argv[2]
W, H, S = 400, 210, 3

FONT = {
 'A': ["01110","10001","10001","11111","10001","10001","10001"],
 'B': ["11110","10001","10001","11110","10001","10001","11110"],
 'C': ["01111","10000","10000","10000","10000","10000","01111"],
 'D': ["11110","10001","10001","10001","10001","10001","11110"],
 'E': ["11111","10000","10000","11110","10000","10000","11111"],
 'H': ["10001","10001","10001","11111","10001","10001","10001"],
 'I': ["11111","00100","00100","00100","00100","00100","11111"],
 'J': ["00111","00010","00010","00010","00010","10010","01100"],
 'L': ["10000","10000","10000","10000","10000","10000","11111"],
 'M': ["10001","11011","10101","10101","10001","10001","10001"],
 'N': ["10001","11001","10101","10011","10001","10001","10001"],
 'O': ["01110","10001","10001","10001","10001","10001","01110"],
 'P': ["11110","10001","10001","11110","10000","10000","10000"],
 'R': ["11110","10001","10001","11110","10100","10010","10001"],
 'T': ["11111","00100","00100","00100","00100","00100","00100"],
 'U': ["10001","10001","10001","10001","10001","10001","01110"],
 'V': ["10001","10001","10001","10001","10001","01010","00100"],
 'Y': ["10001","10001","01010","00100","00100","00100","00100"],
 '!': ["00100","00100","00100","00100","00100","00000","00100"],
 ' ': ["00000"]*7,
}

def text_w(s, sc, sp=1):
    return len(s) * (5 + sp) * sc - sp * sc

def draw_text(d, x, y, s, sc, fill, shadow=None, sp=1):
    for ch in s:
        g = FONT[ch]
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == '1':
                    if shadow:
                        d.rectangle([x + c*sc + sc//2 + 1, y + r*sc + sc//2 + 1,
                                     x + c*sc + sc - 1 + sc//2 + 1, y + r*sc + sc - 1 + sc//2 + 1], fill=shadow)
        x2 = x
        x += (5 + sp) * sc
    return x

def draw_text_fg(d, x, y, s, sc, fill, sp=1):
    for ch in s:
        for r, row in enumerate(FONT[ch]):
            for c, v in enumerate(row):
                if v == '1':
                    d.rectangle([x + c*sc, y + r*sc, x + c*sc + sc - 1, y + r*sc + sc - 1], fill=fill)
        x += (5 + sp) * sc

def background():
    # banded teal -> navy gradient (palette taken from the app icon)
    top, bot = (47, 128, 152), (14, 34, 74)
    out = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(out)
    bands = 12
    for i in range(bands):
        t = i / (bands - 1)
        c = tuple(round(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        y0 = round(i * H / bands)
        d.rectangle([0, y0, W, round((i + 1) * H / bands)], fill=c)
    # stepped light rays fanning down from the surface
    ray = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ray)
    for x0, spread, a in [(120, 40, 26), (200, 70, 22), (260, 30, 26), (330, 55, 18), (60, 25, 16)]:
        for y in range(0, H, 4):
            w = 6 + y * spread // H
            rd.rectangle([x0 - w // 2 + y // 6, y, x0 + w // 2 + y // 6, y + 3], fill=(170, 230, 240, max(0, a - y // 10)))
    out.paste(ray, (0, 0), ray)
    # seabed strip from the paywall art
    bg = Image.open(f"{ASSETS}/paywall-bg.webp").convert("RGB")
    bw, bh = bg.size
    nh = round(bh * W / bw)
    bg = bg.resize((W, nh), Image.BOX)
    strip = bg.crop((0, nh - 46, W, nh))
    mask = Image.new("L", strip.size, 255)
    md = ImageDraw.Draw(mask)
    for y in range(14):
        md.line([(0, y), (W, y)], fill=round(255 * y / 14))
    out.paste(strip, (0, H - 46), mask)
    out = out.quantize(colors=48, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
    return out

def brain():
    im = Image.open(f"{ASSETS}/splash-icon.png").convert("RGBA")
    im = im.crop(im.getbbox())  # 384x336, 12px grid
    native = im.resize((im.width // 12, im.height // 12), Image.NEAREST)  # 32x28
    return native

def render(kind):
    base = background()
    d = ImageDraw.Draw(base, "RGBA")
    b = brain()
    bs = 4
    bw, bh = b.width * bs, b.height * bs
    bx, by = 26, (H - bh) // 2 - 4
    cx, cy = bx + bw // 2, by + bh // 2
    # stepped pink glow (like the app icon)
    for i, (rad, a) in enumerate([(92, 28), (80, 34), (70, 40), (62, 46)]):
        for yy in range(cy - rad, cy + rad, 4):
            for xx in range(cx - rad, cx + rad, 4):
                if (xx - cx) ** 2 + ((yy - cy) * 1.1) ** 2 < rad ** 2:
                    d.rectangle([xx, yy, xx + 3, yy + 3], fill=(214, 80, 140, a))
    # dark outline then sprite
    big = b.resize((bw, bh), Image.NEAREST)
    alpha = big.split()[3]
    outline = Image.new("RGBA", big.size, (40, 6, 20, 255))
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        base.paste(outline, (bx + dx, by + dy), alpha)
    base.paste(big, (bx, by), big)
    # bubbles
    rnd = random.Random({"duel": 7, "invite": 11, "link": 5}[kind])
    for _ in range(9):
        x, y = rnd.randrange(150, 390), rnd.randrange(10, 200)
        s = rnd.choice([2, 2, 3])
        if 160 < x < 395 and 45 < y < 165: continue
        d.rectangle([x, y, x + s - 1, y + s - 1], fill=(190, 235, 245, 200))
    # text block
    tx = bx + bw + 26
    title = "BRILLION"
    sub = {"duel": "DUEL ME!", "invite": "JOIN ME!", "link": "PLAY ME!"}[kind]
    tag = "DAILY TRIVIA DIVE"
    t1, t2, t3 = 4, 4, 2
    block_h = 7 * t1 + 14 + 7 * t2 + 14 + 7 * t3
    ty = (H - block_h) // 2 - 2
    # title: shadow + face
    draw_text_fg(d, tx + 2, ty + 2, title, t1, (122, 16, 52))
    draw_text_fg(d, tx, ty, title, t1, (255, 227, 234))
    y2 = ty + 7 * t1 + 14
    # subtitle in a gold pill
    sw = text_w(sub, t2)
    d.rectangle([tx - 6, y2 - 6, tx + sw + 5, y2 + 7 * t2 + 5], fill=(8, 16, 44, 230))
    d.rectangle([tx - 6, y2 - 6, tx + sw + 5, y2 - 5], fill=(242, 198, 107))
    d.rectangle([tx - 6, y2 + 7 * t2 + 4, tx + sw + 5, y2 + 7 * t2 + 5], fill=(242, 198, 107))
    d.rectangle([tx - 6, y2 - 6, tx - 5, y2 + 7 * t2 + 5], fill=(242, 198, 107))
    d.rectangle([tx + sw + 4, y2 - 6, tx + sw + 5, y2 + 7 * t2 + 5], fill=(242, 198, 107))
    draw_text_fg(d, tx, y2, sub, t2, (242, 198, 107))
    y3 = y2 + 7 * t2 + 14
    draw_text_fg(d, tx, y3, tag, t3, (169, 205, 235))
    out = base.resize((W * S, H * S), Image.NEAREST)
    out.save(f"{OUT}/og-{kind}.png", optimize=True)

for k in ("duel", "invite", "link"):
    render(k)
# page sprite (brain at 8x, transparent) and touch icon
brain().resize((32 * 8, 28 * 8), Image.NEAREST).save(f"{OUT}/brain.png", optimize=True)
ic = Image.open(f"{ASSETS}/icon.png").convert("RGB")
ic.resize((180, 180), Image.LANCZOS).save(f"{OUT}/apple-touch-icon.png", optimize=True)
ic.resize((64, 64), Image.LANCZOS).save(f"{OUT}/favicon.png", optimize=True)
print("ok")
