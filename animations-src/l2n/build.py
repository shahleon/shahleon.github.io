#!/usr/bin/env python3
"""Generate the L2N Learn-Weights / Update-Weights animation.

Emits ten numbered SVG frames for PowerPoint, plus an index.html that steps
through them for rehearsal. One source of truth for both.

    python3 build.py

Every score and weight on screen is ILLUSTRATIVE. They are chosen so the
search-error beat lands where the algorithm says it should, not taken from any
experiment in the dissertation. The frames say so in the footer.
"""

import html
import pathlib

W, H = 1280, 720
OUT = pathlib.Path(__file__).parent

INK, MUTED, LINE = "#1a1d21", "#8b9199", "#d4d8dd"
BEAM, PATH, ERROR = "#1f6feb", "#17803d", "#c2401a"
PANEL, SURFACE = "#f4f5f7", "#ffffff"

QUERY = "split raw text into tokens"
ALPHA = 0.5
FEATURES = ["Code", "Comment", "Method", "File", "Path"]

W0 = [0.62, 0.31, 0.44, 0.55, 0.28]
W1 = [0.58, 0.24, 0.77, 0.31, 0.04]
F_TRUE = [0.52, 0.30, 0.91, 0.22, 0.18]      # f(token()), strong method match
F_BEAM = [0.61, 0.44, 0.25, 0.70, 0.66]      # mean f over the wrong beam

L1 = [("load()", .78), ("parse()", .71), ("init()", .64), ("run()", .41)]
L2_BEFORE = [("fetch()", .69), ("read()", .66), ("cache()", .62),
             ("token()", .58), ("split()", .44)]
L2_AFTER = [("token()", .74), ("fetch()", .67), ("read()", .61),
            ("cache()", .55), ("split()", .48)]
BEAM_W = 3
PARENT = {"fetch()": "load()", "read()": "load()", "cache()": "init()",
          "token()": "parse()", "split()": "init()"}
TRUE_PATH = ("main()", "parse()", "token()")

GX0, GX1 = 40, 792                            # graph panel
PX0 = 824                                     # side panel
ROW = {0: 168, 1: 312, 2: 456, 3: 600}


def esc(s):
    return html.escape(str(s), quote=False)


def centers(n, x0=GX0 + 24, x1=GX1 - 24):
    step = (x1 - x0) / n
    return [x0 + step * (i + .5) for i in range(n)]


def node(cx, cy, label, *, state="idle", score=None, ring=False, w=124):
    """state: idle | beam | dropped | true | error"""
    fill, stroke, txt, sw = SURFACE, LINE, INK, 1.6
    if state == "beam":
        fill, stroke, txt, sw = "#e8f0fe", BEAM, INK, 2.4
    elif state == "dropped":
        fill, stroke, txt = SURFACE, LINE, MUTED
    elif state == "true":
        fill, stroke, txt, sw = "#e7f5ec", PATH, INK, 2.4
    elif state == "error":
        fill, stroke, txt, sw = "#fdeceb", ERROR, INK, 2.8
    x, y, h = cx - w / 2, cy - 21, 42
    g = [f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="7" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    if ring:
        g.append(f'<rect x="{x-5:.1f}" y="{y-5}" width="{w+10}" height="{h+10}"'
                 f' rx="11" fill="none" stroke="{PATH}" stroke-width="2"'
                 ' stroke-dasharray="4 3"/>')
    g.append(f'<text x="{cx:.1f}" y="{cy+6}" text-anchor="middle" '
             f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" '
             f'font-size="19" fill="{txt}">{esc(label)}</text>')
    if score is not None:
        g.append(f'<text x="{cx:.1f}" y="{cy+37}" text-anchor="middle" '
                 f'font-family="ui-monospace,Menlo,monospace" font-size="16" '
                 f'fill="{MUTED}">{score:.2f}</text>')
    return "".join(g)


def edge(x1, y1, x2, y2, *, faded=False, on_path=False):
    c = PATH if on_path else (LINE if faded else MUTED)
    sw = 2.4 if on_path else 1.6
    return (f'<path d="M {x1:.1f} {y1+21} C {x1:.1f} {y1+60}, {x2:.1f} '
            f'{y2-60}, {x2:.1f} {y2-21}" fill="none" stroke="{c}" '
            f'stroke-width="{sw}"/>')


def cutline(xs, b, y, label="beam width b = 3"):
    """Vertical rule between the b-th and (b+1)-th ranked candidate."""
    x = (xs[b - 1] + xs[b]) / 2
    return (f'<line x1="{x:.1f}" y1="{y-46}" x2="{x:.1f}" y2="{y+28}" '
            f'stroke="{BEAM}" stroke-width="2" stroke-dasharray="7 5"/>'
            f'<text x="{x-10:.1f}" y="{y-56}" text-anchor="end" '
            f'font-family="system-ui,-apple-system,Segoe UI,sans-serif" '
            f'font-size="15" fill="{BEAM}">kept</text>'
            f'<text x="{x+10:.1f}" y="{y-56}" '
            f'font-family="system-ui,-apple-system,Segoe UI,sans-serif" '
            f'font-size="15" fill="{MUTED}">dropped</text>'
            f'<text x="{x:.1f}" y="{y+68}" text-anchor="middle" '
            f'font-family="system-ui,-apple-system,Segoe UI,sans-serif" '
            f'font-size="15" fill="{BEAM}">{esc(label)}</text>')


def bars(weights, prev=None, title="weight vector w"):
    """Five labelled bars. If prev is given, show the change."""
    g = [f'<text x="{PX0}" y="{ROW[0]-46}" '
         f'font-family="system-ui,-apple-system,sans-serif" font-size="17" '
         f'font-weight="600" fill="{INK}">{esc(title)}</text>']
    bx, bw = PX0 + 86, 268
    for i, (name, v) in enumerate(zip(FEATURES, weights)):
        y = ROW[0] - 22 + i * 40
        g.append(f'<text x="{PX0+74}" y="{y+14}" text-anchor="end" '
                 f'font-family="system-ui,-apple-system,sans-serif" '
                 f'font-size="16" fill="{INK}">{esc(name)}</text>')
        g.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="19" rx="3" '
                 f'fill="{PANEL}"/>')
        if prev is not None and abs(prev[i] - v) > .004:
            g.append(f'<rect x="{bx}" y="{y}" width="{bw*prev[i]:.1f}" '
                     f'height="19" rx="3" fill="none" stroke="{MUTED}" '
                     'stroke-width="1.4" stroke-dasharray="3 2"/>')
        up = prev is not None and v > prev[i]
        col = PATH if up else (ERROR if prev is not None and v < prev[i]
                               else BEAM)
        g.append(f'<rect x="{bx}" y="{y}" width="{bw*v:.1f}" height="19" '
                 f'rx="3" fill="{col}" opacity="0.85"/>')
        g.append(f'<text x="{bx+bw+12}" y="{y+14}" '
                 f'font-family="ui-monospace,Menlo,monospace" font-size="15" '
                 f'fill="{MUTED}">{v:.2f}</text>')
    return "".join(g)


def note(lines, y=ROW[2] + 20, accent=INK):
    g = []
    for i, ln in enumerate(lines):
        weight = "600" if i == 0 else "400"
        col = accent if i == 0 else INK
        g.append(f'<text x="{PX0}" y="{y + i*26}" '
                 f'font-family="system-ui,-apple-system,sans-serif" '
                 f'font-size="16" font-weight="{weight}" fill="{col}">'
                 f'{esc(ln)}</text>')
    return "".join(g)


def frame(n, caption, inner, sub=""):
    head = (
        f'<text x="{GX0}" y="52" font-family="system-ui,-apple-system,'
        f'sans-serif" font-size="15" font-weight="600" fill="{BEAM}" '
        f'letter-spacing="1.4">STEP {n} OF 10</text>'
        f'<text x="{GX0}" y="86" font-family="system-ui,-apple-system,'
        f'sans-serif" font-size="27" font-weight="600" fill="{INK}">'
        f'{esc(caption)}</text>')
    if sub:
        head += (f'<text x="{GX0}" y="112" font-family="system-ui,'
                 f'-apple-system,sans-serif" font-size="17" fill="{MUTED}">'
                 f'{esc(sub)}</text>')
    q = (f'<rect x="{PX0}" y="34" width="416" height="40" rx="20" '
         f'fill="{PANEL}"/>'
         f'<text x="{PX0+22}" y="60" font-family="system-ui,-apple-system,'
         f'sans-serif" font-size="17" fill="{INK}">query: '
         f'“{esc(QUERY)}”</text>')
    foot = (f'<text x="{GX0}" y="{H-22}" font-family="system-ui,'
            f'-apple-system,sans-serif" font-size="14" fill="{MUTED}">'
            f'Illustrative values. Beam width 3 shown for legibility; '
            f'experiments used 5.</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img" '
            f'aria-label="{esc(caption)}">'
            f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>'
            f'{head}{q}{inner}{foot}</svg>')


# --------------------------------------------------------------------------- #
# the ten beats
# --------------------------------------------------------------------------- #

def build_frames():
    f = []
    c1, c2 = centers(len(L1)), centers(len(L2_BEFORE))
    root = (GX0 + GX1) / 2
    L1_SORTED = sorted(L1, key=lambda t: -t[1])
    kept1 = c1[:BEAM_W]

    def upper(settled=False, scores=False):
        """Levels 0 and 1. Once settled, they stay as context for later beats."""
        g = []
        src = L1_SORTED if settled else L1
        for i, x in enumerate(c1):
            lbl_i = (L1_SORTED if settled else L1)[i][0]
            g.append(edge(root, ROW[0], x, ROW[1],
                          faded=settled and i >= BEAM_W,
                          on_path=lbl_i == "parse()"))
        g.append(node(root, ROW[0], "main()", state="beam"))
        for i, (x, (lbl, sc)) in enumerate(zip(c1, src)):
            if settled:
                st = ("true" if lbl == "parse()" else
                      ("beam" if i < BEAM_W else "dropped"))
            else:
                st = "idle"
            g.append(node(x, ROW[1], lbl, state=st,
                          score=sc if scores else None,
                          ring=(lbl == "parse()")))
        return "".join(g)

    def lower(scores, *, show_scores=True, only_true=False):
        """Level 2, fanned out from the surviving beam."""
        g = []
        pos1 = {lbl: c1[k] for k, (lbl, _) in enumerate(L1_SORTED)}
        for i, (x2, (lbl2, _)) in enumerate(zip(c2, scores)):
            g.append(edge(pos1[PARENT[lbl2]], ROW[1], x2, ROW[2],
                          faded=only_true and lbl2 != "token()",
                          on_path=lbl2 == "token()"))
        for i, (x, (lbl, sc)) in enumerate(zip(c2, scores)):
            if only_true:
                st = "true" if lbl == "token()" else "dropped"
            elif lbl == "token()":
                st = "true" if i < BEAM_W else "error"
            else:
                st = "beam" if i < BEAM_W else "dropped"
            g.append(node(x, ROW[2], lbl, state=st,
                          score=sc if show_scores else None,
                          ring=(lbl == "token()")))
        return "".join(g)

    # 1 ------------------------------------------------------------------
    f.append(frame(
        1, "Start: one node in the beam",
        node(root, ROW[0], "main()", state="beam") + bars(W0) +
        note(["H(n) = w\u1d40 \u00b7 f(n)",
              "Weights start random in [0,1]\u2075.",
              "The beam holds only the entry point."]),
        "Update-Weights walks one training pair down the graph."))

    # 2 ------------------------------------------------------------------
    f.append(frame(
        2, "BreadthExpand: every successor becomes a candidate",
        upper() + bars(W0) +
        note(["C \u2190 BreadthExpand(B)",
              "Dashed green marks the node on the",
              "training path. The search cannot see it."]),
        "C is everything reachable in one step from the beam."))

    # 3 ------------------------------------------------------------------
    f.append(frame(
        3, "Score every candidate with the current weights",
        upper(scores=True) + bars(W0) +
        note(["H(parse()) = w\u1d40 \u00b7 f(parse())",
              "  = .62(.55) + .31(.40) + .44(.62)",
              "    + .55(.71) + .28(.55)  =  0.71"]),
        "One dot product per candidate. Five features, five weights."))

    # 4 ------------------------------------------------------------------
    f.append(frame(
        4, "Sort, keep the top b. The path survives",
        upper(settled=True, scores=True) + cutline(c1, BEAM_W, ROW[1]) +
        bars(W0) +
        note(["B \u2229 P\u1d62,\u2c7c \u2260 \u2205",
              "parse() is inside the beam.",
              "No correction fires. Move to the next level."], accent=PATH),
        "Update-Weights only acts when the beam loses the path entirely."))

    # 5 ------------------------------------------------------------------
    f.append(frame(
        5, "Expand again from the surviving beam",
        upper(settled=True) + lower(L2_BEFORE, show_scores=False) + bars(W0) +
        note(["Next level, same procedure.",
              "token() is the node on the training",
              "path this time."], y=ROW[2] + 92),
        "Each level repeats: expand, score, sort, cut."))

    # 6 ------------------------------------------------------------------
    f.append(frame(
        6, "The beam drops the path. This is the search error",
        upper(settled=True) + lower(L2_BEFORE) +
        cutline(c2, BEAM_W, ROW[2]) + bars(W0) +
        note(["B \u2229 P\u1d62,\u2c7c = \u2205",
              "token() ranks fourth and falls below",
              "the cut. The search is now wrong and",
              "has no way to notice."], y=ROW[2] + 92, accent=ERROR),
        "The weights over-trust file path and under-trust method name."))

    # 7 ------------------------------------------------------------------
    def vecrow(y, label, vec, col, signed=False):
        gg = [f'<text x="{PX0}" y="{y}" font-family="system-ui,-apple-system,'
              f'sans-serif" font-size="16" font-weight="600" fill="{col}">'
              f'{esc(label)}</text>']
        for i, v in enumerate(vec):
            txt = f"{v:+.2f}" if signed else f"{v:.2f}"
            gg.append(f'<text x="{PX0+140+i*60}" y="{y}" text-anchor="middle" '
                      f'font-family="ui-monospace,Menlo,monospace" '
                      f'font-size="16" fill="{INK}">{txt}</text>')
        return "".join(gg)

    delta = [a - b for a, b in zip(F_TRUE, F_BEAM)]
    hdr = "".join(
        f'<text x="{PX0+140+i*60}" y="{ROW[0]-44}" text-anchor="middle" '
        f'font-family="system-ui,-apple-system,sans-serif" font-size="14" '
        f'fill="{MUTED}">{esc(n)}</text>' for i, n in enumerate(FEATURES))
    f.append(frame(
        7, "Compare what the beam kept against what it dropped",
        upper(settled=True) + lower(L2_BEFORE) +
        cutline(c2, BEAM_W, ROW[2]) + hdr +
        vecrow(ROW[0] - 14, "h\u1d04\u1d18  path", F_TRUE, PATH) +
        vecrow(ROW[0] + 24, "h\u0299  beam", F_BEAM, BEAM) +
        f'<line x1="{PX0}" y1="{ROW[0]+40}" x2="{PX0+424}" y2="{ROW[0]+40}" '
        f'stroke="{LINE}" stroke-width="1.4"/>' +
        vecrow(ROW[0] + 66, "\u0394  difference", delta, INK, signed=True) +
        note(["Mean feature vector of the beam, against",
              "the mean of the path nodes it dropped.",
              "Method name is where they diverge."], y=ROW[1] + 66),
        "Two averages: the nodes kept, and the nodes that should have been."))

    # 8 ------------------------------------------------------------------
    f.append(frame(
        8, "Perceptron update: move w toward the path",
        upper(settled=True) + lower(L2_BEFORE) +
        cutline(c2, BEAM_W, ROW[2]) + bars(W1, prev=W0) +
        note(["w \u2190 w + \u03b1 (h\u1d04\u1d18 \u2212 h\u0299),"
              "  \u03b1 = 0.5",
              "Method name rises. File and path fall.",
              "Dashed outline marks the old value."], y=ROW[2] + 92),
        "The heuristic learns which signals keep the path inside the beam."))

    # 9 ------------------------------------------------------------------
    f.append(frame(
        9, "Reset the beam onto the path, then continue",
        upper(settled=True) + lower(L2_BEFORE, show_scores=False,
                                    only_true=True) + bars(W1, prev=W0) +
        note(["B \u2190 C \u2229 P\u1d62,\u2c7c",
              "Search resumes from the true node, so",
              "later levels still train on a path that",
              "is actually reachable."], y=ROW[2] + 92),
        "Without the reset, every later level would train from a lost beam."))

    # 10 -----------------------------------------------------------------
    f.append(frame(
        10, "Same level, new weights. The path is kept",
        upper(settled=True) + lower(L2_AFTER) +
        cutline(c2, BEAM_W, ROW[2]) + bars(W1, prev=W0) +
        note(["token() now ranks first.",
              "Nothing about the graph or the query",
              "changed. Only the weights did.",
              "This is what Learn-Weights accumulates."],
             y=ROW[2] + 92, accent=PATH),
        "Learn-Weights repeats this over every pair until w settles."))
    return f


PAGE = """<title>L2N Weight Learning</title>
<style>
  :root {{ color-scheme: light dark;
    --bg:#fbfbfc; --fg:#1a1d21; --dim:#6b7280; --edge:#e3e6ea; --card:#fff; }}
  :root:not([data-theme="light"]) {{ @media (prefers-color-scheme: dark) {{
    --bg:#15171a; --fg:#e9ecef; --dim:#9aa3ad; --edge:#2a2e34; --card:#1d2024; }} }}
  :root[data-theme="dark"] {{ --bg:#15171a; --fg:#e9ecef; --dim:#9aa3ad;
    --edge:#2a2e34; --card:#1d2024; }}
  body {{ background:var(--bg); color:var(--fg); margin:0;
    font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }}
  main {{ max-width:1120px; margin:0 auto; padding:28px 20px 60px; }}
  h1 {{ font-size:21px; margin:0 0 4px; letter-spacing:-.01em; }}
  p.sub {{ margin:0 0 20px; color:var(--dim); font-size:15px; }}
  .stage {{ background:var(--card); border:1px solid var(--edge);
    border-radius:12px; overflow:hidden; }}
  .stage img {{ display:block; width:100%; height:auto; }}
  .bar {{ display:flex; align-items:center; gap:14px; margin-top:16px;
    flex-wrap:wrap; }}
  button {{ font:inherit; font-size:15px; padding:9px 18px; border-radius:8px;
    border:1px solid var(--edge); background:var(--card); color:var(--fg);
    cursor:pointer; }}
  button:hover {{ border-color:#1f6feb; }}
  button:disabled {{ opacity:.4; cursor:default; border-color:var(--edge); }}
  .count {{ color:var(--dim); font-variant-numeric:tabular-nums;
    min-width:96px; }}
  .dots {{ display:flex; gap:6px; margin-left:auto; }}
  .dots b {{ width:9px; height:9px; border-radius:50%;
    background:var(--edge); cursor:pointer; display:block; }}
  .dots b.on {{ background:#1f6feb; }}
  .say {{ margin-top:18px; padding:14px 16px; border-left:3px solid #1f6feb;
    background:var(--card); border-radius:0 8px 8px 0; font-size:15px; }}
  .say b {{ display:block; font-size:12px; letter-spacing:.09em;
    text-transform:uppercase; color:var(--dim); margin-bottom:5px; }}
</style>
<main>
  <h1>Learn-Weights and Update-Weights</h1>
  <p class="sub">Arrow keys or the buttons. Ten frames, each exported as
     <code>frame-NN.svg</code> for the slide deck.</p>
  <div class="stage"><img id="f" alt=""></div>
  <div class="bar">
    <button id="p">← Back</button>
    <button id="n">Next →</button>
    <span class="count" id="c"></span>
    <span class="dots" id="d"></span>
  </div>
  <div class="say"><b>What to say</b><span id="s"></span></div>
</main>
<script>
const SAY = {says};
let i = 0;
const img=document.getElementById('f'), cnt=document.getElementById('c'),
      dots=document.getElementById('d'), say=document.getElementById('s'),
      pv=document.getElementById('p'), nx=document.getElementById('n');
SAY.forEach((_,k)=>{{ const b=document.createElement('b');
  b.onclick=()=>go(k); dots.appendChild(b); }});
function go(k){{ i=Math.max(0,Math.min(SAY.length-1,k));
  img.src=`frame-${{String(i+1).padStart(2,'0')}}.svg`;
  img.alt=SAY[i]; cnt.textContent=`${{i+1}} / ${{SAY.length}}`;
  say.textContent=SAY[i]; pv.disabled=i===0; nx.disabled=i===SAY.length-1;
  [...dots.children].forEach((b,k2)=>b.classList.toggle('on',k2===i)); }}
pv.onclick=()=>go(i-1); nx.onclick=()=>go(i+1);
addEventListener('keydown',e=>{{ if(e.key==='ArrowRight')go(i+1);
  if(e.key==='ArrowLeft')go(i-1); }});
go(0);
</script>"""


STANDALONE = """<title>L2N Weight Learning</title>
<style>
  :root {{ color-scheme: light dark; --bg:#fbfbfc; --fg:#1a1d21; --dim:#6b7280;
    --edge:#e3e6ea; --card:#ffffff; --accent:#1f6feb; }}
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
  .dots {{ display:flex; gap:7px; margin-left:auto; }}
  .dots b {{ width:10px; height:10px; border-radius:50%; background:var(--edge);
    cursor:pointer; display:block; border:0; padding:0; }}
  .dots b.on {{ background:var(--accent); }}
  .say {{ margin-top:18px; padding:15px 17px; border-left:3px solid var(--accent);
    background:var(--card); border-radius:0 9px 9px 0; font-size:15.5px;
    min-height:66px; }}
  .say b {{ display:block; font-size:11.5px; letter-spacing:.1em;
    text-transform:uppercase; color:var(--dim); margin-bottom:6px;
    font-weight:600; }}
</style>
<main>
  <header>
    <h1>Learn-Weights and Update-Weights</h1>
    <span class="tag">L2N · defense</span>
  </header>
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
  b.onclick=()=>go(k); d.appendChild(b);}});
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

SAYS = [
    "Update-Weights takes one training pair, a query and the path it should "
    "have followed, and walks it down the graph. The beam starts with a "
    "single node and the weights start random.",
    "Expanding gives us the candidate set C. The dashed green ring marks the "
    "node that lies on the training path. The search itself cannot see that "
    "ring, it is only there for us.",
    "Each candidate gets one dot product. Five features, five weights, one "
    "number. That number is the whole heuristic.",
    "Sorted and cut at the beam width. Here parse() survives, so the beam "
    "still contains the path and nothing is corrected. The algorithm only "
    "acts on failure.",
    "Next level down. Same procedure, and now token() is the node we need "
    "to keep.",
    "And here it fails. token() ranks fourth and falls below the cut. The "
    "beam has lost the path completely, which is the condition that triggers "
    "the update.",
    "To correct it, we compare two averages. The mean feature vector of what "
    "the beam kept, against the mean of the path nodes it dropped. They "
    "diverge almost entirely on method name.",
    "The update is a perceptron step toward that difference. Method name "
    "rises, file and path fall. The heuristic just learned that in this "
    "repository, method names carry the signal.",
    "The beam resets onto the true node so the remaining levels still train "
    "against a reachable path. Without that, everything downstream would "
    "train from a search that is already lost.",
    "Same level, same query, same graph. Only the weights changed, and now "
    "token() ranks first. Learn-Weights repeats this across every training "
    "pair until the weights stop moving.",
]


def main():
    frames = build_frames()
    assert len(frames) == len(SAYS) == 10, (len(frames), len(SAYS))
    for i, svg in enumerate(frames, 1):
        p = OUT / f"frame-{i:02d}.svg"
        p.write_text(svg, encoding="utf-8")
    says = "[" + ",".join(
        '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
        for s in SAYS) + "]"
    (OUT / "index.html").write_text(PAGE.format(says=says), encoding="utf-8")
    inline = "".join(
        f'<div{" class=\'on\'" if k == 0 else ""}>{svg}</div>'
        for k, svg in enumerate(frames))
    (OUT / "standalone.html").write_text(
        STANDALONE.format(frames=inline, says=says), encoding="utf-8")
    print(f"wrote 10 frames, index.html, standalone.html to {OUT}")


if __name__ == "__main__":
    main()
