# Banner del agujero negro

El banner es una simulación, no un video: se trazan los rayos de luz alrededor de un agujero negro
(métrica de Schwarzschild) y se anota dónde toca cada rayo el disco. Con ese mapa se pintan los fotogramas.

Necesita Python con `numpy` y `Pillow`, y las tipografías Inter y DejaVu Sans Mono.

```bash
cd scripts/agujero
python trazar.py 880 340 0.70 0.5 0.46 mapa.npz   # ancho, alto, centro x, centro y, zoom, salida
python banner.py 60 83                            # fotogramas, milisegundos por fotograma
```

Deja `banner-es.gif` y `banner-en.gif`; se copian a `assets/`.

## Banner v2 (agujero más grande + lluvia de código)

```
python trazar.py 1100 420 0.71 0.5 0.36 mapa2.npz
python banner2.py 60 83 ../../assets/portada
```
