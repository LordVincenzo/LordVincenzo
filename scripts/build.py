"""Genera las piezas del perfil (SVG animados) en dos temas y dos idiomas, y los README.
Uso: python scripts/build.py     (solo biblioteca estándar + scripts/pixel.py, que usa numpy)"""
import json, math, datetime, html, random, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, "scripts"))
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "Inter,'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
DISP = "'Arial Black','Segoe UI Black',Inter,sans-serif"
W = 1214; esc = html.escape
IC = json.load(open(os.path.join(ROOT, "data", "iconos.json")))
ACT = json.load(open(os.path.join(ROOT, "data", "actividad.json")))
TEMAS = {"oscuro": dict(FG="#f2f2f2", BG="#08080a", GR="#9a9a9a", TE="#5c5c5c", LI="#2a2a2c", PAN="#111113", BORDE="#4a4a4e", BARRA="#77777a", CERO="#17171a", LUZ="#fff", SUBINV="#3a3a3c", OSC=1),
         "claro": dict(FG="#0d0d0f", BG="#ffffff", GR="#55555a", TE="#9c9ca2", LI="#dcdce0", PAN="#f3f3f5", BORDE="#bcbcc2", BARRA="#a4a4aa", CERO="#ececef", LUZ="#000", SUBINV="#c8c8cc", OSC=0)}
TEXTOS = {
 "es": dict(sobre="SOBRE MÍ", t1="CONSTRUYO Y", t2="AUTOMATIZO.",
    par=[[("Tecnólogo en ", 0), ("Análisis y Desarrollo de Software", 1), (". Construyo", 0)], [("apps web y móviles de punta a punta y pongo al sistema a", 0)], [("hacer el trabajo repetitivo.", 0)], None,
         [("Hoy gestiono la plataforma educativa ", 0), ("Prizma", 1), (" en la", 0)], [("Corporación ", 0), ("Universitaria Americana", 1), (".", 0)]],
    hoy_t="EN LO QUE ANDO HOY", hoy_x=236, hoy=[("Inteligencia artificial a la medida", "IA", ["Sé armar una inteligencia artificial personalizada de punta a punta:", "clonación de voz para que hable con voz propia, Whisper para que", "entienda lo que le dicen y el cerebro (el modelo de lenguaje)", "corriendo en un servidor propio."]), ("Lógica, datos y automatización", "AUTO", ["Manejo toda la información a nivel de lógica y datos, y construyo", "automatizaciones internas: creación de carpetas y matrices que se", "vinculan entre sí, para que los procesos corran solos y sin", "trabajo manual."])],
    vivo="EN VIVO · MODO CONCENTRACIÓN", stack="STACK · ASÍ FLUYE UN PROYECTO", grupos=["LENGUAJES", "FRONTEND Y MÓVIL", "BACKEND Y DATOS", "AUTOMATIZACIÓN E IA", "HERRAMIENTAS"],
    act="ACTIVIDAD", c_en="commits en 5 proyectos", st=["días activos", "mejor racha", "en fin de semana"], sem="COMMITS POR SEMANA", pico="{n} en una semana", dia="DÍA A DÍA",
    meses=["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"], hora="HORA DEL DÍA", h10="10 a. m.", dsem="DÍA DE LA SEMANA", letras="LMXJVSD",
    nota="commits propios en 5 proyectos · datos al 10 nov 2026", ruta="TRAYECTORIA",
    et=[("2023 — 2025", "Tecnólogo ADSO", "SENA", ["Análisis y desarrollo", "de software."]), ("ENE — JUL 2025", "Calidad de Proveedores", "Procaps", ["Gestión y reportes", "de calidad."]),
        ("SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana", ["Automaticé el cargue de", "cursos con n8n."])],
    paso="SIGUIENTE PASO", c1="¿AUTOMATIZAMOS", c2="ALGO JUNTOS?", cs1="Cuéntame qué tarea repetitiva te quita tiempo", cs2="y la convertimos en un flujo que corre solo.", abajo="Hoja de vida y contacto, aquí abajo ↓",
    tareas="TAREAS", hecho="HECHO", b_cv="Descargar hoja de vida ↓", b_mail="Escríbeme →", b_idioma="English →",
    alt=dict(banner="Briand Castro, analista y desarrollador de software. Animación de un agujero negro rodeado de lluvia de código.",
        yo="Sobre mí: tecnólogo en Análisis y Desarrollo de Software. Construyo apps web y móviles y automatizo el trabajo repetitivo. Hoy gestiono la plataforma Prizma en la Corporación Universitaria Americana creo asistentes de IA personalizados (clonación de voz, reconocimiento con Whisper, modelo en servidor) y manejo lógica, datos y automatizaciones internas. Soledad, Colombia.",
        stack="Stack: C#, TypeScript, JavaScript, PHP, Python, SQL; React, Next.js, Tailwind, Ionic, Capacitor; .NET, Node.js, PostgreSQL, MySQL, MongoDB, Supabase, Firebase, Power BI; n8n, Power Automate, Ollama; Git, Docker, Unity, VS Code, SAP.",
        actividad="Actividad del último año: 165 commits en 5 proyectos, 27 días activos, mejor racha de 4 días, 51 % en fin de semana, hora pico 10 a. m.",
        ruta="Trayectoria: Tecnólogo ADSO en el SENA (2023-2025), Calidad de Proveedores en Procaps (enero a julio de 2025), Gestor de Plataforma Prizma en la Corporación Universitaria Americana (septiembre de 2025 a hoy).",
        cierre="¿Automatizamos algo juntos? Cuéntame qué tarea repetitiva te quita tiempo.", cv="Descargar hoja de vida (PDF)", mail="Escríbeme por correo", idioma="Read in English"), otro="README.en.md", fn="README.md"),
 "en": dict(sobre="ABOUT ME", t1="I BUILD AND", t2="AUTOMATE.",
    par=[[("Technologist in ", 0), ("Software Analysis and Development", 1), (". I build", 0)], [("web and mobile apps end to end and make the system", 0)], [("do the repetitive work.", 0)], None,
         [("Today I manage the ", 0), ("Prizma", 1), (" learning platform at", 0)], [("Corporación ", 0), ("Universitaria Americana", 1), (".", 0)]],
    hoy_t="WHAT I'M ON TODAY", hoy_x=226, hoy=[("Custom artificial intelligence", "AI", ["I know how to put together a custom AI end to end: voice cloning", "so it speaks with its own voice, Whisper so it understands what", "it hears, and the brain (the language model) running on a", "dedicated server."]), ("Logic, data and automation", "AUTO", ["I handle all the information at the logic and data level and build", "internal automations: creating folders and matrices that link to", "each other, so processes run on their own with no manual work."])],
    vivo="LIVE · FOCUS MODE", stack="STACK · HOW A PROJECT FLOWS", grupos=["LANGUAGES", "FRONTEND & MOBILE", "BACKEND & DATA", "AUTOMATION & AI", "TOOLS"],
    act="ACTIVITY", c_en="commits across 5 projects", st=["active days", "best streak", "on weekends"], sem="COMMITS PER WEEK", pico="{n} in one week", dia="DAY BY DAY",
    meses=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], hora="HOUR OF DAY", h10="10 a.m.", dsem="DAY OF WEEK", letras="MTWTFSS",
    nota="own commits across 5 projects · data as of Nov 10, 2026", ruta="CAREER",
    et=[("2023 — 2025", "Software Technologist", "SENA", ["Software analysis and", "development."]), ("JAN — JUL 2025", "Supplier Quality", "Procaps", ["Quality management", "and reporting."]),
        ("SEP 2025 — NOW", "Prizma Platform Manager", "Corporación Universitaria Americana", ["Automated course uploads", "with n8n."])],
    paso="NEXT STEP", c1="SHALL WE AUTOMATE", c2="SOMETHING?", cs1="Tell me which repetitive task eats your time", cs2="and we'll turn it into a flow that runs itself.", abajo="Résumé and contact, right below ↓",
    tareas="TASKS", hecho="DONE", b_cv="Download résumé ↓", b_mail="Write to me →", b_idioma="Español →",
    alt=dict(banner="Briand Castro, software analyst and developer. Animation of a black hole surrounded by falling code.",
        yo="About me: technologist in Software Analysis and Development. I build web and mobile apps and automate repetitive work. Today I manage the Prizma platform at Corporación Universitaria Americana build custom AI assistants (voice cloning, Whisper speech recognition, model on a server) and handle logic, data and internal automations. Soledad, Colombia.",
        stack="Stack: C#, TypeScript, JavaScript, PHP, Python, SQL; React, Next.js, Tailwind, Ionic, Capacitor; .NET, Node.js, PostgreSQL, MySQL, MongoDB, Supabase, Firebase, Power BI; n8n, Power Automate, Ollama; Git, Docker, Unity, VS Code, SAP.",
        actividad="Activity over the last year: 165 commits across 5 projects, 27 active days, best streak of 4 days, 51% on weekends, peak hour 10 a.m.",
        ruta="Career: Software Technologist at SENA (2023-2025), Supplier Quality at Procaps (January to July 2025), Prizma Platform Manager at Corporación Universitaria Americana (September 2025 to now).",
        cierre="Shall we automate something? Tell me which repetitive task eats your time.", cv="Download résumé (PDF)", mail="Write me an email", idioma="Leer en español"), otro="README.md", fn="README.en.md")}
def usar(tema, idioma):
    global T, OUT
    globals().update(TEMAS[tema]); T = TEXTOS[idioma]
    OUT = os.path.join(ROOT, "assets", tema, idioma); os.makedirs(OUT, exist_ok=True)
def guardar(fn, txt): open(os.path.join(OUT, fn), "w", encoding="utf-8").write(txt)

def lluvia(w, h, seed, op=.5, paso=22, n=13, fs=13):
    op = op if OSC else op * .45
    """Lluvia de caracteres estilo Matrix: columnas que caen en bucle, cabeza brillante y cola que se apaga."""
    r = random.Random(seed); ch = "01<>{}/=;$#*+01"; g = []
    for i, x in enumerate(range(12, w, paso)):
        if r.random() < .18: continue
        d = r.uniform(5, 11); ret = -r.uniform(0, d); lh = fs + 3; alto = n * lh
        ts = "".join(f'<tspan x="{x}" dy="{lh}" fill-opacity="{(j+1)/n*(1 if j==n-1 else .55):.2f}">{esc(r.choice(ch))}</tspan>' for j in range(n))
        g.append(f'<text y="0" font-size="{fs}" fill="{LUZ}"><animateTransform attributeName="transform" type="translate" from="0 {-alto}" to="0 {h+20}" dur="{d:.1f}s" begin="{ret:.1f}s" repeatCount="indefinite"/>{ts}</text>')
    return f'<g opacity="{op}" font-family="{MONO}">' + "".join(g) + '</g>'

def base(H, seed, op=.5, ids="x"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><clipPath id="cl{ids}"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
            f'<radialGradient id="vi{ids}" cx="50%" cy="50%" r="75%"><stop offset="0" stop-color="{BG}" stop-opacity=".8"/><stop offset=".7" stop-color="{BG}" stop-opacity=".5"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient></defs>'
            f'<g clip-path="url(#cl{ids})"><rect width="{W}" height="{H}" fill="{BG}"/>{lluvia(W, H, seed, op)}<rect width="{W}" height="{H}" fill="url(#vi{ids})"/>')
def fin(H): return f'</g><rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="none" stroke="{LI}" stroke-width="1.5"/></svg>'
def rot(x, y, t, n=None):
    s = f'<rect x="{x}" y="{y-10}" width="9" height="9" fill="{FG}"/><text x="{x+20}" y="{y}" font-family="{MONO}" font-size="13" fill="{GR}" letter-spacing="3.5">{t}</text>'
    return s
def icono(slug, x, y, s, fill=None):
    fill = fill or FG
    if slug in IC: return f'<path transform="translate({x} {y}) scale({s/24})" fill="{fill}" d="{IC[slug]["p"]}"/>'
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*.2}" fill="none" stroke="{fill}" stroke-width="1.6"/><text x="{x+s/2}" y="{y+s*.66}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="{s*.42}" fill="{fill}">{slug}</text>'

# ---------------- 1. sobre mí + escena ----------------
def escena(ox, oy):
    s = [f'<g transform="translate({ox} {oy})">']
    s.append('<defs><radialGradient id="gl" cx="50%" cy="45%" r="50%"><stop offset="0" stop-color="#fff" stop-opacity=".2"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
             '<linearGradient id="pan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1b1e"/><stop offset="1" stop-color="#0c0c0e"/></linearGradient></defs>')
    s.append('<ellipse cx="250" cy="150" rx="330" ry="210" fill="url(#gl)"/>')
    # símbolos que suben
    for i, (x, t) in enumerate([(70, "{ }"), (150, "</>"), (215, "=>"), (300, "✓"), (365, "SQL"), (430, "API")]):
        s.append(f'<text x="{x}" y="46" font-family="{MONO}" font-size="13" font-weight="700" fill="{FG}" text-anchor="middle" opacity="0">{esc(t)}'
                 f'<animate attributeName="opacity" values="0;.9;0" dur="4s" begin="{-i*.67:.2f}s" repeatCount="indefinite"/><animate attributeName="y" values="52;8" dur="4s" begin="{-i*.67:.2f}s" repeatCount="indefinite"/></text>')
    # monitores
    for mx in (52, 262):
        s.append(f'<rect x="{mx+82}" y="178" width="22" height="40" fill="#1c1c1f"/><rect x="{mx+56}" y="214" width="74" height="7" rx="3" fill="#232326"/>')
        s.append(f'<rect x="{mx}" y="60" width="186" height="120" rx="9" fill="url(#pan)" stroke="#7a7a7a" stroke-width="2"/>')
    # código (monitor izquierdo)
    anchos = [70, 112, 92, 130, 60, 104, 84]
    for i, a in enumerate(anchos):
        y = 76 + i * 13.5; x = 66 + (0, 12, 12, 24, 24, 12, 0)[i]
        s.append(f'<rect x="{x}" y="{y}" height="5" rx="2.5" width="{a}" fill="{FG if i in (0,3) else GR}" opacity=".9"><animate attributeName="width" values="0;{a};{a};{a}" keyTimes="0;.12;.9;1" dur="7s" begin="{-7+i*.7:.2f}s" repeatCount="indefinite"/></rect>')
    s.append(f'<rect x="66" y="166" width="7" height="8" fill="{FG}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
    # flujo (monitor derecho)
    nod = [(282, 92), (336, 122), (398, 92)]
    s.append(f'<path d="M298 100 C318 100 316 130 336 130 M352 130 C376 130 374 100 398 100" stroke="{GR}" stroke-width="1.6" fill="none" stroke-dasharray="3 4"><animate attributeName="stroke-dashoffset" values="14;0" dur=".9s" repeatCount="indefinite"/></path>')
    for i, (x, y) in enumerate(nod):
        s.append(f'<rect x="{x}" y="{y}" width="16" height="16" rx="4" fill="{FG}"><animate attributeName="opacity" values=".35;1;.35" dur="2.4s" begin="{-2.4+i*.8:.1f}s" repeatCount="indefinite"/></rect>')
    s.append(f'<circle cx="423" cy="100" r="7" fill="none" stroke="{FG}" stroke-width="1.6"/><path d="M419.5 100l2.6 2.6 4.6-5" stroke="{FG}" stroke-width="1.6" fill="none"/>')
    for i, a in enumerate([120, 86, 104]):
        s.append(f'<rect x="282" y="{150+i*10}" width="{a}" height="4" rx="2" fill="{TE}"/>')
    # escritorio
    s.append('<rect x="-6" y="221" width="512" height="11" rx="3" fill="#2b2b2f"/><rect x="-6" y="232" width="512" height="3" fill="#000" opacity=".5"/><rect x="14" y="235" width="10" height="150" fill="#1b1b1e"/><rect x="476" y="235" width="10" height="150" fill="#1b1b1e"/>')
    # taza con vapor y planta
    s.append(f'<rect x="444" y="198" width="24" height="23" rx="4" fill="#d8d8d8"/><path d="M468 203h5a5 5 0 0 1 0 12h-5" stroke="#d8d8d8" stroke-width="3" fill="none"/>')
    for i in range(2):
        s.append(f'<path d="M{451+i*9} 192c-4-6 4-9 0-16" stroke="{GR}" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".6"><animate attributeName="opacity" values="0;.8;0" dur="3s" begin="{-i*1.5}s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6;0 -8" dur="3s" begin="{-i*1.5}s" repeatCount="indefinite"/></path>')
    s.append('<path d="M18 221l4-22h22l4 22z" fill="#3a3a3e"/><path d="M33 199c-2-22-16-28-22-30 2 14 8 26 22 30zm0 0c0-26 10-36 20-40 0 16-6 32-20 40zm0 0c-1-16 3-34 2-44" fill="none" stroke="#bdbdbd" stroke-width="2.2" stroke-linecap="round"/>')
    # persona de espaldas
    s.append('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -1.6;0 0" dur="3.6s" repeatCount="indefinite"/>'
             '<path d="M128 392C128 300 170 258 250 258S372 300 372 392Z" fill="#17171a" stroke="#8c8c8c" stroke-width="2"/>'
             '<ellipse cx="250" cy="262" rx="58" ry="22" fill="#202024" stroke="#8c8c8c" stroke-width="2"/>'
             '<circle cx="250" cy="212" r="40" fill="#1a1a1d" stroke="#a0a0a0" stroke-width="2"/>'
             '<path d="M214 196c6-22 22-30 36-30s30 8 36 30" fill="none" stroke="#2c2c30" stroke-width="10" stroke-linecap="round"/>'
             f'<path d="M208 210A42 44 0 0 1 292 210" fill="none" stroke="{FG}" stroke-width="6" stroke-linecap="round"/>'
             f'<rect x="199" y="200" width="15" height="34" rx="7" fill="{FG}"/><rect x="286" y="200" width="15" height="34" rx="7" fill="{FG}"/></g>')
    # silla
    s.append('<rect x="176" y="292" width="148" height="110" rx="26" fill="#0c0c0e" stroke="#5a5a5a" stroke-width="2"/>' + "".join(f'<path d="M196 {312+i*16}h108" stroke="#2a2a2e" stroke-width="2"/>' for i in range(5)))
    s.append('</g>'); return "".join(s)

def yo():
    H = 708; s = [base(H, 11, .6, "a")]
    s.append(rot(48, 62, T["sobre"]))
    s.append(f'<text font-family="{DISP}" font-weight="900" font-size="40" fill="{FG}"><tspan x="46" y="122">{T["t1"]}</tspan><tspan x="46" y="166">{T["t2"]}</tspan></text>')
    par = T["par"]
    y = 212
    for l in par:
        if l is None: y += 12; continue
        s.append(f'<text x="48" y="{y}" font-family="{SANS}" font-size="17.5">' + "".join(f'<tspan fill="{FG if b else GR}" font-weight="{700 if b else 400}">{esc(t)}</tspan>' for t, b in l) + '</text>'); y += 27
    y += 22
    s.append(f'<text x="48" y="{y}" font-family="{MONO}" font-size="12" fill="{GR}" letter-spacing="3">{T["hoy_t"]}</text><path d="M{T["hoy_x"]} {y-4}H590" stroke="{LI}" stroke-width="1.5"/>'); y += 38
    hoy = T["hoy"]
    for i, (n, et, d) in enumerate(hoy):
        s.append(f'<circle cx="54" cy="{y-6}" r="4" fill="{FG}"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" begin="{-i*.6}s" repeatCount="indefinite"/></circle>'
                 f'<text x="70" y="{y}" font-family="{SANS}" font-size="16.5" font-weight="800" fill="{FG}">{n}</text>'
                 f'<rect x="{590-len(et)*8.4-18:.0f}" y="{y-16}" width="{len(et)*8.4+18:.0f}" height="21" rx="6" fill="none" stroke="{TE}"/><text x="{590-(len(et)*8.4+18)/2:.0f}" y="{y-1}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GR}" letter-spacing="1">{et}</text>'
                 "".join(f'<text x="70" y="{y+23+j*21}" font-family="{SANS}" font-size="15" fill="{GR}">{esc(l)}</text>' for j, l in enumerate(d))); y += 42 + 21 * len(d)
    s.append(f'<g font-family="{MONO}" font-size="12.5"><rect x="640" y="{H-64}" width="176" height="30" rx="15" fill="none" stroke="{TE}"/><circle cx="656" cy="{H-49}" r="4" fill="{FG}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle><text x="668" y="{H-44.5}" fill="{FG}">Soledad, Colombia</text></g>')
    import pixel
    sx, sy = 640, 162
    s.append(f'<defs><clipPath id="pxc"><rect x="{sx}" y="{sy}" width="528" height="360" rx="14"/></clipPath></defs><g clip-path="url(#pxc)"><g transform="translate({sx} {sy})">{pixel.svg(3)}</g></g>'
             f'<rect x="{sx}" y="{sy}" width="528" height="360" rx="14" fill="none" stroke="{BORDE}" stroke-width="1.5"/>')
    s.append(f'<text x="{sx+528}" y="{sy+386}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{TE}" letter-spacing="2">{T["vivo"]}</text><circle cx="{sx+528-len(T["vivo"])*8.95-16:.0f}" cy="{sy+382}" r="3.5" fill="{FG}"><animate attributeName="opacity" values="1;.15;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    s.append(fin(H)); guardar("yo.svg", "".join(s))

# ---------------- 2. stack como flujo de automatización ----------------
def stack():
    H = 470; s = [base(H, 23, .42, "b")]
    s.append(f'<defs><pattern id="pt" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.1" fill="{LUZ}" opacity=".1"/></pattern></defs><rect width="{W}" height="{H}" fill="url(#pt)"/>')
    s.append(rot(48, 62, T["stack"]))
    P = 59
    grupos = [("LENGUAJES", [("C#", "C#"), ("typescript", "TypeScript"), ("javascript", "JavaScript"), ("php", "PHP"), ("python", "Python"), ("SQL", "SQL")]),
              ("FRONTEND Y MÓVIL", [("react", "React"), ("nextdotjs", "Next.js"), ("tailwindcss", "Tailwind"), ("ionic", "Ionic"), ("capacitor", "Capacitor")]),
              ("BACKEND Y DATOS", [("dotnet", ".NET"), ("nodedotjs", "Node.js"), ("postgresql", "Postgres"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("supabase", "Supabase"), ("firebase", "Firebase"), ("BI", "Power BI")]),
              ("AUTOMATIZACIÓN E IA", [("n8n", "n8n"), ("PA", "Automate"), ("ollama", "Ollama")]),
              ("HERRAMIENTAS", [("git", "Git"), ("docker", "Docker"), ("unity", "Unity"), ("VS", "VS Code"), ("sap", "SAP")])]
    grupos = [(T["grupos"][i], g[1]) for i, g in enumerate(grupos)]
    anc = lambda g: max(len(g[1]) * P + 26, len(g[0]) * 9.6 + 84)
    NH = 132
    # posiciones: fila 1 (inicio + 2 nodos), fila 2 (3 nodos)
    y1, y2 = 100, 296
    x = 48; pos = []
    ini = (x, y1 + 36, 118, 60); x += 118 + 56
    for g in grupos[:2]: pos.append((x, y1)); x += anc(g) + 56
    f1fin = x - 56
    tot2 = sum(anc(g) for g in grupos[2:]) + 2 * 46; x = (W - tot2) / 2
    for g in grupos[2:]: pos.append((x, y2)); x += anc(g) + 46
    cables = []
    cables.append(f"M{ini[0]+ini[2]} {ini[1]+30} H{pos[0][0]}")
    cables.append(f"M{pos[0][0]+anc(grupos[0])} {y1+NH/2} H{pos[1][0]}")
    xa = pos[1][0] + anc(grupos[1]); xb = pos[2][0]
    cables.append(f"M{xa} {y1+NH/2} C{xa+150} {y1+NH/2} {xa+150} {y1+NH+32} {xa-40} {y1+NH+32} H{xb+22} C{xb-34} {y1+NH+32} {xb-34} {y2+NH/2} {xb} {y2+NH/2}")
    cables.append(f"M{pos[2][0]+anc(grupos[2])} {y2+NH/2} H{pos[3][0]}")
    cables.append(f"M{pos[3][0]+anc(grupos[3])} {y2+NH/2} H{pos[4][0]}")
    for i, c in enumerate(cables):
        s.append(f'<path d="{c}" fill="none" stroke="{TE}" stroke-width="2"/><path d="{c}" fill="none" stroke="{FG}" stroke-width="2" stroke-dasharray="5 9" opacity=".8"><animate attributeName="stroke-dashoffset" values="28;0" dur="1s" repeatCount="indefinite"/></path>')
        d = 5 if i == 2 else 1.8
        s.append(f'<circle r="5" fill="{FG}"><animateMotion dur="{d}s" repeatCount="indefinite" path="{c}"/></circle><circle r="10" fill="{FG}" opacity=".18"><animateMotion dur="{d}s" repeatCount="indefinite" path="{c}"/></circle>')
    # nodo inicio
    x, y, w, h = ini
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="{FG}"/><path d="M{x+26} {y+19}l16 11-16 11z" fill="{BG}"/><text x="{x+54}" y="{y+35}" font-family="{MONO}" font-weight="700" font-size="14" fill="{BG}">IDEA</text>')
    for k, (g, (x, y)) in enumerate(zip(grupos, pos)):
        w = anc(g)
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="16" fill="{PAN}" stroke="{BORDE}" stroke-width="1.5"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="16" fill="none" stroke="{FG}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;.9;0;0" keyTimes="0;.12;.4;1" dur="6s" begin="{-6+k*1.2:.1f}s" repeatCount="indefinite"/></rect>'
                 f'<text x="{x+18}" y="{y+27}" font-family="{MONO}" font-size="11.5" fill="{GR}" letter-spacing="2.5">{k+1:02d} · {esc(g[0])}</text><path d="M{x+1} {y+40}h{w-2}" stroke="{LI}" stroke-width="1.5"/>'
                 f'<circle cx="{x}" cy="{y+NH/2}" r="6" fill="{BG}" stroke="{FG}" stroke-width="2"/><circle cx="{x+w}" cy="{y+NH/2}" r="6" fill="{BG}" stroke="{FG}" stroke-width="2"/>')
        for j, (slug, nom) in enumerate(g[1]):
            cx = x + (w - len(g[1]) * P) / 2 + j * P + P / 2
            s.append(icono(slug, cx - 15, y + 54, 30) + f'<text x="{cx}" y="{y+108}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{GR}">{nom}</text>')
    # fin
    xe = pos[4][0] + anc(grupos[4]) + 6
    s.append(fin(H)); guardar("stack.svg", "".join(s))

# ---------------- 3. actividad ----------------
def actividad():
    H = 470; s = [base(H, 37, .42, "c")]
    dias = ACT["dias"]; finf = datetime.date.fromisoformat(ACT["hasta"]); ini = finf - datetime.timedelta(days=52 * 7 + finf.weekday())
    sem = [sum(dias.get((ini + datetime.timedelta(days=c * 7 + r)).isoformat(), 0) for r in range(7)) for c in range(53)]
    meses = T["meses"]
    s.append(rot(48, 62, T["act"]))
    s.append(f'<text x="44" y="150" font-family="{DISP}" font-weight="900" font-size="84" fill="{FG}">165</text><text x="48" y="178" font-family="{MONO}" font-size="13" fill="{GR}">{T["c_en"]}</text>')
    for i, (v, e) in enumerate([("27", T["st"][0]), ("4", T["st"][1]), ("51 %", T["st"][2])]):
        y = 236 + i * 70
        s.append(f'<path d="M48 {y-34}h170" stroke="{LI}" stroke-width="1.5"/><text x="48" y="{y}" font-family="{DISP}" font-weight="900" font-size="30" fill="{FG}">{v}</text><text x="48" y="{y+19}" font-family="{MONO}" font-size="12" fill="{GR}">{e}</text>')
    # curva semanal
    X0, X1, Y0, Y1 = 312, 846, 252, 96; mx = max(sem)
    px = lambda c: X0 + (X1 - X0) * c / 52; py = lambda v: Y0 - (Y0 - Y1) * v / mx
    pts = [(px(c), py(v)) for c, v in enumerate(sem)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        m = (xa + xb) / 2; d += f" C{m:.1f} {ya:.1f} {m:.1f} {yb:.1f} {xb:.1f} {yb:.1f}"
    s.append(f'<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LUZ}" stop-opacity=".3"/><stop offset="1" stop-color="{LUZ}" stop-opacity="0"/></linearGradient><filter id="bl" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="5"/></filter></defs>')
    s.append(f'<text x="{X0}" y="62" font-family="{MONO}" font-size="12" fill="{GR}" letter-spacing="2">{T["sem"]}</text>')
    for v in (0, 30, 60):
        s.append(f'<path d="M{X0} {py(v):.1f}H{X1}" stroke="{LI}" stroke-width="1"/><text x="{X0-8}" y="{py(v)+4:.1f}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{TE}">{v}</text>')
    s.append(f'<path d="{d} L{X1} {Y0} L{X0} {Y0}Z" fill="url(#ar)"/><path d="{d}" fill="none" stroke="{LUZ}" stroke-width="5" opacity="{.5 if OSC else .18}" filter="url(#bl)"/><path d="{d}" fill="none" stroke="{FG}" stroke-width="2" stroke-linejoin="round"/>')
    s.append(f'<circle r="4.5" fill="{FG}" stroke="{BG}" stroke-width="2"><animateMotion dur="8s" repeatCount="indefinite" path="{d}"/></circle>')
    cm = sem.index(mx); s.append(f'<circle cx="{px(cm):.1f}" cy="{py(mx):.1f}" r="5" fill="{FG}" stroke="{BG}" stroke-width="2"/><text x="{px(cm)-12:.1f}" y="{py(mx)+4:.1f}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{FG}">{T["pico"].format(n=mx)}</text>')
    # mapa de calor
    cw = (X1 - X0) / 53; gy = 300
    s.append(f'<text x="{X0}" y="{gy-12}" font-family="{MONO}" font-size="12" fill="{GR}" letter-spacing="2">{T["dia"]}</text>')
    for c in range(53):
        f0 = ini + datetime.timedelta(days=c * 7)
        if f0.day <= 7: s.append(f'<text x="{X0+c*cw:.1f}" y="{gy+7*cw+16:.0f}" font-family="{MONO}" font-size="10.5" fill="{TE}">{meses[f0.month-1]}</text>')
        for r in range(7):
            f = f0 + datetime.timedelta(days=r)
            if f > finf: continue
            n = dias.get(f.isoformat(), 0)
            k = min(1, n / 20) ** .55; col = CERO if n == 0 else "#%02x%02x%02x" % ((int(70 + 172 * k) if OSC else int(170 - 157 * k),) * 3)
            s.append(f'<rect x="{X0+c*cw:.1f}" y="{gy+r*cw:.1f}" width="{cw-2:.1f}" height="{cw-2:.1f}" rx="2" fill="{col}"/>')
    # derecha: por hora y por día
    RX = 900; RW = W - 48 - RX
    s.append(f'<path d="M{RX-27} 48V{H-48}" stroke="{LI}" stroke-width="1.5"/><text x="{RX}" y="62" font-family="{MONO}" font-size="12" fill="{GR}" letter-spacing="2">{T["hora"]}</text>')
    hs = ACT["horas"]; hm = max(hs); bw = RW / 24; by = 212
    for i, v in enumerate(hs):
        hh = 2 + 104 * v / hm
        s.append(f'<rect x="{RX+i*bw+1:.1f}" y="{by-hh:.1f}" width="{bw-3:.1f}" height="{hh:.1f}" rx="2" fill="{FG if v == hm else BARRA}"/>')
    s.append(f'<text x="{RX+hs.index(hm)*bw+bw/2:.1f}" y="{by-112}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{FG}">{T["h10"]}</text>')
    for hlab in (0, 6, 12, 18):
        s.append(f'<text x="{RX+hlab*bw+1:.1f}" y="{by+16}" font-family="{MONO}" font-size="10.5" fill="{TE}">{hlab:02d}h</text>')
    s.append(f'<text x="{RX}" y="286" font-family="{MONO}" font-size="12" fill="{GR}" letter-spacing="2">{T["dsem"]}</text>')
    ws = ACT["semana"]; wm = max(ws); bw = RW / 7; by = 396
    for i, v in enumerate(ws):
        hh = 96 * v / wm
        s.append(f'<rect x="{RX+i*bw+3:.1f}" y="{by-hh:.1f}" width="{bw-8:.1f}" height="{hh:.1f}" rx="3" fill="{FG if i >= 5 else BARRA}"/><text x="{RX+i*bw+bw/2-1:.1f}" y="{by+17}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GR}">{T["letras"][i]}</text>'
                 f'<text x="{RX+i*bw+bw/2-1:.1f}" y="{by-hh-6:.1f}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{GR}">{v}</text>')
    s.append(f'<text x="{X0}" y="{H-30}" font-family="{MONO}" font-size="10.5" fill="{TE}">{T["nota"]}</text>')
    s.append(fin(H)); guardar("actividad.svg", "".join(s))

# ---------------- 4. trayectoria ----------------
def ruta():
    H = 300; s = [base(H, 51, .5, "d")]
    s.append(rot(48, 62, T["ruta"]))
    et = [e + (i == 2,) for i, e in enumerate(T["et"])]
    cw, gap = 340, 49; y = 96; ch = 164
    for i, (f, a, b, d, hoy) in enumerate(et):
        x = 48 + i * (cw + gap)
        if i < 2:
            xa = x + cw; s.append(f'<path d="M{xa} {y+ch/2}h{gap}" stroke="{TE}" stroke-width="2"/><path d="M{xa} {y+ch/2}h{gap}" stroke="{FG}" stroke-width="2" stroke-dasharray="5 9"><animate attributeName="stroke-dashoffset" values="28;0" dur="1s" repeatCount="indefinite"/></path><path d="M{xa+gap-9} {y+ch/2-6}l8 6-8 6" fill="none" stroke="{FG}" stroke-width="2"/>')
        fg, sub, bg = (BG, SUBINV, FG) if hoy else (FG, GR, PAN)
        s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{bg}" stroke="{"none" if hoy else "{BORDE}"}" stroke-width="1.5"/>')
        s.append(f'<text x="{x+22}" y="{y+34}" font-family="{MONO}" font-size="12" fill="{sub}" letter-spacing="2.5">{f}</text>'
                 f'<text x="{x+cw-22}" y="{y+36}" text-anchor="end" font-family="{DISP}" font-weight="900" font-size="22" fill="{fg}" opacity="{.9 if hoy else .25}">0{i+1}</text>'
                 f'<text x="{x+22}" y="{y+72}" font-family="{SANS}" font-weight="800" font-size="20" fill="{fg}">{a}</text><text x="{x+22}" y="{y+95}" font-family="{SANS}" font-size="13.5" fill="{sub}">{b}</text>'
                 f'<text font-family="{SANS}" font-size="13.5" fill="{sub}"><tspan x="{x+22}" y="{y+126}">{d[0]}</tspan><tspan x="{x+22}" y="{y+145}">{d[1]}</tspan></text>')
        if hoy: s.append(f'<circle cx="{x+cw-30}" cy="{y+ch-28}" r="5" fill="{BG}"/><circle cx="{x+cw-30}" cy="{y+ch-28}" r="5" fill="none" stroke="{BG}" stroke-width="1.5"><animate attributeName="r" values="5;15" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.8s" repeatCount="indefinite"/></circle>')
    s.append(fin(H)); guardar("trayectoria.svg", "".join(s))

# ---------------- 5. cierre con automatización ----------------
def cierre():
    H = 360; s = [base(H, 67, .6, "e")]
    s.append(rot(48, 62, T["paso"]))
    s.append(f'<text font-family="{DISP}" font-weight="900" font-size="46" fill="{FG}"><tspan x="46" y="136">{T["c1"]}</tspan><tspan x="46" y="188">{T["c2"]}</tspan></text>')
    s.append(f'<text font-family="{SANS}" font-size="17" fill="{GR}"><tspan x="48" y="232">{T["cs1"]}</tspan><tspan x="48" y="257">{T["cs2"]}</tspan></text>')
    s.append(f'<text x="48" y="{H-40}" font-family="{MONO}" font-size="12" fill="{TE}" letter-spacing="2">{T["abajo"]}</text>')
    # máquina: tareas entran, engranaje procesa, salen hechas
    cy = 190; x0, xm, x1 = 610, 880, 1166
    s.append(f'<path d="M{x0} {cy}H{x1}" stroke="{TE}" stroke-width="2"/><path d="M{x0} {cy}H{x1}" stroke="{FG}" stroke-width="2" stroke-dasharray="5 9" opacity=".7"><animate attributeName="stroke-dashoffset" values="28;0" dur="1s" repeatCount="indefinite"/></path>')
    for i in range(3):   # documentos que entran
        s.append(f'<g opacity="0"><animateTransform attributeName="transform" type="translate" values="{x0-10} 0;{xm-70} 0" dur="4.5s" begin="{-i*1.5}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="4.5s" begin="{-i*1.5}s" repeatCount="indefinite"/>'
                 f'<rect x="-17" y="{cy-23}" width="34" height="46" rx="5" fill="{PAN}" stroke="{FG}" stroke-width="1.8"/><path d="M-9 {cy-10}h18M-9 {cy-1}h18M-9 {cy+8}h11" stroke="{GR}" stroke-width="2"/></g>')
    for i in range(3):   # hechos que salen
        s.append(f'<g opacity="0"><animateTransform attributeName="transform" type="translate" values="{xm+70} 0;{x1-14} 0" dur="4.5s" begin="{-i*1.5-.7}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="4.5s" begin="{-i*1.5-.7}s" repeatCount="indefinite"/>'
                 f'<circle cx="0" cy="{cy}" r="19" fill="{FG}"/><path d="M-8 {cy}l6 6 11-12" stroke="{BG}" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    # núcleo
    s.append(f'<circle cx="{xm}" cy="{cy}" r="86" fill="{BG}" stroke="{LI}" stroke-width="1.5"/><circle cx="{xm}" cy="{cy}" r="86" fill="none" stroke="{FG}" stroke-width="2" stroke-dasharray="60 480" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="0 {xm} {cy}" to="360 {xm} {cy}" dur="5s" repeatCount="indefinite"/></circle>')
    def eng(cx, cyy, r, n, dur, sent):
        p = []
        for k in range(n * 2):
            a0 = math.pi * k / n; a1 = math.pi * (k + 1) / n; rr = r if k % 2 == 0 else r * .78
            p.append(f'{"M" if k == 0 else "L"}{cx+rr*math.cos(a0):.1f} {cyy+rr*math.sin(a0):.1f} L{cx+rr*math.cos(a1):.1f} {cyy+rr*math.sin(a1):.1f}')
        return (f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cyy}" to="{sent*360} {cx} {cyy}" dur="{dur}s" repeatCount="indefinite"/><path d="{" ".join(p)}Z" fill="{PAN}" stroke="{FG}" stroke-width="2" stroke-linejoin="round"/><circle cx="{cx}" cy="{cyy}" r="{r*.3:.1f}" fill="{BG}" stroke="{FG}" stroke-width="2"/></g>')
    s.append(eng(xm - 20, cy + 8, 42, 10, 8, 1) + eng(xm + 38, cy - 28, 26, 8, 5, -1))
    # tecnologías alrededor
    for i, (slug, ang) in enumerate([("n8n", -150), ("ollama", -90), ("PA", -30), ("supabase", 30), ("react", 90), ("dotnet", 150)]):
        a = math.radians(ang); x = xm + 132 * math.cos(a); y = cy + 132 * math.sin(a)
        s.append(f'<g><animate attributeName="opacity" values=".45;1;.45" dur="3s" begin="{-i*.5}s" repeatCount="indefinite"/><circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{BG}" stroke="{BORDE}" stroke-width="1.5"/>{icono(slug, x-11, y-11, 22)}</g>')
    s.append(f'<text x="{x0+40}" y="{cy+66}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GR}" letter-spacing="2">{T["tareas"]}</text><text x="{x1-40}" y="{cy+66}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GR}" letter-spacing="2">{T["hecho"]}</text>')
    s.append(fin(H)); guardar("contacto.svg", "".join(s))

def boton(fn, txt, lleno):
    w = 44 + len(txt) * 10.4; h = 50
    guardar(fn, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h}" width="{w:.0f}" height="{h}"><rect x="1" y="1" width="{w-2:.0f}" height="{h-2}" rx="12" fill="{FG if lleno else BG}" stroke="{FG}" stroke-width="1.5"/>'
        f'<text x="{w/2:.0f}" y="31" text-anchor="middle" font-family="{MONO}" font-size="15.5" font-weight="700" fill="{BG if lleno else FG}">{txt}</text></svg>')

def readme(idioma):
    T = TEXTOS[idioma]; A = T["alt"]
    pic = lambda f, attr, alt: f'<picture><source media="(prefers-color-scheme: light)" srcset="assets/claro/{idioma}/{f}"><img src="assets/oscuro/{idioma}/{f}" {attr} alt="{esc(alt)}"></picture>'
    L = [f'<p align="right"><a href="{T["otro"]}">{pic("b-idioma.svg", 'height="30"', A["idioma"])}</a></p>', "",
         f'<p align="center"><img src="assets/portada-{idioma}.gif" width="100%" alt="{esc(A["banner"])}"></p>', ""]
    for f, k in (("yo", "yo"), ("stack", "stack"), ("actividad", "actividad"), ("trayectoria", "ruta"), ("contacto", "cierre")): L += [f'<p align="center">{pic(f + ".svg", 'width="100%"', A[k])}</p>', ""]
    L += [f'<p align="center"><a href="https://github.com/LordVincenzo/LordVincenzo/raw/main/Briand_Castro_CV.pdf">{pic("b-cv.svg", 'height="44"', A["cv"])}</a>&nbsp;&nbsp;&nbsp;'
          f'<a href="mailto:Briandcastro11b@gmail.com">{pic("b-mail.svg", 'height="44"', A["mail"])}</a></p>', ""]
    open(os.path.join(ROOT, T["fn"]), "w", encoding="utf-8").write("\n".join(L))

if __name__ == "__main__":
    for tema in TEMAS:
        for idioma in TEXTOS:
            usar(tema, idioma); yo(); stack(); actividad(); ruta(); cierre()
            boton("b-cv.svg", T["b_cv"], True); boton("b-mail.svg", T["b_mail"], False); boton("b-idioma.svg", T["b_idioma"], False)
    for idioma in TEXTOS: readme(idioma)
