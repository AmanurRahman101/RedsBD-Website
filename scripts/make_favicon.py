"""Build transparent REDS favicons from the shield logo source."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "logo" / "favicon-source.png"
OUT = {
    "favicon.png": 32,
    "favicon-32.png": 32,
    "favicon-192.png": 192,
    "apple-touch-icon.png": 180,
}


def flood_transparent(im: Image.Image, threshold: int = 40) -> Image.Image:
    """Make near-black / empty background transparent via corner flood fill."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    visited = [[False] * h for _ in range(w)]
    stack = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]

    def is_bg(x: int, y: int) -> bool:
        r, g, b, a = px[x, y]
        if a < 12:
            return True
        # near-black background
        if r <= threshold and g <= threshold and b <= threshold:
            return True
        return False

    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h or visited[x][y]:
            continue
        visited[x][y] = True
        if not is_bg(x, y):
            continue
        px[x, y] = (0, 0, 0, 0)
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    return im


def trim(im: Image.Image, pad: int = 4) -> Image.Image:
    bbox = im.getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(im.width, r + pad)
    b = min(im.height, b + pad)
    return im.crop((l, t, r, b))


def fit_square(im: Image.Image, size: int) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # keep aspect, fit inside square
    copy = im.copy()
    copy.thumbnail((size, size), Image.Resampling.LANCZOS)
    x = (size - copy.width) // 2
    y = (size - copy.height) // 2
    canvas.paste(copy, (x, y), copy)
    return canvas


def analyze(path: Path) -> None:
    im = Image.open(path).convert("RGBA")
    data = list(im.getdata())
    opaque = sum(1 for *_, a in data if a > 250)
    transparent = sum(1 for *_, a in data if a < 10)
    whiteish = sum(1 for r, g, b, a in data if a > 200 and r > 240 and g > 240 and b > 240)
    print(
        f"{path.name}: {im.size} opaque={opaque} transparent={transparent} "
        f"whiteish={whiteish} corner={im.getpixel((0, 0))}"
    )


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source: {SRC}")

    cleaned = trim(flood_transparent(Image.open(SRC)))
    master = ROOT / "assets" / "logo" / "reds-shield-transparent.png"
    cleaned.save(master, "PNG", optimize=True)

    assets = ROOT / "assets"
    for name, size in OUT.items():
        out = fit_square(cleaned, size)
        out.save(assets / name, "PNG", optimize=True)

    # Root favicon.ico (multi-size PNG-in-ICO for modern browsers)
    ico_sizes = [16, 32, 48]
    ico_images = [fit_square(cleaned, s) for s in ico_sizes]
    ico_path = ROOT / "favicon.ico"
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )

    # Also keep assets/favicon.ico
    ico_images[0].save(
        assets / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )

    for p in [master, ico_path, assets / "favicon.ico"] + [assets / n for n in OUT]:
        analyze(p)


if __name__ == "__main__":
    main()
