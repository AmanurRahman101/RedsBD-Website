"""Rebuild partner logos at higher clarity: crisp SVG/PNG wordmarks + quality upscales."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "assets" / "logos"


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def save_transparent(im: Image.Image, path: Path) -> None:
    im = im.convert("RGBA")
    # Flatten near-white to transparent for cleaner cards
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r > 245 and g > 245 and b > 245:
                px[x, y] = (255, 255, 255, 0)
    im.save(path, "PNG", optimize=True)
    print(f"wrote {path.name} {im.size}")


def upscale(path: Path, scale: int = 3) -> None:
    im = Image.open(path).convert("RGBA")
    # Only upscale if currently small
    if max(im.size) >= 600 and path.name not in {"titas-gas.png", "health-advances.png", "mercer.png"}:
        print(f"skip large {path.name} {im.size}")
        return
    new_size = (im.width * scale, im.height * scale)
    out = im.resize(new_size, Image.Resampling.LANCZOS)
    # Mild sharpen to recover edge definition
    out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))
    out = ImageEnhance.Contrast(out).enhance(1.05)
    # Trim and pad
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
        out = ImageOps.expand(out, border=8, fill=(0, 0, 0, 0))
    out.save(path, "PNG", optimize=True)
    print(f"upscaled {path.name} -> {out.size}")


def make_health_advances() -> None:
    w, h = 720, 200
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    color = (15, 45, 95, 255)
    f1 = font(64, True)
    f2 = font(64, True)
    # Measure
    t1 = "HEALTH"
    t2 = "ADVANCES"
    b1 = d.textbbox((0, 0), t1, font=f1)
    b2 = d.textbbox((0, 0), t2, font=f2)
    tw1, th1 = b1[2] - b1[0], b1[3] - b1[1]
    tw2 = b2[2] - b2[0]
    gap = 28
    total = tw1 + gap + tw2
    x0 = (w - total) // 2
    y = (h - th1) // 2 - 8
    d.text((x0, y), t1, font=f1, fill=color)
    d.text((x0 + tw1 + gap, y), t2, font=f2, fill=color)
    # Underline under HEALTH only
    underline_y = y + th1 + 10
    d.line((x0, underline_y, x0 + tw1, underline_y), fill=color, width=5)
    save_transparent(im, LOGO / "health-advances.png")


def make_mercer() -> None:
    w, h = 780, 200
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    teal = (0, 176, 185, 255)
    navy = (0, 90, 120, 255)
    cyan = (64, 196, 205, 255)

    # Geometric M / hexagon mark (approx)
    ox, oy = 70, 100
    s = 42
    # overlapping hex-ish facets
    facets = [
        ([(ox, oy - s), (ox + s * 0.55, oy - s * 0.35), (ox + s * 0.2, oy + s * 0.15), (ox - s * 0.35, oy - s * 0.1)], navy),
        ([(ox + s * 0.55, oy - s * 0.35), (ox + s * 1.15, oy - s * 0.55), (ox + s * 0.95, oy + s * 0.05), (ox + s * 0.2, oy + s * 0.15)], teal),
        ([(ox - s * 0.1, oy + s * 0.05), (ox + s * 0.35, oy + s * 0.25), (ox + s * 0.05, oy + s * 0.85), (ox - s * 0.55, oy + s * 0.45)], cyan),
        ([(ox + s * 0.35, oy + s * 0.25), (ox + s * 0.95, oy + s * 0.05), (ox + s * 1.2, oy + s * 0.55), (ox + s * 0.45, oy + s * 0.9)], teal),
    ]
    for pts, col in facets:
        d.polygon([(int(x), int(y)) for x, y in pts], fill=col)

    f = font(72, True)
    text = "MERCER"
    d.text((155, 55), text, font=f, fill=teal)
    save_transparent(im, LOGO / "mercer.png")


def make_bangladesh_railway() -> None:
    """Crisp text + upscaled seal if present, else redraw wordmark with simple seal."""
    seal_path = LOGO / "bangladesh-bank.png"
    # Build from national-style circle redraw + crisp text
    w, h = 720, 220
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # Seal
    cx, cy, r = 110, 110, 90
    green = (0, 106, 78, 255)
    red = (190, 20, 35, 255)
    gold = (230, 190, 50, 255)
    white = (255, 255, 255, 255)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=green)
    d.ellipse((cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18), fill=red)
    # Simple map blob (abstract Bangladesh shape)
    map_pts = [
        (cx - 18, cy - 40),
        (cx + 10, cy - 45),
        (cx + 28, cy - 20),
        (cx + 22, cy + 10),
        (cx + 30, cy + 35),
        (cx + 5, cy + 42),
        (cx - 20, cy + 30),
        (cx - 32, cy),
        (cx - 28, cy - 22),
    ]
    d.polygon(map_pts, fill=gold)
    # Stars
    for ang_x, ang_y in ((cx - 72, cy), (cx + 72, cy), (cx, cy - 72), (cx, cy + 72)):
        pass
    # side stars on green ring
    def star(x: int, y: int, size: int = 7) -> None:
        pts = []
        import math

        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = size if i % 2 == 0 else size * 0.4
            pts.append((x + rad * math.cos(ang), y + rad * math.sin(ang)))
        d.polygon(pts, fill=red)

    star(cx - 78, cy)
    star(cx + 78, cy)

    # Ring text simplified as arcs already colored; add tiny labels via small font optional
    f1 = font(42, True)
    f2 = font(34, False)
    d.text((220, 58), "BANGLADESH", font=f1, fill=red)
    d.text((220, 118), "RAILWAY", font=f2, fill=(40, 40, 40, 255))
    save_transparent(im, LOGO / "bangladesh-railway.png")


def make_titas_svg_png() -> None:
    """Render a cleaner Titas Gas emblem at high resolution."""
    size = 512
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = cy = size // 2
    r = 230
    # Outer circle
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(20, 20, 20, 255), width=6)
    # Flame
    flame_outer = [
        (cx, cy - 110),
        (cx + 55, cy - 20),
        (cx + 40, cy + 40),
        (cx, cy + 70),
        (cx - 40, cy + 40),
        (cx - 55, cy - 20),
    ]
    d.polygon(flame_outer, fill=(220, 40, 40, 255))
    flame_inner = [
        (cx, cy - 40),
        (cx + 22, cy + 10),
        (cx, cy + 45),
        (cx - 22, cy + 10),
    ]
    d.polygon(flame_inner, fill=(250, 200, 40, 255))
    # Center box + text
    box = (cx - 105, cy + 85, cx + 105, cy + 130)
    d.rectangle(box, outline=(20, 20, 20, 255), width=3)
    f = font(28, True)
    text = "TITAS GAS"
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text((cx - tw / 2, cy + 92), text, font=f, fill=(20, 20, 20, 255))
    # Year
    f2 = font(26, True)
    ytext = "1964"
    yb = d.textbbox((0, 0), ytext, font=f2)
    d.text((cx - (yb[2] - yb[0]) / 2, cy + 145), ytext, font=f2, fill=(20, 20, 20, 255))

    # Curved top label approximated as straight arcs of short segments
    import math

    label = "TRANSMISSION AND DISTRIBUTION CO. LTD."
    f3 = font(14, True)
    radius = 185
    start = math.radians(-110)
    end = math.radians(110)
    # place characters along arc
    # measure total width approx
    chars = list(label)
    # equal angular spacing
    for i, ch in enumerate(chars):
        if ch == " ":
            continue
        t = i / max(1, len(chars) - 1)
        ang = start + (end - start) * t
        x = cx + radius * math.sin(ang)
        y = cy - radius * math.cos(ang)
        # rotate each glyph
        glyph = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((8, 4), ch, font=f3, fill=(20, 20, 20, 255))
        rot = glyph.rotate(-math.degrees(ang), resample=Image.Resampling.BICUBIC, expand=True)
        im.alpha_composite(rot, (int(x - rot.width / 2), int(y - rot.height / 2)))

    save_transparent(im, LOGO / "titas-gas.png")


def main() -> None:
    make_health_advances()
    make_mercer()
    make_bangladesh_railway()
    make_titas_svg_png()

    # Upscale remaining partner logos that are still small rasters
    for name in [
        "telstar-azbil.png",
        "keyplants.png",
        "biogard.png",
        "navigant.png",
        "quintilesims.png",
        "clearview.png",
        "bangladesh-bank.png",
        "crp.png",
    ]:
        path = LOGO / name
        if path.exists():
            upscale(path, scale=3)


if __name__ == "__main__":
    main()
