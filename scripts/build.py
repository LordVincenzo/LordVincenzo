#!/usr/bin/env python3
"""Genera las imágenes SVG del perfil. Solo usa la librería estándar.

  python scripts/build.py            -> regenera todo; la actividad se consulta a GitHub
                                        si existe GITHUB_TOKEN, y si no queda "sincronizando".
"""
import datetime as dt, html, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
USER = "LordVincenzo"
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
BG0, BG1, PANEL, LINE = "#080d1c", "#101936", "#0c1430", "#22305a"
TXT, MUTED, DIM = "#f2f5ff", "#9aa7c7", "#5b6a92"
TEAL, BLUE, AMBER, VIOLET = "#5eead4", "#60a5fa", "#fbbf24", "#a78bfa"
e = html.escape
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def frame(W, H, rx=22, glow=TEAL, gx=.85, gy=.1, dots=True):
    d = (f'<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#7f93c9" fill-opacity=".22"/></pattern>'
         f'<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset=".8" stop-color="#fff"/></linearGradient>'
         f'<mask id="mk"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>') if dots else ""
    defs = (f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>'
            f'<radialGradient id="glow" cx="{gx}" cy="{gy}" r=".75"><stop offset="0" stop-color="{glow}" stop-opacity=".17"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{rx}"/></clipPath>{d}')
    body = (f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
            + (f'<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#mk)"/>' if dots else "")
            + f'<rect width="{W}" height="{H}" fill="url(#glow)"/></g>'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{rx}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    return defs, body


def svg(W, H, label, defs, style, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(label)}">'
            f'<defs>{defs}</defs><style>{style}{REDUCE}</style>{body}</svg>')


def kicker(x, y, text, color=TEAL):
    return (f'<path d="M{x} {y-5} l7 -7 l7 7 l-7 7 Z" fill="{color}"/>'
            f'<text x="{x+24}" y="{y}" font-family="{MONO}" font-size="14" letter-spacing="4" fill="{color}">{e(text)}</text>')


def chips(items, x, y, maxw, color, size=13, h=26, gap=8):
    out, cx, cy = [], x, y
    for t in items:
        w = int(len(t) * size * 0.60) + 24
        if cx + w > x + maxw:
            cx, cy = x, cy + h + gap
        out.append(f'<rect x="{cx}" y="{cy}" width="{w}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".35"/>'
                   f'<text x="{cx+w/2}" y="{cy+h/2+size*.35}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{color}">{e(t)}</text>')
        cx += w + gap
    return "".join(out)


# ───────────────────────────── cabecera ─────────────────────────────
def header():
    W, H = 1200, 420
    defs, bg = frame(W, H, 24, TEAL, .8, .45)
    defs += f'<linearGradient id="name" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset=".5" stop-color="#d7fff8"><animate attributeName="offset" values="-.2;1.2;1.2" keyTimes="0;.45;1" dur="5s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
    defs += f'<radialGradient id="orb"><stop offset="0" stop-color="{BLUE}" stop-opacity=".16"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
    N = [(730, 214, "inicio", TEAL, '<path d="M-6 -9 L9 0 L-6 9 Z"/>'),
         (860, 138, "datos", BLUE, '<ellipse cx="0" cy="-7" rx="10" ry="4"/><path d="M-10 -7 V7 C-10 12 10 12 10 7 V-7"/><path d="M-10 0 C-10 5 10 5 10 0"/>'),
         (860, 290, "código", VIOLET, '<path d="M-5 -9 C-10 -9 -6 -1 -11 0 C-6 1 -10 9 -5 9"/><path d="M5 -9 C10 -9 6 -1 11 0 C6 1 10 9 5 9"/>'),
         (1000, 214, "proceso", AMBER, '<circle r="4"/><path d="M0 -11 V-8 M0 8 V11 M-11 0 H-8 M8 0 H11 M-7.8 -7.8 L-5.7 -5.7 M5.7 5.7 L7.8 7.8 M-7.8 7.8 L-5.7 5.7 M5.7 -5.7 L7.8 -7.8"/>'),
         (1120, 214, "listo", TEAL, '<path d="M-9 0 L-3 7 L10 -7"/>')]
    P = ["M760 206 C805 206 800 138 830 138", "M760 222 C805 222 800 290 830 290",
         "M890 138 C940 138 930 206 970 206", "M890 290 C940 290 930 222 970 222", "M1030 214 H1090"]
    wires = "".join(f'<path d="{p}" class="w"/>' for p in P)
    pulses = "".join(f'<circle r="4" fill="{TEAL}"><animateMotion dur="{d}s" begin="-{b}s" repeatCount="indefinite" path="{p}"/></circle>'
                     for p, d, b in zip(P, (2.6, 2.6, 2.6, 2.6, 1.6), (0, .5, 1.3, 1.8, .4)))
    nodes = "".join(
        f'<g class="n n{i}"><rect x="{x-30}" y="{y-30}" width="60" height="60" rx="16" fill="{PANEL}" stroke="{c}" stroke-opacity=".75" stroke-width="1.5"/>'
        f'<g transform="translate({x},{y}) scale(1.1)" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{g}</g></g>'
        f'<text x="{x}" y="{y+50}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{DIM}">{lab}</text>'
        for i, (x, y, lab, c, g) in enumerate(N))
    # frases que se escriben solas
    frases = ["Automatizo lo repetitivo.", "Construyo apps web y móviles.", "Convierto datos en decisiones."]
    typed = ""
    for i, f in enumerate(frases):
        w = round(len(f) * 10.8)
        a = i / 3
        kt = f"0;{a:.3f};{a+.11:.3f};{a+.27:.3f};{a+.325:.3f};1"
        typed += (f'<clipPath id="t{i}"><rect x="72" y="296" height="30" width="0"><animate attributeName="width" dur="10.5s" repeatCount="indefinite" values="0;0;{w+2};{w+2};0;0" keyTimes="{kt}"/></rect></clipPath>'
                  f'<text x="72" y="318" clip-path="url(#t{i})" font-family="{MONO}" font-size="18" fill="{TXT}" textLength="{w}" lengthAdjust="spacingAndGlyphs">{e(f)}</text>'
                  f'<rect y="300" width="9" height="22" fill="{TEAL}" opacity="0"><animate attributeName="x" dur="10.5s" repeatCount="indefinite" values="74;74;{w+78};{w+78};74;74" keyTimes="{kt}"/>'
                  f'<animate attributeName="opacity" dur="10.5s" repeatCount="indefinite" values="0;1;1;1;0;0" keyTimes="0;{max(a,.001):.3f};{a+.11:.3f};{a+.325:.3f};{a+.33:.3f};1" calcMode="discrete"/></rect>')
    style = (f".w{{fill:none;stroke:{TEAL};stroke-opacity:.5;stroke-width:1.6;stroke-dasharray:5 7;animation:flow 1.4s linear infinite}}"
             "@keyframes flow{to{stroke-dashoffset:-24}}"
             ".n{animation:pop 5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
             ".n1{animation-delay:.6s}.n2{animation-delay:1.1s}.n3{animation-delay:2s}.n4{animation-delay:2.9s}"
             "@keyframes pop{0%,12%,100%{transform:scale(1)}6%{transform:scale(1.1)}}"
             ".live{animation:live 2.2s ease-in-out infinite}@keyframes live{50%{opacity:.3}}"
             ".orb{animation:orb 9s ease-in-out infinite alternate}@keyframes orb{to{transform:translate(-60px,24px)}}"
             ".tw{opacity:.1;animation:tw 4s ease-in-out infinite}@keyframes tw{50%{opacity:.85}}")
    body = f'''{bg}
<g clip-path="url(#clip)"><circle class="orb" cx="1010" cy="70" r="230" fill="url(#orb)"/></g>
<circle class="tw" style="animation-delay:0.0s" cx="310" cy="96" r="1.6" fill="#cfe9ff"/><circle class="tw" style="animation-delay:0.7s" cx="520" cy="70" r="1.2" fill="#cfe9ff"/><circle class="tw" style="animation-delay:1.4s" cx="640" cy="150" r="1.8" fill="#cfe9ff"/><circle class="tw" style="animation-delay:2.1s" cx="585" cy="300" r="1.3" fill="#cfe9ff"/><circle class="tw" style="animation-delay:2.8s" cx="430" cy="345" r="1.5" fill="#cfe9ff"/><circle class="tw" style="animation-delay:3.5s" cx="250" cy="300" r="1.1" fill="#cfe9ff"/><circle class="tw" style="animation-delay:0.2s" cx="668" cy="52" r="1.4" fill="#cfe9ff"/><circle class="tw" style="animation-delay:0.9s" cx="700" cy="330" r="1.6" fill="#cfe9ff"/><circle class="tw" style="animation-delay:1.6s" cx="1160" cy="120" r="1.3" fill="#cfe9ff"/><circle class="tw" style="animation-delay:2.3s" cx="940" cy="340" r="1.5" fill="#cfe9ff"/><circle class="tw" style="animation-delay:3.0s" cx="1080" cy="96" r="1.1" fill="#cfe9ff"/><circle class="tw" style="animation-delay:3.7s" cx="800" cy="70" r="1.6" fill="#cfe9ff"/><circle cx="46" cy="46" r="6" fill="{TEAL}"/><circle cx="68" cy="46" r="6" fill="{BLUE}" fill-opacity=".8"/><circle cx="90" cy="46" r="6" fill="{VIOLET}" fill-opacity=".7"/>
<text x="118" y="51" font-family="{MONO}" font-size="15" fill="{MUTED}">briand@dev<tspan fill="{DIM}">:</tspan><tspan fill="{BLUE}">~/workspace</tspan> <tspan fill="{DIM}">(main)</tspan></text>
<g transform="translate(1158,46)"><rect x="-196" y="-18" width="196" height="36" rx="18" fill="{PANEL}" stroke="{LINE}"/>
<circle class="live" cx="-174" cy="0" r="4.5" fill="{TEAL}"/><text x="-160" y="5" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{TXT}">Soledad, Colombia</text></g>
<text x="46" y="134" font-family="{MONO}" font-size="14" letter-spacing="4.5" fill="{TEAL}">DESARROLLO  ·  AUTOMATIZACIÓN  ·  DATOS</text>
<text x="44" y="212" font-family="{SANS}" font-size="74" font-weight="800" letter-spacing="-1.8" fill="{TXT}">Briand <tspan fill="url(#name)">Castro</tspan></text>
<text x="46" y="258" font-family="{SANS}" font-size="25" fill="{MUTED}">Analista y Desarrollador de Software</text>
<text x="46" y="318" font-family="{MONO}" font-size="18" fill="{TEAL}">&gt;</text>{typed}
<line x1="46" x2="1154" y1="362" y2="362" stroke="{LINE}" stroke-opacity=".8"/>
<text x="46" y="393" font-family="{MONO}" font-size="13.5" fill="{DIM}">ahora  <tspan fill="{MUTED}">Gestor de plataforma educativa Prizma · Corporación Universitaria Americana</tspan></text>
<text x="1154" y="393" text-anchor="end" font-family="{MONO}" font-size="13.5" fill="{DIM}">formación  <tspan fill="{MUTED}">Tecnólogo ADSO · SENA</tspan></text>
{wires}{pulses}{nodes}'''
    save("header.svg", svg(W, H, "Briand Castro — Analista y Desarrollador de Software", defs, style, body))


# ───────────────────────────── qué hago ─────────────────────────────
def pilar(fn, num, tag, t1, t2, lines, color, art):
    W, H = 392, 300
    defs, bg = frame(W, H, 20, color, 1, 0, dots=False)
    style = (".a{animation:a 3s ease-in-out infinite}.a2{animation-delay:.4s}.a3{animation-delay:.8s}.a4{animation-delay:1.2s}.a5{animation-delay:1.6s}"
             "@keyframes a{50%{opacity:.25}}"
             ".grow{animation:grow 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}@keyframes grow{0%,100%{transform:scaleY(.55)}50%{transform:scaleY(1)}}"
             f".w{{stroke-dasharray:4 6;animation:flow 1.2s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-20}}}}")
    desc = "".join(f'<text x="28" y="{222 + i*22}" font-family="{SANS}" font-size="15" fill="{MUTED}">{e(l)}</text>' for i, l in enumerate(lines))
    body = f'''{bg}
<text x="28" y="44" font-family="{MONO}" font-size="12.5" letter-spacing="2.5" fill="{color}">{num}  /  {e(tag)}</text>
<g transform="translate(28,66)" stroke="{color}" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{art}</g>
<text x="28" y="166" font-family="{SANS}" font-size="23" font-weight="750" letter-spacing="-.3" fill="{TXT}">{e(t1)}</text>
<text x="28" y="193" font-family="{SANS}" font-size="23" font-weight="750" letter-spacing="-.3" fill="{TXT}">{e(t2)}</text>
{desc}'''
    save(fn, svg(W, H, f"{t1} {t2}: {' '.join(lines)}", defs, style, body))


def pilares():
    web = ('<rect x="0" y="0" width="96" height="62" rx="8"/><path d="M0 16 H96"/><circle cx="10" cy="8" r="1.5"/><circle cx="18" cy="8" r="1.5"/>'
           '<path class="a" d="M12 30 H56"/><path class="a a2" d="M12 42 H70"/><path class="a a3" d="M12 52 H40"/>'
           '<rect x="112" y="6" width="34" height="56" rx="7"/><path class="a a4" d="M121 22 H137"/><path class="a a5" d="M121 32 H137"/><path d="M125 54 H133"/>')
    pilar("hago-desarrollo.svg", "01", "DESARROLLO", "Web y móvil", "de punta a punta",
          ["Interfaces, APIs y bases de datos:", "de la idea a la app funcionando."], BLUE, web)
    auto = ('<rect x="0" y="16" width="34" height="34" rx="9"/><path d="M12 25 L24 33 L12 41 Z"/>'
            '<path class="w" d="M34 33 H62"/><rect x="62" y="16" width="34" height="34" rx="9"/><circle cx="79" cy="33" r="5"/>'
            '<path class="w" d="M96 33 H124"/><rect x="124" y="16" width="34" height="34" rx="9"/><path d="M133 33 L139 39 L150 27"/>'
            '<circle r="3.5" stroke="none" fill="currentColor"><animateMotion dur="2.4s" repeatCount="indefinite" path="M34 33 H124"/></circle>')
    pilar("hago-automatizacion.svg", "02", "AUTOMATIZACIÓN", "Que lo repetitivo", "lo haga el sistema",
          ["Flujos con n8n y Power Automate", "que ahorran horas de trabajo manual."], TEAL, auto.replace("currentColor", TEAL))
    datos = "".join(f'<rect class="grow" style="animation-delay:{i*.25}s" x="{i*26}" y="{62-h}" width="16" height="{h}" rx="4"/>' for i, h in enumerate([24, 40, 32, 54, 62]))
    datos += '<path class="a" d="M-2 44 L34 26 L60 34 L86 10 L122 -2" stroke-opacity=".6"/><path d="M-4 66 H130" stroke-opacity=".4"/>'
    pilar("hago-datos.svg", "03", "DATOS", "Datos que", "se entienden",
          ["Reportes y tableros en Power BI", "sobre bases SQL y NoSQL."], AMBER, datos)


# ───────────────────────────── trayectoria ─────────────────────────────
def trayectoria():
    W, H = 1200, 310
    defs, bg = frame(W, H, 22, VIOLET, .1, 0, dots=False)
    defs += f'<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>'
    hitos = [(60, "2023 — 2025", "Tecnólogo ADSO", "SENA", ["Análisis y Desarrollo de Software.", "Servicio Nacional de Aprendizaje."], VIOLET, []),
             (440, "ENE — JUL 2025", "Calidad de Proveedores", "Procaps", ["Informes y análisis de datos, automatización", "documental y registros de calidad (QM)."], BLUE, ["Power BI", "Power Automate", "SAP"]),
             (820, "SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana", ["Cargue y publicación de cursos; automaticé", "el proceso para reducir tareas manuales."], TEAL, ["n8n", "Prizma"])]
    body = f'{bg}{kicker(40, 50, "TRAYECTORIA", VIOLET)}<path d="M60 112 H1140" stroke="{LINE}" stroke-width="2"/><path class="ln" d="M60 112 H1140" stroke="url(#ln)" stroke-width="2.5" fill="none"/>'
    for i, (x, fecha, tit, org, ds, c, tech) in enumerate(hitos):
        last = i == len(hitos) - 1
        body += (f'<circle cx="{x+8}" cy="112" r="8" fill="{BG0}" stroke="{c}" stroke-width="2.5"/>'
                 + (f'<circle class="ping" cx="{x+8}" cy="112" r="8" fill="none" stroke="{c}" stroke-width="2"/><circle cx="{x+8}" cy="112" r="3.5" fill="{c}"/>' if last else "")
                 + f'<text x="{x+26}" y="94" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{c}">{fecha}</text>'
                 f'<text x="{x}" y="156" font-family="{SANS}" font-size="21" font-weight="750" fill="{TXT}">{e(tit)}</text>'
                 f'<text x="{x}" y="180" font-family="{SANS}" font-size="15" font-weight="600" fill="{c}">{e(org)}</text>'
                 + "".join(f'<text x="{x}" y="{208+j*21}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{e(d)}</text>' for j, d in enumerate(ds))
                 + chips(tech, x, 250, 330, c, size=12, h=24, gap=7))
    style = (".ln{stroke-dasharray:1080;stroke-dashoffset:1080;animation:draw 6s ease-out infinite}"
             "@keyframes draw{0%{stroke-dashoffset:1080}55%,100%{stroke-dashoffset:0}}"
             ".ping{animation:ping 2s ease-out infinite;transform-box:fill-box;transform-origin:center}@keyframes ping{to{transform:scale(2.6);opacity:0}}")
    save("trayectoria.svg", svg(W, H, "Trayectoria: SENA 2023–2025, Procaps 2025, Corporación Universitaria Americana desde septiembre de 2025", defs, style, body))


# ───────────────────────────── stack ─────────────────────────────
def stack():
    rows = [("LENGUAJES", TEAL, ["TypeScript", "JavaScript", "C#", "PHP", "SQL"]),
            ("FRONTEND Y MÓVIL", BLUE, ["React", "Next.js", "Tailwind CSS", "Ionic", "Capacitor"]),
            ("BACKEND Y DATOS", VIOLET, ["Node.js", ".NET 8", "PostgreSQL", "MySQL", "MongoDB", "Supabase", "Firebase"]),
            ("AUTOMATIZACIÓN E IA", AMBER, ["n8n", "Power Automate", "Power BI", "Ollama", "Whisper"]),
            ("HERRAMIENTAS", TEAL, ["Git", "Docker", "Unity", "VS Code", "SAP"])]
    W, rh, top = 1200, 56, 84
    H = top + rh * len(rows) + 14
    defs, bg = frame(W, H, 22, TEAL, .95, 0, dots=False)
    body = bg + kicker(40, 50, "STACK")
    for i, (lab, c, items) in enumerate(rows):
        y = top + i * rh
        body += (f'<line x1="40" x2="{W-40}" y1="{y-12}" y2="{y-12}" stroke="{LINE}" stroke-opacity=".6"/>'
                 f'<circle cx="46" cy="{y+16}" r="4" fill="{c}"/><text x="62" y="{y+21}" font-family="{MONO}" font-size="13.5" letter-spacing="2.5" fill="{MUTED}">{e(lab)}</text>'
                 + chips(items, 300, y, 860, c, size=14.5, h=32, gap=10))
    save("stack.svg", svg(W, H, "Stack: " + "; ".join(f"{l}: {', '.join(it)}" for l, _, it in rows), defs, "", body))


# ───────────────────────────── actividad ─────────────────────────────
def fetch_calendar():
    if os.environ.get("PERFIL_SIN_RED"):
        return None
    tok = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        return None
    q = 'query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q, "variables": {"u": USER}}).encode(),
                                 headers={"Authorization": f"bearer {tok}", "User-Agent": "perfil-build"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        return [[(x["date"], x["contributionCount"]) for x in w["contributionDays"]] for w in cal["weeks"]]
    except Exception as ex:  # sin red o sin permisos: no se toca la imagen existente
        print("No se pudo consultar la actividad:", ex, file=sys.stderr)
        return None


def mejor_racha(days):
    best = cur = 0
    for _, c in days:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    return best


def semanas_locales(data):
    """Arma las 53 semanas (domingo a sábado) que terminan en data['hasta'] con los commits guardados."""
    fin = dt.date.fromisoformat(data["hasta"])
    ini = fin - dt.timedelta(days=(fin.weekday() + 1) % 7 + 52 * 7)
    weeks, d = [], ini
    while d <= fin:
        w = []
        for _ in range(7):
            if d <= fin:
                w.append((d.isoformat(), data["dias"].get(d.isoformat(), 0)))
            d += dt.timedelta(days=1)
        weeks.append(w)
    return weeks


def hora12(h):
    return f"{(h % 12) or 12} {'a. m.' if h < 12 else 'p. m.'}"


def actividad(cal):
    """Panel de actividad. Con datos de GitHub (cal) usa las contribuciones; si no, los commits de data/actividad.json."""
    W, H = 1200, 690
    defs, bg = frame(W, H, 22, BLUE, .5, 0, dots=False)
    data = json.load(open(os.path.join(ROOT, "data", "actividad.json"), encoding="utf-8"))
    langs = json.load(open(os.path.join(ROOT, "data", "lenguajes.json"), encoding="utf-8"))["lenguajes"]
    cols = [TEAL, BLUE, VIOLET, AMBER, "#f472b6", "#34d399", DIM]
    MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    weeks = cal if cal is not None else semanas_locales(data)
    etiqueta, sub0 = ("CONTRIBUCIONES", "en GitHub, último año") if cal is not None else ("COMMITS", f"en {data['proyectos']} proyectos, último año")
    days = [d for w in weeks for d in w]
    total, activos, best = sum(c for _, c in days), sum(1 for _, c in days if c), mejor_racha(days)
    tiles = ""
    for i, (lab, v, s_, c) in enumerate([(etiqueta, f"{total:,}".replace(",", "."), sub0, TEAL),
                                         ("DÍAS ACTIVOS", str(activos), "con al menos un commit", AMBER),
                                         ("MEJOR RACHA", str(best), "día seguido" if best == 1 else "días seguidos", VIOLET)]):
        x = 40 + i * 252
        tiles += (f'<rect x="{x}" y="78" width="236" height="140" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
                  f'<text x="{x+20}" y="108" font-family="{MONO}" font-size="12" letter-spacing="2.2" fill="{MUTED}">{lab}</text>'
                  f'<text x="{x+20}" y="170" font-family="{SANS}" font-size="52" font-weight="800" letter-spacing="-1" fill="{c}">{v}</text>'
                  f'<text x="{x+20}" y="198" font-family="{SANS}" font-size="14" fill="{MUTED}">{s_}</text>')
    lx, lw = 796, 364
    lang = (f'<rect x="{lx}" y="78" width="{lw}" height="140" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="{lx+20}" y="108" font-family="{MONO}" font-size="12" letter-spacing="2.2" fill="{MUTED}">LENGUAJES · {data["proyectos"]} PROYECTOS RECIENTES</text>'
            f'<clipPath id="lb"><rect x="{lx+20}" y="122" width="{lw-40}" height="12" rx="6"/></clipPath><g clip-path="url(#lb)">')
    cx = lx + 20
    for (n, p), c in zip(langs, cols):
        w = (lw - 40) * p / 100
        lang += f'<rect x="{cx:.1f}" y="122" width="{w+.6:.1f}" height="12" fill="{c}"/>'
        cx += w
    lang += "</g>"
    for i, ((n, p), c) in enumerate(zip(langs, cols)):
        x, y = lx + 20 + (i % 2) * 166, 160 + (i // 2) * 17.5
        lang += (f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{c}"/><text x="{x+15}" y="{y}" font-family="{SANS}" font-size="12.5" fill="{TXT}">{e(n)}</text>'
                 f'<text x="{x+146}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{p:.0f}%</text>')
    # mapa de calor
    gx, gy, cell, step = 86, 286, 15, 19.3
    grid, months, last_m = "", "", None
    OPS = [0, .3, .52, .76, 1]
    for wi, col in enumerate(weeks):
        if col:
            m = int(col[0][0][5:7])
            if m != last_m and wi < len(weeks) - 2:
                months += f'<text x="{gx+wi*step:.1f}" y="{gy-10}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{MES[m-1]}</text>'
                last_m = m
        for date, c in col:
            wd = (dt.date.fromisoformat(date).weekday() + 1) % 7
            lvl = 0 if c == 0 else 1 if c < 2 else 2 if c < 5 else 3 if c < 10 else 4
            fill = f'fill="{TEAL}" fill-opacity="{OPS[lvl]}"' if lvl else 'fill="#18223f"'
            cls = f' class="hot" style="animation-delay:{(wi % 9) * .22:.2f}s"' if lvl >= 3 else ""
            grid += f'<rect{cls} x="{gx+wi*step:.1f}" y="{gy+wd*step:.1f}" width="{cell}" height="{cell}" rx="4" {fill}><title>{date}: {c}</title></rect>'
    dias = "".join(f'<text x="40" y="{gy+i*step+12:.1f}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{d}</text>' for i, d in ((1, "lun"), (3, "mié"), (5, "vie")))
    fy = gy + 7 * step + 22
    hasta = dt.date.fromisoformat(data["hasta"])
    nota = "se actualiza sola cada día" if cal is not None else f"datos al {hasta.day} {MES[hasta.month-1]} {hasta.year}"
    pie = (f'<text x="40" y="{fy:.0f}" font-family="{SANS}" font-size="13.5" fill="{MUTED}">Último año · {nota}</text>'
           f'<text x="{W-170}" y="{fy:.0f}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{MUTED}">menos</text>'
           + "".join(f'<rect x="{W-160+i*19}" y="{fy-12:.0f}" width="15" height="15" rx="4" ' + (f'fill="{TEAL}" fill-opacity="{o}"' if o else 'fill="#18223f"') + '/>' for i, o in enumerate(OPS))
           + f'<text x="{W-58}" y="{fy:.0f}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">más</text>')
    # cuándo programo: por hora y por día de la semana
    ty, base, hmax = 490, 640, 86
    horas, sem = data["horas"], data["semana"]
    pico, mh = horas.index(max(horas)), max(horas + [1])
    hb = f'<line x1="40" x2="{W-40}" y1="{ty-28}" y2="{ty-28}" stroke="{LINE}" stroke-opacity=".6"/>' + kicker(40, ty, "CUÁNDO PROGRAMO", AMBER)
    for h, v in enumerate(horas):
        x, bh = 44 + h * 29.5, max(3, hmax * v / mh)
        c = AMBER if h == pico else BLUE
        hb += f'<rect class="up" style="animation-delay:{h*.14:.2f}s" x="{x:.1f}" y="{base-bh:.1f}" width="20" height="{bh:.1f}" rx="5" fill="{c}" fill-opacity="{1 if h == pico else .55}"/>'
        if h % 6 == 0 or h == 23:
            hb += f'<text x="{x+10:.1f}" y="{base+20}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{hora12(h)}</text>'
    px = 44 + pico * 29.5 + 10
    hb += f'<text x="{px:.1f}" y="{base - hmax - 10}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="{AMBER}">pico: {hora12(pico)}</text>'
    ms, orden = max(sem + [1]), sorted(range(7), key=lambda i: -sem[i])[:2]
    for i, v in enumerate(sem):
        x, bh = 836 + i * 46, max(3, hmax * v / ms)
        top = i in orden
        hb += (f'<rect class="up" style="animation-delay:{i*.14:.2f}s" x="{x}" y="{base-bh:.1f}" width="30" height="{bh:.1f}" rx="6" fill="{TEAL if top else VIOLET}" fill-opacity="{1 if top else .5}"/>'
               f'<text x="{x+15}" y="{base+20}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{TXT if top else MUTED}">{"LMXJVSD"[i]}</text>')
    finde = round(100 * (sem[5] + sem[6]) / max(1, sum(sem)))
    hb += f'<text x="{W-40}" y="{ty}" text-anchor="end" font-family="{SANS}" font-size="13.5" fill="{MUTED}">{finde} % de los commits, en fin de semana</text>'
    style = (".hot{animation:hot 3.6s ease-in-out infinite}@keyframes hot{50%{fill-opacity:.45}}"
             ".up{animation:up 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}@keyframes up{50%{transform:scaleY(.8)}}")
    body = f'{bg}{kicker(40, 50, "ACTIVIDAD", BLUE)}{tiles}{lang}{months}{dias}{grid}{pie}{hb}'
    save("actividad.svg", svg(W, H, f"Actividad: {total} {etiqueta.lower()} y {activos} días activos en el último año, mejor racha de {best} días; pico de actividad a las {hora12(pico)}.", defs, style, body))


def cierre():
    W, H = 1200, 170
    defs, bg = frame(W, H, 22, TEAL, .9, .5)
    defs += f'<linearGradient id="cta" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
    ola = "M0 150 " + " ".join(f"Q{60+i*120} {132 if i % 2 == 0 else 168} {120+i*120} 150" for i in range(10))
    style = (f".ola{{fill:none;stroke:{TEAL};stroke-opacity:.35;stroke-width:1.6;stroke-dasharray:6 10;animation:ola 2.2s linear infinite}}@keyframes ola{{to{{stroke-dashoffset:-32}}}}"
             ".fl{animation:fl 1.6s ease-in-out infinite}@keyframes fl{50%{transform:translateX(6px)}}")
    body = f'''{bg}<g clip-path="url(#clip)"><path class="ola" d="{ola}"/></g>
<text x="46" y="78" font-family="{SANS}" font-size="38" font-weight="800" letter-spacing="-.8" fill="{TXT}">¿Automatizamos algo <tspan fill="url(#cta)">juntos</tspan>?</text>
<text x="46" y="112" font-family="{SANS}" font-size="18" fill="{MUTED}">Cuéntame qué tarea repetitiva te quita tiempo y vemos cómo resolverla.</text>
<rect x="{W-266}" y="56" width="220" height="56" rx="28" fill="url(#cta)"/>
<text x="{W-170}" y="91" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="700" fill="{BG0}">Escríbeme</text>
<path class="fl" d="M{W-104} 84 h22 m-8 -8 l8 8 l-8 8" fill="none" stroke="{BG0}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'''
    save("cierre.svg", svg(W, H, "¿Automatizamos algo juntos? Escríbeme.", defs, style, body))


def boton(fn, text, color):
    w = int(len(text) * 9.6) + 64
    body = (f'<rect x="1" y="1" width="{w-2}" height="42" rx="21" fill="{BG0}" stroke="{color}" stroke-opacity=".7" stroke-width="1.5"/>'
            f'<circle class="d" cx="26" cy="22" r="4.5" fill="{color}"/><text x="42" y="27.5" font-family="{MONO}" font-size="15" fill="{TXT}">{e(text)}</text>')
    save(fn, svg(w, 44, text, "", ".d{animation:d 2s ease-in-out infinite}@keyframes d{50%{opacity:.3}}", body))


if __name__ == "__main__":
    header(); pilares(); trayectoria(); stack()
    boton("btn-email.svg", "Escríbeme", TEAL); boton("btn-repos.svg", "Ver repositorios", BLUE)
    cierre()
    actividad(fetch_calendar())
    print("Listo:", sorted(os.listdir(OUT)))
