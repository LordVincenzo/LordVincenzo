#!/usr/bin/env python3
"""Genera los bloques SVG del perfil (mosaico en rojo, negro y blanco). Solo librería estándar.

    python scripts/build.py

Los datos salen de data/actividad.json y data/lenguajes.json. Si hay GITHUB_TOKEN y red,
el mapa de calor usa las contribuciones de GitHub en vez de los commits guardados.
"""
import datetime as dt, html, json, math, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
USER = "LordVincenzo"
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
DISPLAY = "'Arial Black', 'Segoe UI Black', Inter, 'Helvetica Neue', Arial, sans-serif"
NEGRO, TINTA, LINEA, VACIO = "#050505", "#0d0d0d", "#2b2b2b", "#1c1c1c"
BLANCO, GRIS, TENUE, ROJO = "#ffffff", "#a3a3a3", "#666666", "#ff2d3d"
W1, W2, W3 = 400, 807, 1214          # ancho de bloque: un tercio, dos tercios, fila completa
MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
e = html.escape
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def save(name, W, H, label, body, style="", defs=""):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(label)}">'
                f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>{defs}</defs><style>{style}{REDUCE}</style>{body}</svg>')


def fondo(W, H, tono="negro", malla=False):
    """Fondo del bloque: negro (con borde), rojo o blanco."""
    if tono == "negro":
        m = (f'<pattern id="malla" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0 H0 V30" fill="none" stroke="#fff" stroke-opacity=".055"/></pattern>'
             f'<rect width="{W}" height="{H}" fill="url(#malla)"/>') if malla else ""
        return (f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{TINTA}"/>{m}</g>'
                f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{LINEA}" stroke-width="1.5"/>')
    if tono == "rojo":
        return f'<rect width="{W}" height="{H}" rx="16" fill="{ROJO}"/>'
    return f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="{BLANCO}" stroke="#d0d0d0" stroke-width="1.5"/>'


def rotulo(x, y, text, color=BLANCO, punto=ROJO):
    return (f'<rect x="{x}" y="{y-11}" width="11" height="11" fill="{punto}"/>'
            f'<text x="{x+22}" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="{color}">{e(text)}</text>')


def hora12(h):
    return f"{(h % 12) or 12} {'a. m.' if h < 12 else 'p. m.'}"


def cargar(nombre):
    return json.load(open(os.path.join(ROOT, "data", nombre), encoding="utf-8"))


# ───────────── fila 1: nombre + flujo ─────────────
def nombre():
    W, H = W2, 400
    frases = ["Automatizo lo repetitivo.", "Construyo apps web y móviles.", "Convierto datos en decisiones."]
    typed = ""
    for i, f in enumerate(frases):
        w, a = round(len(f) * 10.8), i / 3
        kt = f"0;{a:.3f};{a+.11:.3f};{a+.27:.3f};{a+.325:.3f};1"
        typed += (f'<clipPath id="t{i}"><rect x="66" y="336" height="30" width="0"><animate attributeName="width" dur="10.5s" repeatCount="indefinite" values="0;0;{w+2};{w+2};0;0" keyTimes="{kt}"/></rect></clipPath>'
                  f'<text x="66" y="358" clip-path="url(#t{i})" font-family="{MONO}" font-size="18" fill="{BLANCO}" textLength="{w}" lengthAdjust="spacingAndGlyphs">{e(f)}</text>'
                  f'<rect y="340" width="9" height="22" fill="{ROJO}" opacity="0"><animate attributeName="x" dur="10.5s" repeatCount="indefinite" values="68;68;{w+72};{w+72};68;68" keyTimes="{kt}"/>'
                  f'<animate attributeName="opacity" dur="10.5s" repeatCount="indefinite" values="0;1;1;1;0;0" keyTimes="0;{max(a,.001):.3f};{a+.11:.3f};{a+.325:.3f};{a+.33:.3f};1" calcMode="discrete"/></rect>')
    defs = ('<clipPath id="wipe"><rect x="36" y="180" height="130" width="0"><animate attributeName="width" dur="7s" repeatCount="indefinite" values="0;0;740;740;0" keyTimes="0;.12;.42;.8;1" '
            'calcMode="spline" keySplines="0 0 1 1;.4 0 .2 1;0 0 1 1;.4 0 .2 1"/></rect></clipPath>')
    t = f'font-family="{DISPLAY}" font-size="150" font-weight="900" textLength="700" lengthAdjust="spacingAndGlyphs"'
    body = f'''{fondo(W, H, malla=True)}
<rect class="p" x="40" y="34" width="12" height="12" fill="{ROJO}"/>
<text x="64" y="45" font-family="{MONO}" font-size="13.5" letter-spacing="3" fill="{GRIS}">LORDVINCENZO <tspan fill="{TENUE}">/</tspan> README.md</text>
<text x="{W-40}" y="45" text-anchor="end" font-family="{MONO}" font-size="13.5" letter-spacing="3" fill="{GRIS}">ANALISTA Y DESARROLLADOR DE SOFTWARE</text>
<text x="36" y="176" {t} fill="{BLANCO}">BRIAND</text>
<text x="36" y="302" {t} fill="none" stroke="{ROJO}" stroke-width="3">CASTRO</text>
<text x="36" y="302" {t} fill="{ROJO}" clip-path="url(#wipe)">CASTRO</text>
<text x="40" y="358" font-family="{MONO}" font-size="18" font-weight="700" fill="{ROJO}">&gt;</text>{typed}'''
    save("nombre.svg", W, H, "Briand Castro — Analista y Desarrollador de Software", body,
         ".p{animation:p 1.4s steps(1) infinite}@keyframes p{50%{opacity:0}}", defs)


def flujo():
    W, H = W1, 400
    N = [(200, 96, '<path d="M-7 -10 L10 0 L-7 10 Z"/>'),
         (96, 200, '<ellipse cx="0" cy="-7" rx="10" ry="4"/><path d="M-10 -7 V7 C-10 12 10 12 10 7 V-7"/><path d="M-10 0 C-10 5 10 5 10 0"/>'),
         (304, 200, '<path d="M-5 -9 C-10 -9 -6 -1 -11 0 C-6 1 -10 9 -5 9"/><path d="M5 -9 C10 -9 6 -1 11 0 C6 1 10 9 5 9"/>'),
         (200, 304, '<path d="M-10 0 L-3 8 L11 -8"/>')]
    P = ["M176 120 C150 150 130 150 110 170", "M224 120 C250 150 270 150 290 170",
         "M110 230 C130 250 150 250 176 280", "M290 230 C270 250 250 250 224 280"]
    cables = "".join(f'<path d="{p}" class="w"/>' for p in P)
    pulsos = "".join(f'<circle r="5.5" fill="{BLANCO}"><animateMotion dur="2.2s" begin="-{b}s" repeatCount="indefinite" path="{p}"/></circle>' for p, b in zip(P, (0, .6, 1.1, 1.7)))
    nodos = "".join(f'<g class="n n{i}"><rect x="{x-34}" y="{y-34}" width="68" height="68" rx="12" fill="{NEGRO}"/>'
                    f'<g transform="translate({x},{y}) scale(1.25)" fill="none" stroke="{BLANCO}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{g}</g></g>' for i, (x, y, g) in enumerate(N))
    body = f'''{fondo(W, H, "rojo")}
<g clip-path="url(#clip)"><circle class="r" cx="200" cy="200" r="150" fill="none" stroke="{NEGRO}" stroke-opacity=".22" stroke-width="2" stroke-dasharray="4 10"/></g>
{cables}{pulsos}{nodos}
<rect class="c" x="186" y="186" width="28" height="28" fill="{NEGRO}"/>
<text x="28" y="{H-26}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="2.5" fill="{NEGRO}">SOLEDAD, COLOMBIA</text>
<text x="{W-28}" y="{H-26}" text-anchor="end" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="2.5" fill="{BLANCO}">AUTOMATIZACIÓN</text>'''
    style = (f".w{{fill:none;stroke:{NEGRO};stroke-width:2.2;stroke-dasharray:5 7;animation:f 1.3s linear infinite}}@keyframes f{{to{{stroke-dashoffset:-24}}}}"
             ".n{animation:n 4.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}.n1{animation-delay:.55s}.n2{animation-delay:1.1s}.n3{animation-delay:1.65s}"
             "@keyframes n{0%,14%,100%{transform:scale(1)}7%{transform:scale(1.13)}}"
             ".c{animation:c 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes c{50%{transform:rotate(45deg) scale(.7)}}"
             ".r{animation:r 40s linear infinite;transform-origin:200px 200px}@keyframes r{to{transform:rotate(360deg)}}")
    save("flujo.svg", W, H, "Flujo de automatización animado. Soledad, Colombia.", body, style)


# ───────────── fila 2: sobre mí (al lado del GIF) ─────────────
def sobre():
    W, H = W2, 304
    parr = [[("Tecnólogo en ", 0), ("Análisis y Desarrollo de Software", 1), (". Construyo aplicaciones", 0)],
            [("web y móviles de punta a punta, y automatizo procesos para que el", 0)],
            [("trabajo repetitivo lo haga el sistema.", 0)], None,
            [("Hoy gestiono la plataforma educativa ", 0), ("Prizma", 1), (" en la Corporación", 0)],
            [("Universitaria Americana, donde automaticé el cargue de cursos con ", 0), ("n8n", 1), (".", 0)], None,
            [("Me interesan la ", 0), ("IA que corre en local", 1), (", las ", 0), ("apps en tiempo real", 1)],
            [("y los ", 0), ("flujos de automatización", 1), (".", 0)]]
    y, txt = 96, ""
    for l in parr:
        if l is None:
            y += 14
            continue
        txt += f'<text x="40" y="{y}" font-family="{SANS}" font-size="19" fill="{GRIS}">' + "".join(
            f'<tspan fill="{BLANCO}" font-weight="700">{e(t)}</tspan>' if b else e(t) for t, b in l) + "</text>"
        y += 28
    body = f'{fondo(W, H)}{rotulo(40, 52, "SOBRE MÍ")}<rect class="b" x="40" y="66" width="60" height="3" fill="{ROJO}"/>{txt}'
    save("sobre.svg", W, H, "Sobre mí: tecnólogo en Análisis y Desarrollo de Software. Construyo aplicaciones web y móviles y automatizo procesos. "
         "Gestiono la plataforma educativa Prizma en la Corporación Universitaria Americana, donde automaticé el cargue de cursos con n8n. "
         "Me interesan la IA que corre en local, las apps en tiempo real y los flujos de automatización.", body,
         ".b{animation:b 4s ease-in-out infinite;transform-origin:40px 0}@keyframes b{50%{transform:scaleX(4)}}")


# ───────────── fila 3: tres cifras ─────────────
def cifra(fn, tono, valor, largo, etiqueta, nota):
    W, H = W1, 220
    tinta, sec, punto = {"blanco": (NEGRO, "#555555", ROJO), "negro": (BLANCO, GRIS, ROJO), "rojo": (BLANCO, NEGRO, NEGRO)}[tono]
    body = (f'{fondo(W, H, tono)}{rotulo(28, 44, etiqueta, tinta, punto)}'
            f'<text class="v" x="24" y="156" font-family="{DISPLAY}" font-size="104" font-weight="900" fill="{ROJO if tono == "blanco" else tinta}" textLength="{largo}" lengthAdjust="spacingAndGlyphs">{e(valor)}</text>'
            f'<text x="28" y="192" font-family="{SANS}" font-size="15" font-weight="600" fill="{sec}">{e(nota)}</text>')
    save(fn, W, H, f"{etiqueta}: {valor}. {nota}", body, ".v{animation:v 5s ease-in-out infinite}@keyframes v{50%{opacity:.82}}")


# ───────────── fila 4: qué hago (lista) ─────────────
def hago():
    W, H = W3, 300
    filas = [("01", "DESARROLLO", "Web y móvil de punta a punta", "Interfaces, APIs y bases de datos: de la idea a la app funcionando."),
             ("02", "AUTOMATIZACIÓN", "Que lo repetitivo lo haga el sistema", "Flujos con n8n y Power Automate que ahorran horas de trabajo manual."),
             ("03", "DATOS", "Datos que se entienden", "Reportes y tableros en Power BI sobre bases SQL y NoSQL.")]
    body = fondo(W, H)
    for i, (n, tag, tit, desc) in enumerate(filas):
        y = i * 100
        body += ((f'<line x1="36" x2="{W-36}" y1="{y}" y2="{y}" stroke="{LINEA}"/>' if i else "")
                 + f'<g clip-path="url(#clip)"><rect class="s s{i}" x="0" y="{y+1}" width="8" height="98" fill="{ROJO}"/></g>'
                 f'<text x="40" y="{y+68}" font-family="{DISPLAY}" font-size="56" font-weight="900" fill="none" stroke="{TENUE}" stroke-width="1.6" textLength="84" lengthAdjust="spacingAndGlyphs">{n}</text>'
                 f'<text x="160" y="{y+42}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="3" fill="{ROJO}">{tag}</text>'
                 f'<text x="160" y="{y+74}" font-family="{SANS}" font-size="25" font-weight="800" fill="{BLANCO}">{e(tit)}</text>'
                 f'<text x="646" y="{y+58}" font-family="{SANS}" font-size="14.5" fill="{GRIS}">{e(desc)}</text>'
                 f'<path class="fl s{i}" d="M{W-76} {y+52} h26 m-10 -10 l10 10 l-10 10" fill="none" stroke="{BLANCO}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    style = (".s{animation:s 6s ease-in-out infinite;opacity:.18}.s1{animation-delay:2s}.s2{animation-delay:4s}@keyframes s{0%,34%,100%{opacity:.18}8%,26%{opacity:1}}"
             ".fl{animation:fl 6s ease-in-out infinite;opacity:.25}.fl.s1{animation-delay:2s}.fl.s2{animation-delay:4s}@keyframes fl{0%,34%,100%{opacity:.25;transform:translateX(0)}8%,26%{opacity:1;transform:translateX(8px)}}")
    save("hago.svg", W, H, "Qué hago: " + " ".join(f"{t}. {d}" for _, _, t, d in filas), body, style)


# ───────────── fila 5: stack en cintas + trayectoria ─────────────
def stack():
    W, H = W2, 420
    filas = [("LENGUAJES", ["TypeScript", "JavaScript", "C#", "PHP", "SQL"], True),
             ("FRONTEND Y MÓVIL", ["React", "Next.js", "Tailwind CSS", "Ionic", "Capacitor"], False),
             ("BACKEND Y DATOS", ["Node.js", ".NET 8", "PostgreSQL", "MySQL", "MongoDB", "Supabase", "Firebase"], False),
             ("AUTOMATIZACIÓN E IA", ["n8n", "Power Automate", "Power BI", "Ollama", "Whisper"], True),
             ("HERRAMIENTAS", ["Git", "Docker", "Unity", "VS Code", "SAP"], False)]
    body, style = fondo(W, H) + rotulo(36, 50, "STACK"), ""
    for i, (lab, items, rojo) in enumerate(filas):
        y = 78 + i * 66
        unidad, x = "", 0
        for t in items:
            w = int(len(t) * 10.2) + 34
            unidad += (f'<rect x="{x}" y="0" width="{w}" height="38" rx="6" fill="{ROJO if rojo else "none"}" stroke="{ROJO if rojo else "#5a5a5a"}" stroke-width="1.4"/>'
                       f'<text x="{x+w/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{BLANCO}" textLength="{w-34}" lengthAdjust="spacingAndGlyphs">{e(t)}</text>')
            x += w + 12
        reps = -(-(W + x) // x) + 1
        cinta = "".join(f'<g transform="translate({k*x},0)">{unidad}</g>' for k in range(int(reps)))
        sentido = "normal" if i % 2 == 0 else "reverse"
        style += f".c{i}{{animation:c{i} {x/28:.1f}s linear infinite {sentido}}}@keyframes c{i}{{to{{transform:translateX(-{x}px)}}}}"
        body += (f'<text x="36" y="{y+8}" font-family="{MONO}" font-size="11" letter-spacing="2.4" fill="{TENUE}">{lab}</text>'
                 f'<g clip-path="url(#clip)"><g transform="translate(0,{y+16})"><g class="c{i}">{cinta}</g></g></g>')
    body += f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{LINEA}" stroke-width="1.5"/>'
    save("stack.svg", W, H, "Stack: " + "; ".join(f"{l}: {', '.join(it)}" for l, it, _ in filas), body, style)


def ruta():
    W, H = W1, 420
    hitos = [("SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana", True),
             ("ENE — JUL 2025", "Calidad de Proveedores", "Procaps", False),
             ("2023 — 2025", "Tecnólogo ADSO", "SENA", False)]
    body = fondo(W, H) + rotulo(32, 50, "TRAYECTORIA") + f'<line x1="44" x2="44" y1="96" y2="372" stroke="{LINEA}" stroke-width="2"/><line class="l" x1="44" x2="44" y1="96" y2="372" stroke="{ROJO}" stroke-width="2.5"/>'
    for i, (fecha, tit, org, hoy) in enumerate(hitos):
        y = 104 + i * 104
        body += ((f'<circle class="ping" cx="44" cy="{y}" r="9" fill="none" stroke="{ROJO}" stroke-width="2"/>' if hoy else "")
                 + f'<circle cx="44" cy="{y}" r="9" fill="{ROJO if hoy else TINTA}" stroke="{ROJO if hoy else BLANCO}" stroke-width="2.5"/>'
                 f'<text x="72" y="{y+4}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{ROJO}">{fecha}</text>'
                 f'<text x="72" y="{y+32}" font-family="{SANS}" font-size="19" font-weight="800" fill="{BLANCO}">{e(tit)}</text>'
                 f'<text x="72" y="{y+54}" font-family="{SANS}" font-size="14" fill="{GRIS}">{e(org)}</text>')
    style = (".l{stroke-dasharray:276;animation:l 6s ease-in-out infinite}@keyframes l{0%{stroke-dashoffset:276}50%,100%{stroke-dashoffset:0}}"
             ".ping{animation:ping 2s ease-out infinite;transform-box:fill-box;transform-origin:center}@keyframes ping{to{transform:scale(2.6);opacity:0}}")
    save("ruta.svg", W, H, "Trayectoria: " + "; ".join(f"{t}, {o} ({f})" for f, t, o, _ in hitos), body, style)


# ───────────── fila 6: mapa de calor + reloj ─────────────
def semanas_locales(data):
    fin = dt.date.fromisoformat(data["hasta"])
    d, weeks = fin - dt.timedelta(days=(fin.weekday() + 1) % 7 + 52 * 7), []
    while d <= fin:
        w = []
        for _ in range(7):
            if d <= fin:
                w.append((d.isoformat(), data["dias"].get(d.isoformat(), 0)))
            d += dt.timedelta(days=1)
        weeks.append(w)
    return weeks


def calendario_github():
    tok = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not tok or os.environ.get("PERFIL_SIN_RED"):
        return None
    q = 'query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q, "variables": {"u": USER}}).encode(),
                                 headers={"Authorization": f"bearer {tok}", "User-Agent": "perfil-build"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        return [[(x["date"], x["contributionCount"]) for x in w["contributionDays"]] for w in cal["weeks"]]
    except Exception as ex:
        print("Sin datos de GitHub, se usan los commits guardados:", ex, file=sys.stderr)
        return None


def calor(data, cal):
    W, H = W2, 300
    weeks = cal or semanas_locales(data)
    gx, gy, cell, step = 74, 104, 11, 13.25
    OPS = [0, .34, .56, .78, 1]
    grid, months, last = "", "", None
    for wi, col in enumerate(weeks):
        m = int(col[0][0][5:7])
        if m != last and wi < len(weeks) - 2:
            months += f'<text x="{gx+wi*step:.1f}" y="{gy-12}" font-family="{MONO}" font-size="11" fill="{GRIS}">{MES[m-1]}</text>'
            last = m
        for date, c in col:
            wd = (dt.date.fromisoformat(date).weekday() + 1) % 7
            lvl = 0 if c == 0 else 1 if c < 2 else 2 if c < 5 else 3 if c < 10 else 4
            fill = f'fill="{ROJO}" fill-opacity="{OPS[lvl]}"' if lvl else f'fill="{VACIO}"'
            cls = f' class="h" style="animation-delay:{(wi % 9) * .25:.2f}s"' if lvl >= 3 else ""
            grid += f'<rect{cls} x="{gx+wi*step:.1f}" y="{gy+wd*step:.1f}" width="{cell}" height="{cell}" rx="2.5" {fill}><title>{date}: {c}</title></rect>'
    dias = "".join(f'<text x="36" y="{gy+i*step+9.5:.1f}" font-family="{MONO}" font-size="11" fill="{GRIS}">{d}</text>' for i, d in ((1, "lun"), (3, "mié"), (5, "vie")))
    fy, hasta = gy + 7 * step + 34, dt.date.fromisoformat(data["hasta"])
    nota = "contribuciones en GitHub" if cal else f"commits en {data['proyectos']} proyectos · datos al {hasta.day} {MES[hasta.month-1]} {hasta.year}"
    body = (f'{fondo(W, H)}{rotulo(36, 50, "ACTIVIDAD · ÚLTIMO AÑO")}{months}{dias}{grid}'
            f'<text x="36" y="{fy:.0f}" font-family="{SANS}" font-size="13.5" fill="{GRIS}">{nota}</text>'
            f'<text x="{W-140}" y="{fy:.0f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{GRIS}">menos</text>'
            + "".join(f'<rect x="{W-132+i*15}" y="{fy-10:.0f}" width="11" height="11" rx="2.5" ' + (f'fill="{ROJO}" fill-opacity="{o}"' if o else f'fill="{VACIO}"') + '/>' for i, o in enumerate(OPS))
            + f'<text x="{W-52}" y="{fy:.0f}" font-family="{MONO}" font-size="11" fill="{GRIS}">más</text>')
    save("calor.svg", W, H, f"Mapa de actividad del último año: {nota}.", body, ".h{animation:h 3.6s ease-in-out infinite}@keyframes h{50%{fill-opacity:.45}}")
    return [d for w in weeks for d in w]


def reloj(data):
    W, H = W1, 300
    horas = data["horas"]
    pico, mx = horas.index(max(horas)), max(horas + [1])
    cx, cy, r0 = 200, 176, 50
    rayos = ""
    for h, v in enumerate(horas):
        ang = math.radians(h * 15 - 90)
        r1 = r0 + 8 + 48 * v / mx
        x0, y0, x1, y1 = cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)
        rayos += f'<line class="y" style="animation-delay:{h*.12:.2f}s" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{ROJO if h == pico else BLANCO}" stroke-opacity="{1 if h == pico else .4}" stroke-width="{9 if h == pico else 7}" stroke-linecap="round"/>'
    marcas = "".join(f'<text x="{cx + 138*math.cos(math.radians(h*15-90)):.0f}" y="{cy + 114*math.sin(math.radians(h*15-90)) + 4:.0f}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{TENUE}">{t}</text>'
                     for h, t in ((0, "12 a. m."), (6, "6 a. m."), (12, "12 p. m."), (18, "6 p. m.")))
    body = (f'{fondo(W, H)}{rotulo(28, 44, "HORA PICO")}{rayos}{marcas}'
            f'<g class="g"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r0+10}" stroke="{ROJO}" stroke-width="2" stroke-linecap="round"/></g><circle cx="{cx}" cy="{cy}" r="4" fill="{ROJO}"/>'
            f'<text x="{cx}" y="{cy+30}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="{BLANCO}">{hora12(pico)}</text>')
    style = (".y{animation:y 2.9s ease-in-out infinite}@keyframes y{50%{stroke-opacity:.15}}"
             f".g{{animation:g 24s linear infinite;transform-origin:{cx}px {cy}px}}@keyframes g{{to{{transform:rotate(360deg)}}}}")
    save("reloj.svg", W, H, f"Reloj de 24 horas con mis commits por hora: el pico es a las {hora12(pico)}.", body, style)


# ───────────── fila 7: lenguajes ─────────────
def lenguajes(data):
    W, H = W3, 132
    langs = cargar("lenguajes.json")["lenguajes"]
    cols = [ROJO, BLANCO, "#ff6b76", "#9c1622", "#b4b4b8", "#ffc9ce", TENUE]
    x0, bw = 36, W - 72
    body = fondo(W, H) + rotulo(36, 42, f"LENGUAJES · {data['proyectos']} PROYECTOS RECIENTES") + f'<clipPath id="lb"><rect x="{x0}" y="58" width="{bw}" height="18" rx="5"/></clipPath><g clip-path="url(#lb)">'
    cx = x0
    for i, ((n, p), c) in enumerate(zip(langs, cols)):
        w = bw * p / 100
        body += f'<rect class="q" style="animation-delay:{i*.3:.1f}s" x="{cx:.1f}" y="58" width="{w+.6:.1f}" height="18" fill="{c}"/>'
        cx += w
    body += "</g>"
    for i, ((n, p), c) in enumerate(zip(langs, cols)):
        x = x0 + i * bw / len(langs)
        body += (f'<rect x="{x:.1f}" y="97" width="10" height="10" fill="{c}"/><text x="{x+18:.1f}" y="107" font-family="{SANS}" font-size="15" font-weight="700" fill="{BLANCO}">{e(n)}'
                 f'<tspan dx="8" font-family="{MONO}" font-size="13" font-weight="400" fill="{GRIS}">{p:.0f} %</tspan></text>')
    save("lenguajes.svg", W, H, "Lenguajes: " + ", ".join(f"{n} {p:.0f} %" for n, p in langs), body, ".q{animation:q 4.2s ease-in-out infinite}@keyframes q{50%{opacity:.6}}")


# ───────────── fila 8: semana + cierre ─────────────
def semana(data):
    W, H = W1, 200
    sem = data["semana"]
    mx, top = max(sem + [1]), sorted(range(7), key=lambda i: -sem[i])[:2]
    finde = round(100 * (sem[5] + sem[6]) / max(1, sum(sem)))
    body = fondo(W, H) + rotulo(28, 44, "SEMANA")
    for i, v in enumerate(sem):
        x, bh = 30 + i * 50, max(4, 78 * v / mx)
        body += (f'<rect class="u" style="animation-delay:{i*.16:.2f}s" x="{x}" y="{150-bh:.1f}" width="34" height="{bh:.1f}" rx="5" fill="{ROJO if i in top else BLANCO}" fill-opacity="{1 if i in top else .32}"/>'
                 f'<text x="{x+17}" y="174" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{BLANCO if i in top else TENUE}">{"LMXJVSD"[i]}</text>')
    body += f'<text x="{W-28}" y="44" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="{GRIS}">{finde} % en fin de semana</text>'
    save("semana.svg", W, H, f"Commits por día de la semana: {finde} % en fin de semana.", body,
         ".u{animation:u 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}@keyframes u{50%{transform:scaleY(.8)}}")


def cierre():
    W, H = W2, 200
    defs = '<pattern id="ray" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)"><rect width="13" height="26" fill="#000" fill-opacity=".07"/></pattern>'
    body = f'''{fondo(W, H, "rojo")}<g clip-path="url(#clip)"><rect class="ray" x="-60" width="{W+120}" height="{H}" fill="url(#ray)"/></g>
<text x="36" y="80" font-family="{DISPLAY}" font-size="42" font-weight="900" fill="{NEGRO}" textLength="430" lengthAdjust="spacingAndGlyphs">¿AUTOMATIZAMOS</text>
<text x="36" y="128" font-family="{DISPLAY}" font-size="42" font-weight="900" fill="{BLANCO}" textLength="356" lengthAdjust="spacingAndGlyphs">ALGO JUNTOS?</text>
<text x="36" y="162" font-family="{SANS}" font-size="15" font-weight="600" fill="{NEGRO}">Cuéntame qué tarea repetitiva te quita tiempo.</text>
<rect x="{W-246}" y="68" width="210" height="64" rx="8" fill="{NEGRO}"/>
<text x="{W-160}" y="108" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="{BLANCO}">Escríbeme</text>
<path class="fl" d="M{W-92} 100 h24 m-9 -9 l9 9 l-9 9" fill="none" stroke="{ROJO}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'''
    save("cierre.svg", W, H, "¿Automatizamos algo juntos? Escríbeme.", body,
         ".ray{animation:ray 3s linear infinite}@keyframes ray{to{transform:translateX(26px)}}.fl{animation:fl 1.4s ease-in-out infinite}@keyframes fl{50%{transform:translateX(7px)}}", defs)


if __name__ == "__main__":
    data = cargar("actividad.json")
    nombre(); flujo(); sobre(); hago(); stack(); ruta(); lenguajes(data); semana(data); cierre(); reloj(data)
    dias = calor(data, calendario_github())
    total, activos = sum(c for _, c in dias), sum(1 for _, c in dias if c)
    racha = cur = 0
    for _, c in dias:
        cur = cur + 1 if c else 0
        racha = max(racha, cur)
    cifra("cifra-commits.svg", "blanco", str(total), 60 * len(str(total)) + 20, "COMMITS", f"en {data['proyectos']} proyectos, último año")
    cifra("cifra-dias.svg", "negro", str(activos), 60 * len(str(activos)) + 20, "DÍAS ACTIVOS", "con al menos un commit")
    cifra("cifra-racha.svg", "rojo", str(racha), 60 * len(str(racha)) + 20, "MEJOR RACHA", "día seguido" if racha == 1 else "días seguidos")
    print("Listo:", sorted(os.listdir(OUT)))
