#!/usr/bin/env python3
"""
Generador de assets estilo Nothing OS (matriz de puntos) para tu perfil de GitHub.

Uso:
    python generate.py "TU NOMBRE" "TU SUBTITULO"
    python generate.py "MIKE" "FULL STACK DEV"

Solo se admiten: A-Z, 0-9, espacio y . _ - / : >
"""
import sys
import os

RED = "#D71921"

FONT = {
    "A": "01110/10001/10001/11111/10001/10001/10001",
    "B": "11110/10001/10001/11110/10001/10001/11110",
    "C": "01110/10001/10000/10000/10000/10001/01110",
    "D": "11110/10001/10001/10001/10001/10001/11110",
    "E": "11111/10000/10000/11110/10000/10000/11111",
    "F": "11111/10000/10000/11110/10000/10000/10000",
    "G": "01110/10001/10000/10111/10001/10001/01111",
    "H": "10001/10001/10001/11111/10001/10001/10001",
    "I": "01110/00100/00100/00100/00100/00100/01110",
    "J": "00111/00010/00010/00010/00010/10010/01100",
    "K": "10001/10010/10100/11000/10100/10010/10001",
    "L": "10000/10000/10000/10000/10000/10000/11111",
    "M": "10001/11011/10101/10101/10001/10001/10001",
    "N": "10001/11001/10101/10011/10001/10001/10001",
    "O": "01110/10001/10001/10001/10001/10001/01110",
    "P": "11110/10001/10001/11110/10000/10000/10000",
    "Q": "01110/10001/10001/10001/10101/10010/01101",
    "R": "11110/10001/10001/11110/10100/10010/10001",
    "S": "01111/10000/10000/01110/00001/00001/11110",
    "T": "11111/00100/00100/00100/00100/00100/00100",
    "U": "10001/10001/10001/10001/10001/10001/01110",
    "V": "10001/10001/10001/10001/10001/01010/00100",
    "W": "10001/10001/10001/10101/10101/11011/10001",
    "X": "10001/10001/01010/00100/01010/10001/10001",
    "Y": "10001/10001/01010/00100/00100/00100/00100",
    "Z": "11111/00001/00010/00100/01000/10000/11111",
    "0": "01110/10001/10011/10101/11001/10001/01110",
    "1": "00100/01100/00100/00100/00100/00100/01110",
    "2": "01110/10001/00001/00010/00100/01000/11111",
    "3": "11110/00001/00001/01110/00001/00001/11110",
    "4": "00010/00110/01010/10010/11111/00010/00010",
    "5": "11111/10000/11110/00001/00001/10001/01110",
    "6": "00110/01000/10000/11110/10001/10001/01110",
    "7": "11111/00001/00010/00100/01000/01000/01000",
    "8": "01110/10001/10001/01110/10001/10001/01110",
    "9": "01110/10001/10001/01111/00001/00010/01100",
    " ": "00000/00000/00000/00000/00000/00000/00000",
    ".": "00000/00000/00000/00000/00000/00000/00100",
    "_": "00000/00000/00000/00000/00000/00000/11111",
    "-": "00000/00000/00000/11111/00000/00000/00000",
    "/": "00001/00010/00010/00100/01000/01000/10000",
    ":": "00000/00100/00100/00000/00100/00100/00000",
    ">": "10000/01000/00100/00010/00100/01000/10000",
}

THEMES = {
    "dark": dict(bg="#000000", unlit="#1c1c1c", title="#FFFFFF", sub="#8f8f8f",
                 label="#6e6e6e", glyph="#FFFFFF", border="#2a2a2a"),
    "light": dict(bg="#F2F2F0", unlit="#DADAD7", title="#0A0A0A", sub="#7a7a7a",
                  label="#8a8a8a", glyph="#0A0A0A", border="#cfcfcb"),
}

P = 14      # separación entre puntos
R = 4.6     # radio punto encendido
ROWS = 28


def clean(text):
    text = text.upper()
    return "".join(c if c in FONT else " " for c in text)


def text_width(text):
    return len(text) * 6 - 1


def dots(text, col0, row0, fill, r=R):
    out = []
    for i, ch in enumerate(text):
        glyph = FONT[ch].split("/")
        for y, line in enumerate(glyph):
            for x, bit in enumerate(line):
                if bit == "1":
                    cx = (col0 + i * 6 + x + 0.5) * P
                    cy = (row0 + y + 0.5) * P
                    out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r}" fill="{fill}"/>')
    return "\n    ".join(out)


def banner(theme, title, subtitle):
    t = THEMES[theme]
    title, subtitle = clean(title), clean(subtitle)
    sub_w = text_width(subtitle) + 1 + 6 + 5  # texto + hueco + cursor
    cols = max(85, 6 + max(text_width(title), sub_w))
    W, H = cols * P, ROWS * P

    # cursor parpadeante (bloque 5x7 rojo)
    cursor_col = 3 + text_width(subtitle) + 2
    block = []
    for y in range(7):
        for x in range(5):
            cx = (cursor_col + x + 0.5) * P
            cy = (16 + y + 0.5) * P
            block.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{R}" fill="{RED}"/>')
    block = "\n      ".join(block)

    gx = W - 3 * P  # glifos abajo a la derecha
    gy = H - 2 * P
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
  <defs>
    <pattern id="grid" width="{P}" height="{P}" patternUnits="userSpaceOnUse">
      <circle cx="{P/2}" cy="{P/2}" r="2.1" fill="{t['unlit']}"/>
    </pattern>
    <clipPath id="clip"><rect width="{W}" height="{H}" rx="28"/></clipPath>
  </defs>

  <g clip-path="url(#clip)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#grid)"/>

    <!-- TITULO -->
    <g>
    {dots(title, 3, 6, t['title'])}
    </g>

    <!-- SUBTITULO -->
    <g>
    {dots(subtitle, 3, 16, t['sub'])}
    </g>

    <!-- CURSOR -->
    <g>
      {block}
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/>
    </g>

    <!-- LED ROJO -->
    <circle cx="{W - 3.5 * P:g}" cy="{3.5 * P:g}" r="9" fill="{RED}">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{W - 3.5 * P:g}" cy="{3.5 * P:g}" r="16" fill="none" stroke="{RED}" stroke-opacity="0.35" stroke-width="1.5"/>

    <!-- ETIQUETAS -->
    <text x="{3 * P}" y="{3.5 * P + 4:g}" font-family="'Courier New', monospace" font-size="13" letter-spacing="4" fill="{t['label']}">NOTHING-STYLE // PROFILE</text>
    <circle cx="{3 * P + 4}" cy="{(ROWS - 2) * P:g}" r="3.5" fill="{RED}"/>
    <text x="{3 * P + 18}" y="{(ROWS - 2) * P + 4:g}" font-family="'Courier New', monospace" font-size="12" letter-spacing="3" fill="{t['label']}">SYS.ONLINE</text>

    <!-- GLIFOS -->
    <g stroke-linecap="round" stroke-width="7" fill="none">
      <line x1="{gx - 84}" y1="{gy}" x2="{gx - 60}" y2="{gy}" stroke="{t['glyph']}"/>
      <line x1="{gx - 48}" y1="{gy}" x2="{gx - 24}" y2="{gy}" stroke="{t['glyph']}" stroke-opacity="0.45"/>
      <line x1="{gx - 12}" y1="{gy}" x2="{gx + 12}" y2="{gy}" stroke="{RED}"/>
    </g>
  </g>

  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="{t['border']}"/>
</svg>
'''


def divider():
    cols = 85
    W, H = cols * P, P * 2
    parts = []
    for c in range(cols):
        cx, cy = (c + 0.5) * P, P
        if c < 6:
            parts.append(f'<circle cx="{cx:g}" cy="{cy}" r="{R}" fill="{RED}"/>')
        else:
            parts.append(f'<circle cx="{cx:g}" cy="{cy}" r="2.1" fill="#808080" fill-opacity="0.55"/>')
    body = "\n  ".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="presentation">
  {body}
</svg>
'''


if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "USERNAME"
    subtitle = sys.argv[2] if len(sys.argv) > 2 else "CREATIVE DEV"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        with open(os.path.join(out, f"banner-{theme}.svg"), "w") as f:
            f.write(banner(theme, title, subtitle))
    with open(os.path.join(out, "divider.svg"), "w") as f:
        f.write(divider())
    print("Listo -> carpeta assets/")
