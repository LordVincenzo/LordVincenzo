"""Traza los rayos de luz alrededor de un agujero negro (Schwarzschild, rs = 1) y guarda dónde tocan el disco."""
import numpy as np, sys, time
W, H = int(sys.argv[1]), int(sys.argv[2])
CX, CY = float(sys.argv[3]), float(sys.argv[4])      # centro del agujero en la imagen (0..1)
D, ELEV, ESC = 24.0, np.radians(6.5), float(sys.argv[5])   # distancia, elevación sobre el disco, escala del campo de visión
R_IN, R_OUT, NH = 2.3, 9.5, 3
cam = D * np.array([0.0, np.sin(ELEV), -np.cos(ELEV)])
fwd = -cam / np.linalg.norm(cam); right = np.cross([0, 1, 0], fwd); right /= np.linalg.norm(right); up = np.cross(fwd, right)
jj, ii = np.meshgrid(np.arange(W), np.arange(H))
u = (jj + .5 - CX * W) / H * ESC; v = -(ii + .5 - CY * H) / H * ESC
d = fwd[None, None, :] + u[..., None] * right + v[..., None] * up
d /= np.linalg.norm(d, axis=-1, keepdims=True)
N = W * H
x = np.tile(cam, (N, 1)).astype(np.float64); vel = d.reshape(N, 3).astype(np.float64)
h2 = np.sum(np.cross(x, vel) ** 2, axis=1)
hit_r = np.zeros((NH, N), np.float32); hit_phi = np.zeros((NH, N), np.float32); hit_b = np.zeros((NH, N), np.float32)
nh = np.zeros(N, np.int8); vivo = np.ones(N, bool); cap = np.zeros(N, bool)
def acc(p):
    r2 = np.sum(p * p, axis=1)
    return -1.5 * h2_a[:, None] * p / (r2 ** 2.5)[:, None]
t0 = time.time()
for paso in range(1400):
    idx = np.nonzero(vivo)[0]
    if idx.size == 0: break
    p, w = x[idx], vel[idx]; h2_a = h2[idx]
    r = np.linalg.norm(p, axis=1)
    dt = np.clip(0.045 * r, 0.012, 0.5)[:, None]
    # RK4
    k1x, k1v = w, acc(p)
    k2x, k2v = w + .5 * dt * k1v, acc(p + .5 * dt * k1x)
    k3x, k3v = w + .5 * dt * k2v, acc(p + .5 * dt * k2x)
    k4x, k4v = w + dt * k3v, acc(p + dt * k3x)
    pn = p + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x); wn = w + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    cruza = (p[:, 1] * pn[:, 1] < 0)
    if cruza.any():
        c = np.nonzero(cruza)[0]; f = (p[c, 1] / (p[c, 1] - pn[c, 1]))[:, None]
        q = p[c] + f * (pn[c] - p[c]); rq = np.hypot(q[:, 0], q[:, 2])
        ok = (rq > R_IN) & (rq < R_OUT) & (nh[idx[c]] < NH)
        c, q, rq = c[ok], q[ok], rq[ok]; g = idx[c]; k = nh[g]
        phi = np.arctan2(q[:, 2], q[:, 0])
        tang = np.stack([-np.sin(phi), np.zeros_like(phi), np.cos(phi)], axis=1)      # sentido de giro del disco
        vorb = np.sqrt(.5 / rq)                                                       # velocidad orbital (en unidades de c)
        hit_r[k, g] = rq; hit_phi[k, g] = phi; hit_b[k, g] = vorb * np.sum(tang * (-w[c]), axis=1)
        nh[g] += 1
    x[idx], vel[idx] = pn, wn
    rn = np.linalg.norm(pn, axis=1)
    cae = rn < 1.01; fuera = (rn > 40) & (np.sum(pn * wn, axis=1) > 0)
    cap[idx[cae]] = True; vivo[idx[cae | fuera]] = False
print("pasos", paso, "seg", round(time.time() - t0, 1), "capturados", cap.mean().round(4), "con disco", (nh > 0).mean().round(3))
np.savez_compressed(sys.argv[6], hit_r=hit_r, hit_phi=hit_phi, hit_b=hit_b, nh=nh, cap=cap, dirf=vel.astype(np.float32), W=W, H=H)
