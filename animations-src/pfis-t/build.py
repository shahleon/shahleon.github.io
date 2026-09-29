#!/usr/bin/env python3
"""Generate the PFIS-T animation: fourteen SVG frames plus a rehearsal page.

Pass A, ten frames: a target that PFIS3 cannot reach at all becomes reachable
through social cues and rises to the top. This is the coverage story behind
unknowns falling from 33.63% to 21.06%.

Pass B, four frames: the social gate itself, with the saturating curve.

    python3 build.py

Model parameters are the published defaults from the PFIS-T parameter table.
Per-node activations and cue strengths are ILLUSTRATIVE, but every gate value
on screen is computed from the real formula, not asserted.
"""

import html
import math
import pathlib

W, H = 1280, 720
OUT = pathlib.Path(__file__).parent

INK, MUTED, LINE = "#1a1d21", "#8b9199", "#d4d8dd"
BEAM, PATH, ERROR = "#1f6feb", "#17803d", "#c2401a"
SOCIAL = "#7c3aed"                         # the social layer, its own hue
PANEL, SURFACE = "#f4f5f7", "#ffffff"

# Published defaults (PFIS-T parameter table)
ALPHA, BETA = 0.85, 0.90
S_E, S_I = 0.25, 0.10
KAPPA, RHO = 0.8, 0.1
W_E, W_I = 1.0, 1.0
TOP_N = 5

GX0, GX1 = 40, 792
PX0 = 824

# Illustrative baseline activations after spreading.
A0 = {"layout()": .85, "paint()": .71, "shape()": .66, "fill()": .58,
      "drawTri()": .55}
# Teammates working the same defect touch nearby code, so shortlisted
# candidates normally carry some implicit support. Zero across the board is
# the extreme case, not the typical one.
CUES = {"drawTri()": (1.0, 1.0), "layout()": (0.0, 0.30),
        "paint()": (0.0, 0.25), "shape()": (0.0, 0.15), "fill()": (0.0, 0.10)}

POS = {"render()": (150, 372), "layout()": (330, 268), "paint()": (330, 476),
       "shape()": (500, 214), "fill()": (500, 420), "drawTri()": (688, 330)}
EDGES = [("render()", "layout()"), ("render()", "paint()"),
         ("layout()", "shape()"), ("paint()", "fill()"),
         ("layout()", "fill()")]


def esc(s):
    return html.escape(str(s), quote=False)


def social_support(r):
    e, i = CUES[r]
    return W_E * e + W_I * i


def p_soc(s):
    return (1 - RHO) * (1 - math.exp(-KAPPA * s)) + RHO / TOP_N


def gated():
    out = {r: A0[r] * p_soc(social_support(r)) for r in A0}
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


# --------------------------------------------------------------------------- #
# drawing primitives
# --------------------------------------------------------------------------- #

def patch(name, *, act=None, state="idle", w=132):
    """state: idle | seed | active | target | unreachable | won"""
    cx, cy = POS[name]
    fill, stroke, txt, sw, dash = SURFACE, LINE, INK, 1.6, ""
    if state == "seed":
        fill, stroke, sw = "#e8f0fe", BEAM, 2.8
    elif state == "active":
        fill, stroke, sw = "#eef4fe", BEAM, 2.0
    elif state == "unreachable":
        fill, stroke, txt = SURFACE, LINE, MUTED
        dash = ' stroke-dasharray="5 4"'
    elif state == "target":
        fill, stroke, sw = "#f5efff", SOCIAL, 2.6
    elif state == "won":
        fill, stroke, sw = "#e7f5ec", PATH, 3.0
    x, y = cx - w / 2, cy - 22
    g = [f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="44" rx="8" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>']
    g.append(f'<text x="{cx}" y="{cy+6}" text-anchor="middle" '
             f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" '
             f'font-size="18" fill="{txt}">{esc(name)}</text>')
    if act is not None:
        col = PATH if state == "won" else (SOCIAL if state == "target" else BEAM)
        g.append(f'<rect x="{x:.0f}" y="{cy+26:.0f}" width="{w}" height="7" '
                 f'rx="3.5" fill="{PANEL}"/>')
        g.append(f'<rect x="{x:.0f}" y="{cy+26:.0f}" width="{w*act:.1f}" '
                 f'height="7" rx="3.5" fill="{col}" opacity=".85"/>')
        g.append(f'<text x="{cx}" y="{cy+50}" text-anchor="middle" '
                 f'font-family="ui-monospace,Menlo,monospace" font-size="14" '
                 f'fill="{MUTED}">{act:.2f}</text>')
    return "".join(g)


def link(a, b, *, col=None, dash=False, wide=False):
    (x1, y1), (x2, y2) = POS[a], POS[b]
    c = col or LINE
    d = ' stroke-dasharray="6 4"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" '
            f'stroke-width="{2.6 if wide else 1.7}"{d} opacity=".85"/>')


def teammate(cx, cy, who, what, kind):
    col = SOCIAL if kind == "explicit" else "#0e7490"
    tag = "explicit cue" if kind == "explicit" else "implicit cue"
    wdt = 250
    return (f'<rect x="{cx-wdt/2:.0f}" y="{cy-30:.0f}" width="{wdt}" '
            f'height="60" rx="10" fill="{SURFACE}" stroke="{col}" '
            f'stroke-width="2"/>'
            f'<text x="{cx-wdt/2+14:.0f}" y="{cy-10}" '
            f'font-family="system-ui,-apple-system,sans-serif" font-size="13" '
            f'font-weight="600" fill="{col}" letter-spacing=".06em">'
            f'{esc(who)} · {esc(tag.upper())}</text>'
            f'<text x="{cx-wdt/2+14:.0f}" y="{cy+14}" '
            f'font-family="system-ui,-apple-system,sans-serif" font-size="15" '
            f'fill="{INK}">{esc(what)}</text>')


def ranklist(rows, *, y0=150, title="ranked candidates", mark=None,
             unknown=False):
    g = [f'<text x="{PX0}" y="{y0-22}" font-family="system-ui,-apple-system,'
         f'sans-serif" font-size="17" font-weight="600" fill="{INK}">'
         f'{esc(title)}</text>']
    for i, (name, val) in enumerate(rows):
        y = y0 + i * 42
        hit = name == mark
        col = PATH if hit else BEAM
        if hit:
            g.append(f'<rect x="{PX0-10}" y="{y-4}" width="430" height="36" '
                     f'rx="7" fill="#e7f5ec"/>')
        g.append(f'<text x="{PX0}" y="{y+20}" font-family="system-ui,'
                 f'-apple-system,sans-serif" font-size="15" fill="{MUTED}">'
                 f'{i+1}</text>')
        g.append(f'<text x="{PX0+26}" y="{y+20}" font-family="ui-monospace,'
                 f'Menlo,monospace" font-size="16" fill="{INK}">'
                 f'{esc(name)}</text>')
        g.append(f'<rect x="{PX0+186}" y="{y+7}" width="180" height="14" '
                 f'rx="7" fill="{PANEL}"/>')
        g.append(f'<rect x="{PX0+186}" y="{y+7}" width="{180*val:.1f}" '
                 f'height="14" rx="7" fill="{col}" opacity=".85"/>')
        g.append(f'<text x="{PX0+378}" y="{y+20}" font-family="ui-monospace,'
                 f'Menlo,monospace" font-size="15" fill="{MUTED}">'
                 f'{val:.2f}</text>')
    if unknown:
        y = y0 + len(rows) * 42 + 16
        g.append(f'<rect x="{PX0-10}" y="{y}" width="430" height="46" rx="9" '
                 f'fill="#fdeceb" stroke="{ERROR}" stroke-width="1.8"/>')
        g.append(f'<text x="{PX0+8}" y="{y+29}" font-family="system-ui,'
                 f'-apple-system,sans-serif" font-size="16" font-weight="600" '
                 f'fill="{ERROR}">drawTri() is not in the graph → Unknown'
                 f'</text>')
    return "".join(g)


def callout(text, sub, y=470, col=PATH, bg="#e7f5ec"):
    return (f'<rect x="{PX0-10}" y="{y}" width="430" height="74" rx="10" '
            f'fill="{bg}" stroke="{col}" stroke-width="1.8"/>'
            f'<text x="{PX0+10}" y="{y+30}" font-family="system-ui,'
            f'-apple-system,sans-serif" font-size="17" font-weight="600" '
            f'fill="{col}">{esc(text)}</text>'
            f'<text x="{PX0+10}" y="{y+55}" font-family="system-ui,'
            f'-apple-system,sans-serif" font-size="15" fill="{INK}">'
            f'{esc(sub)}</text>')


def params(keys, y=560):
    """Small strip of the published defaults actually in play."""
    g = []
    for i, (sym, val) in enumerate(keys):
        x = PX0 + i * 104
        g.append(f'<text x="{x}" y="{y}" font-family="ui-monospace,Menlo,'
                 f'monospace" font-size="15" fill="{MUTED}">{esc(sym)} = '
                 f'{esc(val)}</text>')
    return "".join(g)


def note(lines, y=560, accent=INK):
    g = []
    for i, ln in enumerate(lines):
        g.append(f'<text x="{PX0}" y="{y + i*25}" font-family="system-ui,'
                 f'-apple-system,sans-serif" font-size="16" '
                 f'font-weight="{"600" if i == 0 else "400"}" '
                 f'fill="{accent if i == 0 else INK}">{esc(ln)}</text>')
    return "".join(g)


def frame(tag, n, total, caption, inner, sub=""):
    head = (f'<text x="{GX0}" y="52" font-family="system-ui,-apple-system,'
            f'sans-serif" font-size="15" font-weight="600" fill="{BEAM}" '
            f'letter-spacing="1.4">{esc(tag)} · STEP {n} OF {total}</text>'
            f'<text x="{GX0}" y="86" font-family="system-ui,-apple-system,'
            f'sans-serif" font-size="27" font-weight="600" fill="{INK}">'
            f'{esc(caption)}</text>')
    if sub:
        head += (f'<text x="{GX0}" y="112" font-family="system-ui,'
                 f'-apple-system,sans-serif" font-size="17" fill="{MUTED}">'
                 f'{esc(sub)}</text>')
    foot = (f'<text x="{GX0}" y="{H-22}" font-family="system-ui,-apple-system,'
            f'sans-serif" font-size="14" fill="{MUTED}">Model parameters are '
            f'the published defaults. Activations and cue strengths are '
            f'illustrative; gate values are computed.</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img" aria-label="{esc(caption)}">'
            f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>'
            f'{head}{inner}{foot}</svg>')


# --------------------------------------------------------------------------- #

def base_graph(*, acts=None, target_state="unreachable", social=False,
               social_wide=False):
    g = [link(a, b) for a, b in EDGES]
    if social:
        g.append(link("drawTri()", "layout()", col=SOCIAL, dash=True,
                      wide=social_wide))
        g.append(link("drawTri()", "fill()", col=SOCIAL, dash=True,
                      wide=social_wide))
    order = ["render()", "layout()", "paint()", "shape()", "fill()"]
    for nm in order:
        st = "seed" if nm == "render()" else ("active" if acts else "idle")
        g.append(patch(nm, act=(1.0 if nm == "render()" else acts.get(nm))
                       if acts else None, state=st))
    tact = None
    if acts and target_state in ("target", "won"):
        tact = A0["drawTri()"] if target_state == "target" else None
    g.append(patch("drawTri()", act=tact, state=target_state))
    return "".join(g)


def curve(x0, y0, w, h, *, marks=(), highlight=None):
    """P_soc as a function of social support S, over S in [0, 3]."""
    smax = 3.0
    pts = []
    for k in range(121):
        s = smax * k / 120
        pts.append(f"{x0 + w*s/smax:.1f},{y0 + h - h*p_soc(s):.1f}")
    g = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{PANEL}" '
         f'rx="6"/>']
    for frac in (0.25, .5, .75):
        yy = y0 + h - h * frac
        g.append(f'<line x1="{x0}" y1="{yy:.0f}" x2="{x0+w}" y2="{yy:.0f}" '
                 f'stroke="{SURFACE}" stroke-width="1.4"/>')
    fy = y0 + h - h * (RHO / TOP_N)
    g.append(f'<line x1="{x0}" y1="{fy:.1f}" x2="{x0+w}" y2="{fy:.1f}" '
             f'stroke="{ERROR}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    g.append(f'<polyline points="{" ".join(pts)}" fill="none" '
             f'stroke="{SOCIAL}" stroke-width="3"/>')
    for s, lbl in marks:
        px, py = x0 + w * s / smax, y0 + h - h * p_soc(s)
        on = highlight is not None and abs(highlight - s) < 1e-6
        g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{7 if on else 5}" '
                 f'fill="{PATH if on else SOCIAL}" stroke="{SURFACE}" '
                 f'stroke-width="2"/>')
        g.append(f'<text x="{px:.1f}" y="{py-15:.0f}" text-anchor="middle" '
                 f'font-family="system-ui,-apple-system,sans-serif" '
                 f'font-size="14" font-weight="600" '
                 f'fill="{PATH if on else INK}">{esc(lbl)}</text>')
    g.append(f'<text x="{x0+w/2}" y="{y0+h+28}" text-anchor="middle" '
             f'font-family="system-ui,-apple-system,sans-serif" '
             f'font-size="15" fill="{MUTED}">social support S(r)</text>')
    g.append(f'<text x="{x0-12}" y="{y0+12}" text-anchor="end" '
             f'font-family="system-ui,-apple-system,sans-serif" '
             f'font-size="14" fill="{MUTED}">1.0</text>')
    g.append(f'<text x="{x0-12}" y="{fy+5:.0f}" text-anchor="end" '
             f'font-family="system-ui,-apple-system,sans-serif" '
             f'font-size="14" fill="{ERROR}">ρ/N</text>')
    return "".join(g)


def build():
    f, says = [], []
    PA, PB = "PASS A · COVERAGE", "PASS B · THE GATE"
    baseline = sorted(((k, v) for k, v in A0.items() if k != "drawTri()"),
                      key=lambda kv: -kv[1])
    withtgt = sorted(A0.items(), key=lambda kv: -kv[1])
    final = list(gated().items())

    # A1
    f.append(frame(PA, 1, 10, "PFIS3: the programmer's own graph",
                   base_graph() +
                   note(["Patches are methods. Edges are structural",
                         "and lexical. drawTri() is dashed because",
                         "nothing in this graph reaches it."], y=180),
                   "Current patch render(), recent path behind it."))
    says.append("This is PFIS3, the individual model. The programmer is in "
                "render(). The graph holds the methods reachable from there "
                "by structure and by shared identifiers. drawTri() sits "
                "outside it.")

    # A2
    f.append(frame(PA, 2, 10, "Seed activation from the individual",
                   base_graph(acts={}) +
                   note(["A₀(mₜ) = 1", "The recent path is seeded by recency,",
                         "decayed by β."], y=180) +
                   params([("β", f"{BETA}")], y=290),
                   "Stage 1, using only what this programmer has done."))
    says.append("Activation starts at one on the current patch, and the "
                "programmer's recent path gets seeded by recency with the "
                "path decay beta.")

    # A3
    f.append(frame(PA, 3, 10, "Spread activation across the graph",
                   base_graph(acts=A0) +
                   note(["Activation decays by α at each hop.",
                         "drawTri() receives nothing. There is no",
                         "edge that reaches it."], y=180) +
                   params([("α", f"{ALPHA}")], y=290),
                   "Stage 2. Lexical and structural edges only."))
    says.append("Activation spreads outward, decaying by alpha at each hop. "
                "Every reachable patch picks up a score. drawTri() receives "
                "nothing, because no edge reaches it.")

    # A4
    f.append(frame(PA, 4, 10, "PFIS3 returns Unknown",
                   base_graph(acts=A0) +
                   ranklist(baseline, mark=None, unknown=True),
                   "The developer's actual next step was drawTri()."))
    says.append("So PFIS3 ranks the five patches it can see, and the step the "
                "developer actually took is not among them. The model scores "
                "this as Unknown. Across the ten teams that happened on a "
                "third of all steps.")

    # A5
    f.append(frame(PA, 5, 10, "Stage 0: teammates supply what the graph lacks",
                   base_graph(social=True, target_state="target") +
                   teammate(PX0 + 210, 190, "P2", "opened drawTri() 40s ago",
                            "implicit") +
                   teammate(PX0 + 210, 300, "P3", "“check drawTriangle”",
                            "explicit") +
                   note(["The graph is cloned, not modified.",
                         "These edges decay unless reinforced."], y=400),
                   "Implicit cues from navigation, explicit from conversation."))
    says.append("PFIS-T clones the graph and adds two kinds of cue. Implicit "
                "ones, the patches teammates opened recently. Explicit ones, "
                "identifiers they named in conversation. drawTri() is now "
                "attached to the graph by temporary edges.")

    # A6
    f.append(frame(PA, 6, 10, "Stage 1: seed the social cues too",
                   base_graph(acts={}, social=True, target_state="target") +
                   note(["Explicit cues seed higher than implicit.",
                         "Naming something is more intentional",
                         "than passing through it."], y=180) +
                   params([("Sₑ", f"{S_E}"), ("Sᵢ", f"{S_I}")], y=290),
                   "Explicit 0.25, implicit 0.10."))
    says.append("Both cue types get seeded, but not equally. An explicit "
                "mention seeds at nought point two five, an implicit visit at "
                "nought point one. Saying a method's name is more "
                "intentional than passing through it.")

    # A7
    f.append(frame(PA, 7, 10, "Stage 2: drawTri() finally receives activation",
                   base_graph(acts=A0, social=True, target_state="target") +
                   ranklist(withtgt, mark="drawTri()"),
                   "Reachable now, but still last of five."))
    says.append("Now activation reaches it. drawTri() is in the candidate "
                "set for the first time, but it is still ranked last. "
                "Reachability alone does not get it predicted.")

    # A8
    rows = [(r, social_support(r)) for r, _ in withtgt]
    f.append(frame(PA, 8, 10, "Stage 3: compute social support",
                   base_graph(acts=A0, social=True, target_state="target") +
                   ranklist([(r, s / 2) for r, s in rows],
                            title="social support S(r) = wₑE(r) + wᵢI(r)",
                            mark="drawTri()") +
                   params([("wₑ", f"{W_E:.0f}"), ("wᵢ", f"{W_I:.0f}"),
                           ("N", f"{TOP_N}")], y=560),
                   "Only the top-N candidates are gated."))
    says.append("For the top five candidates we compute social support, the "
                "weighted sum of explicit and implicit cue strength. "
                "drawTri() was both opened and named, so it scores two. "
                "Everything else is near zero.")

    # A9
    f.append(frame(PA, 9, 10, "Stage 3: reweight through the social gate",
                   base_graph(acts=A0, social=True, social_wide=True,
                              target_state="target") +
                   ranklist([(r, p_soc(social_support(r))) for r, _ in rows],
                            title="gate factor P_soc(r)", mark="drawTri()") +
                   callout("Re-ranking, not rescoring",
                           "Similar support scales similarly, so order is kept.",
                           y=392, col=BEAM, bg="#e8f0fe") +
                   params([("κ", f"{KAPPA}"), ("ρ", f"{RHO}")], y=560),
                   "A(r) = A₀(r) · P_soc(r)"))
    says.append("Support becomes a weighting factor through a saturating "
                "function, and each activation is multiplied by it. Note "
                "this only re-ranks the shortlist. Candidates with similar "
                "support are scaled almost identically, so their order "
                "among themselves barely moves. What changes is that a "
                "strongly cued candidate climbs past them.")

    # A10
    f.append(frame(PA, 10, 10, "A step the individual model could not predict",
                   base_graph(acts=A0, social=True, social_wide=True,
                              target_state="won") +
                   ranklist(final, title="PFIS-T ranked output",
                            mark="drawTri()", y0=140) +
                   callout("Unknown → predicted",
                           "Unknowns fell from 33.63% to 21.06% across ten teams.",
                           y=392),
                   "Where it ranks matters less than that it is on the list."))
    says.append("And it is predicted. Where exactly it ranks matters less "
                "than the fact that it appears at all, because PFIS3 could "
                "not produce this step under any ranking. That is the "
                "coverage gain, and across the ten teams it moved unknowns "
                "from a third of all steps to a fifth. How far a cued "
                "candidate climbs depends on the team: some are signal-rich, "
                "some are signal-sparse.")

    # ---- Pass B -------------------------------------------------------
    f.append(frame(PB, 1, 4, "Support is the weighted sum of two cue types",
                   f'<text x="{GX0}" y="200" font-family="ui-monospace,Menlo,'
                   f'monospace" font-size="26" fill="{INK}">S(r) = wₑ·E(r) '
                   f'+ wᵢ·I(r)</text>' +
                   note(["E(r) is the normalised strength of direct mentions.",
                         "Sparse, but high impact.",
                         "",
                         "I(r) is the strength from teammates' recent",
                         "navigation. Broader coverage, weaker per event."],
                        y=270) +
                   params([("wₑ", f"{W_E:.0f}"), ("wᵢ", f"{W_I:.0f}")],
                          y=470),
                   "Both weights default to 1, so neither type dominates."))
    says.append("The gate takes one input, social support, which is just the "
                "weighted sum of the two cue strengths. Both weights default "
                "to one, so neither kind of evidence dominates by "
                "construction.")

    marks = [(0.0, "no support"), (1.0, "one signal"), (2.0, "two signals"),
             (3.0, "three")]
    f.append(frame(PB, 2, 4, "Support becomes a weight through a saturating curve",
                   curve(GX0 + 60, 180, 640, 300, marks=marks) +
                   f'<text x="{PX0}" y="200" font-family="ui-monospace,Menlo,'
                   f'monospace" font-size="17" fill="{INK}">'
                   f'P_soc = (1−ρ)(1−e^−κS) + ρ/N</text>' +
                   params([("κ", f"{KAPPA}"), ("ρ", f"{RHO}"),
                           ("N", f"{TOP_N}")], y=240),
                   "Consensus selectivity κ sets how fast it rises."))
    says.append("That support is converted into a multiplier by this curve. "
                "It rises quickly at first and then flattens. Kappa controls "
                "how fast.")

    d1 = p_soc(1) - p_soc(0)
    d2 = p_soc(2) - p_soc(1)
    d3 = p_soc(3) - p_soc(2)
    f.append(frame(PB, 3, 4, "Diminishing returns on extra agreement",
                   curve(GX0 + 60, 180, 640, 300, marks=marks, highlight=2.0) +
                   note(["first signal   +%.2f" % d1,
                         "second signal  +%.2f" % d2,
                         "third signal   +%.2f" % d3,
                         "",
                         "A third teammate agreeing adds little.",
                         "The team cannot drown out the individual."],
                        y=200),
                   "Why saturate: consensus should inform, not overwhelm."))
    says.append("The flattening is the point. The first teammate signal is "
                "worth a lot, the second much less, the third almost "
                "nothing. That keeps a chorus of agreement from simply "
                "overwriting what the individual was doing.")

    f.append(frame(PB, 4, 4, "The exploration floor keeps alternatives alive",
                   curve(GX0 + 60, 180, 640, 300, marks=[(0.0, "no support")],
                         highlight=0.0) +
                   note(["P_soc never reaches zero.",
                         "ρ/N = %.2f" % (RHO / TOP_N),
                         "",
                         "A candidate with no social support is",
                         "demoted, never deleted. If the team is",
                         "wrong, the right answer is still on the list."],
                        y=200, accent=ERROR),
                   "The dashed red line is the floor."))
    says.append("And the curve never reaches zero. A candidate with no social "
                "support at all keeps a small floor, so it is demoted rather "
                "than deleted. If the team is collectively wrong, the right "
                "answer is still somewhere on the list.")

    return f, says


PAGE = """<title>PFIS-T Social Gate</title>
<style>
  :root {{ color-scheme: light dark; --bg:#fbfbfc; --fg:#1a1d21; --dim:#6b7280;
    --edge:#e3e6ea; --card:#ffffff; --accent:#7c3aed; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
    --bg:#14161a; --fg:#e9ecef; --dim:#98a2ad; --edge:#282d34; --card:#1c1f24; }} }}
  :root[data-theme="dark"] {{ --bg:#14161a; --fg:#e9ecef; --dim:#98a2ad;
    --edge:#282d34; --card:#1c1f24; }}
  body {{ background:var(--bg); color:var(--fg); margin:0;
    font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
  main {{ max-width:1180px; margin:0 auto; padding:30px 22px 64px; }}
  header {{ display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;
    margin-bottom:18px; }}
  h1 {{ font-size:22px; margin:0; letter-spacing:-.012em; font-weight:650; }}
  .tag {{ font-size:12px; letter-spacing:.1em; text-transform:uppercase;
    color:var(--dim); border:1px solid var(--edge); padding:3px 9px;
    border-radius:20px; }}
  .stage {{ background:#fff; border:1px solid var(--edge); border-radius:13px;
    overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.05); }}
  .stage > div {{ display:none; }} .stage > div.on {{ display:block; }}
  .stage svg {{ display:block; width:100%; height:auto; }}
  .bar {{ display:flex; align-items:center; gap:12px; margin-top:16px;
    flex-wrap:wrap; }}
  button {{ font:inherit; font-size:15px; padding:9px 17px; border-radius:8px;
    border:1px solid var(--edge); background:var(--card); color:var(--fg);
    cursor:pointer; }}
  button:hover:not(:disabled) {{ border-color:var(--accent);
    color:var(--accent); }}
  button:disabled {{ opacity:.38; cursor:default; }}
  .count {{ color:var(--dim); font-variant-numeric:tabular-nums;
    min-width:74px; font-size:15px; }}
  .dots {{ display:flex; gap:6px; margin-left:auto; }}
  .dots b {{ width:10px; height:10px; border-radius:50%; background:var(--edge);
    cursor:pointer; display:block; }}
  .dots b.on {{ background:var(--accent); }}
  .dots b.pb {{ border-radius:2px; }}
  .say {{ margin-top:18px; padding:15px 17px; border-left:3px solid var(--accent);
    background:var(--card); border-radius:0 9px 9px 0; font-size:15.5px;
    min-height:70px; }}
  .say b {{ display:block; font-size:11.5px; letter-spacing:.1em;
    text-transform:uppercase; color:var(--dim); margin-bottom:6px;
    font-weight:600; }}
</style>
<main>
  <header><h1>PFIS-T: social cues and the gate</h1>
    <span class="tag">10 + 4 frames · defense</span></header>
  <div class="stage" id="stage">{frames}</div>
  <div class="bar">
    <button id="p">← Back</button><button id="n">Next →</button>
    <span class="count" id="c"></span><span class="dots" id="d"></span>
  </div>
  <div class="say"><b>What to say</b><span id="s"></span></div>
</main>
<script>
const SAY={says};
const st=document.getElementById('stage'), fr=[...st.children];
const c=document.getElementById('c'), d=document.getElementById('d'),
      s=document.getElementById('s'), pv=document.getElementById('p'),
      nx=document.getElementById('n');
let i=0;
SAY.forEach((_,k)=>{{const b=document.createElement('b');
  if(k>=10) b.className='pb'; b.onclick=()=>go(k); d.appendChild(b);}});
function go(k){{ i=Math.max(0,Math.min(fr.length-1,k));
  fr.forEach((f,j)=>f.classList.toggle('on',j===i));
  c.textContent=(i+1)+' / '+fr.length; s.textContent=SAY[i];
  pv.disabled=i===0; nx.disabled=i===fr.length-1;
  [...d.children].forEach((b,j)=>b.classList.toggle('on',j===i)); }}
pv.onclick=()=>go(i-1); nx.onclick=()=>go(i+1);
addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key===' ')go(i+1);
  if(e.key==='ArrowLeft')go(i-1);}});
go(0);
</script>"""


def main():
    frames, says = build()
    assert len(frames) == len(says) == 14, (len(frames), len(says))
    for i, svg in enumerate(frames, 1):
        tag = "A" if i <= 10 else "B"
        k = i if i <= 10 else i - 10
        (OUT / f"pfist-{tag}{k:02d}.svg").write_text(svg, encoding="utf-8")
    js = "[" + ",".join(
        '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
        for s in says) + "]"
    inline = "".join(
        f'<div{" class=\'on\'" if k == 0 else ""}>{svg}</div>'
        for k, svg in enumerate(frames))
    (OUT / "standalone.html").write_text(
        PAGE.format(frames=inline, says=js), encoding="utf-8")
    print(f"wrote 14 frames + standalone.html to {OUT}")
    print(f"  gate check: P_soc(0)={p_soc(0):.3f}  P_soc(2)={p_soc(2):.3f}")
    for r, v in gated().items():
        print(f"  {r:12} A0={A0[r]:.2f}  S={social_support(r):.1f}  "
              f"A={v:.3f}")


if __name__ == "__main__":
    main()
