"""Check Rev D and both capacity options; refresh review/assembly previews.

No Gerbers or drill files are generated. Set KICAD_CLI if it is not on PATH.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from kicad_sexpr import nodes, kind

ROOT=Path(__file__).resolve().parents[1]
CLI=os.environ.get('KICAD_CLI') or shutil.which('kicad-cli') or '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'

def run(*args):
    subprocess.run([str(a) for a in args],cwd=ROOT,check=True)

def geometry(path):
    board=path.read_text()
    return [n for _,_,n in nodes(board) if kind(n) in ('segment','via','zone')]

baseline=(ROOT/'pcb/steno-squid.kicad_pcb').read_text()
base_edges=[n for _,_,n in nodes(baseline) if kind(n) in ('gr_line','gr_arc') and '(layer "Edge.Cuts")' in n]
def artwork(board):
    return {re.search(r'\(uuid "([^"]+)"',n)[1]:
            [tuple(map(float,p)) for p in re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)',n)]
            for _,_,n in nodes(board) if kind(n)=='gr_poly' and '(layer "F.SilkS")' in n}
base_art=artwork(baseline)
for size in (16,32,64):
    out=ROOT/'pcb' if size==16 else ROOT/'variants'/('%dmb'%size)
    pcb=out/'steno-squid.kicad_pcb';sch=out/'steno-squid.kicad_sch'
    run(CLI,'sch','erc','--format','json','--severity-all','--exit-code-violations','-o',out/'checks/erc.json',sch)
    run(CLI,'sch','export','netlist','--format','kicadxml','-o',out/'checks/netlist.xml',sch)
    run(CLI,'pcb','drc','--refill-zones','--save-board','--schematic-parity','--severity-all',
        '--exit-code-violations','--format','json','-o',out/'checks/drc.json',pcb)
    run(sys.executable,ROOT/'tools/validate.py',out)
    run(sys.executable,ROOT/'tools/make_fit_template.py',out)
    board=pcb.read_text()
    assert [n for _,_,n in nodes(board) if kind(n) in ('gr_line','gr_arc') and '(layer "Edge.Cuts")' in n]==base_edges
    assert artwork(board)==base_art
    # Verify local footprint exactly agrees with the board pad sizes/centres/layers.
    import re
    footprint=next(n for _,_,n in nodes(board) if kind(n)=='footprint' and '(property "Reference" "U1"' in n)
    package='6x5' if size==16 else '8x6'
    land=(out/('footprints/StenoSquid.pretty/WSON-8_%smm_P1.27mm_EP3.4x4.3mm.kicad_mod'%package)).read_text()
    def pad_geometry(fp):
        return [(re.search(r'\(pad "([^"]*)"',n)[1],
                 *[re.search(r'\('+p+r' ([^)]*)\)',n)[1] for p in ('at','size','layers')])
                for _,_,n in nodes(fp) if kind(n)=='pad']
    assert pad_geometry(footprint)==pad_geometry(land)
    for ref in ('C2','R2'):
        fp=next(n for _,_,n in nodes(board) if kind(n)=='footprint' and '(property "Reference" "%s"'%ref in n)
        assert re.search(r'\(attr [^)]*\bdnp\b',fp), ref+' must stay DNP'
    report=json.loads((out/'validation.json').read_text())
    report.update(capacity_bytes=size*1024*1024, baseline_outline_preserved=True,
                  baseline_pop_artwork_preserved=True, footprint_pad_geometry_matches_local_library=True,
                  fabrication_release=False,electrical_baseline_tag='rev-d',mechanical_update_date=report['review_date'],
                  baseline_board_sha256=hashlib.sha256((ROOT/'pcb/steno-squid.kicad_pcb').read_bytes()).hexdigest())
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    run(CLI,'sch','export','svg','--output',str(out/'previews')+'/',sch)
    run(CLI,'pcb','export','pos','--format','csv','--units','mm','--side','front',
        '--smd-only','--exclude-dnp','--output',out/'assembly-positions-draft.csv',pcb)
    run(CLI,'pcb','export','step','--force','--no-dnp','--output',out/'steno-squid.step',pcb)
    for artifact in ('assembly-positions-draft.csv','steno-squid.step'):
        p=out/artifact
        p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
    for side,name in [('top','front-pop' if size==16 else 'front'),('bottom','back')]:
        run(CLI,'pcb','render','--width','1000','--height','1400','--side',side,
            '--quality','high','--use-board-stackup-colors','--background','opaque',
            '--output',out/'previews'/('%s.png'%name),pcb)

assert geometry(ROOT/'variants/32mb/steno-squid.kicad_pcb')==geometry(ROOT/'variants/64mb/steno-squid.kicad_pcb'), 'Capacity variants must share copper'
print('All three capacities passed; shared 32/64 MB copper and common outline verified. No fabrication files generated.')
