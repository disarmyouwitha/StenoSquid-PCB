"""Draw the 16 MB review outline against its frozen main baseline.

SVG uses only the standard library. PNG is also written when Pillow is available.
"""
from pathlib import Path
import json
import math
import re
import subprocess
from kicad_sexpr import nodes, kind

ROOT=Path(__file__).resolve().parents[1]
info=json.loads((ROOT/'pcb/interface.json').read_text())
candidate=info['mechanical_candidate']
old=subprocess.check_output(['git','show',candidate['base_commit']+':pcb/steno-squid.kicad_pcb'],cwd=ROOT,text=True)
new=(ROOT/'pcb/steno-squid.kicad_pcb').read_text()

def shapes(board):
    result=[]
    for _,_,n in nodes(board):
        if kind(n) not in ('gr_line','gr_arc') or '(layer "Edge.Cuts")' not in n:continue
        p={label:(float(x),float(y)) for label,x,y in re.findall(r'\((start|mid|end) ([-\d.]+) ([-\d.]+)\)',n)}
        result.append((kind(n),p))
    return result

def circle(a,b,c):
    ax,ay=a;bx,by=b;cx,cy=c
    d=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    x=((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    y=((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    cross=(bx-ax)*(cy-by)-(by-ay)*(cx-bx)
    return (x,y),math.dist((x,y),a),cross>0

def svg_paths(board,offset=(14.8,14.4)):
    paths=[]
    def pos(p):return p[0]+offset[0],p[1]+offset[1]
    for typ,p in shapes(board):
        a=pos(p['start']);c=pos(p['end'])
        if typ=='gr_line':tail='L %g %g'%c
        else:
            _,r,sweep=circle(p['start'],p['mid'],p['end'])
            tail='A %g %g 0 0 %d %g %g'%(r,r,int(sweep),*c)
        paths.append('<path d="M %g %g %s"/>'%(*a,tail))
    return '\n'.join(paths)

svg='''<svg xmlns="http://www.w3.org/2000/svg" width="185mm" height="125mm" viewBox="0 0 185 125" font-family="sans-serif">
<rect width="185" height="125" fill="white"/>
<text x="10" y="13" font-size="5">16 MB plate-radius fit candidate</text>
<text x="10" y="21" font-size="3">Grey dashed: main cb7d1fc / Blue: proposed outline / Black: fixed header</text>
<g fill="none" stroke="#999" stroke-width=".25" stroke-dasharray="1 .7">OLD</g>
<g fill="none" stroke="#1768c4" stroke-width=".3">NEW</g>
<g fill="none" stroke="#111" stroke-width=".2">PADS</g>
<text x="85" y="44" font-size="3.5">1.5 mm shorter away from header</text>
<text x="85" y="52" font-size="3.5">21.78 × 44.82 mm</text>
<text x="85" y="63" font-size="3.5">Top corners R5.35 mm</text>
<text x="85" y="70" font-size="2.8">Radius from native BLE plate CAD</text>
<text x="85" y="81" font-size="3.5">Header-end corners remain R1 mm</text>
<text x="85" y="89" font-size="2.8">All eight contacts and electrical routing fixed</text>
<text x="10" y="109" font-size="3">Print at 100% for this overlay; use the separate fit template for the complete contact drawing.</text>
<path d="M10 117 H60 M10 115 V119 M60 115 V119" stroke="black" stroke-width=".2"/>
<text x="65" y="118" font-size="2.8">50 mm</text>
</svg>'''
pads=''.join('<circle cx="%g" cy="84.4" r=".85"/><circle cx="%g" cy="84.4" r=".5"/>'%(27.2+2.54*i+14.8,27.2+2.54*i+14.8) for i in range(8))
for key,value in [('OLD',svg_paths(old)),('NEW',svg_paths(new)),('PADS',pads)]:svg=svg.replace(key,value)
out=ROOT/'pcb/previews'
(out/'outline-comparison.svg').write_text(svg+'\n')

try:
    from PIL import Image,ImageDraw,ImageFont
except ImportError:
    raise SystemExit('SVG written; install Pillow to also render a PNG.')
im=Image.new('RGB',(1180,1100),'white');draw=ImageDraw.Draw(im)
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
font=lambda size:ImageFont.truetype(fontpath,size)
draw.text((45,25),'16 MB: plate-radius fit candidate',font=font(32),fill='#172b42')
draw.text((45,73),'Grey = current main    Blue = proposal    Black = fixed header',font=font(21),fill='#405468')
def xy(p):return 100+(p[0]-25.2)*18,140+(p[1]-25.6)*18
def polyline(typ,p):
    if typ=='gr_line':return [xy(p['start']),xy(p['end'])]
    center,r,sweep=circle(p['start'],p['mid'],p['end'])
    a=math.atan2(p['start'][1]-center[1],p['start'][0]-center[0]);b=math.atan2(p['end'][1]-center[1],p['end'][0]-center[0])
    angle=(b-a)%(2*math.pi) if sweep else -((a-b)%(2*math.pi))
    return [xy((center[0]+r*math.cos(a+angle*i/100),center[1]+r*math.sin(a+angle*i/100))) for i in range(101)]
for typ,p in shapes(old):draw.line(polyline(typ,p),fill='#aaaaaa',width=5)
for typ,p in shapes(new):draw.line(polyline(typ,p),fill='#1768c4',width=4)
for i in range(8):
    x,y=xy((27.2+2.54*i,70));rr=.85*18
    draw.ellipse((x-rr,y-rr,x+rr,y+rr),outline='#202020',width=2)
    rr=.5*18;draw.ellipse((x-rr,y-rr,x+rr,y+rr),outline='#202020',width=2)
    draw.text((x-5,y+45),str(i+1),font=font(17),fill='#202020')
labels=[('1.5 mm shorter',200),('Cut only at the end',241),('away from the header',272),('21.78 x 44.82 mm',350),('Top corners R5.35',450),('From native BLE plate CAD',491),('Header end remains R1',660),('Contacts, parts and',750),('signal routing unchanged',781),('16 MB only; other versions',880),('await your approval',911)]
for text,y in labels:draw.text((600,y),text,font=font(28 if y in (200,350,450,660) else 23),fill='#1768c4' if y in (200,350,450) else '#26384a')
im.save(out/'outline-comparison.png')
print('Wrote outline-comparison.svg and .png')
