"""Derive the 32/64 MB drafts from pcb/ without touching the 16 MB Rev D baseline.

Run with normal Python, then tools/check_capacity_variants.py with KiCad installed.
Package E dimensions: Winbond W25Q256JV Rev G p85 and W25Q512JV Rev G p88.
This deliberately builds a shared 8x6 mm WSON layout, not the SOIC breadboard part.
"""
from pathlib import Path
import csv
import json
import math
import re
import shutil
import uuid
from kicad_sexpr import nodes, kind

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'pcb'
OLD = 'WSON-8_6x5mm_P1.27mm_EP3.4x4.3mm'
NEW = 'WSON-8_8x6mm_P1.27mm_EP3.4x4.3mm'
MODEL = 'WSON-8_8x6mm_EP3.4x4.3mm.step'
DATASHEETS = {
    32: 'https://www.mouser.com/datasheet/2/949/w25q256jv_spi_revg_08032017-1489574.pdf',
    64: 'https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf',
}

def replace_children(text, fn):
    for a, b, child in reversed(list(nodes(text))):
        replacement = fn(child)
        if replacement is not None:
            text = text[:a] + replacement + text[b:]
    return text

def grow_package(fp):
    fp = fp.replace(OLD, NEW).replace('WSON-8_6x5mm_EP3.4x4.3mm.step', MODEL)
    fp = fp.replace('Winbond W25Q128JV package P. Body 6x5mm',
                    'Winbond W25Q256JV / W25Q512JV package E. Body 8x6mm')
    def grow_child(child):
        # Only footprint-local graphics, properties and pads; do not move its board origin.
        if kind(child) not in ('property', 'fp_line', 'fp_circle', 'pad'):
            return child
        def point(m):
            x, y = float(m[2]), float(m[3])
            if abs(x) >= 2.5:
                x += math.copysign(1.0, x)
            if abs(y) >= 2.5:
                y += math.copysign(.5, y)
            return '(%s %g %g' % (m[1], x, y)
        return re.sub(r'\((at|start|end|center) ([-\d.]+) ([-\d.]+)', point, child)
    return replace_children(fp, grow_child)

def grow_step(text):
    # Move package body and terminals, retaining the existing 3.4x4.3 mm exposed pad.
    # Orthogonal BREP and circular pin-1 marker remain analytic, with no scale transform.
    def point(m):
        x, y, z = map(float, m.groups())
        if abs(x) >= 2.0:
            x += math.copysign(1, x)
        if abs(y) >= 2.5:
            y += math.copysign(.5, y)
        return "CARTESIAN_POINT('',(%s,%s,%s))" % tuple(format(v, '.10g') for v in (x,y,z))
    return re.sub(r"CARTESIAN_POINT\('',\(([-\d.Ee+]+),([-\d.Ee+]+),([-\d.Ee+]+)\)\)", point,
                  text.replace('6x5mm', '8x6mm'))

def build(size):
    out = ROOT / 'variants' / ('%dmb' % size)
    for sub in ('checks', 'previews', 'models', 'footprints/StenoSquid.pretty'):
        (out / sub).mkdir(parents=True, exist_ok=True)
    for filename in ('steno-squid.kicad_pro', 'steno-squid.kicad_dru', 'sym-lib-table', 'fp-lib-table'):
        shutil.copy2(BASE / filename, out / filename)
    for name in ('C_0603_1608Metric', 'R_0603_1608Metric', 'PinHeader_1x08_P2.54mm_Vertical'):
        shutil.copy2(BASE / 'footprints/StenoSquid.pretty' / (name+'.kicad_mod'),
                     out / 'footprints/StenoSquid.pretty' / (name+'.kicad_mod'))
    (out/'footprints/StenoSquid.pretty'/ (NEW+'.kicad_mod')).write_text(
        grow_package((BASE/'footprints/StenoSquid.pretty'/(OLD+'.kicad_mod')).read_text()))
    (out/'models'/MODEL).write_text(grow_step((BASE/'models/WSON-8_6x5mm_EP3.4x4.3mm.step').read_text()))
    part = 'W25Q%dJVEIQ' % (size*8)
    symbol = 'W25Q%dJV' % (size*8)
    revision = 'D-%dMB draft' % size
    for filename in ('steno-squid.kicad_sch', 'steno-squid.kicad_sym'):
        content = (BASE/filename).read_text().replace('W25Q128JVPIQ', part).replace('W25Q128JV', symbol)
        content = content.replace(OLD, NEW).replace('D provisional', revision)
        content = content.replace('Steno Squid - 8-contact QSPI electrical proposal',
                                  'Steno Squid - %d MB QSPI draft' % size)
        (out/filename).write_text(content)
    interface = json.loads((BASE/'interface.json').read_text())
    interface.update(revision=revision, flash_ordering_code=part+' / WSON-8 8x6 mm',
                     flash_body_mm=[8,6], capacity_bytes=size*1024*1024,
                     jedec_id='EF4019' if size==32 else 'EF4020',
                     baseline='rev-d electrical and mechanical design; current Pop artwork',
                     status='capacity draft; host mechanical, RF and switched rail qualification pending',
                     datasheet=DATASHEETS[size])
    (out/'interface.json').write_text(json.dumps(interface,indent=2)+'\n')
    with (BASE/'BOM.csv').open() as f:
        reader=csv.DictReader(f); fields=reader.fieldnames; bom=list(reader)
    u=next(r for r in bom if r['Reference']=='U1')
    lcsc={32:'C2682312',64:'C3034691'}[size]
    url='https://jlcpcb.com/partdetail/WinbondElec-%s/%s' % (part,lcsc)
    u.update(Value='%dMbit (%d MB) QSPI NOR' % (size*8,size), Prototype_MPN=part,
             Footprint='WSON-8 8x6mm P1.27mm EP3.4x4.3mm', Source=url,
             Notes='Package E; 0.8mm max; Extended catalog candidate; stock and stencil review pending',
             LCSC_Part=lcsc,Assembly_Source=url)
    with (out/'BOM.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(bom)
    with (out/'assembly-bom-draft.csv').open('w') as f:
        writer=csv.writer(f)
        writer.writerow(['Comment','Designator','Footprint','LCSC Part #'])
        for r in bom:
            if r['Reference'] in ('U1','C1','R1'):
                writer.writerow([r['Prototype_MPN'],r['Reference'],r['Footprint'],r['LCSC_Part']])

    # Shared placement and routing. The larger body needs new escapes; merely
    # stretching Rev D's tracks creates shorts at the left pad bank.
    placements={'C1':(41.3,60.095),'C2':(40.8,57.8),'R1':(27.5,64),'R2':(30,57.5)}
    def update(child):
        if kind(child)=='footprint':
            if '(property "Reference" "U1"' in child:
                return grow_package(child).replace('W25Q128JVPIQ',part)
            for ref,xy in placements.items():
                if '(property "Reference" "%s"' % ref in child:
                    return re.sub(r'\(at ([-\d.]+) ([-\d.]+)( [\d.]+)?\)',
                                  lambda m:'(at %g %g%s)' % (*xy,m[3] or ''),child,count=1)
        if kind(child) in ('segment','via'):
            return ''
        if kind(child)=='gr_text':
            child=child.replace('(at 34.2 58.1 0)', '(at 34.2 57.6 0)')
            child=child.replace('(at 28.5 65.8 0)', '(at 27.5 65.8 0)')
            child=child.replace('(at 30 56.5 0)', '(at 30 56 0)')
            child=child.replace('(at 39 56.85 0)', '(at 40.8 56.35 0)')
            child=child.replace('(at 41.3 61.5 0)', '(at 43.4 61.5 0)')
            child=child.replace('"STENO SQUID"','"STENO SQUID %dMB"' % size)
        return child
    board=replace_children((BASE/'steno-squid.kicad_pcb').read_text(),update)
    board=board.replace('D provisional',revision)
    added=[]
    def ident(s):
        return str(uuid.uuid5(uuid.NAMESPACE_URL,'StenoSquid-capacity-layout/'+s))
    def track(net,layer,*points):
        width=.4 if net=='VCC_SW' else .2
        for a,b in zip(points,points[1:]):
            added.append('(segment (start %g %g) (end %g %g) (width %g) (layer "%s.Cu") (net "/%s") (uuid "%s"))' %
                         (*a,*b,width,layer,net,ident(repr((net,layer,a,b)))))
    def via(net,point):
        added.append('(via (at %g %g) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net "/%s") (uuid "%s"))' %
                     (*point,net,ident(repr((net,point)))))
    track('CS_N','F',(30.375,60.095),(28.8,60.095))
    via('CS_N',(28.8,60.095));via('CS_N',(26.8,63.2))
    track('CS_N','B',(28.8,60.095),(26.8,62.095),(26.8,63.2))
    track('CS_N','F',(26.8,63.2),(26.675,64),(27.2,70))
    track('IO1','F',(30.375,61.365),(28.8,61.365))
    via('IO1',(28.8,61.365))
    track('IO1','B',(28.8,61.365),(28.1,62.065),(28.1,64),(34.1,70),(34.82,70))
    track('IO2','F',(30.375,62.635),(28.8,62.635))
    via('IO2',(28.8,62.635));via('IO2',(41.1,66.65))
    track('IO2','B',(28.8,62.635),(31.4,62.635),(31.4,64.5),(33.55,66.65),(41.1,66.65))
    track('IO2','F',(41.1,66.65),(44.7,66.85),(44.98,67.85),(44.98,70))
    track('IO0','F',(29.74,70),(38.025,63.905))
    track('IO3','F',(32.28,70),(37.4,65.65))
    via('IO3',(37.4,65.65));via('IO3',(39,61.365))
    track('IO3','B',(37.4,65.65),(37.4,62.965),(39,61.365))
    track('IO3','F',(39,61.365),(38.025,61.365))
    track('CLK','F',(38.025,62.635),(38.8,62.635))
    via('CLK',(38.8,62.635))
    track('CLK','B',(38.8,62.635),(42.44,66.275),(42.44,70))
    track('VCC_SW','F',(37.36,70),(40.525,60.095),(38.025,60.095))
    track('VCC_SW','F',(40.525,60.095),(40.025,57.8),(38.525,56.3),(29.225,56.3),(29.225,57.5))
    track('VCC_SW','F',(29.225,57.5),(27.8,58.925),(27.8,62.8),(28.325,64))
    track('GND','F',(39.9,70),(39.9,65.75))
    for point in ((33.2,64.9),(42.5,58.9),(30.4,58.8),(36.4,58.9)):
        via('GND',point)
    board=board.rstrip()[:-1]+'\n'+'\n'.join(added)+'\n)\n'
    (out/'steno-squid.kicad_pcb').write_text(board)
    print(out)

if __name__=='__main__':
    for size in (32,64):
        build(size)
