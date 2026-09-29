#!/usr/bin/env python3
"""Collective priors pipeline figure: traces, transition counts, ranked candidates.

Illustrative example, drawn in the deck palette. Method names are synthetic.

Emits four SVGs:
  collective-pipeline.svg   the whole figure on white (used as a static figure)
  collective-panel-1.svg    panel 1 only, transparent, full canvas
  collective-panel-2.svg    panel 2 plus its incoming arrow, transparent, full canvas
  collective-panel-3.svg    panel 3 plus its incoming arrow, transparent, full canvas

The three panel files share the pipeline's canvas and coordinates, so stacking
them at the same position on a slide reproduces the whole figure. That is what
lets the deck reveal one step per click without moving anything.
"""
import pathlib

W, H = 1280, 470
OUT = pathlib.Path(__file__).parent
INK, GREY, LINE = "#1A1A1A", "#5F6368", "#D0D4D9"
COL, COL_T = "#0E8A6A", "#E2F3EE"
PANEL = "#F7F8F9"
SANS = "system-ui,-apple-system,Segoe UI,Roboto,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"


def chip(x, y, label, w=96, h=34, fill="#FFFFFF", stroke=LINE, tc=INK, sw=1.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 6}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="17" fill="{tc}">{label}</text>')


def arrow(x1, y, x2, col=GREY, w=2.0):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{col}" '
            f'stroke-width="{w}"/>'
            f'<polygon points="{x2},{y} {x2 - 10},{y - 5} {x2 - 10},{y + 5}" fill="{col}"/>')


def edge(p1, p2, n, cw=100, ch=34, pad=6):
    """Directed transition edge p1 -> p2, arrowhead at the target chip's border.

    Stroke width encodes the count: 1 -> 2.0, 2 -> 4.0, 3 -> 6.0.
    """
    import math
    (x1, y1), (x2, y2) = p1, p2
    c1 = (x1 + cw / 2, y1 + ch / 2)
    c2 = (x2 + cw / 2, y2 + ch / 2)
    dx, dy = c1[0] - c2[0], c1[1] - c2[1]
    hw, hh = cw / 2 + pad, ch / 2 + pad
    ts = [hw / abs(dx) if dx else 9e9, hh / abs(dy) if dy else 9e9]
    tt = min(ts)
    bx, by = c2[0] + tt * dx, c2[1] + tt * dy      # where the line meets the chip
    ux, uy = (bx - c1[0]), (by - c1[1])
    L = math.hypot(ux, uy) or 1.0
    ux, uy = ux / L, uy / L
    hl, hwid = 15.0, 6.5                            # arrowhead length, half-width
    tipx, tipy = bx, by
    basex, basey = bx - ux * hl, by - uy * hl
    px, py = -uy, ux
    col = COL if n > 1 else LINE
    w = 2.0 + 2.0 * (n - 1)
    return (f'<line x1="{c1[0]}" y1="{c1[1]}" x2="{basex:.1f}" y2="{basey:.1f}" '
            f'stroke="{col}" stroke-width="{w}" opacity="0.75"/>'
            f'<polygon points="{tipx:.1f},{tipy:.1f} '
            f'{basex + px * hwid:.1f},{basey + py * hwid:.1f} '
            f'{basex - px * hwid:.1f},{basey - py * hwid:.1f}" fill="{col}" opacity="0.9"/>')


def head(x, n, label, w):
    return (f'<circle cx="{x + 15}" cy="46" r="15" fill="{COL}"/>'
            f'<text x="{x + 15}" y="52" text-anchor="middle" font-family="{SANS}" '
            f'font-size="16" font-weight="700" fill="#FFFFFF">{n}</text>'
            f'<text x="{x + 40}" y="52" font-family="{SANS}" font-size="19" '
            f'font-weight="600" fill="{INK}">{label}</text>')


def panel1():
    """Prior teams' traces."""
    g = [f'<rect x="16" y="72" width="392" height="330" rx="12" fill="{PANEL}"/>',
         head(16, "1", "Prior teams' traces", 392)]
    teams = [("Team A", ["main()", "parse()", "token()"]),
             ("Team B", ["main()", "parse()", "token()"]),
             ("Team C", ["main()", "parse()", "cache()"])]
    for r, (who, path) in enumerate(teams):
        y = 104 + r * 104
        g.append(f'<text x="40" y="{y + 16}" font-family="{SANS}" font-size="15" '
                 f'fill="{GREY}">{who}</text>')
        for c, m in enumerate(path):
            x = 40 + c * 118
            on = m in ("parse()", "token()")
            g.append(chip(x, y + 30, m, w=100, fill=COL_T if on else "#FFFFFF",
                          stroke=COL if on else LINE))
            if c < len(path) - 1:
                g.append(arrow(x + 100, y + 47, x + 118, GREY, 1.8))
    return g


def panel2():
    """Transition counts."""
    g = [f'<rect x="444" y="72" width="360" height="330" rx="12" fill="{PANEL}"/>',
         head(444, "2", "Transition counts", 360)]
    nodes = {"main()": (498, 120), "parse()": (646, 212), "token()": (492, 310),
             "cache()": (668, 330)}
    # counts read off panel 1: A and B both go parse->token, only C goes parse->cache
    edges = [("main()", "parse()", 3), ("parse()", "token()", 2),
             ("parse()", "cache()", 1)]
    for a, b, n in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        g.append(edge(nodes[a], nodes[b], n))
        mx, my = (x1 + x2) / 2 + 50, (y1 + y2) / 2 + 12
        g.append(f'<circle cx="{mx}" cy="{my}" r="14" fill="#FFFFFF" stroke="{LINE}"/>'
                 f'<text x="{mx}" y="{my + 5}" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="14" fill="{INK}">{n}</text>')
    for m, (x, y) in nodes.items():
        on = m in ("parse()", "token()")
        g.append(chip(x, y, m, w=100, fill=COL_T if on else "#FFFFFF",
                      stroke=COL if on else LINE))
    g.append(f'<text x="624" y="392" text-anchor="middle" font-family="{SANS}" '
             f'font-size="14" fill="{GREY}">Counted across every team except the one being tested</text>')
    return g


def panel3():
    """Ranked candidates for a new team."""
    g = [f'<rect x="840" y="72" width="424" height="330" rx="12" fill="{PANEL}"/>',
         head(840, "3", "Ranked for a new team", 424),
         chip(864, 96, "New team is at parse()", w=376, h=36, fill="#FFFFFF",
              stroke=COL, tc=INK)]
    rows = [("token()", 0.75, True, ""), ("cache()", 0.25, False, ""),
            ("render()", 0.08, False, "5 4")]
    for r, (m, v, best, dash) in enumerate(rows):
        y = 156 + r * 78
        g.append(f'<text x="864" y="{y + 24}" font-family="{SANS}" font-size="16" '
                 f'fill="{GREY}">{r + 1}</text>')
        g.append(chip(886, y, m, w=124, fill=COL_T if best else "#FFFFFF",
                      stroke=COL if best else LINE, dash=dash))
        bx, bw = 1026, 200
        g.append(f'<rect x="{bx}" y="{y + 9}" width="{bw}" height="16" rx="8" fill="{LINE}"/>')
        g.append(f'<rect x="{bx}" y="{y + 9}" width="{bw * v:.0f}" height="16" rx="8" '
                 f'fill="{COL if best else GREY}" opacity="{1 if best else 0.55}"/>')
        if best:
            g.append(f'<text x="{bx}" y="{y + 48}" font-family="{SANS}" font-size="14" '
                     f'font-weight="600" fill="{COL}">the step the team actually took</text>')
        if dash:
            g.append(f'<text x="886" y="{y + 52}" font-family="{SANS}" font-size="13" '
                     f'fill="{GREY}">added by the call graph, never visited before</text>')
    return g


def caption():
    return [f'<text x="16" y="{H - 14}" font-family="{SANS}" font-size="13" '
            f'fill="{GREY}">Illustrative example. Method names are synthetic.</text>']


def svg(parts, white_bg):
    bg = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>' if white_bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
            f'height="{H}" role="img" aria-label="Collective prior pipeline">'
            + bg + "".join(parts) + "</svg>")


def build():
    a1 = arrow(412, 236, 440, GREY, 2.5)
    a2 = arrow(808, 236, 836, GREY, 2.5)
    p1, p2, p3, cap = panel1(), panel2(), panel3(), caption()

    files = {
        "collective-pipeline.svg": svg(p1 + p2 + p3 + [a1, a2] + cap, True),
        "collective-panel-1.svg": svg(p1 + cap, False),
        "collective-panel-2.svg": svg([a1] + p2, False),
        "collective-panel-3.svg": svg([a2] + p3, False),
    }
    for name, body in files.items():
        (OUT / name).write_text(body, encoding="utf-8")
        print("wrote", OUT / name)


if __name__ == "__main__":
    build()
