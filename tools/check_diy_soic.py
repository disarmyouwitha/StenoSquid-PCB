"""Validate either DIY hand-solderable SOIC edition.

This is a package-aware sibling of validate.py: it reuses the same ERC/DRC/
netlist/header-position checks, but replaces the WSON-specific assumptions
(pad 9 = exposed GND pad, C2/R2 present) with the selected SOIC package contract.

Usage: python3 tools/check_diy_soic.py [path to DIY project]
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from kicad_sexpr import nodes, kind

ROOT = Path(__file__).resolve().parents[1]
output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'variants/16mb-diy-soic'

interface = json.loads((output / 'interface.json').read_text())
drc = json.loads((output / 'checks/drc.json').read_text())
erc = json.loads((output / 'checks/erc.json').read_text())
erc_issues = [issue for sheet in erc['sheets'] for issue in sheet['violations']]
assert not erc_issues, erc_issues
assert not drc['violations'], drc['violations']
assert not drc['unconnected_items']
assert not drc['schematic_parity'], drc['schematic_parity']
assert not erc['ignored_checks'], 'Every ERC category must be enabled'
assert not drc['ignored_checks'], 'Every DRC category must be enabled'

netlist_path = output / 'checks/netlist.xml'
netlist_text = netlist_path.read_text()
netlist_text = re.sub(r'(<source>)[^<]*[/\\]([^/<\\]+)(</source>)', r'\1\2\3', netlist_text)
netlist_path.write_text(netlist_text)
netlist = ET.fromstring(netlist_text)
members = {net.get('name').lstrip('/'): {(node.get('ref'), node.get('pin')) for node in net.findall('node')}
           for net in netlist.findall('./nets/net')}

board = (output / 'steno-squid.kicad_pcb').read_text()
footprints = {}
for _, _, node in nodes(board):
    if kind(node) == 'footprint':
        reference = re.search(r'\(property "Reference" "([^"]+)"', node)[1]
        footprints[reference] = node


def pads(reference):
    return [n for _, _, n in nodes(footprints[reference]) if kind(n) == 'pad']


def pad_net(reference, number):
    for n in pads(reference):
        if n.startswith(f'(pad "{number}" '):
            return re.search(r'\(net "([^"]+)"\)', n)[1].lstrip('/')
    raise AssertionError((reference, number))


# Winbond package-specific pin assignments, keyed by the host signal.
package = interface.get('flash_package', 'SOIC-8')
contracts = {
    'SOIC-8': (16, 'SOIC-8_5.3x5.3mm_P1.27mm', 8, (1, 5, 7, 2, 8, 4, 6, 3)),
    'SOIC-16': (64, 'SOIC-16W_7.5x10.3mm_P1.27mm', 16, (7, 15, 1, 8, 2, 10, 16, 9)),
}
capacity, footprint_name, lead_count, flash_pins = contracts[package]
u1_pads = pads('U1')
numbers = sorted(int(re.search(r'\(pad "(\d+)"', n)[1]) for n in u1_pads)
assert numbers == list(range(1, lead_count + 1)), numbers
u1_fpid = re.search(r'\(footprint "([^"]+)"', footprints['U1'])[1]
assert u1_fpid == f'StenoSquid:{footprint_name}', u1_fpid
land = (output / 'footprints/StenoSquid.pretty' / f'{footprint_name}.kicad_mod').read_text()

def geometry(pad_nodes):
    return [(re.search(r'\(pad "(\d+)"', p)[1],
             *(re.search(r'\(' + field + r' ([^)]*)\)', p)[1]
               for field in ('at', 'size', 'layers'))) for p in pad_nodes]

assert geometry(u1_pads) == geometry([n for _, _, n in nodes(land) if kind(n) == 'pad'])
pad_pos = {int(re.search(r'\(pad "(\d+)"', n)[1]):
           float(re.search(r'\(at [-\d.]+ ([-\d.]+)', n)[1]) for n in u1_pads}
for start in (1, lead_count // 2 + 1):
    ys = sorted(pad_pos[n] for n in range(start, start + lead_count // 2))
    assert all(abs(b - a - 1.27) < 1e-6 for a, b in zip(ys, ys[1:])), ys
assert any(kind(n) == 'fp_poly' and '(layer "F.SilkS")' in n
           for _, _, n in nodes(footprints['U1'])), 'missing pin-1 marker on U1'

signals = ('CS_N', 'IO0', 'IO3', 'IO1', 'VCC_SW', 'GND', 'CLK', 'IO2')
expected = {pin: (signal, j1) for j1, (pin, signal) in enumerate(zip(flash_pins, signals), 1)}
assert [(c['flash_pad'], c['signal'], c['position']) for c in interface['contacts']] == [
    (pin, signal, j1) for pin, (signal, j1) in expected.items()]
if package == 'SOIC-16':
    assert pad_net('U1', 3) == 'VCC_SW'
    assert ('U1', '3') in members['VCC_SW']
    for pin in (4, 5, 6, 11, 12, 13, 14):
        signal = pad_net('U1', pin)
        assert signal.startswith('unconnected-'), (pin, signal)
        assert members[signal] == {('U1', str(pin))}
        assert f'(net "{signal}")' not in '\n'.join(
            n for _, _, n in nodes(board) if kind(n) in ('segment', 'via', 'zone'))
for u1_pin, (signal, j1_pin) in expected.items():
    assert pad_net('U1', u1_pin) == signal, (u1_pin, signal)
    assert pad_net('J1', j1_pin) == signal, (j1_pin, signal)
    assert ('U1', str(u1_pin)) in members[signal]
    assert ('J1', str(j1_pin)) in members[signal]

# --- 3. Power: R1/C1 values, 0805 footprints, no C2/R2, VCC_SW min width rule.
assert 'C2' not in footprints and 'R2' not in footprints, 'DIY edition must omit C2/R2'
assert ('C1', '1') in members['VCC_SW'] and ('C1', '2') in members['GND']
assert ('R1', '1') in members['VCC_SW'] and ('R1', '2') in members['CS_N']
assert footprints['C1'].startswith('(footprint "StenoSquid:C_0805_2012Metric"')
assert footprints['R1'].startswith('(footprint "StenoSquid:R_0805_2012Metric"')

lengths, segment_counts, minimum_widths, via_counts = {}, {}, {}, {}
for _, _, node in nodes(board):
    if kind(node) not in ('segment', 'via'):
        continue
    net = re.search(r'\(net "([^"]+)"\)', node)[1]
    if kind(node) == 'via':
        via_counts[net] = via_counts.get(net, 0) + 1
    else:
        start = tuple(map(float, re.search(r'\(start ([\d.e+-]+) ([\d.e+-]+)\)', node).groups()))
        end = tuple(map(float, re.search(r'\(end ([\d.e+-]+) ([\d.e+-]+)\)', node).groups()))
        lengths[net] = lengths.get(net, 0) + sum((a - b) ** 2 for a, b in zip(start, end)) ** 0.5
        segment_counts[net] = segment_counts.get(net, 0) + 1
        width = float(re.search(r'\(width ([\d.e+-]+)\)', node)[1])
        minimum_widths[net] = min(width, minimum_widths.get(net, width))
assert minimum_widths['/VCC_SW'] >= 0.4
project = json.loads((output / 'steno-squid.kicad_pro').read_text())
assert any(item['netclass'] == 'Power' and item['pattern'] == '/VCC_SW'
           for item in project['net_settings']['netclass_patterns'])
assert '(constraint track_width (min 0.4mm))' in (output / 'steno-squid.kicad_dru').read_text()

# --- 4. Mechanical: common outline and fixed header centres.
header_at = re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)', footprints['J1'])
assert tuple(map(float, header_at.groups())) == (27.2, 70.0, 90.0)
header_positions = []
for n in pads('J1'):
    number = int(re.search(r'\(pad "(\d+)"', n)[1])
    x, y = map(float, re.search(r'\(at ([-\d.]+) ([-\d.]+)', n).groups())
    assert abs(27.2 + y - (27.2 + 2.54 * (number - 1))) < 1e-7 and abs(x) < 1e-7
    header_positions.append([number, round(27.2 + y, 3), 70.0])
baseline_board = (ROOT / 'pcb/steno-squid.kicad_pcb').read_text()
base_edges = [n for _, _, n in nodes(baseline_board) if kind(n) in ('gr_line', 'gr_arc') and '(layer "Edge.Cuts")' in n]
this_edges = [n for _, _, n in nodes(board) if kind(n) in ('gr_line', 'gr_arc') and '(layer "Edge.Cuts")' in n]
assert base_edges == this_edges, 'DIY board outline must match the shared baseline exactly'

# --- 5. Artwork and finish.
f_silk_text = {re.search(r'\(gr_text "([^"]+)"', n)[1]
               for _, _, n in nodes(board) if kind(n) == 'gr_text' and '(layer "F.SilkS")' in n}
assert 'STENO SQUID' in f_silk_text and f'{capacity} MB' in f_silk_text


def artwork(cad, layer):
    return sorted(re.findall(r'\(xy ([^)]+)\)', n) for _, _, n in nodes(cad)
                  if kind(n) == 'gr_poly' and f'(layer "{layer}")' in n)


finish = interface.get('artwork_finish', 'silkscreen')
assert finish in ('silkscreen', 'enig')
if finish == 'enig':
    diy_base = (ROOT / f'variants/{capacity}mb-diy-soic/steno-squid.kicad_pcb').read_text()
    wson_gold_dir = 'enig' if capacity == 16 else '64mb-enig'
    wson_gold = (ROOT / 'variants' / wson_gold_dir / 'steno-squid.kicad_pcb').read_text()
    assert artwork(board, 'F.Cu') == artwork(board, 'F.Mask') == artwork(diy_base, 'F.SilkS')
    assert artwork(board, 'F.Cu') and not artwork(board, 'F.SilkS')
    assert '(copper_finish "ENIG")' in board

    def halos(cad):
        return [n for _, _, n in nodes(cad) if kind(n) == 'zone' and '(name "Gold Pop halo ' in n]

    assert halos(board) and halos(board) == halos(wson_gold)
    for object_kind in ('footprint', 'segment', 'via'):
        assert sorted(n for _, _, n in nodes(board) if kind(n) == object_kind) == sorted(
            n for _, _, n in nodes(diy_base) if kind(n) == object_kind
        ), f'Gold edition changed DIY {object_kind} geometry or connectivity'
else:
    assert not artwork(board, 'F.Cu') and not artwork(board, 'F.Mask')

schematic = (output / 'steno-squid.kicad_sch').read_text()
for cad in (board, schematic):
    assert f'(rev "{interface["revision"]}")' in cad
    assert f'(title "Steno Squid {interface["variant"]}")' in cad

report = {
    'revision': interface['revision'],
    'variant': interface['variant'],
    'artwork_finish': finish,
    'review_date': drc['date'].split('T')[0],
    'ERC_violations': len(erc_issues),
    'DRC_violations': len(drc['violations']),
    'unconnected_items': len(drc['unconnected_items']),
    'schematic_parity_issues': len(drc['schematic_parity']),
    'u1_footprint': u1_fpid,
    'capacity_bytes': capacity * 1024 * 1024,
    'u1_pad_count': len(u1_pads),
    'c2_r2_present': False,
    'all_eight_contacts_verified_against_schematic_and_PCB': True,
    'configured_ignored_DRC_categories': drc['ignored_checks'],
    'configured_ignored_ERC_categories': erc['ignored_checks'],
    'supply_minimum_width_rule_mm': 0.4,
    'copper_track_lengths_mm': {net: round(value, 3) for net, value in lengths.items()},
    'minimum_track_widths_mm': minimum_widths,
    'track_segment_counts': segment_counts,
    'via_counts': via_counts,
    'header_centres_kicad_mm': sorted(header_positions),
    'outline_matches_baseline': True,
    'host_fit_verified': False,
    'host_power_qualified': False,
    'first_hand_assembly_verified': False,
    'hashes': {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [output / 'steno-squid.kicad_pcb', output / 'steno-squid.kicad_sch',
                         output / 'steno-squid.kicad_pro', output / 'steno-squid.kicad_dru']},
}
(output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'ERC, DRC, unconnected, parity all zero. {package} pad contract, net map, '
      'power network and outline all verified.')
