#!/usr/bin/env python3
"""Genera los bloques del perfil: mosaico en rojo, negro y blanco.

    python scripts/build.py

Crea cuatro juegos en assets/<tema>/<idioma>/ (oscuro o claro, es o en) y los dos README.
Los datos salen de data/actividad.json y data/lenguajes.json. Solo usa la librería estándar.
"""
import datetime as dt, html, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
DISPLAY = "'Arial Black', 'Segoe UI Black', Inter, 'Helvetica Neue', Arial, sans-serif"
NEGRO, BLANCO = "#050505", "#ffffff"          # absolutos: no cambian con el tema
W1, W2, W3 = 400, 807, 1214                   # un tercio, dos tercios, fila completa
CORREO = "Briandcastro11b@gmail.com"
CV = "https://github.com/LordVincenzo/LordVincenzo/raw/main/Briand_Castro_CV.pdf"
e = html.escape
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

TEMAS = {
    "oscuro": dict(FG="#ffffff", BG="#0d0d0d", LINEA="#2b2b2b", VACIO="#1c1c1c", GRIS="#a3a3a3", TENUE="#666666", ROJO="#ff2d3d",
                   R_IZQ="#8f0f1a", R_DER="#c81c2a", SUELO="#161616", SUELO_L="#242424"),
    "claro": dict(FG="#0a0a0a", BG="#f3f3f3", LINEA="#d6d6d6", VACIO="#e2e2e2", GRIS="#555555", TENUE="#9b9b9b", ROJO="#e5202f",
                  R_IZQ="#8f0f1a", R_DER="#bf1826", SUELO="#e6e6e6", SUELO_L="#d2d2d2"),
}
TEXTOS = {
    "es": dict(
        rol="ANALISTA Y DESARROLLADOR DE SOFTWARE", frases=["Automatizo lo repetitivo.", "Construyo apps web y móviles.", "Convierto datos en decisiones."],
        auto="AUTOMATIZACIÓN", sobre="SOBRE MÍ",
        sobre_txt=[[("Tecnólogo en ", 0), ("Análisis y Desarrollo de Software", 1), (". Construyo aplicaciones", 0)],
                   [("web y móviles de punta a punta, y automatizo procesos para que el", 0)], [("trabajo repetitivo lo haga el sistema.", 0)], None,
                   [("Hoy gestiono la plataforma educativa ", 0), ("Prizma", 1), (" en la Corporación", 0)],
                   [("Universitaria Americana, donde automaticé el cargue de cursos con ", 0), ("n8n", 1), (".", 0)], None,
                   [("Me interesan la ", 0), ("IA que corre en local", 1), (", las ", 0), ("apps en tiempo real", 1)], [("y los ", 0), ("flujos de automatización", 1), (".", 0)]],
        sobre_alt="Sobre mí: tecnólogo en Análisis y Desarrollo de Software. Construyo aplicaciones web y móviles de punta a punta y automatizo procesos. Gestiono la plataforma educativa Prizma en la Corporación Universitaria Americana, donde automaticé el cargue de cursos con n8n. Me interesan la IA que corre en local, las apps en tiempo real y los flujos de automatización.",
        commits=("COMMITS", "en {n} proyectos, último año"), dias=("DÍAS ACTIVOS", "con al menos un commit"), racha=("MEJOR RACHA", "días seguidos"),
        hago=[("DESARROLLO", "Web y móvil de punta a punta", "Interfaces, APIs y bases de datos: de la idea a la app funcionando."),
              ("AUTOMATIZACIÓN", "Que lo repetitivo lo haga el sistema", "Flujos con n8n y Power Automate que ahorran horas de trabajo manual."),
              ("DATOS", "Datos que se entienden", "Reportes y tableros en Power BI sobre bases SQL y NoSQL.")],
        stack=["LENGUAJES", "FRONTEND Y MÓVIL", "BACKEND Y DATOS", "AUTOMATIZACIÓN E IA", "HERRAMIENTAS"],
        ruta="TRAYECTORIA", hitos=[("SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana"),
                                   ("ENE — JUL 2025", "Calidad de Proveedores", "Procaps"), ("2023 — 2025", "Tecnólogo ADSO", "SENA")],
        ciudad="CIUDAD DE COMMITS", ciudad_n="Cada edificio es un día; la altura, sus commits.",
        calor="ACTIVIDAD · ÚLTIMO AÑO", calor_n="commits en {n} proyectos · datos al {f}", menos="menos", mas="más",
        meses=["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"], dsem=["lun", "mié", "vie"],
        reloj="HORA PICO", am="a. m.", pm="p. m.", leng="LENGUAJES · {n} PROYECTOS RECIENTES", otros="Otros",
        semana="SEMANA", letras="LMXJVSD", finde="{p} % en fin de semana",
        cv="HOJA DE VIDA", cv1="Descargar", cv2="PDF", cierre=("¿AUTOMATIZAMOS", "ALGO JUNTOS?"),
        cierre_s="Cuéntame qué tarea repetitiva te quita tiempo.", escribe="Escríbeme",
        consola="Animación de una terminal ejecutando un flujo de automatización paso a paso",
        robot="Robot en pixel art programando en un portátil. Soledad, Colombia.", otro=("EN", "README.en.md", "Read in English")),
    "en": dict(
        rol="SOFTWARE ANALYST & DEVELOPER", frases=["I automate the repetitive.", "I build web and mobile apps.", "I turn data into decisions."],
        auto="AUTOMATION", sobre="ABOUT ME",
        sobre_txt=[[("Technologist in ", 0), ("Software Analysis and Development", 1), (". I build web", 0)],
                   [("and mobile apps end to end, and I automate processes so the", 0)], [("repetitive work is done by the system.", 0)], None,
                   [("Today I manage the ", 0), ("Prizma", 1), (" learning platform at Corporación", 0)],
                   [("Universitaria Americana, where I automated course loading with ", 0), ("n8n", 1), (".", 0)], None,
                   [("I'm into ", 0), ("AI that runs locally", 1), (", ", 0), ("real-time apps", 1)], [("and ", 0), ("automation workflows", 1), (".", 0)]],
        sobre_alt="About me: technologist in Software Analysis and Development. I build web and mobile apps end to end and automate processes. I manage the Prizma learning platform at Corporación Universitaria Americana, where I automated course loading with n8n. I'm into AI that runs locally, real-time apps and automation workflows.",
        commits=("COMMITS", "in {n} projects, past year"), dias=("ACTIVE DAYS", "with at least one commit"), racha=("BEST STREAK", "days in a row"),
        hago=[("DEVELOPMENT", "Web and mobile, end to end", "Interfaces, APIs and databases: from the idea to a working app."),
              ("AUTOMATION", "Let the system do the repetitive", "n8n and Power Automate workflows that save hours of manual work."),
              ("DATA", "Data people understand", "Power BI reports and dashboards on SQL and NoSQL databases.")],
        stack=["LANGUAGES", "FRONTEND & MOBILE", "BACKEND & DATA", "AUTOMATION & AI", "TOOLS"],
        ruta="JOURNEY", hitos=[("SEP 2025 — NOW", "Prizma Platform Manager", "Corporación Universitaria Americana"),
                               ("JAN — JUL 2025", "Supplier Quality", "Procaps"), ("2023 — 2025", "ADSO Technologist", "SENA")],
        ciudad="COMMIT CITY", ciudad_n="Each building is a day; its height, the commits.",
        calor="ACTIVITY · PAST YEAR", calor_n="commits in {n} projects · data as of {f}", menos="less", mas="more",
        meses=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], dsem=["Mon", "Wed", "Fri"],
        reloj="PEAK HOUR", am="AM", pm="PM", leng="LANGUAGES · {n} RECENT PROJECTS", otros="Other",
        semana="WEEK", letras="MTWTFSS", finde="{p}% on weekends",
        cv="RÉSUMÉ", cv1="Download", cv2="PDF", cierre=("LET'S AUTOMATE", "SOMETHING?"),
        cierre_s="Tell me which repetitive task eats your time.", escribe="Email me",
        consola="Animated terminal running an automation workflow step by step",
        robot="Pixel-art robot coding on a laptop. Soledad, Colombia.", otro=("ES", "README.md", "Leer en español")),
}
TEMA, IDIOMA, OUT = "oscuro", "es", ""
FG = BG = LINEA = VACIO = GRIS = TENUE = ROJO = R_IZQ = R_DER = SUELO = SUELO_L = ""
T = {}


def usar(tema, idioma):
    global TEMA, IDIOMA, OUT, T
    TEMA, IDIOMA, T = tema, idioma, TEXTOS[idioma]
    globals().update(TEMAS[tema])
    OUT = os.path.join(ROOT, "assets", tema, idioma)
    os.makedirs(OUT, exist_ok=True)


def save(name, W, H, label, body, style="", defs=""):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(label)}">'
                f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>{defs}</defs><style>{style}{REDUCE}</style>{body}</svg>')


def fondo(W, H, tono="base", malla=False):
    """base: bloque del tema · rojo · inverso: blanco en tema oscuro y negro en tema claro."""
    if tono == "rojo":
        return f'<rect width="{W}" height="{H}" rx="16" fill="{ROJO}"/>'
    if tono == "inverso":
        return f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="{FG}"/>'
    m = (f'<pattern id="malla" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0 H0 V30" fill="none" stroke="{FG}" stroke-opacity=".06"/></pattern>'
         f'<rect width="{W}" height="{H}" fill="url(#malla)"/>') if malla else ""
    return (f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{BG}"/>{m}</g>'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{LINEA}" stroke-width="1.5"/>')


def rotulo(x, y, text, color=None, punto=None):
    return (f'<rect x="{x}" y="{y-11}" width="11" height="11" fill="{punto or ROJO}"/>'
            f'<text x="{x+22}" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="{color or FG}">{e(text)}</text>')


def ancho(text, size, f=.7):
    """Ancho fijo para titulares, para que no dependa de la tipografía del visitante."""
    return round(len(text) * size * f)


def hora12(h):
    return f"{(h % 12) or 12} {T['am'] if h < 12 else T['pm']}"


def cargar(nombre):
    return json.load(open(os.path.join(ROOT, "data", nombre), encoding="utf-8"))


# ───────────── nombre ─────────────
def nombre():
    W, H = W2, 400
    typed = ""
    for i, f in enumerate(T["frases"]):
        w, a = round(len(f) * 10.8), i / 3
        kt = f"0;{a:.3f};{a+.11:.3f};{a+.27:.3f};{a+.325:.3f};1"
        typed += (f'<clipPath id="t{i}"><rect x="66" y="336" height="30" width="0"><animate attributeName="width" dur="10.5s" repeatCount="indefinite" values="0;0;{w+2};{w+2};0;0" keyTimes="{kt}"/></rect></clipPath>'
                  f'<text x="66" y="358" clip-path="url(#t{i})" font-family="{MONO}" font-size="18" fill="{FG}" textLength="{w}" lengthAdjust="spacingAndGlyphs">{e(f)}</text>'
                  f'<rect y="340" width="9" height="22" fill="{ROJO}" opacity="0"><animate attributeName="x" dur="10.5s" repeatCount="indefinite" values="68;68;{w+72};{w+72};68;68" keyTimes="{kt}"/>'
                  f'<animate attributeName="opacity" dur="10.5s" repeatCount="indefinite" values="0;1;1;1;0;0" keyTimes="0;{max(a,.001):.3f};{a+.11:.3f};{a+.325:.3f};{a+.33:.3f};1" calcMode="discrete"/></rect>')
    defs = ('<clipPath id="wipe"><rect x="36" y="180" height="130" width="0"><animate attributeName="width" dur="7s" repeatCount="indefinite" values="0;0;740;740;0" keyTimes="0;.12;.42;.8;1" '
            'calcMode="spline" keySplines="0 0 1 1;.4 0 .2 1;0 0 1 1;.4 0 .2 1"/></rect></clipPath>')
    t = f'font-family="{DISPLAY}" font-size="150" font-weight="900" textLength="700" lengthAdjust="spacingAndGlyphs"'
    body = f'''{fondo(W, H, malla=True)}
<rect class="p" x="40" y="34" width="12" height="12" fill="{ROJO}"/>
<text x="64" y="45" font-family="{MONO}" font-size="13.5" letter-spacing="3" fill="{GRIS}">LORDVINCENZO <tspan fill="{TENUE}">/</tspan> README</text>
<text x="{W-40}" y="45" text-anchor="end" font-family="{MONO}" font-size="13.5" letter-spacing="3" fill="{GRIS}">{e(T["rol"])}</text>
<text x="36" y="176" {t} fill="{FG}">BRIAND</text>
<text x="36" y="302" {t} fill="none" stroke="{ROJO}" stroke-width="3">CASTRO</text>
<text x="36" y="302" {t} fill="{ROJO}" clip-path="url(#wipe)">CASTRO</text>
<text x="40" y="358" font-family="{MONO}" font-size="18" font-weight="700" fill="{ROJO}">&gt;</text>{typed}'''
    save("nombre.svg", W, H, f"Briand Castro — {T['rol'].title()}", body, ".p{animation:p 1.4s steps(1) infinite}@keyframes p{50%{opacity:0}}", defs)


# ───────────── robot en pixel art ─────────────
def robot():
    W, H, U = W1, 400, 9          # U: tamaño de cada píxel
    K, G, L, B = NEGRO, "#3a3a3a", "#d9d9d9", BLANCO
    def px(x0, y0, x1, y1, c, extra=""):
        return f'<rect x="{x0*U}" y="{y0*U}" width="{(x1-x0+1)*U}" height="{(y1-y0+1)*U}" fill="{c}"{extra}/>'
    cabeza = (px(15, 0, 16, 0, B, ' class="luz"') + px(15, 1, 16, 2, K) + px(9, 3, 22, 3, K) + px(8, 4, 23, 13, K) + px(9, 14, 22, 14, K)
              + px(6, 7, 7, 10, L) + px(24, 7, 25, 10, L) + px(10, 6, 21, 10, G)
              + f'<g class="ojos">{px(12, 7, 14, 9, B)}{px(17, 7, 19, 9, B)}</g>' + px(14, 12, 17, 12, B) + px(14, 15, 17, 15, L))
    cuerpo = px(10, 16, 21, 24, K) + px(14, 18, 17, 20, B) + px(15, 19, 16, 19, ROJO, ' class="luz"')
    brazos = (f'<g class="bi">{px(7, 17, 9, 22, K)}{px(6, 22, 9, 23, L)}</g><g class="bd">{px(22, 17, 24, 22, K)}{px(22, 22, 25, 23, L)}</g>')
    portatil = px(8, 22, 23, 28, B) + px(8, 22, 23, 22, L) + px(15, 24, 16, 25, K, ' class="luz"') + px(5, 29, 26, 29, K) + px(4, 30, 27, 30, L)
    simbolos = "".join(f'<text class="s s{i}" x="{x}" y="{y}" font-family="{MONO}" font-size="{sz}" font-weight="700" fill="{c}">{e(t)}</text>'
                       for i, (x, y, t, sz, c) in enumerate([(26, 118, "{ }", 26, NEGRO), (318, 96, "</>", 24, BLANCO), (40, 232, "=>", 22, BLANCO), (326, 214, "01", 22, NEGRO)]))
    body = f'''{fondo(W, H, "rojo")}{simbolos}
<ellipse class="sombra" cx="200" cy="344" rx="112" ry="9" fill="{NEGRO}" fill-opacity=".22"/>
<g class="bot" transform="translate(56,44)" shape-rendering="crispEdges">{cabeza}{cuerpo}{brazos}{portatil}</g>
<text x="28" y="{H-22}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="2.5" fill="{NEGRO}">SOLEDAD, COLOMBIA</text>
<text x="{W-28}" y="{H-22}" text-anchor="end" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="2.5" fill="{BLANCO}">{T["auto"]}</text>'''
    style = (".bot{animation:bot 3s ease-in-out infinite}@keyframes bot{50%{transform:translate(56px,38px)}}"
             ".sombra{animation:so 3s ease-in-out infinite;transform-origin:200px 344px}@keyframes so{50%{transform:scaleX(.9)}}"
             ".ojos{animation:oj 4.6s infinite;transform-box:fill-box;transform-origin:center}@keyframes oj{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.12)}}"
             ".luz{animation:lz 1.2s steps(1) infinite}@keyframes lz{50%{opacity:.25}}"
             f".bi{{animation:br .36s steps(1) infinite}}.bd{{animation:br .36s steps(1) infinite;animation-delay:.18s}}@keyframes br{{50%{{transform:translateY(-{U}px)}}}}"
             ".s{animation:s 5s ease-in-out infinite;opacity:0}.s1{animation-delay:1.2s}.s2{animation-delay:2.4s}.s3{animation-delay:3.6s}"
             "@keyframes s{0%{opacity:0;transform:translateY(14px)}25%,60%{opacity:.9}100%{opacity:0;transform:translateY(-22px)}}")
    save("robot.svg", W, H, T["robot"], body, style)


# ───────────── sobre mí ─────────────
def sobre():
    W, H = W2, 304
    y, txt = 96, ""
    for l in T["sobre_txt"]:
        if l is None:
            y += 14
            continue
        txt += f'<text x="40" y="{y}" font-family="{SANS}" font-size="19" fill="{GRIS}">' + "".join(
            f'<tspan fill="{FG}" font-weight="700">{e(t)}</tspan>' if b else e(t) for t, b in l) + "</text>"
        y += 28
    body = f'{fondo(W, H)}{rotulo(40, 52, T["sobre"])}<rect class="b" x="40" y="66" width="60" height="3" fill="{ROJO}"/>{txt}'
    save("sobre.svg", W, H, T["sobre_alt"], body, ".b{animation:b 4s ease-in-out infinite;transform-origin:40px 0}@keyframes b{50%{transform:scaleX(4)}}")


# ───────────── cifras ─────────────
def cifra(fn, tono, valor, etiqueta, nota):
    W, H = W1, 220
    tinta, sec, punto, num = {"inverso": (BG, TENUE if TEMA == "oscuro" else "#bdbdbd", ROJO, ROJO), "base": (FG, GRIS, ROJO, FG),
                              "rojo": (BLANCO, NEGRO, NEGRO, BLANCO)}[tono]
    if tono == "inverso" and TEMA == "oscuro":
        sec = "#555555"
    body = (f'{fondo(W, H, tono)}{rotulo(28, 44, etiqueta, tinta, punto)}'
            f'<text class="v" x="24" y="156" font-family="{DISPLAY}" font-size="104" font-weight="900" fill="{num}" textLength="{60*len(valor)+20}" lengthAdjust="spacingAndGlyphs">{e(valor)}</text>'
            f'<text x="28" y="192" font-family="{SANS}" font-size="15" font-weight="600" fill="{sec}">{e(nota)}</text>')
    save(fn, W, H, f"{etiqueta}: {valor}. {nota}", body, ".v{animation:v 5s ease-in-out infinite}@keyframes v{50%{opacity:.82}}")


# ───────────── qué hago ─────────────
def hago():
    W, H = W3, 300
    body = fondo(W, H)
    for i, (tag, tit, desc) in enumerate(T["hago"]):
        y = i * 100
        body += ((f'<line x1="36" x2="{W-36}" y1="{y}" y2="{y}" stroke="{LINEA}"/>' if i else "")
                 + f'<g clip-path="url(#clip)"><rect class="s s{i}" x="0" y="{y+1}" width="8" height="98" fill="{ROJO}"/></g>'
                 f'<text x="40" y="{y+68}" font-family="{DISPLAY}" font-size="56" font-weight="900" fill="none" stroke="{TENUE}" stroke-width="1.6" textLength="84" lengthAdjust="spacingAndGlyphs">0{i+1}</text>'
                 f'<text x="160" y="{y+42}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="3" fill="{ROJO}">{tag}</text>'
                 f'<text x="160" y="{y+74}" font-family="{SANS}" font-size="25" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 f'<text x="646" y="{y+58}" font-family="{SANS}" font-size="14.5" fill="{GRIS}">{e(desc)}</text>'
                 f'<path class="fl s{i}" d="M{W-76} {y+52} h26 m-10 -10 l10 10 l-10 10" fill="none" stroke="{FG}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    style = (".s{animation:s 6s ease-in-out infinite;opacity:.18}.s1{animation-delay:2s}.s2{animation-delay:4s}@keyframes s{0%,34%,100%{opacity:.18}8%,26%{opacity:1}}"
             ".fl{animation:fl 6s ease-in-out infinite;opacity:.25}.fl.s1{animation-delay:2s}.fl.s2{animation-delay:4s}@keyframes fl{0%,34%,100%{opacity:.25;transform:translateX(0)}8%,26%{opacity:1;transform:translateX(8px)}}")
    save("hago.svg", W, H, " ".join(f"{t}. {d}" for _, t, d in T["hago"]), body, style)


# ───────────── stack en cintas + trayectoria ─────────────
STACK = [(["TypeScript", "JavaScript", "C#", "PHP", "SQL"], True), (["React", "Next.js", "Tailwind CSS", "Ionic", "Capacitor"], False),
         (["Node.js", ".NET 8", "PostgreSQL", "MySQL", "MongoDB", "Supabase", "Firebase"], False),
         (["n8n", "Power Automate", "Power BI", "Ollama", "Whisper"], True), (["Git", "Docker", "Unity", "VS Code", "SAP"], False)]


def stack():
    W, H = W2, 420
    body, style = fondo(W, H) + rotulo(36, 50, "STACK"), ""
    for i, ((items, rojo), lab) in enumerate(zip(STACK, T["stack"])):
        y = 78 + i * 66
        unidad, x = "", 0
        for t in items:
            w = int(len(t) * 10.2) + 34
            unidad += (f'<rect x="{x}" y="0" width="{w}" height="38" rx="6" fill="{ROJO if rojo else "none"}" stroke="{ROJO if rojo else TENUE}" stroke-width="1.4"/>'
                       f'<text x="{x+w/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{BLANCO if rojo else FG}" textLength="{w-34}" lengthAdjust="spacingAndGlyphs">{e(t)}</text>')
            x += w + 12
        reps = int(-(-(W + x) // x) + 1)
        cinta = "".join(f'<g transform="translate({k*x},0)">{unidad}</g>' for k in range(reps))
        style += f".c{i}{{animation:c{i} {x/28:.1f}s linear infinite {'normal' if i % 2 == 0 else 'reverse'}}}@keyframes c{i}{{to{{transform:translateX(-{x}px)}}}}"
        body += (f'<text x="36" y="{y+8}" font-family="{MONO}" font-size="11" letter-spacing="2.4" fill="{TENUE}">{e(lab)}</text>'
                 f'<g clip-path="url(#clip)"><g transform="translate(0,{y+16})"><g class="c{i}">{cinta}</g></g></g>')
    body += f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{LINEA}" stroke-width="1.5"/>'
    save("stack.svg", W, H, "Stack: " + "; ".join(f"{l}: {', '.join(it)}" for (it, _), l in zip(STACK, T["stack"])), body, style)


def ruta():
    W, H = W1, 420
    body = fondo(W, H) + rotulo(32, 50, T["ruta"]) + f'<line x1="44" x2="44" y1="96" y2="372" stroke="{LINEA}" stroke-width="2"/><line class="l" x1="44" x2="44" y1="96" y2="372" stroke="{ROJO}" stroke-width="2.5"/>'
    for i, (fecha, tit, org) in enumerate(T["hitos"]):
        y, hoy = 104 + i * 104, i == 0
        body += ((f'<circle class="ping" cx="44" cy="{y}" r="9" fill="none" stroke="{ROJO}" stroke-width="2"/>' if hoy else "")
                 + f'<circle cx="44" cy="{y}" r="9" fill="{ROJO if hoy else BG}" stroke="{ROJO if hoy else FG}" stroke-width="2.5"/>'
                 f'<text x="72" y="{y+4}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{ROJO}">{fecha}</text>'
                 f'<text x="72" y="{y+32}" font-family="{SANS}" font-size="19" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 f'<text x="72" y="{y+54}" font-family="{SANS}" font-size="14" fill="{GRIS}">{e(org)}</text>')
    style = (".l{stroke-dasharray:276;animation:l 6s ease-in-out infinite}@keyframes l{0%{stroke-dashoffset:276}50%,100%{stroke-dashoffset:0}}"
             ".ping{animation:ping 2s ease-out infinite;transform-box:fill-box;transform-origin:center}@keyframes ping{to{transform:scale(2.6);opacity:0}}")
    save("ruta.svg", W, H, f"{T['ruta'].title()}: " + "; ".join(f"{t}, {o} ({f})" for f, t, o in T["hitos"]), body, style)


# ───────────── actividad: semanas, ciudad, mapa, reloj ─────────────
def semanas(data):
    fin = dt.date.fromisoformat(data["hasta"])
    d, weeks = fin - dt.timedelta(days=(fin.weekday() + 1) % 7 + 52 * 7), []
    while d <= fin:
        w = []
        for _ in range(7):
            if d <= fin:
                w.append((d, data["dias"].get(d.isoformat(), 0)))
            d += dt.timedelta(days=1)
        weeks.append(w)
    return weeks


def ciudad(data):
    """Vista isométrica: una baldosa por día y un edificio por cada día con commits."""
    W, H = W3, 500
    weeks = semanas(data)
    a, b, ox, oy = 18.4, 6.1, 172, 92
    celdas = sorted(((wi + di, wi, di, c) for wi, col in enumerate(weeks) for di, (_, c) in enumerate(col)))
    suelo, torres = "", ""
    for _, wi, di, c in celdas:
        x, y = ox + (wi - di) * a, oy + (wi + di) * b
        ax, by = a - 1.3, b - .45
        if not c:
            suelo += f'<path d="M{x:.1f} {y-by:.1f} L{x+ax:.1f} {y:.1f} L{x:.1f} {y+by:.1f} L{x-ax:.1f} {y:.1f} Z" fill="{SUELO}" stroke="{SUELO_L}" stroke-width=".8"/>'
            continue
        h, d = 10 + 16 * math.sqrt(c), wi * .11
        vent = ""
        if h > 44:
            for k in range(int((h - 16) // 15)):
                vy = y - h + 15 + k * 15
                vent += f'<path class="vt" style="animation-delay:{(wi*7+di+k*3) % 11 * .4:.1f}s" d="M{x+4:.1f} {vy+b*.75:.1f} l5.5 -1.8 v5 l-5.5 1.8 Z M{x+10.5:.1f} {vy+b*.75-2.15:.1f} l5.5 -1.8 v5 l-5.5 1.8 Z" fill="{BLANCO}"/>'
        torres += (f'<g><path d="M{x-ax:.1f} {y-h:.1f} L{x:.1f} {y+by-h:.1f} V{y+by:.1f} L{x-ax:.1f} {y:.1f} Z" fill="{R_IZQ}"/>'
                   f'<path d="M{x:.1f} {y+by-h:.1f} L{x+ax:.1f} {y-h:.1f} V{y:.1f} L{x:.1f} {y+by:.1f} Z" fill="{R_DER}"/>{vent}'
                   f'<path class="tp" style="animation-delay:{d:.2f}s" d="M{x:.1f} {y-by-h:.1f} L{x+ax:.1f} {y-h:.1f} L{x:.1f} {y+by-h:.1f} L{x-ax:.1f} {y-h:.1f} Z" fill="{ROJO}"/></g>')
    meses, last = "", None
    for wi, col in enumerate(weeks):
        m = col[0][0].month
        if m != last and wi < len(weeks) - 2:
            meses += f'<text x="{ox+(wi-7.6)*a:.0f}" y="{oy+(wi+7.6)*b+12:.0f}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GRIS}">{T["meses"][m-1]}</text>'
            last = m
    dias = [x for w in weeks for x in w]
    total, tope = sum(c for _, c in dias), max(dias, key=lambda t: t[1])
    body = (f'{fondo(W, H, malla=True)}{rotulo(36, 50, T["ciudad"])}'
            f'<text x="36" y="78" font-family="{SANS}" font-size="14" fill="{GRIS}">{e(T["ciudad_n"])}</text>'
            f'{suelo}{torres}{meses}'
            f'<text x="{W-36}" y="56" text-anchor="end" font-family="{DISPLAY}" font-size="58" font-weight="900" fill="{FG}" textLength="{ancho(str(total), 58)}" lengthAdjust="spacingAndGlyphs">{total}</text>'
            f'<text x="{W-36}" y="80" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{GRIS}">COMMITS</text>'
            f'<text x="36" y="{H-30}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{GRIS}">MAX <tspan fill="{ROJO}" font-weight="700">{tope[1]}</tspan> · {tope[0].day} {T["meses"][tope[0].month-1]} {tope[0].year}</text>')
    style = (f".tp{{animation:tp 6.4s ease-in-out infinite}}@keyframes tp{{0%,6%,100%{{fill:{ROJO}}}2.5%{{fill:{BLANCO}}}}}"
             ".vt{animation:vt 4.4s steps(1) infinite;opacity:.85}@keyframes vt{55%{opacity:.15}}")
    save("ciudad.svg", W, H, f"{T['ciudad'].title()}: {T['ciudad_n']} {total} commits.", body, style)
    return dias


def calor(data):
    W, H = W2, 300
    weeks = semanas(data)
    gx, gy, cell, step = 74, 104, 11, 13.25
    OPS = [0, .34, .56, .78, 1]
    grid, months, last = "", "", None
    for wi, col in enumerate(weeks):
        m = col[0][0].month
        if m != last and wi < len(weeks) - 2:
            months += f'<text x="{gx+wi*step:.1f}" y="{gy-12}" font-family="{MONO}" font-size="11" fill="{GRIS}">{T["meses"][m-1]}</text>'
            last = m
        for d, c in col:
            wd = (d.weekday() + 1) % 7
            lvl = 0 if c == 0 else 1 if c < 2 else 2 if c < 5 else 3 if c < 10 else 4
            if lvl:
                grid += (f'<rect class="z" style="animation-delay:{wi/53*9:.2f}s" x="{gx+wi*step:.1f}" y="{gy+wd*step:.1f}" width="{cell}" height="{cell}" rx="2.5" fill="{ROJO}" fill-opacity="{OPS[lvl]}"><title>{d}: {c}</title></rect>')
            else:
                grid += f'<rect x="{gx+wi*step:.1f}" y="{gy+wd*step:.1f}" width="{cell}" height="{cell}" rx="2.5" fill="{VACIO}"/>'
    barra = f'<rect class="scan" x="{gx-3}" y="{gy-5}" width="3" height="{7*step+7:.0f}" fill="{FG}" fill-opacity=".8"/>'
    dias = "".join(f'<text x="36" y="{gy+i*step+9.5:.1f}" font-family="{MONO}" font-size="11" fill="{GRIS}">{t}</text>' for i, t in zip((1, 3, 5), T["dsem"]))
    fy, hasta = gy + 7 * step + 34, dt.date.fromisoformat(data["hasta"])
    nota = T["calor_n"].format(n=data["proyectos"], f=f"{hasta.day} {T['meses'][hasta.month-1]} {hasta.year}")
    body = (f'{fondo(W, H)}{rotulo(36, 50, T["calor"])}{months}{dias}{grid}{barra}'
            f'<text x="36" y="{fy:.0f}" font-family="{SANS}" font-size="13.5" fill="{GRIS}">{nota}</text>'
            f'<text x="{W-140}" y="{fy:.0f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{GRIS}">{T["menos"]}</text>'
            + "".join(f'<rect x="{W-132+i*15}" y="{fy-10:.0f}" width="11" height="11" rx="2.5" ' + (f'fill="{ROJO}" fill-opacity="{o}"' if o else f'fill="{VACIO}"') + '/>' for i, o in enumerate(OPS))
            + f'<text x="{W-52}" y="{fy:.0f}" font-family="{MONO}" font-size="11" fill="{GRIS}">{T["mas"]}</text>')
    style = (f".scan{{animation:scan 9s linear infinite}}@keyframes scan{{to{{transform:translateX({53*step:.0f}px)}}}}"
             f".z{{animation:z 9s linear infinite}}@keyframes z{{0%{{fill:{FG};fill-opacity:1}}7%,100%{{fill:{ROJO}}}}}")
    save("calor.svg", W, H, f"{T['calor']}: {nota}.", body, style)


def reloj(data):
    W, H = W1, 300
    horas = data["horas"]
    pico, mx = horas.index(max(horas)), max(horas + [1])
    cx, cy, r0 = 200, 176, 50
    rayos = ""
    for h, v in enumerate(horas):
        ang = math.radians(h * 15 - 90)
        r1 = r0 + 8 + 48 * v / mx
        rayos += (f'<line class="y" style="animation-delay:{h*.12:.2f}s" x1="{cx+r0*math.cos(ang):.1f}" y1="{cy+r0*math.sin(ang):.1f}" x2="{cx+r1*math.cos(ang):.1f}" y2="{cy+r1*math.sin(ang):.1f}" '
                  f'stroke="{ROJO if h == pico else FG}" stroke-opacity="{1 if h == pico else .4}" stroke-width="{9 if h == pico else 7}" stroke-linecap="round"/>')
    marcas = "".join(f'<text x="{cx + 138*math.cos(math.radians(h*15-90)):.0f}" y="{cy + 114*math.sin(math.radians(h*15-90)) + 4:.0f}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{TENUE}">{hora12(h)}</text>' for h in (0, 6, 12, 18))
    body = (f'{fondo(W, H)}{rotulo(28, 44, T["reloj"])}{rayos}{marcas}'
            f'<g class="g"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r0+10}" stroke="{ROJO}" stroke-width="2" stroke-linecap="round"/></g><circle cx="{cx}" cy="{cy}" r="4" fill="{ROJO}"/>'
            f'<text x="{cx}" y="{cy+30}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="{FG}">{hora12(pico)}</text>')
    style = (".y{animation:y 2.9s ease-in-out infinite}@keyframes y{50%{stroke-opacity:.15}}"
             f".g{{animation:g 24s linear infinite;transform-origin:{cx}px {cy}px}}@keyframes g{{to{{transform:rotate(360deg)}}}}")
    save("reloj.svg", W, H, f"{T['reloj'].title()}: {hora12(pico)}.", body, style)


# ───────────── lenguajes + semana ─────────────
def lenguajes(data):
    W, H = W2, 200
    langs = [(T["otros"] if n == "Otros" else n, p) for n, p in cargar("lenguajes.json")["lenguajes"]]
    cols = [ROJO, FG, "#ff6b76", "#9c1622", GRIS, "#ffb3ba" if TEMA == "oscuro" else "#f29aa2", TENUE]
    x0, bw = 36, W - 72
    body = fondo(W, H) + rotulo(36, 50, T["leng"].format(n=data["proyectos"])) + f'<clipPath id="lb"><rect x="{x0}" y="72" width="{bw}" height="22" rx="5"/></clipPath><g clip-path="url(#lb)">'
    cx = x0
    for i, ((n, p), c) in enumerate(zip(langs, cols)):
        w = bw * p / 100
        body += f'<rect class="q" style="animation-delay:{i*.3:.1f}s" x="{cx:.1f}" y="72" width="{w+.6:.1f}" height="22" fill="{c}"/>'
        cx += w
    body += "</g>"
    for i, ((n, p), c) in enumerate(zip(langs, cols)):
        x, y = x0 + (i % 4) * bw / 4, 130 + (i // 4) * 32
        body += (f'<rect x="{x:.1f}" y="{y-10}" width="10" height="10" fill="{c}"/><text x="{x+18:.1f}" y="{y}" font-family="{SANS}" font-size="15" font-weight="700" fill="{FG}">{e(n)}'
                 f'<tspan dx="8" font-family="{MONO}" font-size="13" font-weight="400" fill="{GRIS}">{p:.0f}%</tspan></text>')
    save("lenguajes.svg", W, H, T["leng"].format(n=data["proyectos"]).title() + ": " + ", ".join(f"{n} {p:.0f}%" for n, p in langs), body,
         ".q{animation:q 4.2s ease-in-out infinite}@keyframes q{50%{opacity:.6}}")


def semana(data):
    W, H = W1, 200
    sem = data["semana"]
    mx, top = max(sem + [1]), sorted(range(7), key=lambda i: -sem[i])[:2]
    finde = T["finde"].format(p=round(100 * (sem[5] + sem[6]) / max(1, sum(sem))))
    body = fondo(W, H) + rotulo(28, 44, T["semana"]) + f'<text x="{W-28}" y="44" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="{GRIS}">{finde}</text>'
    for i, v in enumerate(sem):
        x, bh = 30 + i * 50, max(4, 78 * v / mx)
        body += (f'<rect class="u" style="animation-delay:{i*.16:.2f}s" x="{x}" y="{150-bh:.1f}" width="34" height="{bh:.1f}" rx="5" fill="{ROJO if i in top else FG}" fill-opacity="{1 if i in top else .32}"/>'
                 f'<text x="{x+17}" y="174" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{FG if i in top else TENUE}">{T["letras"][i]}</text>')
    save("semana.svg", W, H, f"{T['semana'].title()}: {finde}.", body,
         ".u{animation:u 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}@keyframes u{50%{transform:scaleY(.8)}}")


# ───────────── hoja de vida + cierre ─────────────
def cv():
    W, H = W1, 200
    body = f'''{fondo(W, H, "inverso")}{rotulo(28, 44, T["cv"], BG)}
<text x="26" y="112" font-family="{DISPLAY}" font-size="40" font-weight="900" fill="{BG}" textLength="{ancho(T["cv1"], 40, .6)}" lengthAdjust="spacingAndGlyphs">{T["cv1"]}</text>
<text x="26" y="158" font-family="{DISPLAY}" font-size="40" font-weight="900" fill="{ROJO}" textLength="{ancho(T["cv2"], 40, .72)}" lengthAdjust="spacingAndGlyphs">{T["cv2"]}</text>
<rect x="{W-112}" y="78" width="84" height="84" rx="10" fill="{ROJO}"/>
<path class="dl" d="M{W-70} 100 v34 m-14 -13 l14 14 l14 -14" fill="none" stroke="{BLANCO}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M{W-90} 148 h40" stroke="{BLANCO}" stroke-width="5" stroke-linecap="round"/>'''
    save("cv.svg", W, H, f"{T['cv'].title()}: {T['cv1']} {T['cv2']}", body, ".dl{animation:dl 1.5s ease-in-out infinite}@keyframes dl{50%{transform:translateY(6px)}}")


def cierre():
    W, H = W2, 200
    c1, c2 = T["cierre"]
    defs = '<pattern id="ray" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)"><rect width="13" height="26" fill="#000" fill-opacity=".07"/></pattern>'
    body = f'''{fondo(W, H, "rojo")}<g clip-path="url(#clip)"><rect class="ray" x="-60" width="{W+120}" height="{H}" fill="url(#ray)"/></g>
<text x="36" y="80" font-family="{DISPLAY}" font-size="42" font-weight="900" fill="{NEGRO}" textLength="{ancho(c1, 42, .73)}" lengthAdjust="spacingAndGlyphs">{e(c1)}</text>
<text x="36" y="128" font-family="{DISPLAY}" font-size="42" font-weight="900" fill="{BLANCO}" textLength="{ancho(c2, 42, .73)}" lengthAdjust="spacingAndGlyphs">{e(c2)}</text>
<text x="36" y="162" font-family="{SANS}" font-size="15" font-weight="600" fill="{NEGRO}">{e(T["cierre_s"])}</text>
<rect x="{W-246}" y="68" width="210" height="64" rx="8" fill="{NEGRO}"/>
<text x="{W-160}" y="108" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="{BLANCO}">{e(T["escribe"])}</text>
<path class="fl" d="M{W-92} 100 h24 m-9 -9 l9 9 l-9 9" fill="none" stroke="{ROJO}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'''
    save("cierre.svg", W, H, f"{c1} {c2} {T['escribe']}.", body,
         ".ray{animation:ray 3s linear infinite}@keyframes ray{to{transform:translateX(26px)}}.fl{animation:fl 1.4s ease-in-out infinite}@keyframes fl{50%{transform:translateX(7px)}}", defs)


def idioma_btn():
    cod = T["otro"][0]
    body = (f'<rect x="1" y="1" width="134" height="34" rx="6" fill="{BG}" stroke="{LINEA}" stroke-width="1.5"/>'
            f'<rect x="14" y="12" width="11" height="11" fill="{ROJO}"/><text x="36" y="23" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{TENUE}">'
            f'{"ES" if cod == "EN" else "EN"} <tspan fill="{TENUE}">/</tspan> <tspan fill="{FG}">{cod} →</tspan></text>')
    with open(os.path.join(OUT, "idioma.svg"), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 136 36" width="136" height="36" role="img" aria-label="{e(T["otro"][2])}">{body}</svg>')


# ───────────── README ─────────────
def readme(idioma, alts):
    T_ = TEXTOS[idioma]
    def img(nombre, ancho_, alt, enlace=None, alto=None):
        ext = "gif" if nombre == "consola" else "svg"
        dim = f'height="{alto}"' if alto else f'width="{ancho_}"'
        pic = (f'<picture><source media="(prefers-color-scheme: light)" srcset="assets/claro/{idioma}/{nombre}.{ext}">'
               f'<img src="assets/oscuro/{idioma}/{nombre}.{ext}" {dim} alt="{e(alt)}"></picture>')
        return f'<a href="{enlace}">{pic}</a>' if enlace else pic
    filas = [("nombre", "66.4%"), ("robot", "32.9%"), ("consola", "32.9%"), ("sobre", "66.4%"), ("cifra-commits", "32.9%"), ("cifra-dias", "32.9%"), ("cifra-racha", "32.9%"),
             ("hago", "100%"), ("stack", "66.4%"), ("ruta", "32.9%"), ("ciudad", "100%"), ("calor", "66.4%"), ("reloj", "32.9%"), ("lenguajes", "66.4%"), ("semana", "32.9%"),
             ("cv", "32.9%", CV), ("cierre", "66.4%", f"mailto:{CORREO}")]
    out = [f'<p align="right">{img("idioma", None, T_["otro"][2], T_["otro"][1], alto=30)}</p>', "", "<p>"]
    out += [img(f[0], f[1], alts[f[0]], f[2] if len(f) > 2 else None) for f in filas]
    out += ["</p>", ""]
    with open(os.path.join(ROOT, T_["otro"][1] == "README.md" and "README.en.md" or "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def alts_de(idioma):
    """Lee el texto alternativo que cada bloque guardó en su aria-label."""
    import re
    d = os.path.join(ROOT, "assets", "oscuro", idioma)
    alts = {n[:-4]: html.unescape(re.search(r'aria-label="([^"]*)"', open(os.path.join(d, n), encoding="utf-8").read()).group(1)) for n in os.listdir(d) if n.endswith(".svg")}
    alts["consola"] = TEXTOS[idioma]["consola"]
    return alts


if __name__ == "__main__":
    data = cargar("actividad.json")
    for tema in TEMAS:
        for idi in TEXTOS:
            usar(tema, idi)
            nombre(); robot(); sobre(); hago(); stack(); ruta(); calor(data); reloj(data); lenguajes(data); semana(data); cv(); cierre(); idioma_btn()
            dias = ciudad(data)
            total, activos = sum(c for _, c in dias), sum(1 for _, c in dias if c)
            racha = cur = 0
            for _, c in dias:
                cur = cur + 1 if c else 0
                racha = max(racha, cur)
            cifra("cifra-commits.svg", "inverso", str(total), T["commits"][0], T["commits"][1].format(n=data["proyectos"]))
            cifra("cifra-dias.svg", "base", str(activos), *T["dias"])
            cifra("cifra-racha.svg", "rojo", str(racha), *T["racha"])
    for idi in TEXTOS:
        readme(idi, alts_de(idi))
    print("Listo")
