"""Build the HINAMI logo set (plate and chopsticks) as standalone SVGs.

Usage: python build.py <out dir> <CormorantGaramond-Medium.ttf>   (needs fonttools)
"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

OUT, FONT = sys.argv[1], sys.argv[2]
COLORS = {'gold': '#8F7832', 'gold-dark': '#B8995F', 'ink': '#16130F', 'kinari': '#F2EDE4'}

# ---------- symbols, each returns (svg body in a 100x100 box, y of the band center) ----------
import math
def _quad(x0, y0, x1, y1, wt, wh):
    a = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(a), math.cos(a)
    p = [(x0 + nx * wt / 2, y0 + ny * wt / 2), (x1 + nx * wh / 2, y1 + ny * wh / 2), (x1 - nx * wh / 2, y1 - ny * wh / 2), (x0 - nx * wt / 2, y0 - ny * wt / 2)]
    return (f'M{p[0][0]:.2f} {p[0][1]:.2f} L{p[1][0]:.2f} {p[1][1]:.2f} L{p[2][0]:.2f} {p[2][1]:.2f} '
            f'L{p[3][0]:.2f} {p[3][1]:.2f} A{wt / 2:.2f} {wt / 2:.2f} 0 0 1 {p[0][0]:.2f} {p[0][1]:.2f} Z')
RING, RIM, TIP_W, HANDLE_W, GAP = 4.2, 2.0, 1.8, 4.0, 3.0  # two weights: rim = handle, inner rim = half
def _sticks(cx, cy, r):
    """The pair enters at the lower left (tips poke out past the rim) and leaves at the upper right (handles)."""
    ang, shift, ext_l, ext_r = -24, 5, 7, 7  # tips and handles stick out past the rim by the same length
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    bx, by = cx + nx * shift, cy + ny * shift
    tip = (bx - ux * (r + ext_l), by - uy * (r + ext_l)); end = (bx + ux * (r + ext_r), by + uy * (r + ext_r))
    st, sh = (TIP_W + GAP) / 2, (HANDLE_W + GAP) / 2  # keep the visible gap between the two sticks constant
    return [_quad(tip[0] + nx * k * st, tip[1] + ny * k * st, end[0] + nx * k * sh, end[1] + ny * k * sh, TIP_W, HANDLE_W) for k in (-1, 1)]
def chopsticks(c):
    """A plate seen from above, crossed by a pair of chopsticks: tips to the lower left, handles to the upper right."""
    cx, cy, r = 50, 50, 33  # the plate sits in the middle of the square
    sticks = _sticks(cx, cy, r)
    holes = ''.join(f'<path d="{d}" fill="black" stroke="black" stroke-width="4" stroke-linejoin="round"/>' for d in sticks)
    body = (f'<defs><mask id="gap" maskUnits="userSpaceOnUse" x="-10" y="-10" width="120" height="120">'
            f'<rect x="-10" y="-10" width="120" height="120" fill="white"/>{holes}</mask></defs>'
            f'<g mask="url(#gap)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="{RING}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 8}" fill="none" stroke="{c}" stroke-width="{RIM}"/></g>'
            + ''.join(f'<path d="{d}" fill="{c}"/>' for d in sticks))
    return body, cy, (cy - r - RING / 2, cy + r + RING / 2)
def chopsticks_simple(c):
    """For 16-32 px: no inner rim, heavier strokes."""
    cx, cy, r = 50, 50, 33  # the plate sits in the middle of the square
    sticks = _sticks(cx, cy, r)
    holes = ''.join(f'<path d="{d}" fill="black" stroke="black" stroke-width="5" stroke-linejoin="round"/>' for d in sticks)
    return (f'<defs><mask id="gap" maskUnits="userSpaceOnUse" x="-10" y="-10" width="120" height="120">'
            f'<rect x="-10" y="-10" width="120" height="120" fill="white"/>{holes}</mask></defs>'
            f'<g mask="url(#gap)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="6.5"/></g>'
            + ''.join(f'<path d="{d}" fill="{c}" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/>' for d in sticks))
SYMBOLS = {'chopsticks': chopsticks}

# ---------- wordmark: HINAMI in Cormorant Garamond Medium, outlined, tracked, with kerning on N-A and A-M ----------
font = TTFont(FONT); gs = font.getGlyphSet(); cmap = font.getBestCmap(); hmtx = font['hmtx']
TRACK = 190; KERN = {('N', 'A'): -28, ('A', 'M'): -28}
def wordmark_paths(text='HINAMI'):
    parts, x = [], 0; xmin = ymin = 10**9; xmax = ymax = -10**9
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]; bp = BoundsPen(gs); gs[g].draw(bp); b = bp.bounds
        xmin = min(xmin, x + b[0]); xmax = max(xmax, x + b[2]); ymin = min(ymin, b[1]); ymax = max(ymax, b[3])
        sp = SVGPathPen(gs); gs[g].draw(TransformPen(sp, (1, 0, 0, -1, x, 0))); parts.append(sp.getCommands())
        if i < len(text) - 1: x += hmtx[g][0] + TRACK + KERN.get((ch, text[i + 1]), 0)
    return ' '.join(parts), (xmin, -ymax, xmax - xmin, ymax - ymin)
WM_D, WM_BOX = wordmark_paths(); CAP = WM_BOX[3]
def wordmark(c, x, y, h):
    s = h / CAP
    return f'<path transform="translate({x - WM_BOX[0] * s:.3f} {y - WM_BOX[1] * s:.3f}) scale({s:.5f})" d="{WM_D}" fill="{c}"/>'
def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="HINAMI"><title>HINAMI</title>{body}</svg>\n'

for key, fn in SYMBOLS.items():
    d = OUT; os.makedirs(d, exist_ok=True)
    for cname, c in COLORS.items():
        body, band_y, (t, b) = fn(c)
        open(os.path.join(d, f'symbol-{cname}.svg'), 'w').write(svg(100, 100, body))
        open(os.path.join(d, f'symbol-simple-{cname}.svg'), 'w').write(svg(100, 100, chopsticks_simple(c)))
        open(os.path.join(d, f'wordmark-{cname}.svg'), 'w').write(svg(WM_BOX[2] * 100 / CAP, 100, wordmark(c, 0, 0, 100)))
        # horizontal: the band lines up with the middle of the capitals
        cap = 100; gap = 0.8 * cap; sw = WM_BOX[2] * cap / CAP
        k = 2.2
        xmin, xmax = 14.0, 91.0   # drawn extent of the symbol inside its 100 box
        ys = cap / 2 - k * band_y
        top = min(0, ys + k * t); bottom = max(cap, ys + k * b); shift = -top
        sym_w = (xmax - xmin) * k
        body_h = (f'<g transform="translate({-xmin * k:.2f} {ys + shift:.2f}) scale({k})">{body}</g>'
                  + wordmark(c, sym_w + gap, shift, cap))
        open(os.path.join(d, f'lockup-horizontal-{cname}.svg'), 'w').write(svg(sym_w + gap + sw, bottom - top, body_h))
        # vertical: symbol above, wordmark below
        kv = 3.4; gapv = 0.9 * cap; w = max((xmax - xmin) * kv, sw)
        sx = (w - 100 * kv) / 2  # the plate center sits on the axis
        body_v = (f'<g transform="translate({sx:.2f} {-t * kv:.2f}) scale({kv})">{body}</g>'
                  + wordmark(c, (w - sw) / 2, (b - t) * kv + gapv, cap))
        open(os.path.join(d, f'lockup-vertical-{cname}.svg'), 'w').write(svg(w, (b - t) * kv + gapv + cap, body_v))
    # app icon artwork (1024 square; iOS applies the corner mask)
    scale = 0.74
    for name, bg, c in (('app-icon', '#16130F', '#B8995F'), ('app-icon-tinted', '#000000', '#C8C8C8')):
        body, _, _ = fn(c); s = 1024 * scale; o = (1024 - s) / 2
        open(os.path.join(d, f'{name}.svg'), 'w').write(svg(1024, 1024, f'<rect width="1024" height="1024" fill="{bg}"/><g transform="translate({o:.2f} {o:.2f}) scale({s / 100:.4f})">{body}</g>'))
print('wrote logo files to', OUT)
