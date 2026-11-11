"""Banner v2: agujero negro más grande + lluvia de caracteres (estilo Matrix) que el agujero se traga."""
import numpy as np, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from render import cargar, estrellas, cuadro, tono
m, W, H = cargar("mapa3.npz"); cielo = estrellas(m["dirf"], m["cap"], m["nh"])
NF, DUR, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
F = "/usr/share/fonts/opentype/inter/"
f_nom = ImageFont.truetype(F + "Inter-Black.otf", 84)
f_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)
f_ll = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)
def espaciado(d, x, y, txt, paso, fill):
    for ch in txt: d.text((x, y), ch, font=f_mono, fill=fill); x += paso
def texto(sub):
    capa = Image.new("L", (W, H), 0); d = ImageDraw.Draw(capa)
    d.rectangle((54, 40, 66, 52), fill=255); espaciado(d, 82, 38, "LORDVINCENZO / README", 12.6, 170)
    d.text((48, 62), "BRIAND", font=f_nom, fill=255)
    con = Image.new("L", (W, H), 0); dc = ImageDraw.Draw(con)
    dc.text((48, 144), "CASTRO", font=f_nom, fill=255, stroke_width=2, stroke_fill=255); dc.text((48, 144), "CASTRO", font=f_nom, fill=0)
    capa = Image.fromarray(np.maximum(np.asarray(capa), np.asarray(con))); d = ImageDraw.Draw(capa)
    espaciado(d, 54, 252, sub.upper(), 12.6, 190)
    return capa
# lluvia: cada columna da un número entero de vueltas por bucle
rng = np.random.default_rng(5); PX, LH, NT = 20, 18, 15
cols = [(x, rng.integers(1, 3), rng.uniform(0, 1), [rng.choice(list("01<>{}/=;$#*+01")) for _ in range(H // LH + NT + 2)]) for x in range(8, W, PX) if rng.random() > .12]
cap = np.asarray(Image.fromarray((m["cap"].reshape(H, W) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)), np.float32) / 255
def lluvia(t):
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); rec = H + NT * LH
    for x, v, f0, chs in cols:
        cab = ((f0 + v * t) % 1) * rec
        for j in range(NT):
            y = cab - j * LH; fila = int(y // LH)
            if -LH < y < H: d.text((x, fila * LH), chs[fila % len(chs)], font=f_ll, fill=int(235 if j == 0 else 120 * (1 - j / NT) ** 1.3))
    return np.asarray(im, np.float32)
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), radius=24, fill=255); fuera = np.asarray(mask) == 0
RAMPA = (np.clip(.16 + .84 * (np.arange(W) - 380) / 240, .16, 1)[None, :]) ** 1.2
base = []
for i in range(NF):
    b = tono(cuadro(m, W, H, i / NF, cielo) * .72, W, H).astype(np.float32) * RAMPA
    ll = lluvia(i / NF) * (1 - np.clip(cap * 1.6, 0, 1)) * np.clip(1 - b / 110, 0, 1)      # el agujero y el disco tapan la lluvia
    base.append(np.maximum(b, ll * .62))
for idi, sub in (("es", "Analista y desarrollador de software"), ("en", "Software analyst & developer")):
    tx = texto(sub); halo = np.asarray(tx.filter(ImageFilter.GaussianBlur(9)), np.float32) / 255; txa = np.asarray(tx, np.float32); frames = []
    for b in base:
        a = np.maximum(b * (1 - np.clip(halo * 1.5, 0, .88)), txa)                          # se apaga la lluvia justo detrás de las letras
        a = (np.clip(a, 0, 252) // 6 * 6).astype(np.uint8); a[fuera] = 255
        frames.append(Image.fromarray(a, "L"))
    frames[0].save(f"{OUT}-{idi}.gif", save_all=True, append_images=frames[1:], duration=DUR, loop=0, transparency=255, disposal=2, optimize=False)
    frames[NF // 3].save(f"{OUT}-{idi}.png")
