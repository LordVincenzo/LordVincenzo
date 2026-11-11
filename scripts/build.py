#!/usr/bin/env python3
"""Genera los botones, la cinta del stack y los dos README. Solo librería estándar.

    python scripts/build.py

El banner animado se genera aparte: ver scripts/agujero/LEEME.md.
"""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', 'SFMono-Regular', Consolas, 'DejaVu Sans Mono', monospace"
CORREO = "Briandcastro11b@gmail.com"
CV = "https://github.com/LordVincenzo/LordVincenzo/raw/main/Briand_Castro_CV.pdf"
STACK = ["TypeScript", "React", "Next.js", "Node.js", ".NET", "PostgreSQL", "MongoDB", "Supabase", "n8n", "Power Automate", "Power BI", "Docker", "Unity"]
TEMAS = {"oscuro": ("#f2f2f2", "#0d0d0d"), "claro": ("#0d0d0d", "#ffffff")}        # (tinta, fondo del botón lleno)
TEXTOS = {
    "es": dict(frase="Automatizo lo repetitivo con <b>n8n</b> y construyo apps web y móviles de punta a punta.",
               botones=[("escribeme", "Escríbeme", f"mailto:{CORREO}"), ("cv", "Hoja de vida", CV), ("idioma", "English", "README.en.md")],
               banner="Briand Castro, analista y desarrollador de software. Soledad, Colombia. Animación de un agujero negro con su disco de luz girando.",
               stack="Stack"),
    "en": dict(frase="I automate the repetitive with <b>n8n</b> and build web and mobile apps end to end.",
               botones=[("escribeme", "Email me", f"mailto:{CORREO}"), ("cv", "Résumé", CV), ("idioma", "Español", "README.md")],
               banner="Briand Castro, software analyst and developer. Soledad, Colombia. Animation of a black hole with its spinning disk of light.",
               stack="Stack"),
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


def readme(idioma):
    T = TEXTOS[idioma]
    bot = []
    for clave, texto, url in T["botones"]:
        bot.append(f'<a href="{url}"><picture><source media="(prefers-color-scheme: light)" srcset="assets/claro/{idioma}/btn-{clave}.svg">'
                   f'<img src="assets/oscuro/{idioma}/btn-{clave}.svg" height="44" alt="{e(texto)}"></picture></a>')
    out = [f'<img src="assets/banner-{idioma}.gif" width="100%" alt="{e(T["banner"])}">', "", "<br>", "",
           f'<p align="center">{T["frase"]}</p>', "", '<p align="center">', "&nbsp;\n".join(bot), "</p>", "",
           f'<img src="assets/cinta.svg" width="100%" alt="Stack: {e(", ".join(STACK))}">', ""]
    open(os.path.join(ROOT, "README.md" if idioma == "es" else "README.en.md"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    for tema in TEMAS:
        for idioma, T in TEXTOS.items():
            for i, (clave, texto, _) in enumerate(T["botones"]):
                boton(tema, idioma, clave, texto, i == 0)
    cinta()
    for idioma in TEXTOS:
        readme(idioma)
    print("Listo")
