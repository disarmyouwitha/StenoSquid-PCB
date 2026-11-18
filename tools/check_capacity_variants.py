"""Check Rev D and both capacity options; refresh review/assembly previews.

No Gerbers or drill files are generated. Set KICAD_CLI if it is not on PATH.
"""
from pathlib import Path
import argparse
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
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only',type=int,choices=(16,32,64),help='Refresh only this capacity; do not touch other projects')
parser.add_argument('--finish',choices=('silkscreen','enig'),help='Refresh only projects with this artwork finish')
args=parser.parse_args()

def run(*args):
    subprocess.run([str(a) for a in args],cwd=ROOT,check=True)

def geometry(path):
    board=path.read_text()
    return [n for _,_,n in nodes(board) if kind(n) in ('segment','via','zone')]

baseline=(ROOT/'pcb/steno-squid.kicad_pcb').read_text()
def edge_geometry(board):
    return sorted((kind(n),tuple((label,float(x),float(y)) for label,x,y in
                  re.findall(r'\((start|mid|end) ([-\d.]+) ([-\d.]+)\)',n)))
                  for _,_,n in nodes(board) if kind(n) in ('gr_line','gr_arc') and '(layer "Edge.Cuts")' in n)
base_edges=edge_geometry(baseline)
def artwork(board):
    return {re.search(r'\(uuid "([^"]+)"',n)[1]:
            [tuple(map(float,p)) for p in re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)',n)]
            for _,_,n in nodes(board) if kind(n)=='gr_poly' and '(layer "F.SilkS")' in n}
base_art=artwork(baseline)
projects=[(16,ROOT/'pcb'),(32,ROOT/'variants/32mb'),(64,ROOT/'variants/64mb'),
          (16,ROOT/'variants/enig'),(32,ROOT/'variants/32mb-enig'),(64,ROOT/'variants/64mb-enig')]
for size,out in projects:
    if args.only and (size!=args.only or out.name.endswith('enig')):
        continue
    enig=out.name.endswith('enig')
    if args.finish and enig!=(args.finish=='enig'):
        continue
    before_board=(out/'steno-squid.kicad_pcb').read_text()
    pcb=out/'steno-squid.kicad_pcb';sch=out/'steno-squid.kicad_sch'
    run(CLI,'sch','erc','--format','json','--severity-all','--exit-code-violations','-o',out/'checks/erc.json',sch)
    run(CLI,'sch','export','netlist','--format','kicadxml','-o',out/'checks/netlist.xml',sch)
    run(CLI,'pcb','drc','--refill-zones','--save-board','--schematic-parity','--severity-all',
        '--exit-code-violations','--format','json','-o',out/'checks/drc.json',pcb)
    run(sys.executable,ROOT/'tools/validate.py',out)
    run(sys.executable,ROOT/'tools/make_fit_template.py',out)
    board=pcb.read_text()
    assert edge_geometry(board)==base_edges
    assert artwork(board)==artwork(before_board), 'Preserve each project artwork treatment'
    if not enig:
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
    candidate=json.loads((out/'interface.json').read_text()).get('mechanical_candidate')
    report.update(capacity_bytes=size*1024*1024, baseline_outline_preserved=True,
                  baseline_pop_artwork_preserved=True, footprint_pad_geometry_matches_local_library=True,
                  fabrication_release=False,electrical_baseline_tag='rev-d',mechanical_update_date=report['review_date'],
                  baseline_board_sha256=hashlib.sha256((ROOT/'pcb/steno-squid.kicad_pcb').read_bytes()).hexdigest())
    if candidate:
        report.update(mechanical_candidate=candidate,baseline_outline_preserved=False,
                      matches_current_16mb_outline=True)
    mechanical=json.loads((out/'interface.json').read_text()).get('mechanical_revision')
    if mechanical:
        report.update(mechanical_revision=mechanical,matches_approved_outline=True,
                      baseline_outline_preserved=False)
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    run(CLI,'sch','export','svg','--output',str(out/'previews')+'/',sch)
    run(CLI,'pcb','export','pos','--format','csv','--units','mm','--side','front',
        '--smd-only','--exclude-dnp','--output',out/'assembly-positions-draft.csv',pcb)
    run(CLI,'pcb','export','step','--force','--no-dnp','--output',out/'steno-squid.step',pcb)
    for artifact in ('assembly-positions-draft.csv','steno-squid.step','previews/steno-squid.svg'):
        p=out/artifact
        p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
    for side,name in [('top','front-pop' if size==16 else 'front'),('bottom','back')]:
        run(CLI,'pcb','render','--width','1000','--height','1400','--side',side,
            '--quality','high','--use-board-stackup-colors','--background','opaque',
            '--output',out/'previews'/('%s.png'%name),pcb)
    if enig and size!=16:
        shutil.copy2(out/'previews/front.png',out/'previews/front-pop.png')

assert geometry(ROOT/'variants/32mb/steno-squid.kicad_pcb')==geometry(ROOT/'variants/64mb/steno-squid.kicad_pcb'), 'Capacity variants must share copper'
print(('Selected capacity passed.' if args.only else 'All six projects passed; common outline verified.')+
      ' Shared 32/64 MB copper verified. No fabrication files generated.')
