#!/usr/bin/env python3
"""Genera los bloques del perfil: mosaico en negro, blanco y gris.

    python scripts/build.py

Crea cuatro juegos en assets/<tema>/<idioma>/ (oscuro o claro, es o en) y los dos README.
El banner del agujero negro se genera aparte: ver scripts/agujero/LEEME.md.
Los datos salen de data/actividad.json y data/lenguajes.json. Solo usa la librería estándar.
"""
import datetime as dt, html, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
DISPLAY = "'Arial Black', 'Segoe UI Black', Inter, 'Helvetica Neue', Arial, sans-serif"
NEGRO, BLANCO = "#050505", "#ffffff"          # absolutos: no cambian con el tema
W1, W2, W3 = 390, 802, 1214                   # un tercio, dos tercios, fila completa
G, V = 22, 22                                 # separación entre bloques: horizontal y vertical
# Lugar de cada bloque en su fila. La separación va dentro del propio SVG, como margen transparente.
POS = {"sobre": "ini", "consola": "fin", "galaxia": "ini", "ruta": "fin", "cifra-commits": "ini", "cifra-dias": "med", "cifra-hora": "fin", "cv": "ini", "cierre": "fin"}


def margenes(nombre):
    pos = POS.get(nombre, "todo")
    return (G / 2 if pos in ("med", "fin") else 0), (G / 2 if pos in ("ini", "med") else 0)


def ancho_pct(nombre, base, en_fila):
    """Ancho en % para el README: proporcional a sus unidades, dejando sitio a los espacios entre imágenes."""
    izq, der = margenes(nombre)
    return f"{(base + izq + der) / W3 * (100 - .6 * (en_fila - 1)):.2f}%"
CORREO = "Briandcastro11b@gmail.com"
CV = "https://github.com/LordVincenzo/LordVincenzo/raw/main/Briand_Castro_CV.pdf"
e = html.escape
REDUCE = (".viaje{animation:viaje 9s linear infinite}@keyframes viaje{to{stroke-dashoffset:-1000}}"
          "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")

TEMAS = {
    # ACENTO: lo que se resalta (blanco sobre negro, negro sobre claro). MEDIO: el gris de los bloques de color.
    "oscuro": dict(FG="#ffffff", BG="#0d0d0d", LINEA="#2b2b2b", VACIO="#1c1c1c", GRIS="#a3a3a3", TENUE="#666666", ACENTO="#ffffff", MEDIO="#707070",
                   R_IZQ="#474747", R_DER="#8c8c8c", SUELO="#161616", SUELO_L="#242424",
                   ESCALA=["#ffffff", "#cfcfcf", "#a6a6a6", "#7d7d7d", "#5c5c5c", "#444444", "#303030"]),
    "claro": dict(FG="#0a0a0a", BG="#f3f3f3", LINEA="#d6d6d6", VACIO="#e2e2e2", GRIS="#555555", TENUE="#9b9b9b", ACENTO="#0a0a0a", MEDIO="#707070",
                  R_IZQ="#3a3a3a", R_DER="#6a6a6a", SUELO="#e6e6e6", SUELO_L="#d2d2d2",
                  ESCALA=["#0a0a0a", "#3a3a3a", "#5e5e5e", "#858585", "#a6a6a6", "#c0c0c0", "#d4d4d4"]),
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
        commits=("COMMITS", "en {n} proyectos, último año"), dias=("DÍAS ACTIVOS", "con al menos un commit"), racha=("MEJOR RACHA", "días seguidos"), hora=("HORA PICO", "cuando más programo"),
        hago=[("DESARROLLO", "Web y móvil de punta a punta", "Interfaces, APIs y bases de datos: de la idea a la app funcionando."),
              ("AUTOMATIZACIÓN", "Que lo repetitivo lo haga el sistema", "Flujos con n8n y Power Automate que ahorran horas de trabajo manual."),
              ("DATOS", "Datos que se entienden", "Reportes y tableros en Power BI sobre bases SQL y NoSQL.")],
        stack=["LENGUAJES", "FRONTEND Y MÓVIL", "BACKEND Y DATOS", "AUTOMATIZACIÓN E IA", "HERRAMIENTAS"],
        ruta="TRAYECTORIA", hitos=[("SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana"),
                                   ("ENE — JUL 2025", "Calidad de Proveedores", "Procaps"), ("2023 — 2025", "Tecnólogo ADSO", "SENA")],
        gal="MI AÑO EN COMMITS", gal_n="Cada estrella es un día con commits; la galaxia gira.",
        ciudad="CIUDAD DE COMMITS", ciudad_n="Cada edificio es un día; la altura, sus commits.",
        calor="ACTIVIDAD · ÚLTIMO AÑO", calor_n="commits en {n} proyectos · datos al {f}", menos="menos", mas="más",
        meses=["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"], dsem=["lun", "mié", "vie"],
        reloj="HORA PICO", am="a. m.", pm="p. m.", leng="LENGUAJES · {n} PROYECTOS RECIENTES", otros="Otros",
        semana="SEMANA", letras="LMXJVSD", finde="{p} % en fin de semana",
        cv="HOJA DE VIDA", cv1="Descargar", cv2="PDF", cierre=("¿AUTOMATIZAMOS", "ALGO JUNTOS?"),
        cierre_s="Cuéntame qué tarea repetitiva te quita tiempo.", escribe="Escríbeme",
        consola="Animación de una terminal ejecutando un flujo de automatización paso a paso",
        banner="Briand Castro, analista y desarrollador de software. Animación de un agujero negro con su disco de luz girando.",
        flujo="Flujo de automatización animado. Soledad, Colombia.", otro=("EN", "README.en.md", "Read in English")),
    "en": dict(
        rol="SOFTWARE ANALYST & DEVELOPER", frases=["I automate the repetitive.", "I build web and mobile apps.", "I turn data into decisions."],
        auto="AUTOMATION", sobre="ABOUT ME",
        sobre_txt=[[("Technologist in ", 0), ("Software Analysis and Development", 1), (". I build web", 0)],
                   [("and mobile apps end to end, and I automate processes so the", 0)], [("repetitive work is done by the system.", 0)], None,
                   [("Today I manage the ", 0), ("Prizma", 1), (" learning platform at Corporación", 0)],
                   [("Universitaria Americana, where I automated course loading with ", 0), ("n8n", 1), (".", 0)], None,
                   [("I'm into ", 0), ("AI that runs locally", 1), (", ", 0), ("real-time apps", 1)], [("and ", 0), ("automation workflows", 1), (".", 0)]],
        sobre_alt="About me: technologist in Software Analysis and Development. I build web and mobile apps end to end and automate processes. I manage the Prizma learning platform at Corporación Universitaria Americana, where I automated course loading with n8n. I'm into AI that runs locally, real-time apps and automation workflows.",
        commits=("COMMITS", "in {n} projects, past year"), dias=("ACTIVE DAYS", "with at least one commit"), racha=("BEST STREAK", "days in a row"), hora=("PEAK HOUR", "when I code the most"),
        hago=[("DEVELOPMENT", "Web and mobile, end to end", "Interfaces, APIs and databases: from the idea to a working app."),
              ("AUTOMATION", "Let the system do the repetitive", "n8n and Power Automate workflows that save hours of manual work."),
              ("DATA", "Data people understand", "Power BI reports and dashboards on SQL and NoSQL databases.")],
        stack=["LANGUAGES", "FRONTEND & MOBILE", "BACKEND & DATA", "AUTOMATION & AI", "TOOLS"],
        ruta="JOURNEY", hitos=[("SEP 2025 — NOW", "Prizma Platform Manager", "Corporación Universitaria Americana"),
                               ("JAN — JUL 2025", "Supplier Quality", "Procaps"), ("2023 — 2025", "ADSO Technologist", "SENA")],
        gal="MY YEAR IN COMMITS", gal_n="Each star is a day with commits; the galaxy spins.",
        ciudad="COMMIT CITY", ciudad_n="Each building is a day; its height, the commits.",
        calor="ACTIVITY · PAST YEAR", calor_n="commits in {n} projects · data as of {f}", menos="less", mas="more",
        meses=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], dsem=["Mon", "Wed", "Fri"],
        reloj="PEAK HOUR", am="AM", pm="PM", leng="LANGUAGES · {n} RECENT PROJECTS", otros="Other",
        semana="WEEK", letras="MTWTFSS", finde="{p}% on weekends",
        cv="RÉSUMÉ", cv1="Download", cv2="PDF", cierre=("LET'S AUTOMATE", "SOMETHING?"),
        cierre_s="Tell me which repetitive task eats your time.", escribe="Email me",
        consola="Animated terminal running an automation workflow step by step",
        banner="Briand Castro, software analyst and developer. Animation of a black hole with its spinning disk of light.",
        flujo="Animated automation workflow. Soledad, Colombia.", otro=("ES", "README.md", "Leer en español")),
}
TEMA, IDIOMA, OUT = "oscuro", "es", ""
FG = BG = LINEA = VACIO = GRIS = TENUE = ACENTO = MEDIO = R_IZQ = R_DER = SUELO = SUELO_L = ""
ESCALA = []
T = {}


def usar(tema, idioma):
    global TEMA, IDIOMA, OUT, T
    TEMA, IDIOMA, T = tema, idioma, TEXTOS[idioma]
    globals().update(TEMAS[tema])
    OUT = os.path.join(ROOT, "assets", tema, idioma)
    os.makedirs(OUT, exist_ok=True)


def save(name, W, H, label, body, style="", defs=""):
    izq, der = margenes(name[:-4])
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W+izq+der:g} {H+V}" width="{W+izq+der:g}" height="{H+V}" role="img" aria-label="{e(label)}">'
                f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>{defs}</defs><style>{style}{REDUCE}</style>'
                f'<g transform="translate({izq:g},0)">{body}</g></svg>')


def esquinas(W, H, color, op=.55, d=14, l=12):
    """Marcas en las cuatro esquinas, como las de un visor."""
    p = "".join(f"M{x} {y+sy*l} V{y} H{x+sx*l} " for x, y, sx, sy in ((d, d, 1, 1), (W - d, d, -1, 1), (d, H - d, 1, -1), (W - d, H - d, -1, -1)))
    return f'<path d="{p}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.6" stroke-linecap="round"/>'


def fondo(W, H, tono="base", malla=False):
    """Tarjeta. base: la del tema · medio: gris · inverso: blanca en tema oscuro y negra en tema claro.

    Lleva degradado, un brillo en la esquina, borde que se apaga hacia abajo, marcas en las esquinas
    y un destello que recorre el borde.
    """
    oscuro = TEMA == "oscuro"
    if tono == "medio":
        c0, c1, tinta, luz = "#7d7d7d", "#585858", BLANCO, .22
    elif tono == "inverso":
        c0, c1, tinta, luz = ("#ffffff", "#dcdcdc", NEGRO, .0) if oscuro else ("#1c1c1c", "#060606", BLANCO, .1)
    else:
        c0, c1, tinta, luz = ("#171717", "#090909", BLANCO, .075) if oscuro else ("#ffffff", "#ececec", NEGRO, .0)
    defs = (f'<defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>'
            f'<radialGradient id="tl" cx="0" cy="0" r="1"><stop offset="0" stop-color="#fff" stop-opacity="{luz}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="tb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{tinta}" stop-opacity=".5"/><stop offset=".5" stop-color="{tinta}" stop-opacity=".14"/><stop offset="1" stop-color="{tinta}" stop-opacity=".06"/></linearGradient>'
            f'<pattern id="malla" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{tinta}" fill-opacity=".16"/></pattern>'
            f'<linearGradient id="tf" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="tm"><rect width="{W}" height="{H}" fill="url(#tf)"/></mask></defs>')
    m = f'<rect width="{W}" height="{H}" fill="url(#malla)" mask="url(#tm)"/>' if (malla or tono == "base") else ""
    return (f'{defs}<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#tg)"/>{m}<rect width="{W}" height="{H}" fill="url(#tl)"/></g>'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="url(#tb)" stroke-width="1.5"/>'
            f'<rect class="viaje" x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{tinta}" stroke-opacity=".9" stroke-width="1.6" stroke-linecap="round" pathLength="1000" stroke-dasharray="46 954"/>'
            f'{esquinas(W, H, tinta)}')


def rotulo(x, y, text, color=None, punto=None):
    return (f'<rect x="{x}" y="{y-11}" width="11" height="11" fill="{punto or ACENTO}"/>'
            f'<text x="{x+22}" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="{color or FG}">{e(text)}</text>')


def ancho(text, size, f=.7):
    """Ancho fijo para titulares, para que no dependa de la tipografía del visitante."""
    return round(len(text) * size * f)


def hora12(h):
    return f"{(h % 12) or 12} {T['am'] if h < 12 else T['pm']}"


def cargar(nombre):
    return json.load(open(os.path.join(ROOT, "data", nombre), encoding="utf-8"))


# ───────────── nombre ─────────────
# ───────────── flujo de automatización ─────────────
# ───────────── sobre mí ─────────────
def sobre():
    W, H = W2, 340
    y, txt = 116, ""
    for l in T["sobre_txt"]:
        if l is None:
            y += 16
            continue
        txt += f'<text x="48" y="{y}" font-family="{SANS}" font-size="19" fill="{GRIS}">' + "".join(
            f'<tspan fill="{FG}" font-weight="700">{e(t)}</tspan>' if b else e(t) for t, b in l) + "</text>"
        y += 29
    body = f'{fondo(W, H)}{rotulo(48, 62, T["sobre"])}<rect class="b" x="48" y="78" width="60" height="3" fill="{ACENTO}"/>{txt}'
    save("sobre.svg", W, H, T["sobre_alt"], body, ".b{animation:b 4s ease-in-out infinite;transform-origin:48px 0}@keyframes b{50%{transform:scaleX(4)}}")


# ───────────── cifras ─────────────
def cifra(fn, tono, valor, etiqueta, nota, tam=104):
    W, H = W1, 220
    tinta, sec, punto, num = {"inverso": (BG, TENUE if TEMA == "oscuro" else "#bdbdbd", MEDIO, BG), "base": (FG, GRIS, ACENTO, FG),
                              "medio": (BLANCO, NEGRO, NEGRO, BLANCO)}[tono]
    if tono == "inverso" and TEMA == "oscuro":
        sec = "#555555"
    body = (f'{fondo(W, H, tono)}{rotulo(28, 44, etiqueta, tinta, punto)}'
            f'<text class="v" x="24" y="156" font-family="{DISPLAY}" font-size="{tam}" font-weight="900" fill="{num}" textLength="{round(tam*.58*len(valor))+20}" lengthAdjust="spacingAndGlyphs">{e(valor)}</text>'
            f'<text x="28" y="192" font-family="{SANS}" font-size="15" font-weight="600" fill="{sec}">{e(nota)}</text>')
    save(fn, W, H, f"{etiqueta}: {valor}. {nota}", body, ".v{animation:v 5s ease-in-out infinite}@keyframes v{50%{opacity:.82}}")


# ───────────── qué hago ─────────────
def hago():
    W, H = W3, 366
    body = fondo(W, H)
    for i, (tag, tit, desc) in enumerate(T["hago"]):
        y = i * 122
        body += ((f'<line x1="48" x2="{W-48}" y1="{y}" y2="{y}" stroke="{LINEA}"/>' if i else "")
                 + f'<g clip-path="url(#clip)"><rect class="s s{i}" x="0" y="{y+1}" width="8" height="120" fill="{ACENTO}"/></g>'
                 f'<text x="48" y="{y+80}" font-family="{DISPLAY}" font-size="56" font-weight="900" fill="none" stroke="{TENUE}" stroke-width="1.6" textLength="84" lengthAdjust="spacingAndGlyphs">0{i+1}</text>'
                 f'<text x="176" y="{y+52}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="3" fill="{ACENTO}">{tag}</text>'
                 f'<text x="176" y="{y+86}" font-family="{SANS}" font-size="25" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 f'<text x="640" y="{y+68}" font-family="{SANS}" font-size="14.5" fill="{GRIS}">{e(desc)}</text>'
                 f'<path class="fl s{i}" d="M{W-84} {y+63} h26 m-10 -10 l10 10 l-10 10" fill="none" stroke="{FG}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    style = (".s{animation:s 6s ease-in-out infinite;opacity:.18}.s1{animation-delay:2s}.s2{animation-delay:4s}@keyframes s{0%,34%,100%{opacity:.18}8%,26%{opacity:1}}"
             ".fl{animation:fl 6s ease-in-out infinite;opacity:.25}.fl.s1{animation-delay:2s}.fl.s2{animation-delay:4s}@keyframes fl{0%,34%,100%{opacity:.25;transform:translateX(0)}8%,26%{opacity:1;transform:translateX(8px)}}")
    save("hago.svg", W, H, " ".join(f"{t}. {d}" for _, t, d in T["hago"]), body, style)


# ───────────── stack en cintas + trayectoria ─────────────
# Iconos del stack: se sirven desde el CDN de Simple Icons, en un solo color. (nombre, slug)
ICONOS = [[("TypeScript", "typescript"), ("JavaScript", "javascript"), ("PHP", "php"), ("React", "react"), ("Next.js", "nextdotjs"), ("Tailwind CSS", "tailwindcss"),
           ("Ionic", "ionic"), ("Capacitor", "capacitor"), ("Node.js", "nodedotjs"), (".NET", "dotnet")],
          [("PostgreSQL", "postgresql"), ("MySQL", "mysql"), ("MongoDB", "mongodb"), ("Supabase", "supabase"), ("Firebase", "firebase"), ("n8n", "n8n"),
           ("Ollama", "ollama"), ("Docker", "docker"), ("Git", "git"), ("Unity", "unity")]]
SIN_ICONO = ["C#", "Power BI", "Power Automate", "SAP", "VS Code"]


def stack_titulo():
    """Rótulo del stack, sin fondo: los iconos van debajo, sobre la página."""
    W, H = W3, 46
    body = (rotulo(4, 30, "STACK") + f'<line x1="118" x2="{W-4}" y1="25" y2="25" stroke="{LINEA}" stroke-width="1.5"/>'
            f'<circle class="p" r="3.5" cy="25" fill="{FG}"><animate attributeName="cx" dur="6s" repeatCount="indefinite" values="118;{W-4}"/><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.1;.85;1"/></circle>')
    save("stack-titulo.svg", W, H, "Stack", body)


def ruta():
    W, H = W1, 350
    body = fondo(W, H) + rotulo(32, 50, T["ruta"]) + f'<line x1="44" x2="44" y1="104" y2="276" stroke="{LINEA}" stroke-width="2"/><line class="l" x1="44" x2="44" y1="104" y2="276" stroke="{ACENTO}" stroke-width="2.5"/>'
    for i, (fecha, tit, org) in enumerate(T["hitos"]):
        y, hoy = 108 + i * 82, i == 0
        body += ((f'<circle class="ping" cx="44" cy="{y}" r="8" fill="none" stroke="{ACENTO}" stroke-width="2"/>' if hoy else "")
                 + f'<circle cx="44" cy="{y}" r="8" fill="{ACENTO if hoy else BG}" stroke="{ACENTO if hoy else FG}" stroke-width="2.5"/>'
                 f'<text x="70" y="{y+4}" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="2" fill="{GRIS}">{fecha}</text>'
                 f'<text x="70" y="{y+28}" font-family="{SANS}" font-size="18.5" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 f'<text x="70" y="{y+50}" font-family="{SANS}" font-size="13.5" fill="{GRIS}">{e(org)}</text>')
    style = (".l{stroke-dasharray:172;animation:l 6s ease-in-out infinite}@keyframes l{0%{stroke-dashoffset:172}50%,100%{stroke-dashoffset:0}}"
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


def galaxia(data):
    """Una galaxia espiral hecha con los commits: el tiempo avanza del centro hacia el borde por dos brazos."""
    import random
    W, H = W2, 350
    fin = dt.date.fromisoformat(data["hasta"])
    cuenta = [data["dias"].get((fin - dt.timedelta(days=364 - k)).isoformat(), 0) for k in range(365)]
    r = random.Random(42)
    polvo, soles = "", ""
    for k, c in enumerate(cuenta):
        s = k / 364
        ang = (k % 2) * math.pi + s * 2.35 * 2 * math.pi + r.uniform(-.09, .09)
        rad = 30 + s * 262 + r.uniform(-8, 8)
        x, y = rad * math.cos(ang), rad * math.sin(ang)
        if c:
            rr = min(12, 3.4 + 1.4 * math.sqrt(c))
            soles += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr*3:.1f}" fill="url(#halo)"/>'
                      f'<circle class="tw" style="animation-delay:{r.uniform(0, 3):.1f}s" cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{FG}"/>')
        else:
            polvo += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.choice([1.1, 1.4, 1.8])}" fill="{FG}" fill-opacity="{r.uniform(.2, .55):.2f}"/>'
    for _ in range(800):
        s = r.random() ** .8; ang = r.choice([0, math.pi]) + s * 2.35 * 2 * math.pi + r.gauss(0, .22); rad = 24 + s * 272 + r.gauss(0, 11)
        polvo += f'<circle cx="{rad*math.cos(ang):.1f}" cy="{rad*math.sin(ang):.1f}" r="{r.choice([.5, .7, .9])}" fill="{FG}" fill-opacity="{r.uniform(.06, .26):.2f}"/>'
    defs = (f'<radialGradient id="halo"><stop offset="0" stop-color="{FG}" stop-opacity=".5"/><stop offset=".4" stop-color="{FG}" stop-opacity=".12"/><stop offset="1" stop-color="{FG}" stop-opacity="0"/></radialGradient>'
            '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>')
    body = (f'{fondo(W, H)}<g clip-path="url(#clip)">'
            f'<g transform="translate(476 170) rotate(-14) scale(1.08 .52)"><circle r="320" fill="url(#halo)" opacity=".3"/><g class="gal">{polvo}{soles}</g>'
            f'<circle r="84" fill="url(#halo)"/><circle r="20" fill="{FG}" filter="url(#blur)"/><circle r="10" fill="{FG}"/></g></g>'
            f'{rotulo(36, 50, T["gal"])}<text x="36" y="{H-30}" font-family="{SANS}" font-size="13.5" fill="{GRIS}">{e(T["gal_n"])}</text>')
    save("galaxia.svg", W, H, f"{T['gal'].title()}: {T['gal_n']}", body,
         ".gal{animation:gal 150s linear infinite}@keyframes gal{to{transform:rotate(360deg)}}.tw{animation:tw 3.2s ease-in-out infinite}@keyframes tw{50%{opacity:.25}}", defs)


# ───────────── lenguajes + semana ─────────────
# ───────────── hoja de vida + cierre ─────────────
def cv():
    W, H = W1, 200
    body = f'''{fondo(W, H, "inverso")}{rotulo(28, 44, T["cv"], BG, MEDIO)}
<text x="26" y="112" font-family="{DISPLAY}" font-size="40" font-weight="900" fill="{BG}" textLength="{ancho(T["cv1"], 40, .6)}" lengthAdjust="spacingAndGlyphs">{T["cv1"]}</text>
<text x="26" y="158" font-family="{DISPLAY}" font-size="40" font-weight="900" fill="{MEDIO}" textLength="{ancho(T["cv2"], 40, .72)}" lengthAdjust="spacingAndGlyphs">{T["cv2"]}</text>
<rect x="{W-112}" y="78" width="84" height="84" rx="10" fill="{BG}"/>
<path class="dl" d="M{W-70} 100 v34 m-14 -13 l14 14 l14 -14" fill="none" stroke="{FG}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M{W-90} 148 h40" stroke="{FG}" stroke-width="5" stroke-linecap="round"/>'''
    save("cv.svg", W, H, f"{T['cv'].title()}: {T['cv1']} {T['cv2']}", body, ".dl{animation:dl 1.5s ease-in-out infinite}@keyframes dl{50%{transform:translateY(6px)}}")


def cierre():
    W, H = W2, 200
    c1, c2 = T["cierre"]
    defs = '<pattern id="ray" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)"><rect width="13" height="26" fill="#000" fill-opacity=".07"/></pattern>'
    body = f'''{fondo(W, H, "medio")}<g clip-path="url(#clip)"><rect class="ray" x="-60" width="{W+120}" height="{H}" fill="url(#ray)"/></g>
<text x="36" y="80" font-family="{DISPLAY}" font-size="42" font-weight="900" fill="{NEGRO}" textLength="{ancho(c1, 42, .73)}" lengthAdjust="spacingAndGlyphs">{e(c1)}</text>
<text x="36" y="128" font-family="{DISPLAY}" font-size="42" font-weight="900" fill="{BLANCO}" textLength="{ancho(c2, 42, .73)}" lengthAdjust="spacingAndGlyphs">{e(c2)}</text>
<text x="36" y="162" font-family="{SANS}" font-size="15" font-weight="600" fill="{NEGRO}">{e(T["cierre_s"])}</text>
<rect x="{W-246}" y="68" width="210" height="64" rx="8" fill="{NEGRO}"/>
<text x="{W-160}" y="108" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="{BLANCO}">{e(T["escribe"])}</text>
<path class="fl" d="M{W-92} 100 h24 m-9 -9 l9 9 l-9 9" fill="none" stroke="{BLANCO}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'''
    save("cierre.svg", W, H, f"{c1} {c2} {T['escribe']}.", body,
         ".ray{animation:ray 3s linear infinite}@keyframes ray{to{transform:translateX(26px)}}.fl{animation:fl 1.4s ease-in-out infinite}@keyframes fl{50%{transform:translateX(7px)}}", defs)


def idioma_btn():
    cod = T["otro"][0]
    body = (f'<rect x="1" y="1" width="134" height="34" rx="6" fill="{BG}" stroke="{LINEA}" stroke-width="1.5"/>'
            f'<rect x="14" y="12" width="11" height="11" fill="{ACENTO}"/><text x="36" y="23" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="{TENUE}">'
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
    def icono(nombre, slug):
        return (f'<picture><source media="(prefers-color-scheme: light)" srcset="https://cdn.simpleicons.org/{slug}/0d0d0d">'
                f'<img src="https://cdn.simpleicons.org/{slug}/f2f2f2" height="34" alt="{e(nombre)}" title="{e(nombre)}"></picture>')
    BASE = {"sobre": W2, "consola": W1, "hago": W3, "galaxia": W2, "ruta": W1, "cifra-commits": W1, "cifra-dias": W1, "cifra-hora": W1, "cv": W1, "cierre": W2}
    def fila(*xs):
        return [img(x[0], ancho_pct(x[0], BASE[x[0]], len(xs)), alts[x[0]], x[1] if len(x) > 1 else None) for x in xs]
    sep = "&nbsp;&nbsp;&nbsp;&nbsp;\n"
    out = [f'<p align="right">{img("idioma", None, T_["otro"][2], T_["otro"][1], alto=30)}</p>', "",
           f'<p><img src="assets/banner-{idioma}.gif" width="100%" alt="{e(T_["banner"])}"></p>', "", "<p>"]
    out += fila(("sobre",), ("consola",)) + fila(("hago",)) + ["</p>", "",
            img("stack-titulo", "100%", "Stack"), "",
            '<p align="center">', sep.join(icono(*i) for i in ICONOS[0]), "<br><br>", sep.join(icono(*i) for i in ICONOS[1]),
            "<br><br>", "<sub>" + " &nbsp;·&nbsp; ".join(SIN_ICONO) + "</sub>", "</p>", "", "<br>", "", "<p>"]
    out += (fila(("galaxia",), ("ruta",)) + fila(("cifra-commits",), ("cifra-dias",), ("cifra-hora",))
            + fila(("cv", CV), ("cierre", f"mailto:{CORREO}")) + ["</p>", ""])
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
            sobre(); hago(); stack_titulo(); ruta(); galaxia(data); cv(); cierre(); idioma_btn()
            dias = [x for w in semanas(data) for x in w]
            total, activos = sum(c for _, c in dias), sum(1 for _, c in dias if c)
            racha = cur = 0
            for _, c in dias:
                cur = cur + 1 if c else 0
                racha = max(racha, cur)
            cifra("cifra-commits.svg", "inverso", str(total), T["commits"][0], T["commits"][1].format(n=data["proyectos"]))
            cifra("cifra-dias.svg", "base", str(activos), *T["dias"])
            pico = data["horas"].index(max(data["horas"]))
            cifra("cifra-hora.svg", "medio", hora12(pico), *T["hora"], tam=60)
    for idi in TEXTOS:
        readme(idi, alts_de(idi))
    print("Listo")
