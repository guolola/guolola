"""Generate the README's SVG interface: section headers, link chips, project plates,
technology tiles and the night footer.

Display type is converted to outlines so every OS renders the same lettering:
  * Barlow Condensed (OFL) for Latin and numerals
  * Smiley Sans / 得意黑 (OFL) for Chinese
Fonts are not committed; download them into FONT_DIR first (see assets/CREDITS.md).

Requires: Python 3, fontTools, uharfbuzz, svgelements
  FONT_DIR=path/to/fonts python scripts/build_ui.py
"""
from pathlib import Path
import os
import re
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from svgelements import SVG
import sprites as SP

ROOT = Path(__file__).resolve().parents[1] / "assets"
UI, ICONS = ROOT / "ui", ROOT / "icons"
UI.mkdir(exist_ok=True)
FONT_DIR = Path(os.environ.get("FONT_DIR", Path(__file__).resolve().parent / "fonts"))

# Palette ------------------------------------------------------------------------------------
NIGHT, NAVY, COBALT, AZURE, CYAN, ICE, INK = "#040b22", "#0a1f5c", "#123a9c", "#1f6bff", "#33e1ff", "#d9f6ff", "#10224f"
THEME = {
    "light": dict(num=AZURE, title=NAVY, shadow="#5fdcff", en=AZURE, rule="#c4d9ff"),
    "dark": dict(num=CYAN, title="#ffffff", shadow=AZURE, en="#7fdcff", rule="#1f3b78"),
}


# Type ---------------------------------------------------------------------------------------
class Face:
    def __init__(self, file):
        path = str(FONT_DIR / file)
        self.tt = TTFont(path)
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upm = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(path)))

    def run(self, text, size, x, y, tracking=0.0):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True})
        s, out = size / self.upm, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = SVGPathPen(self.glyphs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
            self.glyphs[self.order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, y - pos.y_offset * s)))
            out.append(pen.getCommands())
            x += pos.x_advance * s + tracking
        return "".join(out), x - tracking


XB, BI, SI, ZH = (Face(f) for f in ("BarlowCondensed-ExtraBoldItalic.ttf", "BarlowCondensed-BoldItalic.ttf",
                                    "BarlowCondensed-SemiBoldItalic.ttf", "SmileySans-Oblique.ttf"))
is_cjk = lambda ch: 0x2E80 <= ord(ch) <= 0x9FFF or 0x3000 <= ord(ch) <= 0x303F or 0xFF00 <= ord(ch) <= 0xFFEF


def text(s, size, x, y, latin=BI, tracking=0.0, latin_scale=1.12):
    """Mixed Chinese/Latin line -> (path data, end x). Latin is scaled to sit with the CJK face."""
    runs, d = re.findall(r"[⺀-鿿　-〿＀-￯]+|[^⺀-鿿　-〿＀-￯]+", s), ""
    for i, r in enumerate(runs):
        cjk = is_cjk(r[0])
        part, x = (ZH.run(r, size, x, y, tracking) if cjk else latin.run(r, size * latin_scale, x, y, tracking))
        d += part
        if i < len(runs) - 1:
            x += tracking
    return d, x


def svg(w, h, body, title=None):
    t = f"<title>{title}</title>" if title else ""
    x = ' xmlns:xlink="http://www.w3.org/1999/xlink"' if "xlink:" in body else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg"{x} width="{w}" height="{h}" viewBox="0 0 {w} {h}">{t}{body}</svg>\n'


MOTION = ('.f0{animation:fa .56s steps(1) infinite}.f1{opacity:0;animation:fb .56s steps(1) infinite}'
          '@keyframes fa{50%{opacity:0}}@keyframes fb{50%{opacity:1}}'
          '.fl{animation:fl 3.6s ease-in-out infinite}@keyframes fl{50%{transform:translate(3px,-7px)}}'
          '.tw{animation:tw 2.8s ease-in-out infinite}@keyframes tw{50%{opacity:.2}}')
REDUCE = '@media (prefers-reduced-motion:reduce){*{animation:none!important}.f1{opacity:0!important}}'


def style(extra=""):
    return f"<style>{MOTION}{extra}{REDUCE}</style>"


def butterfly(x, y, s=3, delay=0.0):
    d = f' style="animation-delay:{delay}s"'
    return (f'<g class="fl"{d}>' + SP.render(SP.BUTTERFLY[0], x, y, s, "f0", d)
            + SP.render(SP.BUTTERFLY[1], x, y, s, "f1", d) + "</g>")


def sparkle(x, y, s=2, delay=0.0):
    return SP.render(SP.SPARKLE, x, y, s, "tw", f' style="animation-delay:{delay}s"')


def save(path, content):
    path.write_text(content, encoding="utf-8")


# Section headers (transparent, light + dark) --------------------------------------------------
SECTIONS = [("about", "01", "关于我", "ABOUT"), ("stack", "02", "技术栈", "STACK"),
            ("projects", "03", "项目", "PROJECTS"), ("activity", "04", "贡献记录", "ACTIVITY")]
for slug, num, zh, en in SECTIONS:
    for theme, c in THEME.items():
        nd, nend = XB.run(num, 124, 2, 108)
        td, tend = text(zh, 58, nend + 6, 90)
        ed, eend = SI.run(en, 19, tend + 24, 90, tracking=4)
        r0 = eend + 20
        body = (f'<path d="{nd}" fill="{c["num"]}" fill-opacity=".07" stroke="{c["num"]}" stroke-width="2.2" stroke-linejoin="round"/>'
                f'<path d="{td}" fill="{c["shadow"]}" transform="translate(4 4)"/><path d="{td}" fill="{c["title"]}"/>'
                f'<path d="{ed}" fill="{c["en"]}"/>'
                f'<path d="M{r0:.0f} 83H842" stroke="{c["rule"]}" stroke-width="2"/>'
                f'<path d="M852 72H866L856 94H842Z" fill="{AZURE}"/><path d="M872 72H880L870 94H862Z" fill="{CYAN}"/>'
                f'<path d="M888 72H900L890 94H878Z" fill="{c["num"]}" fill-opacity=".45"/>'
                + style() + butterfly(776, 24, 4, -0.9 * len(slug)) + sparkle(tend + 2, 18, 2) + sparkle(tend + 18, 44, 1.4, -1.3)
                + SP.render(SP.PETAL, nend - 26, 12, 3))
        save(UI / f"section-{slug}-{theme}.svg", svg(900, 120, body, f"{num} {zh}"))


# Link chips (opaque) --------------------------------------------------------------------------
def chip(slug, label, primary):
    fill, ink, shadow = (CYAN, NAVY, NAVY) if primary else (NAVY, "#ffffff", CYAN)
    d, end = text(label, 23, 38, 40)
    shape = "16,0 304,0 288,60 0,60"
    body = (f'<polygon points="{shape}" fill="{shadow}" transform="translate(6 6)"/><polygon points="{shape}" fill="{fill}"/>'
            + ('' if primary else f'<polygon points="16,0 26,0 10,60 0,60" fill="{CYAN}"/>')
            + f'<path d="{d}" fill="{ink}"/>'
            f'<path d="M258 39L272 25M261 25H272V36" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="square"/>')
    save(UI / f"link-{slug}.svg", svg(310, 66, body, label))


chip("demo", "在线体验 SoftJL", True)
chip("softjl", "SoftJL 源码仓库", False)
chip("repos", "全部仓库", False)


# Project plates (opaque) ----------------------------------------------------------------------
def ripples(w, h, n, y0, amp, color, op):
    out = ""
    for i in range(n):
        y, a = y0 + i * 9, amp * (1 - i / (n + 1))
        pts = " ".join(f"{x},{y + a * (1 if (x // 60) % 2 else -1):.1f}" for x in range(0, w + 60, 60))
        out += f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-opacity="{op * (1 - i / n):.2f}" stroke-width="1.5"/>'
    return out


def tarot(cx, cy, h, numeral, name, symbol, angle):
    w = h * 0.62
    x, y = cx - w / 2, cy - h / 2
    nd, nw = XB.run(numeral, h * 0.17, 0, 0)
    ld, lw = SI.run(name, h * 0.095, 0, 0, tracking=1.2)
    if symbol == "fool":
        art = SP.render(SP.BUTTERFLY[0], cx - 11 * h / 46, cy - 9 * h / 46, h / 23)
    elif symbol == "star":
        pts = " ".join(f"{cx + (h * (.2 if i % 2 == 0 else .08)) * __import__('math').sin(i * 3.14159 / 5):.1f},"
                       f"{cy - (h * (.2 if i % 2 == 0 else .08)) * __import__('math').cos(i * 3.14159 / 5):.1f}" for i in range(10))
        art = f'<polygon points="{pts}" fill="#ffd65a" stroke="{NAVY}" stroke-width="2" stroke-linejoin="round"/>'
    else:
        import math
        rays = "".join(f'<path d="M{cx + h * .13 * math.cos(a):.1f} {cy + h * .13 * math.sin(a):.1f}L{cx + h * .21 * math.cos(a):.1f} {cy + h * .21 * math.sin(a):.1f}" '
                       f'stroke="#ff9d3b" stroke-width="{h * .03:.1f}" stroke-linecap="round"/>' for a in [i * math.pi / 4 for i in range(8)])
        art = rays + f'<circle cx="{cx}" cy="{cy}" r="{h * .1:.1f}" fill="#ffd65a" stroke="{NAVY}" stroke-width="2"/>'
    return (f'<g transform="rotate({angle} {cx} {cy})">'
            f'<rect x="{x + 6}" y="{y + 6}" width="{w:.1f}" height="{h}" rx="5" fill="{CYAN}"/>'
            f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="5" fill="#fdf9ee" stroke="{NAVY}" stroke-width="3"/>'
            f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12:.1f}" height="{h - 12}" rx="2" fill="none" stroke="{AZURE}" stroke-width="1.2"/>'
            f'<path d="{nd}" fill="{NAVY}" transform="translate({cx - nw / 2:.1f} {y + h * .24:.1f})"/>{art}'
            f'<path d="{ld}" fill="{NAVY}" transform="translate({cx - lw / 2:.1f} {y + h * .9:.1f})"/></g>')


def plate(slug, name, caption, num, featured, card):
    W, H = 900, (176 if featured else 124)
    big = 92 if featured else 58
    nd, _ = XB.run(num, H * 1.18, 0, 0)
    nw = XB.run(num, H * 1.18, 0, 0)[1]
    cd, _ = text(caption, 21 if featured else 18, 44, 48 if featured else 40, latin=SI, tracking=1.5)
    td, _ = text(name, big, 40, H - (40 if featured else 26), latin=XB, latin_scale=1.0)
    sl = 0.36 * H
    body = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NIGHT}"/><stop offset=".65" stop-color="{NAVY}"/>'
            f'<stop offset="1" stop-color="{COBALT}"/></linearGradient><clipPath id="c"><rect width="{W}" height="{H}"/></clipPath>'
            f'<pattern id="dt" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.6" fill="{CYAN}"/></pattern>'
            f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".5"/></linearGradient>'
            f'<mask id="m"><rect x="{W - 480}" width="480" height="{H}" fill="url(#fade)"/></mask></defs>'
            f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#g)"/>'
            f'<rect x="{W - 480}" width="480" height="{H}" fill="url(#dt)" mask="url(#m)"/>'
            + "".join(f'<rect x="{40 + (i * 137) % 420}" y="{14 + i * (H - 28) / 9:.0f}" width="{120 + (i * 53) % 160}" height="1.6" fill="#ffffff" fill-opacity=".1"/>' for i in range(10) if featured)
            + ripples(W, H, 4, H - 30, 3, CYAN, 0.22)
            + f'<polygon points="{W - 250},0 {W - 196},0 {W - 196 - sl},{H} {W - 250 - sl},{H}" fill="{AZURE}" fill-opacity=".55"/>'
            f'<polygon points="{W - 186},0 {W - 176},0 {W - 176 - sl},{H} {W - 186 - sl},{H}" fill="{CYAN}"/>'
            f'<path d="{nd}" transform="translate({W - nw - 14} {H * 0.98:.0f})" fill="none" stroke="{CYAN}" stroke-width="2.2" stroke-opacity=".9"/>'
            f'<rect width="10" height="{H}" fill="{CYAN}"/>'
            f'<path d="{cd}" fill="#7fe8ff"/>'
            f'<path d="{td}" fill="{AZURE}" transform="translate(5 5)"/><path d="{td}" fill="#ffffff"/>'
            + tarot(W - 330 if featured else W - 310, H / 2, H * (0.8 if featured else 0.84), *card, -7 if featured else 6)
            + "</g>")
    save(UI / f"project-{slug}.svg", svg(W, H, body, name))


plate("softjl", "SoftJL", "PROJECT 01 ／ 工程实践工作台", "01", True, ("0", "THE FOOL", "fool"))
plate("well", "井工程数据中心", "PROJECT 02 ／ 数据可视化", "02", False, ("XVII", "THE STAR", "star"))
plate("components", "组件集在线演示", "PROJECT 03 ／ 在线演示", "03", False, ("XIX", "THE SUN", "sun"))


# Speech bubble greeting (opaque white bubble, reads on light and dark) ------------------------
def hello():
    import math
    td, tend = text("Hi，我是 guolola。", 46, 58, 88, latin=XB, latin_scale=1.0)
    bw = tend + 44
    cx, cy, rx, ry = bw / 2 + 6, 72, bw / 2, 56
    W = int(cx + rx + 64)
    on = lambda deg, k=1.0: (cx + k * rx * math.cos(math.radians(deg)), cy + k * ry * math.sin(math.radians(deg)))
    tip = (cx + rx + 54, cy + ry + 10)
    (ax, ay), (bx, by) = on(18), on(52)
    (ax2, ay2), (bx2, by2) = on(20, .9), on(50, .9)
    tail = f"{ax:.1f},{ay:.1f} {tip[0]:.1f},{tip[1]:.1f} {bx:.1f},{by:.1f}"
    cover = f"{ax2:.1f},{ay2:.1f} {tip[0] - 9:.1f},{tip[1] - 6:.1f} {bx2:.1f},{by2:.1f}"
    body = (style()
            + f'<g transform="translate(7 7)" fill="{CYAN}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/><polygon points="{tail}"/></g>'
            f'<polygon points="{tail}" fill="#ffffff" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" stroke="{NAVY}" stroke-width="4"/>'
            f'<polygon points="{cover}" fill="#ffffff"/>'
            f'<path d="{td}" fill="{CYAN}" transform="translate(3 3)"/><path d="{td}" fill="{NAVY}"/>'
            + sparkle(W - 92, 4, 3) + sparkle(W - 50, 34, 2, -1.4) + SP.render(SP.PETAL, 10, 116, 4))
    save(UI / "hello.svg", svg(W, 150, body, "Hi，我是 guolola。"))


hello()


# Koromaru chases a butterfly along a dotted line (transparent divider) ------------------------
def divider_run():
    W, H = 900, 76
    run = ('.run{animation:run 11s linear -4.5s infinite}@keyframes run{from{transform:translate(-160px,0)}to{transform:translate(1000px,0)}}'
           '.ra{animation:fa .36s steps(1) infinite}.rb{opacity:0;animation:fb .36s steps(1) infinite}.sit{opacity:0}')
    reduce_extra = '@media (prefers-reduced-motion:reduce){.run{display:none}.sit{opacity:1}}'
    dash = "".join(f'<rect x="{x}" y="66" width="10" height="3" fill="{AZURE if (x // 24) % 3 else CYAN}" fill-opacity=".8"/>' for x in range(0, W, 24))
    dog = SP.render(SP.KOROMARU_RUN[0], 0, 14, 4, "ra") + SP.render(SP.KOROMARU_RUN[1], 0, 14, 4, "rb")
    body = (f"<style>{MOTION}{run}{REDUCE}{reduce_extra}</style>{dash}"
            f'<g class="run">{dog}{butterfly(112, 0, 3)}</g>'
            f'<g class="sit">{SP.render(SP.KOROMARU_SIT, 410, 10, 4)}{butterfly(480, 0, 3)}</g>')
    save(UI / "divider-run.svg", svg(W, H, body))


divider_run()


# Technology tiles -----------------------------------------------------------------------------
LOGOS = {  # slug: (source file under assets/icons, optical size in a 64px tile)
    "dify": ("source/dify.svg", 36), "coze": ("source/coze.svg", 36), "langchain": ("source/langchain.svg", 38),
    "langgraph": ("source/langgraph.svg", 40), "mcp": ("source/mcp.svg", 36), "a2a": ("source/a2a.svg", 38),
    "html5": ("html5.svg", 36), "css3": ("css3.svg", 36), "javascript": ("javascript.svg", 32), "typescript": ("typescript.svg", 32),
    "vuejs": ("vuejs.svg", 38), "react": ("react.svg", 40), "pinia": ("source/pinia.svg", 38), "vite": ("source/vite.svg", 36),
    "webpack": ("webpack.svg", 38), "python": ("python.svg", 36), "fastapi": ("fastapi.svg", 36),
    "pydantic": ("source/pydantic.svg", 36), "sqlalchemy": ("sqlalchemy.svg", 42), "mysql": ("mysql.svg", 40),
    "redis": ("redis.svg", 38), "rabbitmq": ("rabbitmq.svg", 34), "nodejs": ("nodejs.svg", 36), "postgresql": ("postgresql.svg", 38),
    "git": ("git.svg", 36), "githubactions": ("githubactions.svg", 36), "codex": ("source/codex.svg", 34),
    "claude-code": ("source/claude-code.svg", 38), "nextjs": ("nextjs.svg", 36), "fastify": ("fastify.svg", 40),
    "echarts": ("source/echarts.svg", 36),
}
RECOLOR = {"pydantic": [('fill="#fff"', 'fill="#e92063"')], "echarts": [("<path ", '<path fill="#aa344d" ')]}
TIGHT = {"vite"}  # artwork already fills its viewBox; gradient defs would skew the measurement
KEEP_ATTRS = ("fill", "fill-rule", "clip-rule", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin")


def logo(slug, file, size):
    raw = (ICONS / file).read_text(encoding="utf-8")
    raw = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<title>.*?</title>", "", raw, flags=re.S).replace("currentColor", INK)
    for a, b in RECOLOR.get(slug, []):
        raw = raw.replace(a, b)
    root = re.search(r"<svg\b[^>]*>", raw)[0]
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', root)[1].replace(",", " ").split()]
    # measure the drawn artwork, not the canvas, so every mark is optically centred
    probe = re.sub(r"<svg\b[^>]*>", f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{vb[2]}" height="{vb[3]}" viewBox="{" ".join(map(str, vb))}">', raw, count=1)
    x0, y0, x1, y1 = (0, 0, vb[2], vb[3]) if slug in TIGHT else SVG.parse(_io(probe)).bbox()
    bw, bh = x1 - x0, y1 - y0
    bx, by = vb[0] + x0, vb[1] + y0
    keep = " ".join(m for m in re.findall(r'\s([\w-]+="[^"]*")', root) if m.split("=")[0] in KEEP_ATTRS)
    inner = raw[raw.index(root) + len(root):raw.rindex("</svg>")].strip()
    off = (64 - size) / 2
    inner_svg = (f'<svg x="{off:g}" y="{off:g}" width="{size}" height="{size}" viewBox="{bx:.2f} {by:.2f} {bw:.2f} {bh:.2f}" '
                 f'preserveAspectRatio="xMidYMid meet" {keep}>{inner}</svg>')
    body = (f'<path d="M.75 .75H52.5L63.25 11.5V63.25H.75Z" fill="#f6faff" stroke="{NAVY}" stroke-width="1.5"/>'
            f'<path d="M56 .75H63.25V8Z" fill="{CYAN}"/>{inner_svg}')
    save(ICONS / f"tile-{slug}.svg", svg(64, 64, body))


def _io(s):
    import io
    return io.StringIO(s)


for slug, (file, size) in LOGOS.items():
    logo(slug, file, size)


# Night footer: the three of them watching the moon (opaque) ----------------------------------
def footer():
    import random
    W, H, SEA = 900, 220, 164
    rnd = random.Random(11)
    stars = ""
    for i in range(54):
        x, y = rnd.uniform(20, W - 20), rnd.uniform(8, SEA - 14)
        if (660 < x < 840 and y < 110) or (300 < x < 640 and y > 70):
            continue
        s = rnd.choice([2, 2, 2, 3])
        cls = f' class="tw" style="animation-delay:{-rnd.uniform(0, 2.8):.1f}s"' if i % 2 == 0 else ""
        stars += f'<rect{cls} x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}" fill="{ICE}" opacity="{rnd.uniform(.35, .9):.2f}"/>'
    moon, cx, cy, R, P = "", 752, 64, 38, 4
    for gy in range(-R, R + 1, P):
        for gx in range(-R, R + 1, P):
            inside = (gx + 2) ** 2 + (gy + 2) ** 2 <= R * R
            bite = (gx - 22 + 2) ** 2 + (gy - 12 + 2) ** 2 <= (R - 6) ** 2
            if inside and not bite:
                edge = (gx + 2) ** 2 + (gy + 2) ** 2 > (R - 5) ** 2
                moon += f'<rect x="{cx + gx}" y="{cy + gy}" width="{P}" height="{P}" fill="{"#9ee9ff" if edge else "#f2fbff"}"/>'
    glow = f'<circle cx="{cx}" cy="{cy}" r="{R + 30}" fill="url(#glow)"/>'
    refl = "".join(f'<rect x="{cx - 30 + (i * 13) % 34}" y="{SEA + 8 + i * 7}" width="{30 - i * 3}" height="2" fill="#bfefff" opacity="{.75 - i * .1:.2f}" '
                   f'class="tw" style="animation-delay:{-i * .4:.1f}s"/>' for i in range(7))
    ledge = (f'<rect x="300" y="{SEA - 10}" width="330" height="14" fill="#1b2d63"/><rect x="300" y="{SEA - 10}" width="330" height="3" fill="#3f63b8"/>'
             f'<rect x="300" y="{SEA + 4}" width="330" height="10" fill="#0d1a42"/>')
    party = (SP.render(SP.MAKOTO_BACK, 352, SEA - 10 - 64, 4) + SP.render(SP.AIGIS_BACK, 420, SEA - 10 - 68, 4)
             + SP.render(SP.KOROMARU_SIT, 508, SEA - 10 - 50, 4))
    petals = "".join(f'<g class="pf" style="animation-delay:{-d}s">{SP.render(SP.PETAL, x, 0, 3)}</g>' for x, d in ((250, 0), (560, 3.1), (640, 5.7), (120, 7.9)))
    td, _ = SI.run("see you soon", 36, 62, 96, tracking=3)
    gd, _ = SI.run("GUOLOLA", 14, 64, 122, tracking=5)
    extra = ('.pf{animation:pf 10s linear infinite}@keyframes pf{0%{transform:translate(0,-20px);opacity:0}10%{opacity:1}'
             '85%{opacity:1}100%{transform:translate(70px,170px);opacity:0}}.pf{opacity:0}')
    body = (f"<style>{MOTION}{extra}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.f1{{opacity:0!important}}.pf{{display:none}}}}</style>"
            f'<defs><linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NIGHT}"/><stop offset="1" stop-color="{NAVY}"/></linearGradient>'
            f'<radialGradient id="glow"><stop offset="0" stop-color="#9ee9ff" stop-opacity=".35"/><stop offset="1" stop-color="#9ee9ff" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#n)"/>{stars}{glow}{moon}'
            f'<rect y="{SEA}" width="{W}" height="{H - SEA}" fill="#061537"/><path d="M0 {SEA}H{W}" stroke="{AZURE}" stroke-opacity=".6" stroke-width="2"/>'
            + ripples(W, H, 4, SEA + 18, 2, CYAN, 0.18) + refl + ledge + party + butterfly(600, 52, 3) + petals
            + f'<rect width="8" height="{H}" fill="{CYAN}"/>'
            f'<path d="{td}" fill="{ICE}"/><path d="{gd}" fill="{CYAN}"/>')
    save(UI / "footer-night.svg", svg(W, H, body, "see you soon"))


footer()
print("UI written:", len(list(UI.glob("*.svg"))), "files;", len(LOGOS), "tiles")
