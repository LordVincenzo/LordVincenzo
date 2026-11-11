import numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
from render import cargar, estrellas, cuadro, tono
m, W, H = cargar("mapa.npz"); cielo = estrellas(m["dirf"], m["cap"], m["nh"])
NF, DUR = int(sys.argv[1]), int(sys.argv[2])
F = "/usr/share/fonts/opentype/inter/"
f_nom = ImageFont.truetype(F + "Inter-Black.otf", 88)
f_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 12)
rampa = np.clip(.18 + .82 * (np.arange(W) - 40) / 330, .18, 1)[None, :] ** 1.3
def espaciado(d, x, y, txt, paso, fill):
    for ch in txt:
        d.text((x, y), ch, font=f_mono, fill=fill); x += paso
def texto(sub):
    capa = Image.new("L", (W, H), 0); d = ImageDraw.Draw(capa)
    d.rectangle((42, 50, 52, 60), fill=255)
    espaciado(d, 66, 48, "LORDVINCENZO / README", 10.4, 150)
    d.text((36, 84), "BRIAND", font=f_nom, fill=255)
    # CASTRO en contorno: se dibuja relleno y se le resta el interior
    con = Image.new("L", (W, H), 0); dc = ImageDraw.Draw(con)
    dc.text((36, 170), "CASTRO", font=f_nom, fill=255, stroke_width=2, stroke_fill=255); dc.text((36, 170), "CASTRO", font=f_nom, fill=0)
    capa = Image.fromarray(np.maximum(np.asarray(capa), np.asarray(con)))
    d = ImageDraw.Draw(capa)
    espaciado(d, 42, 286, sub.upper(), 10.4, 170)
    return np.asarray(capa, np.float32)
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), radius=20, fill=255); fuera = np.asarray(mask) == 0
base = [tono(cuadro(m, W, H, i / NF, cielo), W, H).astype(np.float32) * rampa for i in range(NF)]
for idi, sub in (("es", "Analista y desarrollador de software"), ("en", "Software analyst & developer")):
    tx = texto(sub); frames = []
    for b in base:
        a = np.maximum(b, tx)
        a = (np.clip(a, 0, 252) // 4 * 4).astype(np.uint8); a[fuera] = 255
        frames.append(Image.fromarray(a, "L"))
    frames[0].save(f"banner-{idi}.gif", save_all=True, append_images=frames[1:], duration=DUR, loop=0, transparency=255, disposal=2, optimize=False)
    frames[NF // 3].save(f"banner-{idi}.png")
