# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Build the TRUST brand SVGs (mark, favicon, wordmark lockups).

The mark is a star sitting on a confidence interval, like one point of a
forest plot. The wordmark is "Trust" in Archivo (SIL OFL 1.1) at width 125
and weight 800, converted to outlines. Requires fontTools and a TrueType copy
of node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2
(decompressed, for example with the wawoff2 npm package). Run from demo/:
    python3 tools/make_brand.py <archivo-wdth.ttf>
"""
import math
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path("public/brand")
INK, BLUE, YELLOW, WHITE = "#1F2830", "#1F57B8", "#F2C21B", "#F7F8F6"
HEAD = "<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->\n"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def star(cx, cy, R, ratio=0.382):
    pts = []
    for i in range(10):
        r = R if i % 2 == 0 else R * ratio
        a = math.radians(-90 + 36 * i)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"


def interval(x0, x1, y, t, cap_h):
    """Horizontal bar with end caps, as one outline (union drawn as three rects)."""
    h = t / 2
    c = cap_h / 2
    rects = [(x0, y - h, x1, y + h), (x0, y - c, x0 + t, y + c), (x1 - t, y - c, x1, y + c)]
    return "".join(f"M{f(a)} {f(b)}H{f(cc)}V{f(d)}H{f(a)}Z" for a, b, cc, d in rects)


def mark(star_fill, bar_fill):
    return (f'<path fill="{star_fill}" d="{star(128, 100, 90)}"/>'
            f'<path fill="{bar_fill}" d="{interval(34, 222, 214, 22, 60)}"/>')


def svg(w, h, body, title):
    return (HEAD + f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f"<title>{title}</title>{body}</svg>\n")


def favicon():
    return (f'<rect width="256" height="256" rx="48" fill="{YELLOW}"/>'
            f'<path fill="{INK}" d="{star(128, 104, 82)}"/>'
            f'<path fill="{INK}" d="{interval(40, 216, 210, 24, 56)}"/>')


def wordmark(font, fill, x0, baseline, size):
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    sc = size / font["head"].unitsPerEm
    hmtx = font["hmtx"]
    x = x0
    out = []
    for ch in "Trust":
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=f)
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, baseline)))
        out.append(pen.getCommands())
        x += hmtx[g][0] * sc
    return f'<path fill="{fill}" d="{"".join(out)}"/>', x


def main():
    font = instancer.instantiateVariableFont(TTFont(sys.argv[1]), {"wdth": 125, "wght": 800})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mark.svg").write_text(svg(256, 256, mark(BLUE, INK), "TRUST mark"))
    (OUT / "mark-mono.svg").write_text(svg(256, 256, mark(INK, INK), "TRUST mark, one colour"))
    (OUT / "mark-reversed.svg").write_text(svg(256, 256, f'<rect width="256" height="256" fill="{INK}"/>' + mark(YELLOW, WHITE), "TRUST mark, reversed"))
    (OUT / "favicon.svg").write_text(svg(256, 256, favicon(), "TRUST"))
    for name, bg, fg, mk in (
        ("lockup.svg", None, INK, (BLUE, INK)),
        ("lockup-mono.svg", None, INK, (INK, INK)),
        ("lockup-reversed.svg", INK, WHITE, (YELLOW, WHITE)),
    ):
        words, end = wordmark(font, fg, 280, 190, 160)
        w = math.ceil(end + 24)
        back = f'<rect width="{w}" height="256" fill="{bg}"/>' if bg else ""
        (OUT / name).write_text(svg(w, 256, back + mark(*mk) + words, "TRUST"))
    print("brand written to", OUT)


if __name__ == "__main__":
    main()
