#!/usr/bin/env python3
"""Genera los paneles del perfil (qué hago, stack, trayectoria, actividad, cierre), los botones y los dos README.

    python scripts/build.py

Solo usa la librería estándar. El banner animado se genera aparte: ver scripts/agujero/LEEME.md.
"""
import datetime as dt, html, json, math, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
CORREO = "Briandcastro11b@gmail.com"
CV = "https://github.com/LordVincenzo/LordVincenzo/raw/main/Briand_Castro_CV.pdf"
STACK = [["TypeScript", "JavaScript", "C#", "PHP", "SQL", "React", "Next.js", "Tailwind CSS", "Ionic"],
         ["Node.js", ".NET", "PostgreSQL", "MySQL", "MongoDB", "Supabase", "Firebase", "n8n", "Power Automate", "Power BI", "Docker", "Unity"]]
NEGRO, FG, GRIS, TENUE, LINEA = "#030303", "#f4f4f4", "#a8a8a8", "#5e5e5e", "#222222"
TEMAS = {"oscuro": ("#f2f2f2", "#0d0d0d"), "claro": ("#0d0d0d", "#ffffff")}        # botones: (tinta, fondo del lleno)
TEXTOS = {
    "es": dict(frase="Automatizo lo repetitivo con <b>n8n</b> y construyo apps web y móviles de punta a punta.",
               sobre="Tecnólogo en Análisis y Desarrollo de Software. Hoy gestiono la plataforma educativa <b>Prizma</b> en la Corporación Universitaria Americana, donde automaticé el cargue de cursos.",
               botones=[("escribeme", "Escríbeme", f"mailto:{CORREO}"), ("cv", "Hoja de vida", CV), ("idioma", "English", "README.en.md")],
               banner="Briand Castro, analista y desarrollador de software. Soledad, Colombia. Animación de un agujero negro con su disco de luz girando.",
               hago=[("DESARROLLO", "Web y móvil", ["Interfaces, APIs y bases de datos:", "de la idea a la app funcionando."]),
                     ("AUTOMATIZACIÓN", "Que lo haga el sistema", ["Flujos con n8n y Power Automate", "que ahorran horas de trabajo manual."]),
                     ("DATOS", "Datos que se entienden", ["Reportes y tableros en Power BI", "sobre bases SQL y NoSQL."])],
               ruta_t="TRAYECTORIA", hitos=[("2023 — 2025", "Tecnólogo ADSO", "SENA"), ("ENE — JUL 2025", "Calidad de Proveedores", "Procaps"),
                                            ("SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana")],
               act_t="MI AÑO EN COMMITS", cifras=["commits", "días activos", "hora pico"], am="a. m.", pm="p. m.",
               act_n=["Cada estrella de la galaxia es un día con commits.", "{n} proyectos · datos al {f}"],
               meses=["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
               cierre="¿Automatizamos algo juntos?", cierre_s="Cuéntame qué tarea repetitiva te quita tiempo.", escribe="Escríbeme"),
    "en": dict(frase="I automate the repetitive with <b>n8n</b> and build web and mobile apps end to end.",
               sobre="Technologist in Software Analysis and Development. Today I manage the <b>Prizma</b> learning platform at Corporación Universitaria Americana, where I automated course loading.",
               botones=[("escribeme", "Email me", f"mailto:{CORREO}"), ("cv", "Résumé", CV), ("idioma", "Español", "README.md")],
               banner="Briand Castro, software analyst and developer. Soledad, Colombia. Animation of a black hole with its spinning disk of light.",
               hago=[("DEVELOPMENT", "Web and mobile", ["Interfaces, APIs and databases:", "from the idea to a working app."]),
                     ("AUTOMATION", "Let the system do it", ["n8n and Power Automate workflows", "that save hours of manual work."]),
                     ("DATA", "Data people understand", ["Power BI reports and dashboards", "on SQL and NoSQL databases."])],
               ruta_t="JOURNEY", hitos=[("2023 — 2025", "ADSO Technologist", "SENA"), ("JAN — JUL 2025", "Supplier Quality", "Procaps"),
                                        ("SEP 2025 — NOW", "Prizma Platform Manager", "Corporación Universitaria Americana")],
               act_t="MY YEAR IN COMMITS", cifras=["commits", "active days", "peak hour"], am="AM", pm="PM",
               act_n=["Each star in the galaxy is a day with commits.", "{n} projects · data as of {f}"],
               meses=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
               cierre="Shall we automate something?", cierre_s="Tell me which repetitive task eats your time.", escribe="Email me"),
}
e = html.escape
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
TW = ".tw{animation:tw 3.2s ease-in-out infinite}@keyframes tw{50%{opacity:.15}}"
DEFS = ('<radialGradient id="esf" cx=".34" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#a9a9a9"/><stop offset="1" stop-color="#161616"/></radialGradient>'
        '<radialGradient id="esf2" cx=".34" cy=".3" r=".8"><stop offset="0" stop-color="#cfcfcf"/><stop offset=".5" stop-color="#6d6d6d"/><stop offset="1" stop-color="#0c0c0c"/></radialGradient>'
        '<radialGradient id="halo"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>')


def panel(idioma, nombre, W, H, label, body, style="", defs="", semilla=1, n=None, fondo=NEGRO):
    """Panel negro con esquinas redondeadas y un cielo de estrellas de fondo."""
    r = random.Random(semilla)
    cielo = ""
    for _ in range(n if n is not None else W * H // 5200):
        tw = f' class="tw" style="animation-delay:{r.uniform(0, 3.2):.1f}s"' if r.random() < .22 else ""
        cielo += f'<circle{tw} cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{r.choice([.6, .8, .8, 1.1, 1.5])}" fill="#fff" fill-opacity="{r.uniform(.2, .8):.2f}"/>'
    d = os.path.join(OUT, idioma); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, nombre), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(label)}">'
        f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="20"/></clipPath>{DEFS}{defs}</defs><style>{TW}{style}{REDUCE}</style>'
        f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{fondo}"/>{cielo}{body}</g>'
        f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="19.5" fill="none" stroke="{LINEA}" stroke-width="1.5"/></svg>')


def rotulo(x, y, texto):
    return (f'<path d="M{x+6} {y-12} Q{x+6} {y-5} {x+13} {y-5} Q{x+6} {y-5} {x+6} {y+2} Q{x+6} {y-5} {x-1} {y-5} Q{x+6} {y-5} {x+6} {y-12} Z" fill="{FG}"/>'
            f'<text x="{x+26}" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="{GRIS}">{e(texto)}</text>')


# ───────────── qué hago: tres tarjetas ─────────────
def hago(idioma):
    T = TEXTOS[idioma]
    anillo = 'rx="92" ry="24" fill="none" stroke="#e9e9e9" stroke-width="5" transform="rotate(-18 196 132)"'
    escenas = [
        # planeta con anillo y una luna
        f'<circle cx="196" cy="132" r="118" fill="url(#halo)" opacity=".7"/><ellipse cx="196" cy="132" {anillo} stroke-opacity=".55"/>'
        f'<circle cx="196" cy="132" r="50" fill="url(#esf)"/><path d="M150 118 q46 12 92 -2 M148 140 q48 14 96 0" fill="none" stroke="#000" stroke-opacity=".16" stroke-width="5"/>'
        f'<path d="M108.5 160.4 A92 24 -18 0 0 283.5 103.6" fill="none" stroke="#e9e9e9" stroke-width="5" stroke-linecap="round" transform="rotate(0)" />'
        f'<g transform="rotate(-18 196 132)"><circle r="7" fill="url(#esf)"><animateMotion dur="7s" repeatCount="indefinite" path="M66 132 a130 34 0 1 0 260 0 a130 34 0 1 0 -260 0"/></circle></g>',
        # sistema que gira solo
        f'<circle cx="196" cy="132" r="90" fill="url(#halo)"/><g transform="rotate(-14 196 132)">'
        + "".join(f'<ellipse cx="196" cy="132" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity=".2" stroke-width="1.3"/>' for rx, ry in ((54, 18), (92, 31), (130, 44)))
        + f'<circle cx="196" cy="132" r="17" fill="#fff"/>'
        + "".join(f'<circle r="{r}" fill="url(#{g})"><animateMotion dur="{d}s" begin="-{b}s" repeatCount="indefinite" path="M{196-rx} 132 a{rx} {ry} 0 1 0 {2*rx} 0 a{rx} {ry} 0 1 0 -{2*rx} 0"/></circle>'
                  for r, g, d, b, rx, ry in ((6, "esf", 3.2, 0, 54, 18), (10, "esf2", 6.5, 2, 92, 31), (8, "esf", 11, 5, 130, 44))) + "</g>",
        # constelación con forma de gráfica
        "".join(f'<path d="M56 {y} H336" stroke="#fff" stroke-opacity=".07"/>' for y in (70, 110, 150, 190))
        + '<path class="traza" d="M62 186 L122 150 L176 166 L242 108 L322 62" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r*3.2}" fill="url(#halo)"/><circle class="tw" style="animation-delay:{i*.6}s" cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
                  for i, (x, y, r) in enumerate([(62, 186, 4), (122, 150, 5), (176, 166, 4), (242, 108, 6), (322, 62, 9)]))]
    for i, ((tag, tit, desc), esc) in enumerate(zip(T["hago"], escenas)):
        body = (esc + f'<text x="34" y="284" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{GRIS}">0{i+1} — {tag}</text>'
                f'<text x="34" y="322" font-family="{SANS}" font-size="27" font-weight="800" letter-spacing="-.3" fill="{FG}">{e(tit)}</text>'
                + "".join(f'<text x="34" y="{352+j*23}" font-family="{SANS}" font-size="16" fill="{GRIS}">{e(l)}</text>' for j, l in enumerate(desc)))
        panel(idioma, f"hago-{i+1}.svg", 392, 410, f"{tit}: {' '.join(desc)}", body,
              ".traza{stroke-dasharray:420;animation:traza 5s ease-in-out infinite}@keyframes traza{0%{stroke-dashoffset:420}45%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-420}}", semilla=20 + i, n=34)


# ───────────── stack ─────────────
def stack(idioma):
    W, H = 1200, 250
    body, style = rotulo(44, 52, "STACK"), ""
    for i, items in enumerate(STACK):
        unidad, x = "", 0
        for t in items:
            w = round(len(t) * 10.4) + 40
            unidad += (f'<rect x="{x}" y="0" width="{w}" height="44" rx="22" fill="{"#fff" if i == 0 else "#0a0a0a"}" stroke="#fff" stroke-opacity="{1 if i == 0 else .45}" stroke-width="1.4"/>'
                       f'<text x="{x+w/2}" y="28.5" text-anchor="middle" font-family="{MONO}" font-size="16.5" font-weight="700" fill="{"#050505" if i == 0 else FG}" textLength="{w-40}" lengthAdjust="spacingAndGlyphs">{e(t)}</text>')
            x += w + 14
        reps = -(-(W + x) // x) + 1
        style += f".c{i}{{animation:c{i} {x/30:.1f}s linear infinite {'normal' if i == 0 else 'reverse'}}}@keyframes c{i}{{to{{transform:translateX(-{x}px)}}}}"
        body += f'<g transform="translate(0,{84+i*62})"><g class="c{i}">{"".join(f"<g transform=\'translate({k*x},0)\'>{unidad}</g>" for k in range(int(reps)))}</g></g>'
    body += ('<rect width="170" height="250" fill="url(#bi)"/><rect x="1030" width="170" height="250" fill="url(#bd)"/>')
    defs = (f'<linearGradient id="bi" x1="0" x2="1"><stop offset="0" stop-color="{NEGRO}"/><stop offset="1" stop-color="{NEGRO}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{NEGRO}" stop-opacity="0"/><stop offset="1" stop-color="{NEGRO}"/></linearGradient>')
    panel(idioma, "stack.svg", W, H, "Stack: " + ", ".join(STACK[0] + STACK[1]), body, style, defs, semilla=5, n=60)


# ───────────── trayectoria: tres planetas sobre una órbita ─────────────
def ruta(idioma):
    T, W, H = TEXTOS[idioma], 1200, 400
    P = [(-60, 318), (300, 40), (820, 20), (1280, 214)]
    def bez(t):
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        return a * P[0][0] + b * P[1][0] + c * P[2][0] + d * P[3][0], a * P[0][1] + b * P[1][1] + c * P[2][1] + d * P[3][1]
    camino = f"M{P[0][0]} {P[0][1]} C{P[1][0]} {P[1][1]} {P[2][0]} {P[2][1]} {P[3][0]} {P[3][1]}"
    body = (rotulo(44, 52, T["ruta_t"]) + f'<path d="{camino}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.5" stroke-dasharray="2 9" stroke-linecap="round"/>'
            f'<g><circle r="4" fill="#fff"/><path d="M0 0 h-46" stroke="url(#cola)" stroke-width="3" stroke-linecap="round"/><animateMotion dur="9s" repeatCount="indefinite" rotate="auto" path="{camino}"/></g>')
    for i, (t, r, (fecha, tit, org)) in enumerate(zip((.15, .43, .69), (17, 26, 44), T["hitos"])):
        x, y = bez(t); hoy = i == 2
        body += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.6:.0f}" fill="url(#halo)" opacity="{.9 if hoy else .45}"/>'
                 + (f'<circle class="onda" cx="{x:.0f}" cy="{y:.0f}" r="{r+8}" fill="none" stroke="#fff" stroke-width="1.4"/>'
                    f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*1.9:.0f}" ry="{r*.45:.0f}" fill="none" stroke="#e9e9e9" stroke-opacity=".5" stroke-width="4" transform="rotate(-16 {x:.0f} {y:.0f})"/>' if hoy else "")
                 + f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="url(#{"esf" if hoy else "esf2"})"/>'
                 + (f'<path d="M{x-r*1.9:.1f} {y:.1f} A{r*1.9:.1f} {r*.45:.1f} 0 0 0 {x+r*1.9:.1f} {y:.1f}" fill="none" stroke="#e9e9e9" stroke-width="4" stroke-linecap="round" transform="rotate(-16 {x:.0f} {y:.0f})"/>' if hoy else "")
                 + f'<text x="{x-r:.0f}" y="{y+r+44+(14 if hoy else 0):.0f}" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{GRIS}">{fecha}</text>'
                 f'<text x="{x-r:.0f}" y="{y+r+76+(14 if hoy else 0):.0f}" font-family="{SANS}" font-size="{26 if hoy else 22}" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 f'<text x="{x-r:.0f}" y="{y+r+102+(14 if hoy else 0):.0f}" font-family="{SANS}" font-size="15.5" fill="{GRIS}">{e(org)}</text>')
    defs = '<linearGradient id="cola" x1="1" x2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    panel(idioma, "ruta.svg", W, H, T["ruta_t"].title() + ": " + "; ".join(f"{t}, {o} ({f})" for f, t, o in T["hitos"]), body,
          ".onda{animation:onda 2.6s ease-out infinite;transform-box:fill-box;transform-origin:center}@keyframes onda{to{transform:scale(1.9);opacity:0}}", defs, semilla=9)


# ───────────── actividad: una galaxia hecha con los commits ─────────────
def actividad(idioma, data):
    T, W, H = TEXTOS[idioma], 1200, 470
    fin = dt.date.fromisoformat(data["hasta"])
    dias = [(fin - dt.timedelta(days=364 - k)) for k in range(365)]
    cuenta = [data["dias"].get(d.isoformat(), 0) for d in dias]
    total, activos = sum(cuenta), sum(1 for c in cuenta if c)
    pico = data["horas"].index(max(data["horas"]))
    hora = f"{(pico % 12) or 12} {T['am'] if pico < 12 else T['pm']}"
    r = random.Random(42)
    polvo, soles = "", ""
    for k, c in enumerate(cuenta):                      # el tiempo avanza del centro hacia el borde, por dos brazos
        s = k / 364
        ang = (k % 2) * math.pi + s * 2.35 * 2 * math.pi + r.uniform(-.09, .09)
        rad = 34 + s * 300 + r.uniform(-9, 9)
        x, y = rad * math.cos(ang), rad * math.sin(ang)
        if c:
            rr = min(13, 3.6 + 1.5 * math.sqrt(c))
            soles += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr*3:.1f}" fill="url(#halo)"/>'
                      f'<circle class="tw" style="animation-delay:{r.uniform(0, 3):.1f}s" cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="#fff"><title>{dias[k]}: {c}</title></circle>')
        else:
            polvo += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.choice([1.1, 1.4, 1.8])}" fill="#fff" fill-opacity="{r.uniform(.2, .55):.2f}"/>'
    for _ in range(900):                                 # bruma de los brazos
        s = r.random() ** .8; ang = r.choice([0, math.pi]) + s * 2.35 * 2 * math.pi + r.gauss(0, .22); rad = 26 + s * 312 + r.gauss(0, 12)
        polvo += f'<circle cx="{rad*math.cos(ang):.1f}" cy="{rad*math.sin(ang):.1f}" r="{r.choice([.5, .7, .9])}" fill="#fff" fill-opacity="{r.uniform(.06, .26):.2f}"/>'
    gx, gy = 800, 226
    galaxia = (f'<g transform="translate({gx} {gy}) rotate(-17) scale(1 .6)"><circle r="360" fill="url(#halo)" opacity=".35"/>'
               f'<g class="gal">{polvo}{soles}</g><circle r="96" fill="url(#halo)"/><circle r="22" fill="#fff" filter="url(#blur)"/><circle r="11" fill="#fff"/></g>')
    body = rotulo(44, 52, T["act_t"]) + galaxia
    for i, (v, lab) in enumerate(zip([str(total), str(activos), hora], T["cifras"])):
        y = 150 + i * 104
        body += (f'<text x="42" y="{y}" font-family="{SANS}" font-size="64" font-weight="800" letter-spacing="-2" fill="{FG}">{v}</text>'
                 f'<text x="46" y="{y+26}" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{GRIS}">{lab.upper()}</text>')
    n1, n2 = T["act_n"]
    n2 = n2.format(n=data["proyectos"], f=f"{fin.day} {T['meses'][fin.month-1]} {fin.year}")
    body += (f'<text x="{W-44}" y="{H-50}" text-anchor="end" font-family="{SANS}" font-size="14" fill="{GRIS}">{e(n1)}</text>'
             f'<text x="{W-44}" y="{H-28}" text-anchor="end" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{TENUE}">{e(n2)}</text>')
    panel(idioma, "actividad.svg", W, H, f"{T['act_t'].title()}: {total} commits, {activos} {T['cifras'][1]}, {T['cifras'][2]} {hora}. {n1}", body,
          ".gal{animation:gal 150s linear infinite}@keyframes gal{to{transform:rotate(360deg)}}", semilla=3, n=70)


# ───────────── cierre: amanecer sobre un planeta ─────────────
def cierre(idioma):
    T, W, H = TEXTOS[idioma], 1200, 300
    w = round(len(T["escribe"]) * 11) + 96
    defs = ('<radialGradient id="alba" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset=".25" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="borde" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    body = f'''<ellipse class="alba" cx="600" cy="262" rx="520" ry="150" fill="url(#alba)"/>
<circle cx="600" cy="1462" r="1200" fill="#000"/><circle cx="600" cy="1462" r="1200" fill="none" stroke="url(#borde)" stroke-width="2.5"/>
<circle cx="600" cy="262" r="26" fill="#fff" filter="url(#blur)"/><circle class="sol" cx="600" cy="262" r="7" fill="#fff"/>
<text x="600" y="92" text-anchor="middle" font-family="{SANS}" font-size="44" font-weight="800" letter-spacing="-1" fill="{FG}">{e(T["cierre"])}</text>
<text x="600" y="128" text-anchor="middle" font-family="{SANS}" font-size="18" fill="{GRIS}">{e(T["cierre_s"])}</text>
<rect x="{600-w/2}" y="158" width="{w}" height="54" rx="27" fill="#fff"/>
<text x="{600-14}" y="192" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="800" fill="#050505">{e(T["escribe"])}</text>
<path class="fl" d="M{600+w/2-52} 185 h22 m-8 -8 l8 8 l-8 8" fill="none" stroke="#050505" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'''
    panel(idioma, "cierre.svg", W, H, f"{T['cierre']} {T['escribe']}.", body,
          ".alba{animation:alba 5s ease-in-out infinite;transform-origin:600px 262px}@keyframes alba{50%{transform:scale(1.12);opacity:.8}}"
          ".sol{animation:sol 5s ease-in-out infinite}@keyframes sol{50%{r:10px}}.fl{animation:fl 1.4s ease-in-out infinite}@keyframes fl{50%{transform:translateX(6px)}}", defs, semilla=14, n=70)


# ───────────── botones y README ─────────────
def boton(tema, idioma, clave, texto, lleno):
    tinta, fondo = TEMAS[tema]
    w = int(len(texto) * 9.4) + 64
    brillo = (f'<clipPath id="c"><rect x="1" y="1" width="{w-2}" height="44" rx="22"/></clipPath>'
              f'<g clip-path="url(#c)"><rect class="b" x="-60" y="0" width="46" height="46" fill="{fondo}" fill-opacity=".28" transform="skewX(-20)"/></g>') if lleno else ""
    d = os.path.join(OUT, "botones", tema, idioma); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"{clave}.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 46" width="{w}" height="46" role="img" aria-label="{e(texto)}">'
        f'<style>.b{{animation:b 3.6s ease-in-out infinite}}@keyframes b{{0%,55%{{transform:translateX(0) skewX(-20deg)}}100%{{transform:translateX({w+120}px) skewX(-20deg)}}}}{REDUCE}</style>'
        f'<rect x="1" y="1" width="{w-2}" height="44" rx="22" fill="{tinta if lleno else "none"}" stroke="{tinta}" stroke-width="1.6"/>{brillo}'
        f'<text x="{w/2}" y="29" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{fondo if lleno else tinta}">{e(texto)}</text></svg>')


def readme(idioma):
    T = TEXTOS[idioma]
    alt = lambda n: html.unescape(re.search(r'aria-label="([^"]*)"', open(os.path.join(OUT, idioma, n + ".svg"), encoding="utf-8").read()).group(1))
    img = lambda n, w: f'<img src="assets/{idioma}/{n}.svg" width="{w}" alt="{e(alt(n))}">'
    bot = [f'<a href="{url}"><picture><source media="(prefers-color-scheme: light)" srcset="assets/botones/claro/{idioma}/{clave}.svg">'
           f'<img src="assets/botones/oscuro/{idioma}/{clave}.svg" height="44" alt="{e(texto)}"></picture></a>' for clave, texto, url in T["botones"]]
    out = [f'<img src="assets/banner-{idioma}.gif" width="100%" alt="{e(T["banner"])}">', "", "<br>", "",
           f'<p align="center">{T["frase"]}<br>{T["sobre"]}</p>', "", '<p align="center">', "&nbsp;\n".join(bot), "</p>", "", "<br>", "",
           "<p>", img("hago-1", "32.9%"), img("hago-2", "32.9%"), img("hago-3", "32.9%"), img("stack", "100%"), img("ruta", "100%"), img("actividad", "100%"),
           f'<a href="mailto:{CORREO}">{img("cierre", "100%")}</a>', "</p>", ""]
    open(os.path.join(ROOT, "README.md" if idioma == "es" else "README.en.md"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    data = json.load(open(os.path.join(ROOT, "data", "actividad.json"), encoding="utf-8"))
    for idioma, T in TEXTOS.items():
        hago(idioma); stack(idioma); ruta(idioma); actividad(idioma, data); cierre(idioma)
        for tema in TEMAS:
            for i, (clave, texto, _) in enumerate(T["botones"]):
                boton(tema, idioma, clave, texto, i == 0)
        readme(idioma)
    print("Listo")
