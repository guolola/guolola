"""Rooftop hero: one approved illustration + a deterministic, seamless motion layer.

Motion (all strictly periodic over N frames, so frame N == frame 0):
  * Makoto breathes: a soft vertical displacement field over his chest, two breaths per loop.
  * Aigis's outer hair strands sway in the breeze (her face, headphones and pose stay fixed).
  * Pixel-sprite petals drift down inside the painted frame and are clipped by it.
  * A few glints pulse on the distant water.

Quality rules:
  * One global palette for every frame plus a screen-fixed ordered dither, so static pixels are
    bit-identical from frame to frame (no palette flicker, small GIF deltas).
  * The warp runs at source resolution and is then downsampled, so motion is sub-pixel smooth
    without blurring the drawing.
  * Faces are excluded from both the warp fields and the petal paths.

Requires Python 3, Pillow and NumPy:  python scripts/build_hero.py
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "assets"
SRC = ROOT / "p3-rooftop-blue.png"
W, H = 1200, 600            # output size
N, DELAY = 144, 60          # 144 frames x 60 ms = 8.64 s loop
TAU = 2 * math.pi
rng = np.random.default_rng(7)

src = np.asarray(Image.open(SRC).convert("RGB"), dtype=np.float32)
SH, SW = src.shape[:2]
S = W / SW                  # source -> output scale

# ---------------------------------------------------------------- warp fields (source px)
yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)


def smooth(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# Makoto's chest and belly rise; his face (x > 1135) and the floor contact stay fixed.
breath_w = (smooth(690, 820, xx) * (1 - smooth(1035, 1118, xx))
            * smooth(535, 612, yy) * (1 - smooth(705, 835, yy)))
# Aigis's loose strands on the right of her head, clear of the face and headphones.
r2 = ((xx - 1378) / 34) ** 2 + ((yy - 158) / 74) ** 2
hair_w = np.clip(1 - r2, 0, 1) ** 2 * smooth(1336, 1352, xx)

BREATH_AMP, HAIR_AMP = 2.1, 1.7
bx0, bx1, by0, by1 = 680, 1125, 525, 845       # bounding box of all warped pixels
hx0, hx1, hy0, hy1 = 1330, 1420, 70, 250


def breath(t):   # two relaxed breaths per loop; slightly quicker inhale than exhale
    u = 2 * t
    return 0.5 - 0.5 * math.cos(TAU * u + 0.35 * math.sin(TAU * u))


def sway(t):
    return 0.75 * math.sin(TAU * t) + 0.25 * math.sin(TAU * 2 * t + 1.1)


def bilinear(img, sx, sy):
    x0 = np.clip(np.floor(sx).astype(int), 0, img.shape[1] - 2)
    y0 = np.clip(np.floor(sy).astype(int), 0, img.shape[0] - 2)
    fx = (sx - x0)[..., None]
    fy = (sy - y0)[..., None]
    a, b = img[y0, x0], img[y0, x0 + 1]
    c, d = img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def warped_source(t):
    out = src.copy()
    sl = (slice(by0, by1), slice(bx0, bx1))
    d = BREATH_AMP * breath(t) * breath_w[sl]
    out[sl] = bilinear(src, xx[sl], yy[sl] + d)          # content moves up by d
    sl = (slice(hy0, hy1), slice(hx0, hx1))
    d = HAIR_AMP * sway(t) * hair_w[sl]
    out[sl] = bilinear(out, xx[sl] - d, yy[sl])
    return out


def downsample(a):
    return np.asarray(Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS), dtype=np.float32)


base = downsample(src)

# ---------------------------------------------------------------- palette
PETAL = {"h": (255, 246, 251), "p": (255, 213, 232), "s": (240, 168, 204), "w": (250, 254, 255)}
reserved = np.array(list(PETAL.values()), dtype=np.float32)


def kmeans_palette(pixels, k):
    img = Image.fromarray(pixels.reshape(1, -1, 3).astype(np.uint8))
    pal = np.array(img.quantize(k, method=Image.Quantize.MEDIANCUT).getpalette()[:k * 3], dtype=np.float32).reshape(-1, 3)
    wts = np.array([0.30, 0.59, 0.11], np.float32) ** 0.5
    for _ in range(10):
        idx = nearest(pixels, pal, wts)
        for j in range(k):
            m = idx == j
            if m.any():
                pal[j] = pixels[m].mean(0)
    return pal


def nearest(px, pal, wts=np.array([0.30, 0.59, 0.11], np.float32) ** 0.5, chunk=40000):
    out = np.empty(len(px), np.int32)
    p = pal * wts
    for i in range(0, len(px), chunk):
        q = px[i:i + chunk] * wts
        d = (q * q).sum(1)[:, None] - 2 * q @ p.T + (p * p).sum(1)[None]
        out[i:i + chunk] = d.argmin(1)
    return out


sample = base.reshape(-1, 3)[rng.choice(W * H, 160000, replace=False)]
NK = 255 - len(reserved)    # k-means colours; then petal colours; index 255 = "unchanged" (transparent)
palette = np.vstack([kmeans_palette(sample, NK), reserved, [[0, 0, 0]]])
PIDX = {k: NK + i for i, k in enumerate(PETAL)}
KEEP = 255

bayer = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
                  [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                  [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                  [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], np.float32) / 64 - 0.5
DITHER = 7.0
thresh = np.tile(bayer, (H // 8 + 1, W // 8 + 1))[:H, :W, None] * DITHER


def quantize(rgb, y0=0, x0=0):
    h, w = rgb.shape[:2]
    px = (rgb + thresh[y0:y0 + h, x0:x0 + w]).reshape(-1, 3)
    return nearest(px, palette[:NK]).reshape(h, w).astype(np.uint8)


base_idx = quantize(base)

# output-space dynamic box (warp regions), padded for resampling support
def obox(x0, x1, y0, y1, pad=4):
    return (max(0, int(x0 * S) - pad), min(W, int(math.ceil(x1 * S)) + pad),
            max(0, int(y0 * S) - pad), min(H, int(math.ceil(y1 * S)) + pad))


DYN = [obox(bx0, bx1, by0, by1), obox(hx0, hx1, hy0, hy1)]

# ---------------------------------------------------------------- petals
SPRITES = [
    ["..hp.", ".hppp", "hppps", ".ppss", "..s.."],
    [".hp.", "hpps", ".pps", "..s."],
    ["hpp..", ".ppps", "..sss"],
    [".ph.", "sppp", "spp.", ".s.."],
]
SMALL = [["hp", "ps"], ["hps"], ["h", "p"], ["pp"]]
FRAME = (int(16 * S) + 2, int(15 * S) + 2, W - int(16 * S) - 2, H - int(16 * S) - 2)  # inside the painted border
FACES = [(1140 * S, 140 * S, 1305 * S, 305 * S), (1150 * S, 495 * S, 1300 * S, 640 * S), (95 * S, 85 * S, 315 * S, 145 * S)]

petals = []


def petal_pos(p, t):
    u = (p["k"] * t + p["phase"]) % 1.0
    y = FRAME[1] - 30 + u * (FRAME[3] - FRAME[1] + 60)
    x = p["x0"] + p["drift"] * u + p["amp"] * math.sin(TAU * (p["m"] * t + p["phi"]))
    return x, y


def hits_face(p):
    sz = 20
    for f in range(N):
        x, y = petal_pos(p, f / N)
        for (a, b, c, d) in FACES:
            if x + sz > a and x < c and y + sz > b and y < d:
                return True
    return False


specs = [  # (count, k traversals/loop, fat-pixel size, sprite set)
    (7, 1, 2, "small"), (6, 1, 2, "big"), (3, 2, 3, "big"),
]
attempt = 0
for count, k, fat, kind in specs:
    made = 0
    while made < count:
        attempt += 1
        p = dict(k=k, fat=fat, kind=kind, phase=rng.random(), x0=rng.uniform(FRAME[0] - 60, FRAME[2] - 40),
                 drift=rng.uniform(60, 140) * (1 if k == 1 else 1.6), amp=rng.uniform(8, 22), m=int(rng.integers(1, 4)),
                 phi=rng.random(), spin=int(rng.integers(2, 5)), spin_phi=rng.random(), sprite=int(rng.integers(0, 4)))
        if not hits_face(p):
            petals.append(p)
            made += 1
print("petals", len(petals), "attempts", attempt)


def draw_petal(idx, p, t):
    x, y = petal_pos(p, t)
    x, y = int(round(x)), int(round(y))
    if p["kind"] == "small":
        spr = SMALL[(p["sprite"] + int(4 * ((p["spin"] * t + p["spin_phi"]) % 1))) % 4]
    else:
        spr = SPRITES[int(4 * ((p["spin"] * t + p["spin_phi"]) % 1))]
    f = p["fat"]
    for r, row in enumerate(spr):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            X0, Y0 = x + c * f, y + r * f
            X0c, Y0c = max(X0, FRAME[0]), max(Y0, FRAME[1])
            X1c, Y1c = min(X0 + f, FRAME[2]), min(Y0 + f, FRAME[3])
            if X1c > X0c and Y1c > Y0c:
                idx[Y0c:Y1c, X0c:X1c] = PIDX[ch]


# ---------------------------------------------------------------- water glints (sea band, output px)
glints = [(int(x * S), int(y * S), int(rng.integers(2, 5)), rng.random(), int(rng.integers(1, 3)))
          for x, y in [(330, 372), (372, 381), (405, 368), (436, 389), (296, 390), (470, 376), (520, 386), (250, 378), (560, 370)]]


def draw_glints(idx, t):
    for x, y, w, ph, m in glints:
        a = max(0.0, math.sin(TAU * (m * t + ph))) ** 3
        if a > 0.45:
            idx[y, x:x + w] = PIDX["w"]
            if a > 0.85:
                idx[y, x + w // 2] = PIDX["h"]


# ---------------------------------------------------------------- render
frames = []
for f in range(N):
    t = f / N
    idx = base_idx.copy()
    full = downsample(warped_source(t))
    for (x0, x1, y0, y1) in DYN:
        idx[y0:y1, x0:x1] = quantize(full[y0:y1, x0:x1], y0, x0)
    draw_glints(idx, t)
    for p in petals:
        draw_petal(idx, p, t)
    frames.append(idx)
    if f % 24 == 0:
        print("frame", f)

flat_pal = palette.round().clip(0, 255).astype(np.uint8).reshape(-1).tolist()


def to_img(a):
    im = Image.fromarray(a, "P")
    im.putpalette(flat_pal)
    return im


# Loop check: the seam must look like any other frame transition.
diffs = [(frames[i] != frames[i - 1]).mean() for i in range(1, N)]
seam = (frames[0] != frames[-1]).mean()
print(f"changed px per step: mean {np.mean(diffs):.5f} max {max(diffs):.5f} seam {seam:.5f}")
assert seam <= max(diffs) * 1.25, "visible loop discontinuity"
# Character identity check: faces must be pixel-identical across all frames.
for (a, b, c, d) in FACES[:2]:
    a, b, c, d = int(a), int(b), int(c), int(d)
    assert all((fr[b:d, a:c] == frames[0][b:d, a:c]).all() for fr in frames), "face region changed"

# Delta encoding: every frame after the first only paints pixels that changed; the rest use the
# transparent KEEP index over the previous frame (disposal 1), which LZW compresses to almost nothing.
imgs = [to_img(frames[0])] + [to_img(np.where(frames[i] == frames[i - 1], KEEP, frames[i]).astype(np.uint8)) for i in range(1, N)]
imgs[0].save(ROOT / "hero-rooftop.gif", save_all=True, append_images=imgs[1:], duration=DELAY, loop=0,
             disposal=1, transparency=KEEP, optimize=False)
Image.fromarray(np.clip(base + 0.5, 0, 255).astype(np.uint8)).save(ROOT / "hero-rooftop-still.png", optimize=True)
print("hero-rooftop.gif", (ROOT / "hero-rooftop.gif").stat().st_size, "bytes;", N, "frames x", DELAY, "ms")
