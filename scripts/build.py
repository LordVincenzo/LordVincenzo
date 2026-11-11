#!/usr/bin/env python3
"""Genera los botones, los bloques (qué hago, trayectoria, actividad), la cinta del stack y los dos README. Solo librería estándar.

    python scripts/build.py

El banner animado se genera aparte: ver scripts/agujero/LEEME.md.
"""
import datetime as dt, html, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
CORREO = "Briandcastro11b@gmail.com"
CV = "https://github.com/LordVincenzo/LordVincenzo/raw/main/Briand_Castro_CV.pdf"
STACK = ["TypeScript", "React", "Next.js", "Node.js", ".NET", "PostgreSQL", "MongoDB", "Supabase", "n8n", "Power Automate", "Power BI", "Docker", "Unity"]
TEMAS = {"oscuro": ("#f2f2f2", "#0d0d0d"), "claro": ("#0d0d0d", "#ffffff")}        # (tinta, fondo del botón lleno)
TONOS = {"oscuro": dict(FG="#f2f2f2", GRIS="#9a9a9a", TENUE="#5c5c5c", LINEA="#2e2e2e"),
         "claro": dict(FG="#0d0d0d", GRIS="#5a5a5a", TENUE="#a6a6a6", LINEA="#d9d9d9")}
TEXTOS = {
    "es": dict(frase="Automatizo lo repetitivo con <b>n8n</b> y construyo apps web y móviles de punta a punta.",
               sobre="Tecnólogo en Análisis y Desarrollo de Software. Hoy gestiono la plataforma educativa <b>Prizma</b> en la Corporación Universitaria Americana, donde automaticé el cargue de cursos.",
               botones=[("escribeme", "Escríbeme", f"mailto:{CORREO}"), ("cv", "Hoja de vida", CV), ("idioma", "English", "README.en.md")],
               banner="Briand Castro, analista y desarrollador de software. Soledad, Colombia. Animación de un agujero negro con su disco de luz girando.",
               hago_t="QUÉ HAGO", hago=[("DESARROLLO", "Web y móvil", ["Interfaces, APIs y bases de datos:", "de la idea a la app funcionando."]),
                                        ("AUTOMATIZACIÓN", "Que lo haga el sistema", ["Flujos con n8n y Power Automate", "que ahorran horas de trabajo manual."]),
                                        ("DATOS", "Datos que se entienden", ["Reportes y tableros en Power BI", "sobre bases SQL y NoSQL."])],
               ruta_t="TRAYECTORIA", hitos=[("2023 — 2025", "Tecnólogo ADSO", "SENA"), ("ENE — JUL 2025", "Calidad de Proveedores", "Procaps"),
                                            ("SEP 2025 — HOY", "Gestor de Plataforma Prizma", "Corporación Universitaria Americana")],
               act_t="ACTIVIDAD · ÚLTIMO AÑO", cifras=["commits", "días activos", "hora pico"], am="a. m.", pm="p. m.",
               act_n="Cada estrella es un día con commits en {n} proyectos · datos al {f}",
               meses=["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]),
    "en": dict(frase="I automate the repetitive with <b>n8n</b> and build web and mobile apps end to end.",
               sobre="Technologist in Software Analysis and Development. Today I manage the <b>Prizma</b> learning platform at Corporación Universitaria Americana, where I automated course loading.",
               botones=[("escribeme", "Email me", f"mailto:{CORREO}"), ("cv", "Résumé", CV), ("idioma", "Español", "README.md")],
               banner="Briand Castro, software analyst and developer. Soledad, Colombia. Animation of a black hole with its spinning disk of light.",
               hago_t="WHAT I DO", hago=[("DEVELOPMENT", "Web and mobile", ["Interfaces, APIs and databases:", "from the idea to a working app."]),
                                         ("AUTOMATION", "Let the system do it", ["n8n and Power Automate workflows", "that save hours of manual work."]),
                                         ("DATA", "Data people understand", ["Power BI reports and dashboards", "on SQL and NoSQL databases."])],
               ruta_t="JOURNEY", hitos=[("2023 — 2025", "ADSO Technologist", "SENA"), ("JAN — JUL 2025", "Supplier Quality", "Procaps"),
                                        ("SEP 2025 — NOW", "Prizma Platform Manager", "Corporación Universitaria Americana")],
               act_t="ACTIVITY · PAST YEAR", cifras=["commits", "active days", "peak hour"], am="AM", pm="PM",
               act_n="Each star is a day with commits across {n} projects · data as of {f}",
               meses=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
}
e = html.escape
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def boton(tema, idioma, clave, texto, lleno):
    tinta, fondo = TEMAS[tema]
    w = int(len(texto) * 9.4) + 64
    brillo = (f'<clipPath id="c"><rect x="1" y="1" width="{w-2}" height="44" rx="22"/></clipPath>'
              f'<g clip-path="url(#c)"><rect class="b" x="-60" y="0" width="46" height="46" fill="{fondo}" fill-opacity=".28" transform="skewX(-20)"/></g>') if lleno else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 46" width="{w}" height="46" role="img" aria-label="{e(texto)}">'
           f'<style>.b{{animation:b 3.6s ease-in-out infinite}}@keyframes b{{0%,55%{{transform:translateX(0) skewX(-20deg)}}100%{{transform:translateX({w+120}px) skewX(-20deg)}}}}{REDUCE}</style>'
           f'<rect x="1" y="1" width="{w-2}" height="44" rx="22" fill="{tinta if lleno else "none"}" stroke="{tinta}" stroke-width="1.6"/>{brillo}'
           f'<text x="{w/2}" y="29" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{fondo if lleno else tinta}">{e(texto)}</text></svg>')
    d = os.path.join(OUT, tema, idioma); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"btn-{clave}.svg"), "w", encoding="utf-8").write(svg)


def cinta():
    """Una sola línea con el stack, desplazándose. Gris medio: se lee igual en tema claro y oscuro."""
    W, H = 1200, 44
    unidad, x = "", 0
    for t in STACK:
        w = round(len(t) * 9.7)
        unidad += f'<text x="{x}" y="28" font-family="{MONO}" font-size="16" fill="#8a8a8a" textLength="{w}" lengthAdjust="spacingAndGlyphs">{e(t)}</text><circle cx="{x+w+23}" cy="22.5" r="2.4" fill="#8a8a8a" fill-opacity=".6"/>'
        x += w + 46
    reps = -(-(W + x) // x) + 1
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Stack: {e(", ".join(STACK))}">'
           f'<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
           f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#f)"/></mask></defs>'
           f'<style>.c{{animation:c {x/34:.1f}s linear infinite}}@keyframes c{{to{{transform:translateX(-{x}px)}}}}{REDUCE}</style>'
           f'<g mask="url(#m)"><g class="c">{"".join(f"<g transform=\'translate({k*x},0)\'>{unidad}</g>" for k in range(reps))}</g></g></svg>')
    open(os.path.join(OUT, "cinta.svg"), "w", encoding="utf-8").write(svg)


def estrella(x, y, r, extra=""):
    """Estrella de cuatro puntas."""
    return f'<path d="M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} Q{x} {y} {x} {y-r} Z"{extra}/>'


def guardar(tema, idioma, nombre, W, H, label, body, style=""):
    d = os.path.join(OUT, tema, idioma); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, nombre), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(label)}"><style>{style}{REDUCE}</style>{body}</svg>')


def rotulo(c, x, y, texto):
    return (estrella(x + 6, y - 5, 7, f' fill="{c["FG"]}" class="tw"')
            + f'<text x="{x+24}" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="{c["GRIS"]}">{e(texto)}</text>')


TW = ".tw{animation:tw 3s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes tw{50%{transform:scale(.6);opacity:.5}}"


def hago(tema, idioma):
    c, T, W, H = TONOS[tema], TEXTOS[idioma], 1200, 270
    FG, GRIS, TENUE, LINEA = c["FG"], c["GRIS"], c["TENUE"], c["LINEA"]
    iconos = [
        # un planeta con su luna
        f'<ellipse cx="40" cy="34" rx="38" ry="13" fill="none" stroke="{TENUE}" stroke-width="1.3" transform="rotate(-14 40 34)"/><circle cx="40" cy="34" r="11" fill="{FG}"/>'
        f'<g transform="rotate(-14 40 34)"><circle r="4" fill="{GRIS}"><animateMotion dur="5s" repeatCount="indefinite" path="M2 34 a38 13 0 1 0 76 0 a38 13 0 1 0 -76 0"/></circle></g>',
        # dos cuerpos girando uno alrededor del otro
        f'<circle cx="40" cy="34" r="27" fill="none" stroke="{TENUE}" stroke-width="1.3" stroke-dasharray="3 6"/><g class="gira"><circle cx="13" cy="34" r="8" fill="{FG}"/><circle cx="67" cy="34" r="5" fill="{GRIS}"/></g>',
        # constelación en forma de gráfica
        f'<path d="M4 54 L26 38 L46 44 L72 12" fill="none" stroke="{TENUE}" stroke-width="1.3"/>'
        + "".join(estrella(x, y, r, f' fill="{FG}" class="tw" style="animation-delay:{i*.5}s"') for i, (x, y, r) in enumerate([(4, 54, 5), (26, 38, 6), (46, 44, 5), (72, 12, 9)]))]
    body = rotulo(c, 0, 26, T["hago_t"])
    for i, ((tag, tit, desc), ico) in enumerate(zip(T["hago"], iconos)):
        x = i * 410
        body += ((f'<line x1="{x-30}" x2="{x-30}" y1="70" y2="250" stroke="{LINEA}"/>' if i else "")
                 + f'<g transform="translate({x},66)">{ico}</g>'
                 f'<text x="{x}" y="166" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{GRIS}">0{i+1} — {tag}</text>'
                 f'<text x="{x}" y="200" font-family="{SANS}" font-size="25" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 + "".join(f'<text x="{x}" y="{228+j*22}" font-family="{SANS}" font-size="15.5" fill="{GRIS}">{e(l)}</text>' for j, l in enumerate(desc)))
    style = TW + ".gira{animation:gira 6s linear infinite;transform-origin:40px 34px}@keyframes gira{to{transform:rotate(360deg)}}"
    guardar(tema, idioma, "hago.svg", W, H, T["hago_t"].title() + ": " + " ".join(f"{t}: {' '.join(d)}" for _, t, d in T["hago"]), body, style)


def ruta(tema, idioma):
    c, T, W, H = TONOS[tema], TEXTOS[idioma], 1200, 230
    FG, GRIS, TENUE, LINEA = c["FG"], c["GRIS"], c["TENUE"], c["LINEA"]
    xs = [14, 414, 814]
    body = (rotulo(c, 0, 26, T["ruta_t"])
            + f'<path d="M14 96 H814" stroke="{TENUE}" stroke-width="1.4"/><path d="M814 96 H1190" stroke="{TENUE}" stroke-width="1.4" stroke-dasharray="3 8"/>'
            f'<circle r="3.5" fill="{FG}"><animateMotion dur="7s" repeatCount="indefinite" path="M14 96 H1190"/><animate attributeName="opacity" dur="7s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.08;.85;1"/></circle>')
    for i, (x, (fecha, tit, org)) in enumerate(zip(xs, T["hitos"])):
        hoy = i == 2
        body += ((f'<circle class="onda" cx="{x}" cy="96" r="12" fill="none" stroke="{FG}" stroke-width="1.5"/>' if hoy else "")
                 + estrella(x, 96, 15 if hoy else 10, f' fill="{FG}" class="tw" style="animation-delay:{i*.7}s"')
                 + f'<text x="{x-10}" y="146" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{GRIS}">{fecha}</text>'
                 f'<text x="{x-10}" y="180" font-family="{SANS}" font-size="22" font-weight="800" fill="{FG}">{e(tit)}</text>'
                 f'<text x="{x-10}" y="206" font-family="{SANS}" font-size="15" fill="{GRIS}">{e(org)}</text>')
    style = TW + ".onda{animation:onda 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center}@keyframes onda{to{transform:scale(2.6);opacity:0}}"
    guardar(tema, idioma, "ruta.svg", W, H, T["ruta_t"].title() + ": " + "; ".join(f"{t}, {o} ({f})" for f, t, o in T["hitos"]), body, style)


def actividad(tema, idioma, data):
    c, T, W, H = TONOS[tema], TEXTOS[idioma], 1200, 300
    FG, GRIS, TENUE = c["FG"], c["GRIS"], c["TENUE"]
    fin = dt.date.fromisoformat(data["hasta"])
    d, dias = fin - dt.timedelta(days=(fin.weekday() + 1) % 7 + 52 * 7), []
    while d <= fin:
        dias.append((d, data["dias"].get(d.isoformat(), 0))); d += dt.timedelta(days=1)
    total, activos = sum(n for _, n in dias), sum(1 for _, n in dias if n)
    pico = data["horas"].index(max(data["horas"]))
    hora = f"{(pico % 12) or 12} {T['am'] if pico < 12 else T['pm']}"
    body = rotulo(c, 0, 26, T["act_t"])
    for i, (v, lab) in enumerate(zip([str(total), str(activos), hora], T["cifras"])):
        x = i * 250
        body += (f'<text x="{x}" y="106" font-family="{SANS}" font-size="54" font-weight="800" letter-spacing="-1.5" fill="{FG}">{v}</text>'
                 f'<text x="{x+2}" y="132" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{GRIS}">{lab.upper()}</text>')
    paso, y0, campo, last = 22.3, 176, "", None
    for k, (dia, n) in enumerate(dias):
        wi, wd = k // 7, k % 7
        x, y = 8 + wi * paso, y0 + wd * 13.5
        if wd == 0 and dia.month != last and wi < 51:
            campo += f'<text x="{x-3:.0f}" y="{y0+7*13.5+20:.0f}" font-family="{MONO}" font-size="11" fill="{TENUE}">{T["meses"][dia.month-1]}</text>'; last = dia.month
        if n:
            campo += estrella(round(x, 1), round(y, 1), round(min(11, 4 + 1.25 * math.sqrt(n)), 1), f' fill="{FG}" class="tw" style="animation-delay:{(k % 13) * .23:.2f}s"') 
        else:
            campo += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.2" fill="{TENUE}" fill-opacity=".7"/>'
    nota = T["act_n"].format(n=data["proyectos"], f=f"{fin.day} {T['meses'][fin.month-1]} {fin.year}")
    body += campo + f'<text x="{W}" y="26" text-anchor="end" font-family="{SANS}" font-size="13" fill="{TENUE}">{e(nota)}</text>'
    guardar(tema, idioma, "actividad.svg", W, H, f"{T['act_t'].title()}: {total} commits, {activos} {T['cifras'][1]}, {T['cifras'][2]} {hora}.", body, TW)


def readme(idioma):
    T = TEXTOS[idioma]
    def pic(nombre, alt, attrs):
        return (f'<picture><source media="(prefers-color-scheme: light)" srcset="assets/claro/{idioma}/{nombre}.svg">'
                f'<img src="assets/oscuro/{idioma}/{nombre}.svg" {attrs} alt="{e(alt)}"></picture>')
    bot = [f'<a href="{url}">{pic("btn-" + clave, texto, 'height="44"')}</a>' for clave, texto, url in T["botones"]]
    alt = lambda n: html.unescape(__import__("re").search(r'aria-label="([^"]*)"', open(os.path.join(OUT, "oscuro", idioma, n + ".svg"), encoding="utf-8").read()).group(1))
    out = [f'<img src="assets/banner-{idioma}.gif" width="100%" alt="{e(T["banner"])}">', "", "<br>", "",
           f'<p align="center">{T["frase"]}<br>{T["sobre"]}</p>', "", '<p align="center">', "&nbsp;\n".join(bot), "</p>", "", "<br>", "",
           pic("hago", alt("hago"), 'width="100%"'), "", "<br>", "",
           f'<img src="assets/cinta.svg" width="100%" alt="Stack: {e(", ".join(STACK))}">', "", "<br>", "",
           pic("ruta", alt("ruta"), 'width="100%"'), "", "<br>", "",
           pic("actividad", alt("actividad"), 'width="100%"'), ""]
    open(os.path.join(ROOT, "README.md" if idioma == "es" else "README.en.md"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    data = json.load(open(os.path.join(ROOT, "data", "actividad.json"), encoding="utf-8"))
    for tema in TEMAS:
        for idioma, T in TEXTOS.items():
            for i, (clave, texto, _) in enumerate(T["botones"]):
                boton(tema, idioma, clave, texto, i == 0)
            hago(tema, idioma); ruta(tema, idioma); actividad(tema, idioma, data)
    cinta()
    for idioma in TEXTOS:
        readme(idioma)
    print("Listo")
