"""Pinta los fotogramas del agujero negro a partir del mapa de rayos."""
import numpy as np, sys
from PIL import Image, ImageFilter, ImageDraw, ImageFont
R_IN, R_OUT = 2.3, 9.5
rng = np.random.default_rng(7)
NB = 34
AMP = rng.uniform(.4, 1, (NB, 7)); FRQ = rng.integers(2, 26, (NB, 7)); FAS = rng.uniform(0, 2 * np.pi, (NB, 7))
VUELTAS = np.round(np.interp(np.arange(NB), [0, NB - 1], [5, 1])).astype(int)        # vueltas por bucle: más rápido adentro

def cargar(path):
    m = np.load(path); W, H = int(m["W"]), int(m["H"])
    return m, W, H

def estrellas(dirf, cap, nh, seed=3):
    """Cielo de fondo: el rayo ya curvado decide qué estrella se ve (por eso se deforman cerca del agujero)."""
    r = np.random.default_rng(seed); SW, SH = 7200, 3600
    cielo = np.zeros((SH, SW), np.float32)
    n = 9000; ys = (np.arccos(r.uniform(-1, 1, n)) / np.pi * SH).astype(int) % SH; xs = r.integers(0, SW, n)
    cielo[ys, xs] = r.uniform(.25, 1, n) ** 2.2
    th = np.arccos(np.clip(dirf[:, 1], -1, 1)); ph = np.arctan2(dirf[:, 2], dirf[:, 0])
    s = cielo[(th / np.pi * SH).astype(int) % SH, ((ph + np.pi) / (2 * np.pi) * SW).astype(int) % SW]
    s[cap] = 0
    return s

def textura(r, phi, t):
    """Vetas del disco: bandas que giran un número entero de vueltas por bucle (así el bucle no salta)."""
    fb = (r - R_IN) / (R_OUT - R_IN) * (NB - 1)
    b0 = np.clip(np.floor(fb).astype(int), 0, NB - 2); w1 = (fb - b0).astype(np.float32)
    def banda(b):
        a = phi[:, None] * FRQ[b] - 2 * np.pi * t * (VUELTAS[b][:, None] * FRQ[b]) + FAS[b]
        return (AMP[b] * np.cos(a)).sum(axis=1) / AMP[b].sum(axis=1)
    v = banda(b0) * (1 - w1) + banda(b0 + 1) * w1
    return np.clip(.5 + .9 * v, 0, 1) ** 1.6

def cuadro(m, W, H, t, cielo):
    N = W * H; img = cielo * .55; trans = np.ones(N, np.float32)
    for k in range(m["hit_r"].shape[0]):
        sel = np.nonzero(m["nh"] > k)[0]
        if sel.size == 0: continue
        r, phi, be = m["hit_r"][k, sel], m["hit_phi"][k, sel], m["hit_b"][k, sel]
        x = (r - R_IN) / (R_OUT - R_IN)
        perfil = np.clip(x / .05, 0, 1) * np.clip((1 - x) / .35, 0, 1) ** 1.5 * (R_IN / r) ** 1.9
        doppler = ((1 + be) / (1 - be)) ** 1.7                                        # el lado que se acerca brilla más
        anillos = .82 + .18 * np.sin(r * 7.3 + 1.3 * np.sin(r * 2.1))
        I = 3.4 * perfil * doppler * anillos * (.3 + .7 * textura(r, phi, t))
        a = np.clip(perfil * 3.0, 0, .92)
        img[sel] = img[sel] * (1 - a) + trans[sel] * 0 + I * a if k == 0 else img[sel] + trans[sel] * I * a
        trans[sel] *= (1 - a)
    return img.reshape(H, W)

def tono(img, W, H):
    im = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8))
    b1 = np.asarray(im.filter(ImageFilter.GaussianBlur(max(2, W // 180))), np.float32) / 255
    b2 = np.asarray(im.filter(ImageFilter.GaussianBlur(max(5, W // 50))), np.float32) / 255
    out = img + .55 * b1 + .5 * b2
    out = 1 - np.exp(-1.25 * out)                                                     # curva suave para no quemar los blancos
    return np.clip(out * 255, 0, 255).astype(np.uint8)

if __name__ == "__main__":
    m, W, H = cargar(sys.argv[1]); cielo = estrellas(m["dirf"], m["cap"], m["nh"])
    Image.fromarray(tono(cuadro(m, W, H, float(sys.argv[2]), cielo), W, H)).resize((W * int(sys.argv[3]), H * int(sys.argv[3])), Image.LANCZOS).save(sys.argv[4])
