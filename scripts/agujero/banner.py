import numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
from render import cargar, estrellas, cuadro, tono
m, W, H = cargar("mapa.npz"); cielo = estrellas(m["dirf"], m["cap"], m["nh"])
NF, DUR = int(sys.argv[1]), int(sys.argv[2])
F = "/usr/share/fonts/opentype/inter/"
f_nom, f_sub = ImageFont.truetype(F + "Inter-ExtraBold.otf", 66), ImageFont.truetype(F + "Inter-Medium.otf", 17)
f_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
rampa = np.clip(.18 + .82 * (np.arange(W) - 40) / 330, .18, 1)[None, :] ** 1.3
def texto(sub):
    capa = Image.new("L", (W, H), 0); d = ImageDraw.Draw(capa)
    x = 44
    for ch in "SOLEDAD, COLOMBIA":
        d.text((x, 62), ch, font=f_mono, fill=150); x += 10.6
    d.rectangle((44, 46, 54, 56), fill=255) if False else None
    d.text((40, 88), "Briand", font=f_nom, fill=255); d.text((40, 156), "Castro", font=f_nom, fill=255)
    d.text((44, 246), sub, font=f_sub, fill=165)
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
