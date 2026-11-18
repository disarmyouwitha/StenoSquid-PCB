"""Generate one actual-size sheet with original/-0.75/-1/-1.5 mm outlines.

This produces paper fit studies only; it does not change any KiCad project.
SVG is the print master. PNG is an inline review preview (Pillow required).
"""
from pathlib import Path
import json
import math
import re
import subprocess
from kicad_sexpr import nodes,kind
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
info=json.loads((ROOT/'pcb/interface.json').read_text())
candidate=info.get('mechanical_revision') or info['mechanical_candidate']
original=subprocess.check_output(['git','show',candidate['base_commit']+':pcb/steno-squid.kicad_pcb'],cwd=ROOT,text=True)
current=(ROOT/'pcb/steno-squid.kicad_pcb').read_text()
PAGE_W,PAGE_H,SCALE=185,145,8
im=Image.new('RGB',(PAGE_W*SCALE,PAGE_H*SCALE),'white');draw=ImageDraw.Draw(im)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="185mm" height="145mm" viewBox="0 0 185 145" font-family="sans-serif">',
     '<title>Steno Squid: original, 0.75, 1 and 1.5 mm shorter; actual size</title>',
     '<rect width="185" height="145" fill="white"/>']
def label(x,y,text,size=3,center=False,color='#172b42'):
    svg.append('<text x="%g" y="%g" font-size="%g" fill="%s"%s>%s</text>'%(x,y,size,color,' text-anchor="middle"' if center else '',text))
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',round(size*SCALE))
    draw.text((x*SCALE,y*SCALE),text,font=font,fill=color,anchor='ms' if center else 'ls')

label(10,12,'Steno Squid — four length options',5)
label(10,21,'Print at actual size (100%). Trace the centre of the red line. Verify the scale bar.',3)
label(10,28,'All header centres align. Width stays 21.78 mm; reductions are TOTAL from the original.',2.8)

def circle(a,b,c):
    ax,ay=a;bx,by=b;cx,cy=c
    den=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    x=((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/den
    y=((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/den
    cross=(bx-ax)*(cy-by)-(by-ay)*(cx-bx)
    return (x,y),math.dist((x,y),a),cross>0

options=[(0,'Original',31),(.75,'−0.75 mm',72),(1,'−1.00 mm',113),(1.5,'−1.50 mm',154)]
for reduction,title,center in options:
    height=46.32-reduction
    label(center,40,title,3.7,True)
    label(center,46,'%g mm overall'%height,3,True)
    label(center,51,'Original R1 corners' if reduction==0 else 'R5.35 at far end',2.4,True)
    board=original if reduction==0 else current
    offset_x,offset_y=center-36.09,30
    def point(x,y):
        if reduction and y<40:y+=reduction-candidate['height_reduction_mm']
        return x+offset_x,y+offset_y
    for _,_,n in nodes(board):
        typ=kind(n)
        if typ not in ('gr_line','gr_arc') or '(layer "Edge.Cuts")' not in n:continue
        p={k:point(float(x),float(y)) for k,x,y in re.findall(r'\((start|mid|end) ([-\d.]+) ([-\d.]+)\)',n)}
        a,c=p['start'],p['end']
        if typ=='gr_line':
            tail='L %.6f %.6f'%c;pixels=[a,c]
        else:
            origin,radius,sweep=circle(a,p['mid'],c)
            tail='A %.6f %.6f 0 0 %d %.6f %.6f'%(radius,radius,int(sweep),*c)
            start=math.atan2(a[1]-origin[1],a[0]-origin[0]);end=math.atan2(c[1]-origin[1],c[0]-origin[0])
            delta=(end-start)%(2*math.pi) if sweep else -((start-end)%(2*math.pi))
            pixels=[(origin[0]+radius*math.cos(start+delta*i/100),origin[1]+radius*math.sin(start+delta*i/100)) for i in range(101)]
        svg.append('<path d="M %.6f %.6f %s" fill="none" stroke="#ff0000" stroke-width=".30"/>'%(*a,tail))
        draw.line([(x*SCALE,y*SCALE) for x,y in pixels],fill='#ff0000',width=3)
    for i in range(8):
        x,y=27.2+i*2.54+offset_x,100
        for radius in (.85,.5):
            svg.append('<circle cx="%.6f" cy="100" r="%g" fill="none" stroke="black" stroke-width=".14"/>'%(x,radius))
            draw.ellipse(((x-radius)*SCALE,(y-radius)*SCALE,(x+radius)*SCALE,(y+radius)*SCALE),outline='black',width=1)
        label(x,105,str(i+1),1.8,True,'#111')
    label(center,113,'%g mm total removed'%reduction,2.6,True)

label(10,127,'50 mm',2.8)
svg.append('<path d="M10 131 H60 M10 129 V133 M60 129 V133" stroke="black" stroke-width=".25" fill="none"/>')
draw.line((10*SCALE,131*SCALE,60*SCALE,131*SCALE),fill='black',width=2)
for x in (10,60):draw.line((x*SCALE,129*SCALE,x*SCALE,133*SCALE),fill='black',width=2)
svg.append('<rect x="96" y="124" width="10" height="10" fill="none" stroke="black" stroke-width=".25"/>')
draw.rectangle((96*SCALE,124*SCALE,106*SCALE,134*SCALE),outline='black',width=2)
label(110,130,'10 mm square',2.8)
label(10,142,'Original = main cb7d1fc. The -1.5 mm option is approved for all six PCB projects.',2.4)
svg.append('</svg>')
out=ROOT/'pcb/previews'
(out/'four-lengths-1to1.svg').write_text('\n'.join(svg)+'\n')
im.save(out/'four-lengths-preview.png',dpi=(203.2,203.2))
assert [round(46.32-r,2) for r,_,_ in options]==[46.32,45.57,45.32,44.82]
print('Wrote four-lengths-1to1.svg and four-lengths-preview.png')
