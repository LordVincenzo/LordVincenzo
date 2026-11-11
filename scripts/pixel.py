"""Escena en pixel art: desarrollador de espaldas frente a dos monitores. Genera fotogramas (niveles de gris 0-7)."""
import numpy as np, random
from PIL import Image
PW, PH, NF = 176, 120, 12
PAL = [(8, 8, 10), (19, 19, 22), (33, 33, 37), (54, 54, 59), (88, 88, 94), (134, 134, 140), (190, 190, 194), (244, 244, 244)]
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
GL = {"<": ["..#", ".#.", "#..", ".#.", "..#"], ">": ["#..", ".#.", "..#", ".#.", "#.."], "/": ["..#", "..#", ".#.", "#..", "#.."],
      "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"]}

def frame(f):
    a = np.zeros((PH, PW), np.int8)
    R = lambda x0, y0, x1, y1, v: a.__setitem__((slice(y0, y1 + 1), slice(x0, x1 + 1)), v)
    def P(x, y, v):
        if 0 <= x < PW and 0 <= y < PH: a[y, x] = v
    rnd = random.Random(1)
    # --- pared con resplandor de los monitores (tramado) ---
    yy, xx = np.mgrid[0:PH, 0:PW]
    dx = np.maximum(np.abs(xx - 86) - 46, 0); dy = np.maximum(np.abs(yy - 44) - 14, 0); dist = np.hypot(dx, dy * 1.25)
    luz = np.clip(1 - dist / (40 + (f % 6 < 3)), 0, 1) ** 1.5 * 2.4 + 1
    a[:] = np.floor(luz + BAYER[yy % 4, xx % 4]).astype(np.int8)
    a[100:, :] = 0; R(0, 100, PW - 1, 100, 2)                      # suelo
    for x in range(0, PW, 16): R(x, 101, x, 119, 1)
    # --- cuadro con lluvia de código (izquierda) ---
    R(12, 12, 34, 40, 5); R(13, 13, 33, 39, 0)
    for c in range(5):
        r2 = random.Random(c * 7 + 3); per = 30; cab = (r2.randrange(per) + f * (2 if c % 2 else 1) * per // NF * 1) % per
        for j in range(7):
            y = 14 + ((cab - j) % per)
            if y <= 38: P(15 + c * 4, y, 7 if j == 0 else max(2, 6 - j)); P(16 + c * 4, y, 7 if j == 0 else max(2, 6 - j)) if (y + c) % 3 else None
    # --- repisa con libros (derecha) ---
    R(136, 26, 168, 27, 4)
    x = 138
    for h, v, w in [(9, 5, 2), (11, 3, 3), (8, 6, 2), (10, 4, 2), (7, 5, 3), (11, 6, 2), (9, 3, 2)]:
        R(x, 26 - h, x + w - 1, 25, v); x += w + 1
    R(160, 19, 166, 25, 4); R(161, 16, 165, 18, 5); P(163, 14, 5); P(162, 15, 5); P(164, 15, 5)   # matera
    # --- escritorio ---
    R(10, 70, 166, 70, 6); R(10, 71, 166, 73, 4); R(10, 74, 166, 74, 2)
    R(14, 75, 16, 99, 3); R(160, 75, 162, 99, 3)
    R(130, 75, 156, 99, 2); R(130, 75, 156, 75, 3); R(130, 87, 156, 87, 1); R(140, 80, 146, 81, 5); R(140, 92, 146, 93, 5)   # cajonera
    # --- torre del PC ---
    R(22, 78, 38, 99, 2); R(22, 78, 38, 78, 4); R(22, 78, 22, 99, 3)
    R(25, 82, 35, 92, 1)
    for k in range(4):
        ang = f * np.pi / 6 + k * np.pi / 2; P(int(round(30 + 3.2 * np.cos(ang))), int(round(87 + 3.2 * np.sin(ang))), 5); P(int(round(30 + 1.6 * np.cos(ang))), int(round(87 + 1.6 * np.sin(ang))), 4)
    P(30, 87, 6); P(26, 96, 7 if f % 4 < 2 else 3); P(29, 96, 5)
    # --- monitores ---
    for mx in (40, 92):
        R(mx + 19, 59, mx + 24, 66, 3); R(mx + 13, 67, mx + 30, 69, 4); R(mx + 13, 67, mx + 30, 67, 5)
        R(mx, 27, mx + 43, 58, 5); R(mx + 1, 28, mx + 42, 57, 6); R(mx + 2, 29, mx + 41, 56, 0)
    # código que avanza
    lineas = [(0, 14, 7), (2, 22, 5), (2, 17, 5), (4, 25, 6), (4, 12, 4), (4, 19, 5), (2, 9, 7), (0, 6, 5), (0, 0, 0), (0, 18, 7), (2, 26, 5), (4, 15, 4), (4, 21, 6), (2, 11, 5), (0, 7, 7), (0, 0, 0)]
    paso = f // 2
    for i in range(8):
        ind, ln, v = lineas[(paso + i) % len(lineas)]
        if i == 7: ln = ln * ((f % 2) + 1) // 2
        if ln: R(45 + ind, 31 + i * 3, 45 + ind + ln, 31 + i * 3, v)
        P(43, 31 + i * 3, 2)
    if f % 4 < 2:
        ind, ln, v = lineas[(paso + 7) % len(lineas)]; l2 = ln * ((f % 2) + 1) // 2; R(47 + ind + l2, 52, 48 + ind + l2, 52, 7)
    # flujo de automatización
    nod = [(105, 33), (115, 42), (125, 33)]
    for (xa, ya), (xb, yb) in zip(nod, nod[1:]):
        for t in range(1, 8):
            x = xa + 5 + (xb - xa - 5) * t // 8; y = ya + 2 + (yb - ya) * t // 8
            P(x, y, 4)
    act = (f // 4) % 3
    for i, (x, y) in enumerate(nod):
        R(x, y, x + 4, y + 4, 7 if i == act else 4); P(x + 2, y + 2, 0 if i == act else 2)
    seg = f % 4; xa, ya = nod[min(act, 1)]; xb, yb = nod[min(act, 1) + 1]
    if act < 2: t = 1 + seg * 2; P(xa + 5 + (xb - xa - 5) * t // 8, ya + 2 + (yb - ya) * t // 8, 7)
    R(103, 49, 103 + 6 + (f * 2) % 18, 50, 5); R(103, 53, 118, 53, 3); R(121, 53, 130, 53, 3)
    for k, (x, y) in enumerate([(127, 47), (128, 48), (129, 47), (130, 46), (131, 45)]): P(x, y, 7 if act == 2 else 3)
    # --- taza con vapor y planta sobre el escritorio ---
    R(146, 63, 152, 69, 6); R(146, 63, 152, 63, 7); R(153, 65, 154, 65, 6); R(155, 66, 155, 67, 6); R(153, 68, 154, 68, 6)
    for k in range(3):
        y = 60 - ((f + k * 4) % 12) // 2 * 2; x = 148 + k * 2 + (1 if ((f + k * 4) // 3) % 2 else 0)
        if y > 48: P(x, y, 5 if y > 54 else 3)
    R(18, 64, 26, 69, 4); R(17, 63, 27, 63, 5)
    for x, y in [(22, 62), (22, 61), (22, 60), (21, 59), (20, 58), (19, 57), (18, 56), (23, 59), (24, 58), (25, 57), (26, 56), (26, 55), (22, 58), (22, 57), (22, 56), (22, 55), (22, 54), (19, 56), (18, 55), (25, 56)]: P(x, y, 5)
    for x, y in [(17, 54), (27, 54), (22, 53), (20, 57), (24, 57)]: P(x, y, 6)
    # teclado y ratón
    R(66, 67, 106, 69, 3); R(66, 67, 106, 67, 5); R(112, 67, 116, 69, 5)
    # --- persona ---
    bob = 1 if f % 6 in (2, 3) else 0
    for s_, lado in ((-1, 0), (1, 1)):                            # antebrazos hacia el teclado
        up = 1 if (f + lado * 2) % 4 < 2 else 0
        for k in range(12):
            x = 86 + s_ * (27 - k); y = 76 - k * 2 // 3 - (up if k > 7 else 0)
            R(min(x, x + s_ * 1), y - 2, max(x, x + s_ * 1), y + 2, 4); P(x, y - 3, 6)
        hx = 86 + s_ * 15; R(min(hx, hx + s_ * 3), 66 - up, max(hx, hx + s_ * 3), 68 - up, 6)
    for y in range(57, 86):                                       # torso / sudadera
        t = (y - 57) / 10; w = int(round(14 + 13 * min(1, t) ** .6))
        R(86 - w, y, 86 + w, y, 3); R(86 - w + 2, y, 86 - w + 5, y, 4); R(86 + w - 5, y, 86 + w - 2, y, 4)
        P(86 - w, y, 6); P(86 + w, y, 6); P(86 - w + 1, y, 5); P(86 + w - 1, y, 5)
    R(73, 56, 99, 56, 6); R(75, 55, 97, 55, 5)
    hy = 42 - bob
    for y in range(-11, 12):                                      # cabeza
        w = int(round(10.5 * np.sqrt(max(0, 1 - (y / 11.5) ** 2))))
        if w: R(86 - w, hy + y, 86 + w, hy + y, 1); P(86 - w, hy + y, 5); P(86 + w, hy + y, 5); P(86 - w + 1, hy + y, 3); P(86 + w - 1, hy + y, 3)
    for x, y in [(81, hy - 6), (82, hy - 5), (85, hy - 8), (86, hy - 7), (90, hy - 6), (91, hy - 5), (84, hy - 2), (88, hy - 3), (89, hy - 2), (83, hy + 3), (87, hy + 2), (90, hy + 4)]: P(x, y, 2)
    for y in range(0, 7):                                         # capucha caída sobre la espalda
        w = 13 - abs(y - 2); R(86 - w, hy + 11 + y, 86 + w, hy + 11 + y, 4); P(86 - w, hy + 11 + y, 6); P(86 + w, hy + 11 + y, 6)
    R(78, hy + 11, 94, hy + 11, 6); R(80, hy + 14, 92, hy + 14, 3); R(82, hy + 16, 90, hy + 16, 3)
    for x in range(-12, 13):                                      # diadema
        y = hy - int(round(12.5 * np.sqrt(max(0, 1 - (x / 12.5) ** 2))))
        P(86 + x, y, 7); P(86 + x, y - 1, 7); P(86 + x, y + 1, 5) if abs(x) < 11 else None
    R(72, hy - 4, 76, hy + 6, 7); R(96, hy - 4, 100, hy + 6, 7); R(71, hy - 2, 71, hy + 4, 5); R(101, hy - 2, 101, hy + 4, 5); R(74, hy - 1, 74, hy + 3, 4); R(98, hy - 1, 98, hy + 3, 4)
    # --- silla ---
    for y in range(72, 101):
        w = 17 if 75 < y < 98 else 15 if y in (74, 75, 98, 99) else 13
        R(86 - w, y, 86 + w, y, 1); P(86 - w, y, 4); P(86 + w, y, 4); P(86 - w + 1, y, 2); P(86 + w - 1, y, 2)
    R(74, 72, 98, 72, 5); R(73, 100, 99, 100, 3)
    for y in range(76, 97): R(76, y, 77, y, 5); R(95, y, 96, y, 5); P(78, y, 3); P(94, y, 3)
    for y in range(78, 96, 3): R(81, y, 91, y, 2)
    R(63, 84, 68, 86, 3); R(104, 84, 109, 86, 3); R(63, 84, 68, 84, 5); R(104, 84, 109, 84, 5); R(66, 87, 67, 93, 2); R(105, 87, 106, 93, 2)   # reposabrazos
    R(84, 101, 88, 108, 3); P(84, 101, 5); R(68, 109, 104, 110, 3); R(68, 109, 104, 109, 5)
    for x in (69, 86, 103): R(x - 1, 111, x + 1, 113, 5); P(x, 114, 2)
    return a

def frames(): return [frame(f) for f in range(NF)]
def gif(fn, esc=4, dur=110):
    ims = []
    for a in frames():
        rgb = np.array(PAL, np.uint8)[a]; ims.append(Image.fromarray(rgb).resize((PW * esc, PH * esc), Image.NEAREST))
    ims[0].save(fn, save_all=True, append_images=ims[1:], duration=dur, loop=0); ims[3].save(fn.replace(".gif", ".png"))

def _rects(a, sel):
    """Rectángulos por tramos horizontales (fusionando filas iguales) de los píxeles marcados en sel."""
    out = []; abiertos = {}
    for y in range(PH):
        x = 0; nuevos = {}
        while x < PW:
            if not sel[y, x]: x += 1; continue
            v = a[y, x]; x0 = x
            while x < PW and sel[y, x] and a[y, x] == v: x += 1
            k = (x0, x, int(v))
            if k in abiertos: nuevos[k] = abiertos.pop(k)
            else: nuevos[k] = y
        for (x0, x1, v), y0 in abiertos.items(): out.append((x0, y0, x1 - x0, y - y0, v))
        abiertos = nuevos
    for (x0, x1, v), y0 in abiertos.items(): out.append((x0, y0, x1 - x0, PH - y0, v))
    return out

def svg(esc=3, dur=.11):
    fr = frames(); F = np.stack(fr); fijo = (F == F[0]).all(axis=0)
    hexs = ["#%02x%02x%02x" % c for c in PAL]
    def pinta(rs):
        por = {}
        for x, y, w, h, v in rs: por.setdefault(v, []).append(f"M{x} {y}h{w}v{h}h{-w}z")
        return "".join(f'<path fill="{hexs[v]}" d="{"".join(d)}"/>' for v, d in sorted(por.items()))
    tot = NF * dur
    s = [f'<g transform="scale({esc})" shape-rendering="crispEdges"><style>.px{{opacity:0;animation:px {tot:.2f}s steps(1) infinite}}.px0{{opacity:1}}@keyframes px{{0%{{opacity:1}}{100/NF:.4f}%{{opacity:0}}100%{{opacity:0}}}}</style>']
    s.append(pinta(_rects(fr[0], np.ones_like(fijo))))            # fotograma 0 completo como base (se ve aunque no haya animación)
    for k in range(1, NF):
        s.append(f'<g class="px" style="animation-delay:{k*dur:.2f}s">' + pinta(_rects(fr[k], ~fijo)) + '</g>')
    s.append('</g>'); return "".join(s)

if __name__ == "__main__":
    gif("personaje.gif"); print(len(svg()))
