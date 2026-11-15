"""Troca texto embutido em imagens: apaga o texto original (inpaint) e escreve o novo."""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = '/home/claude/fonts/'
FONTS = {
    'mi': F + 'montserrat-latin-800-italic.ttf',
    'm8': F + 'montserrat-latin-800-normal.ttf',
    'm7': F + 'montserrat-latin-700-normal.ttf',
    'ei': F + 'exo-2-latin-800-italic.ttf',
    'e7': F + 'exo-2-latin-700-normal.ttf',
    'e6': F + 'exo-2-latin-600-normal.ttf',
    'e5i': F + 'exo-2-latin-500-italic.ttf',
    'e6i': F + 'exo-2-latin-600-italic.ttf',
}


def text_mask(arr, box, thr=None, dark=False):
    x0, y0, x1, y1 = box
    roi = arr[y0:y1, x0:x1].astype(np.float32)
    lum = roi.mean(axis=2)
    if thr is None and not dark:
        thr = np.percentile(lum, 50) + (lum.max() - np.percentile(lum, 50)) * 0.42
    if dark:
        if thr is None: thr = np.percentile(lum, 70) * 0.5
        m = (lum < thr).astype(np.uint8) * 255
    else:
        m = (lum > thr).astype(np.uint8) * 255
    return m, roi


def retext(img, box, text, font='e7', align='left', color=None, thr=None, pad=2,
           fit_w=None, glow=None, size=None, dy=0, stroke=0, stroke_col=None, grow=1.0, dark=False, grad=None):
    arr = np.array(img.convert('RGB'))
    x0, y0, x1, y1 = box
    m, roi = text_mask(arr, box, thr, dark)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        raise ValueError(f'no text in {box}')
    tx0, tx1 = xs.min() + x0, xs.max() + x0
    rc = (m > 0).sum(axis=1); core = np.nonzero(rc > rc.max() * 0.28)[0]
    ty0, ty1 = core.min() + y0, core.max() + y0  # ignora acentos e cedilha
    if color is None:
        px = roi[m > 0]
        bright = px[px.mean(axis=1) <= np.percentile(px.mean(axis=1), 40)] if dark else px[px.mean(axis=1) >= np.percentile(px.mean(axis=1), 60)]
        color = tuple(int(c) for c in np.median(bright, axis=0))
    full = np.zeros(arr.shape[:2], np.uint8)
    full[y0:y1, x0:x1] = m
    full = cv2.dilate(full, np.ones((3, 3), np.uint8), iterations=pad + 1)
    clean = cv2.inpaint(arr[:, :, ::-1], full, 6, cv2.INPAINT_TELEA)[:, :, ::-1]
    out = Image.fromarray(clean)
    # tamanho: altura das maiúsculas = altura detectada
    capH = (ty1 - ty0 + 1) * grow
    fs = size or 10
    if not size:
        while True:
            f = ImageFont.truetype(FONTS[font], fs)
            bb = f.getbbox('HÉ' if text.isupper() else 'Hd')
            hb = f.getbbox('H')
            if hb[3] - hb[1] >= capH * (0.98 if text.isupper() or True else 1):
                break
            fs += 1
    f = ImageFont.truetype(FONTS[font], fs)
    maxw = fit_w or (x1 - x0)
    while f.getlength(text) > maxw and fs > 6:
        fs -= 1
        f = ImageFont.truetype(FONTS[font], fs)
    global LAST_FS
    LAST_FS = fs
    hb = f.getbbox('H')
    tw = f.getlength(text)
    if align == 'left':
        X = tx0
    elif align == 'center':
        X = (tx0 + tx1) / 2 - tw / 2
    else:
        X = tx1 - tw
    Y = ty1 - hb[3] + 1 + dy  # baseline alinhada
    layer = Image.new('RGBA', out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if glow:
        g = Image.new('RGBA', out.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).text((X, Y), text, font=f, fill=glow + (200,))
        g = g.filter(ImageFilter.GaussianBlur(4))
        out = Image.alpha_composite(out.convert('RGBA'), g)
    if grad:
        mk = Image.new('L', out.size, 0)
        ImageDraw.Draw(mk).text((X, Y), text, font=f, fill=255)
        top, bot = grad; gy0 = int(Y + hb[1]); gy1 = int(Y + hb[3])
        g = Image.new('RGBA', out.size)
        gd = ImageDraw.Draw(g)
        for yy in range(out.size[1]):
            t = min(1, max(0, (yy - gy0) / max(1, gy1 - gy0)))
            gd.line([(0, yy), (out.size[0], yy)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
        layer.paste(g, (0, 0), mk)
    else:
        d.text((X, Y), text, font=f, fill=tuple(color) + (255,), stroke_width=stroke,
           stroke_fill=stroke_col)
    out = Image.alpha_composite(out.convert('RGBA'), layer)
    if img.mode == 'RGBA':
        out = out.convert('RGBA'); out.putalpha(img.getchannel('A')); return out
    return out.convert('RGB')
