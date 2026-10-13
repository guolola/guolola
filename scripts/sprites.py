"""Hand-authored pixel sprites for the README interface (rendered as crisp SVG rects).

Each sprite is a list of equal-width strings; '.' is transparent, other characters map to PAL.
"""

PAL = {
    "K": "#0a1f5c",  # outline navy
    "H": "#1d47c8", "h": "#4f86ff",              # Makoto's hair
    "Y": "#f3c866", "y": "#ffe9a8",              # Aigis's hair
    "G": "#eef3fa", "R": "#c8343a",              # headphone units, red accents
    "P": "#aebcd3",                              # earphone cord
    "S": "#ffd9c2",                              # skin
    "U": "#1b2238", "u": "#2f3a5e", "k": "#121726",  # uniform, folds, skirt/trousers
    "W": "#ffffff", "w": "#dfe8f5",              # Koromaru fur, shade
    "E": "#8a2a2a", "N": "#141414",              # Koromaru eye / nose
    "B": "#2a7bff", "C": "#9ff3ff", "c": "#33e1ff",  # butterfly
    "p": "#ffc8df", "q": "#ff9cc4",              # petal
}

MAKOTO_BACK = [
    ".....KKKKKK.....",
    "...KKHHHHHHKK...",
    "..KHHHhhHHHHHK..",
    ".KHHHhHHHHHHHHK.",
    ".KHHhHHHHHHHHHK.",
    "KHHHHHHHHHHHHHHK",
    "KHHHHHHHHHHHHHHK",
    "KHHHHHHHHHHHHHHK",
    ".KHHHHHHHHHHHHHK",
    "..KHHHHHHHHHHHK.",
    "..KPKSSSSSSKPK..",
    "..KUPUUUUUUPUK..",
    ".KUUUPPUUPPUUUK.",
    ".KUUuUUUUUUuUUK.",
    ".KUUuUUUUUUuUUK.",
    ".KUUUUUUUUUUUUK.",
    ".KkkkkkkkkkkkkK.",
    "..KKKKKKKKKKKK..",
]

AIGIS_BACK = [
    "......KKKKKK......",
    "....KKYYYYYYKK....",
    "...KYYYyyYYYYYK...",
    "..KYYYyYYYYYYYYK..",
    "..KYYyYYYYYYYYYK..",
    ".KGGYYYYYYYYYYGGK.",
    "KGGRGYYYYYYYYGRGGK",
    "KGGRGYYYYYYYYGRGGK",
    ".KGGYYYYYYYYYYGGK.",
    "..KYYYYYYYYYYYYK..",
    "..KYYyYYYYYYYYYK..",
    "...KYYKSSSSKYYK...",
    "...KUUUUUUUUUUK...",
    "..KUUUUUUUUUUUUK..",
    "..KUUuUUUUUUuUUK..",
    "..KUUuUUUUUUuUUK..",
    "..KUUUUUUUUUUUUK..",
    "..KkkkkkkkkkkkkK..",
    "...KKKKKKKKKKKK...",
]

KOROMARU_SIT = [
    "........K.K...",
    ".......KWKWK..",
    "......KWWWWWK.",
    "......KWWEWWK.",
    "......KWWWWWWK",
    "......KWWWWWNK",
    ".......KWWWKK.",
    ".......KRRRK..",
    "......KWWWWK..",
    "..KK.KWWWWWWK.",
    ".KWWKWWWWWWWK.",
    ".KWWWWWWWWwWK.",
    "..KWWWWWKWwWK.",
    "..KKKKKKKKKKK.",
]

_RUN_TOP = [
    "...........K.K...",
    "..........KWKWK..",
    ".........KWWWWWK.",
    ".KK......KWWEWWWK",
    "KWWK....KWWWWWWNK",
    "KWWWKKKKKWWWWWKK.",
    ".KWWWWWWWWRRRK...",
    "..KWWWWWWWWWWK...",
    "..KWWWWWWWWWWK...",
    "..KwWWWWWWWWwK...",
]
KOROMARU_RUN = [
    _RUN_TOP + [
        "..KWWKKKKKKWWK...",
        ".KWWK.....KWWK...",
        ".KKK.......KKK...",
    ],
    _RUN_TOP + [
        "..KKWWKKKKWWKK...",
        "...KWWK..KWWK....",
        "...KKK...KKK.....",
    ],
]

BUTTERFLY = [
    [  # wings open
        ".KK.....KK.",
        "KCCK...KCCK",
        "KCcBK.KBcCK",
        "KBBBBKBBBBK",
        ".KBBBKBBBK.",
        "..KBBKBBK..",
        ".KBcK.KcBK.",
        ".KBK...KBK.",
        "..K.....K..",
    ],
    [  # wings raised
        "...KK.KK...",
        "..KCCKCCK..",
        "..KCcKcCK..",
        "..KBBKBBK..",
        "...KBKBK...",
        "...KBKBK...",
        "....KKK....",
        "....K.K....",
        "...........",
    ],
]

PETAL = [
    ".pp.",
    "pppq",
    ".pq.",
]

SPARKLE = [
    "..c..",
    "..c..",
    "ccWcc",
    "..c..",
    "..c..",
]


def render(grid, x=0, y=0, s=4, cls=None, extra=""):
    """Merge horizontal runs of the same colour into single rects."""
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            e = c
            while e < len(row) and row[e] == ch:
                e += 1
            out.append(f'<rect x="{x + c * s:g}" y="{y + r * s:g}" width="{(e - c) * s:g}" height="{s:g}" fill="{PAL[ch]}"/>')
            c = e
    attr = f' class="{cls}"' if cls else ""
    return f'<g{attr} shape-rendering="crispEdges"{extra}>' + "".join(out) + "</g>"


def size(grid, s=4):
    return len(grid[0]) * s, len(grid) * s
