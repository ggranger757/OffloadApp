"""Regenerate the app icons in public/icons. Requires Pillow: pip install pillow"""
import pathlib
from PIL import Image, ImageDraw
OUT = pathlib.Path(__file__).resolve().parent.parent / 'public' / 'icons'
OUT.mkdir(parents=True, exist_ok=True)

def icon(size, pad_frac, name, radius=True):
    S = size*4
    im = Image.new('RGBA', (S,S), (0,0,0,0) if radius else (47,67,224,255))
    dr = ImageDraw.Draw(im)
    if radius: dr.rounded_rectangle([0,0,S-1,S-1], radius=int(S*0.22), fill=(47,67,224,255))
    p = S*pad_frac
    # speech bubble
    bx0,by0,bx1,by1 = p, p*1.05, S-p, S-p*1.35
    dr.rounded_rectangle([bx0,by0,bx1,by1], radius=int((by1-by0)*0.32), fill=(255,255,255,255))
    tw = (bx1-bx0)*0.16
    dr.polygon([(bx0+(bx1-bx0)*0.22,by1-2),(bx0+(bx1-bx0)*0.22+tw,by1-2),(bx0+(bx1-bx0)*0.16,by1+tw*0.9)], fill=(255,255,255,255))
    # three lines of text + yellow dot
    lh = (by1-by0)*0.11; lx = bx0+(bx1-bx0)*0.17
    for i,w in enumerate([0.62,0.46]):
        y = by0+(by1-by0)*(0.32+i*0.24)
        dr.rounded_rectangle([lx,y,lx+(bx1-bx0)*w,y+lh], radius=int(lh/2), fill=(19,22,28,255))
    r = (by1-by0)*0.11; cx = bx1-(bx1-bx0)*0.2; cy = by0+(by1-by0)*0.62
    dr.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(255,227,107,255), outline=(19,22,28,255), width=int(r*0.35))
    im.resize((size,size), Image.LANCZOS).save(OUT/name)
icon(192,0.2,'icon-192.png'); icon(512,0.2,'icon-512.png')
icon(512,0.27,'maskable-512.png',radius=False); icon(180,0.2,'apple-touch-icon.png',radius=False)

