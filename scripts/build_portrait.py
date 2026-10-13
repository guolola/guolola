"""Frame the supplied Denia GIF as a portrait card that matches the page's cut-corner UI.

The source animation (assets/daniya.gif) is untouched; every frame keeps its timing.
Output: assets/denia-portrait.gif (+ denia-portrait-still.png for reduced motion).
The card is opaque navy with transparent cut corners, so it sits on light and dark pages.
Requires Python 3, Pillow and NumPy:  python scripts/build_portrait.py
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageSequence

ROOT = Path(__file__).resolve().parents[1] / "assets"
INNER, PAD, CUT = 336, 14, 30              # image size, frame width, corner cut
SIZE = INNER + 2 * PAD
EAR = 40                                   # pixel cat ears rise above the card
HT = SIZE + EAR
PINK = (255, 170, 205)
NAVY, CYAN, AZURE = (10, 31, 92), (51, 225, 255), (31, 107, 255)
KEEP = 255                                 # transparent index: outside the card / unchanged pixel
FUZZ = 7.0                                 # keep the previous pixel when the new colour is this close

src = Image.open(ROOT / "daniya.gif")
frames, durations = [], []
for fr in ImageSequence.Iterator(src):
    durations.append(fr.info.get("duration", 70))
    frames.append(np.asarray(fr.convert("RGB").resize((INNER, INNER), Image.LANCZOS), np.float32))


def cut_poly(inset, cut):
    a, b = inset, SIZE - 1 - inset
    return [(x, y + EAR) for x, y in [(a, a), (b - cut, a), (b, a + cut), (b, b), (a + cut, b), (a, b - cut)]]


def ears(shrink=0):
    """Two chunky pixel ears standing on the card's top edge (stepped edges on purpose)."""
    out = []
    for x0 in (44, 214):
        out.append([(x0 + shrink * 1.2, EAR + 6), (x0 + 26 + shrink * .2, 2 + shrink * 1.6), (x0 + 82 - shrink * 1.2, EAR + 6)])
    return out


def mask(poly):
    m = Image.new("L", (SIZE, HT), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m) > 127


card = mask(cut_poly(0, CUT))
for e in ears():
    card = card | mask(e)
photo = mask(cut_poly(PAD, CUT - 6))
deco = Image.new("RGB", (SIZE, HT), NAVY)
d = ImageDraw.Draw(deco)
for e, i in zip(ears(), ears(16)):
    d.line(e, fill=CYAN, width=3)
    d.polygon(i, fill=PINK)
d.line(cut_poly(6, CUT - 2) + [cut_poly(6, CUT - 2)[0]], fill=AZURE, width=1)
# cyan brackets on the two cut corners
b, o = SIZE - 1, EAR
d.line([(b - CUT - 22, 3 + o), (b - CUT + 1, 3 + o), (b - 3, CUT - 1 + o), (b - 3, CUT + 22 + o)], fill=CYAN, width=3)
d.line([(3, b - CUT - 22 + o), (3, b - CUT + 1 + o), (CUT - 1, b - 3 + o), (CUT + 22, b - 3 + o)], fill=CYAN, width=3)
deco = np.asarray(deco, np.float32)

# ------------------------------------------------------------- palette (k-means over sampled frames)
rng = np.random.default_rng(3)
W8 = np.array([0.30, 0.59, 0.11], np.float32) ** 0.5


def nearest(px, pal, chunk=40000):
    out = np.empty(len(px), np.int32)
    p = pal * W8
    for i in range(0, len(px), chunk):
        q = px[i:i + chunk] * W8
        out[i:i + chunk] = ((q * q).sum(1)[:, None] - 2 * q @ p.T + (p * p).sum(1)[None]).argmin(1)
    return out


sample = np.concatenate([f.reshape(-1, 3)[rng.choice(INNER * INNER, 4000, replace=False)] for f in frames])
NK = 255 - 3
pal = np.array(Image.fromarray(sample.reshape(1, -1, 3).astype(np.uint8)).quantize(NK, method=Image.Quantize.MEDIANCUT).getpalette()[:NK * 3], np.float32).reshape(-1, 3)
for _ in range(8):
    idx = nearest(sample, pal)
    for j in range(NK):
        m = idx == j
        if m.any():
            pal[j] = sample[m].mean(0)
palette = np.vstack([pal, [NAVY, CYAN, AZURE], [[0, 0, 0]]])
palette[NK - 1] = PINK                       # make sure the ear pink is exact
deco_idx = nearest(deco.reshape(-1, 3), palette[:255]).reshape(HT, SIZE)

bayer = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16 - 0.5)
thr = np.tile(bayer, (INNER // 4, INNER // 4))[..., None] * 6.0

out, prev_inner = [], None
R0 = PAD + EAR
inner_mask = photo[R0:R0 + INNER, PAD:PAD + INNER]
for f in frames:
    q = nearest((f + thr).reshape(-1, 3), palette[:NK]).reshape(INNER, INNER)
    if prev_inner is not None:      # temporal fuzz: ignore changes the eye cannot see
        close = np.sqrt((((palette[prev_inner] - f) * W8) ** 2).sum(-1)) < FUZZ
        q = np.where(close, prev_inner, q)
    prev_inner = q
    full = np.where(card, deco_idx, KEEP).astype(np.uint8)
    region = full[R0:R0 + INNER, PAD:PAD + INNER]
    full[R0:R0 + INNER, PAD:PAD + INNER] = np.where(inner_mask, q, region)
    out.append(full)

flat = palette.round().clip(0, 255).astype(np.uint8).reshape(-1).tolist()


def img(a):
    im = Image.fromarray(a, "P")
    im.putpalette(flat)
    return im


seq = [img(out[0])] + [img(np.where(out[i] == out[i - 1], KEEP, out[i]).astype(np.uint8)) for i in range(1, len(out))]
seq[0].save(ROOT / "denia-portrait.gif", save_all=True, append_images=seq[1:], duration=durations, loop=0,
            disposal=1, transparency=KEEP, optimize=False)

# Reduced-motion still: full-colour frame 0 in the same card, anti-aliased edges.
big = 4
still = Image.new("RGBA", (SIZE * big, HT * big), (0, 0, 0, 0))
sd = ImageDraw.Draw(still)
scale = lambda poly: [(x * big, y * big) for x, y in poly]
for poly in [cut_poly(0, CUT)] + ears():
    sd.polygon(scale(poly), fill=NAVY + (255,))
still = still.resize((SIZE, HT), Image.LANCZOS)
rgba = np.asarray(still).copy()
rgba[..., :3] = np.where(card[..., None], deco, rgba[..., :3]).astype(np.uint8)
first = np.asarray(Image.open(ROOT / "daniya-still.png").convert("RGB").resize((INNER, INNER), Image.LANCZOS))
sub = rgba[R0:R0 + INNER, PAD:PAD + INNER, :3]
sub[inner_mask] = first[inner_mask]
Image.fromarray(rgba, "RGBA").save(ROOT / "denia-portrait-still.png", optimize=True)
print("denia-portrait.gif", (ROOT / "denia-portrait.gif").stat().st_size, "bytes,", len(out), "frames,", sum(durations), "ms")
