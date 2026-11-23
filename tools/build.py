import re, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(HERE, 'base.css')).read()
js = open(os.path.join(HERE, 'base.js')).read()
css += '''
.pts{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:10px;font-size:16px;line-height:1.5}
button{font:inherit;color:inherit}
button.sys{display:block;width:100%;text-align:left;border:1px solid transparent;cursor:pointer;transition:transform .2s ease,border-color .2s ease}
button.sys:hover,button.sys:focus-visible{transform:translateY(-3px);border-color:var(--accent)}
.more{display:inline-block;margin-top:10px;font-size:14px;font-weight:600;color:var(--accent)}
button.btn{cursor:pointer;background:none;border:1px solid var(--dash);align-self:flex-start}
button.btn:hover{border-color:var(--accent);color:var(--accent)}
.sheet{border:none;padding:0;border-radius:28px;width:100%;max-width:min(940px,calc(100vw - 24px));max-height:calc(100vh - 24px);background:var(--bg);color:var(--ink)}
.sheet::backdrop{background:rgba(0,0,0,.6)}
.sheet-in{padding:44px;display:flex;flex-direction:column;gap:18px}
.sheet h2{font-size:clamp(28px,4vw,40px);line-height:1.1;letter-spacing:-.02em}
.sheet h3{font-size:19px;margin-top:10px}
.sheet .x{position:sticky;top:12px;align-self:flex-end;min-height:44px;padding:0 18px;border-radius:980px;border:1px solid var(--dash);background:var(--bg);cursor:pointer;font-size:14px;font-weight:500;margin-bottom:-30px;z-index:1}
.gal{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:8px}
.gal figure{margin:0;display:flex;flex-direction:column;gap:8px}
.gal img,.gal video{width:100%;border-radius:14px;border:1px solid var(--line);background:#fff}
.gal figcaption{font-size:13px;color:var(--grey)}
.fus text{font-family:'Inter',sans-serif;font-size:19px;fill:var(--grey)}
.sheet .eyebrow{padding-right:96px}
.tile.c{justify-content:center;align-items:center;text-align:center}
.tile.c .btn{align-self:center}
.spec{width:100%;border-collapse:collapse;font-size:15px}
.spec th,.spec td{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-bottom:1px solid var(--line)}
.spec th{width:34%;font-weight:600;color:var(--ink)}
.spec td{color:var(--grey)}
.sheet .lead-c{text-align:center;align-items:center}
.kpis{display:flex;flex-wrap:wrap;gap:12px}
.kpis span{flex:1 1 150px;background:var(--surface);border-radius:14px;padding:16px 18px;font-size:13px;color:var(--grey)}
.kpis b{display:block;font-family:'Inter Tight',sans-serif;font-size:24px;color:var(--ink)}
@media (max-width:600px){.sheet-in{padding:24px}}
'''

def img(src, alt, style='', lazy=''):
    return f'<img src="assets/{src}" alt="{html.escape(alt)}" {lazy}style="{style}">'

def sheet(id, eyebrow, title, lead, sections, gallery):
    out = [f'<dialog class="sheet" id="d-{id}" aria-labelledby="t-{id}"><div class="sheet-in">',
           '<button class="x" data-close>Close</button>',
           f'<div class="eyebrow">{eyebrow}</div>', f'<h2 id="t-{id}">{title}</h2>', f'<p class="grey" style="font-size:19px">{lead}</p>']
    for h, items in sections:
        if h == 'KPI':
            out.append('<div class="kpis">' + ''.join(f'<span><b>{b}</b>{t}</span>' for b,t in items) + '</div>'); continue
        out.append(f'<h3>{h}</h3>')
        if isinstance(items, str): out.append(f'<p>{items}</p>')
        elif items and isinstance(items[0], tuple):
            out.append('<table class="spec">' + ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in items) + '</table>')
        else: out.append('<ul class="pts">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>')
    if gallery:
        out.append('<div class="gal">')
        for g in gallery:
            if g[0].endswith('.mp4'):
                out.append(f'<figure><video src="assets/{g[0]}" poster="assets/robot-still.jpg" controls muted playsinline preload="none" aria-label="{html.escape(g[1])}"></video><figcaption>{g[1]}</figcaption></figure>')
            elif g[0] == 'SVG':
                out.append(f'<figure style="grid-column:1/-1">{FUS}<figcaption>{g[1]}</figcaption></figure>')
            else:
                out.append(f'<figure>{img(g[0], g[1], lazy=LAZY)}<figcaption>{g[1]}</figcaption></figure>')
        out.append('</div>')
    out.append('</div></dialog>')
    return '\n'.join(out)

LAZY = 'loading="lazy" '
FUS = '''<svg class="fus" viewBox="0 0 900 230" role="img" aria-label="Side view of the four-section sample fuselage" style="width:100%;height:auto">
<g fill="none" stroke="var(--ink)" stroke-width="2">
<path d="M70 80 L20 110 L70 140 Z"/>
<rect x="70" y="80" width="190" height="60"/><rect x="260" y="80" width="190" height="60"/><rect x="450" y="80" width="190" height="60"/><rect x="640" y="80" width="190" height="60"/>
<path d="M740 80 L770 35 L815 35 L800 80 Z"/><path d="M740 140 L770 185 L815 185 L800 140 Z"/>
<rect x="480" y="62" width="34" height="18"/><rect x="480" y="140" width="34" height="18"/>
</g>
<g fill="var(--accent)" opacity=".28"><rect x="200" y="86" width="120" height="48"/><rect x="390" y="86" width="120" height="48"/><rect x="580" y="86" width="120" height="48"/></g>
<line x1="165" y1="80" x2="165" y2="140" stroke="var(--ink)" stroke-dasharray="4 4"/>
<text x="165" y="215" text-anchor="middle">1 Nose</text><text x="355" y="215" text-anchor="middle">2 Upper body</text><text x="545" y="215" text-anchor="middle">3 Canard module</text><text x="735" y="215" text-anchor="middle">4 Fin can</text>
<text x="260" y="20" text-anchor="middle">Coupler sleeves at each joint</text>
<line x1="260" y1="26" x2="260" y2="84" stroke="var(--grey)"/><line x1="260" y1="26" x2="450" y2="84" stroke="var(--grey)"/><line x1="260" y1="26" x2="640" y2="84" stroke="var(--grey)"/>
</svg>'''

TP = 'Team Phantom · Grounded Low Voltage'
sheets = [
sheet('vcu', TP, 'Vehicle Control Unit',
 'TMS570 microcontroller board. The schematic covers CAN, three contactor enables, BSPD and IMD inputs, BMS UART, a watchdog, a DAC output and on-board buck converters. Revision 4, ten sheets.',
 [('My work', ['Leading the firmware migration from the TMS570 to an STM32H7, with a NUCLEO-H755ZI evaluation board on order.',
   'Reviewing the revision 4 schematic against the 2027 Formula SAE rules.',
   'Assigning tasks and reviewing designs for the hardware and firmware members working on the board.'])],
 [('vcu-3d.jpg','VCU, Altium 3D view'),('vcu-schematic.jpg','VCU schematic, microcontroller signals sheet'),('vcu-can.jpg','VCU schematic, CAN sheet')]),
sheet('daq', TP, 'Data Acquisition',
 'Reads four wheel speed sensors, two coolant pressure sensors, two coolant temperature sensors and an IMU, with a CAN output. The current build is on perfboard.',
 [('My work', ['Leading the PCB design that replaces the perfboard build.',
   'Responsible for sensor implementation on the redesign.'])],
 [('daq-perfboard.jpg','Current DAQ perfboard build'),('daq-perfboard-2.jpg','DAQ perfboard, side view')]),
sheet('pdb', TP, 'Power Distribution Board',
 'Supplies the low-voltage boards from the 13.2 V battery input. LT4363 over- and under-voltage protection with 17.22 V and 9.54 V cutoffs, a current monitor with I2C output across a 0.002 Ω shunt, and an LM3489 12 V to 5 V buck converter.',
 [('My work', ['Debugged and tested the board.',
   'Checking the board against the 2027 Formula SAE rules as part of the low-voltage rules audit.'])],
 [('pdb-3d.jpg','PDB, Altium 3D view'),('pdb-protection.jpg','PDB schematic, protection sheet'),('pdb-supply.jpg','PDB schematic, current monitor and 12 V to 5 V buck sheet')]),
sheet('lvsdb', TP, 'Low-Voltage Shutdown Board and BSPD',
 'One PCB with two safety systems: the low-voltage shutdown circuit, driven from the VCU fault line, and the brake system plausibility device (BSPD).',
 [('My work', ['Performed bring-up and troubleshooting on both safety systems and soldered the replacement board.',
   'Identified five design faults through a schematic and datasheet review.',
   'Found a dual OR gate rated to 3.6 V (NC7WP32) on the 5 V rail and replaced it in the design with the 5 V-rated NC7WZ32.',
   'Found a reversed MOSFET pinout by checking the PCB footprint against the schematic symbol.',
   'Tested both relays in circuit and isolated, and confirmed coil resistance against the datasheet.',
   'Built low-voltage wire harnesses and verified continuity and signal integrity with oscilloscopes and multimeters, including pin-by-pin checks of 30-pin connectors.']),
  ('Status', 'Board working.')],
 [('lvsdb-3d.jpg','LVSDB, Altium 3D view'),('lvsdb-schematic.jpg','Shutdown circuit schematic'),('bspd-schematic.jpg','BSPD schematic')]),
sheet('carrier', TP, 'Carrier Board',
 'One board that consolidates 9 PCBs and 20+ vehicle signals inside the low-voltage enclosure of a 400 V race car.',
 [('My work', ['Designed the carrier board in Altium Designer, with sealed Samtec connectors at the enclosure.',
   'Documented the full low-voltage wiring interface (150+ pins) from harness drawings and board schematics, now the team\'s reference for harness integration and debugging.',
   'Mapped connections for the BMS, fault relay, inverter control board, VCU, PDB and shutdown board.',
   'Integrated the Samtec connectors and fit the PCBs into the enclosure.']),
  ('Connections on the schematic', ['Power from the PDB: 5 V to the accelerator pedal sensors, dashboard, pedal box, DAQ and HV current transducer; 12 V to the BMS, inverter, TSAL, dashboard and HV board.',
   'Faults and safety: BMS fault, IMD fault, BSPD fault, VCU fault, shutdown circuit in and out, set/reset and TSAL enable.',
   'Driver controls: two accelerator pedal position signals, brake signal, ready-to-drive switch and buzzer, and brake light.',
   'Communication: CAN high and low to the dashboard and DAQ, and SPI.',
   'Sensors: four wheel speed, two coolant pressure, two coolant temperature and an IMU.',
   'Connectors: two 30-pin and one 20-pin Samtec, plus headers for the VCU, PDB, shutdown board and DAQ.']),
  ('Status', 'Design complete. Build planned for the next vehicle.')],
 [('carrier-board-schematic.jpg','Carrier board schematic'),('carrier-board-3d.jpg','Carrier board, Altium 3D view'),('glv-enclosure.jpg','Low-voltage enclosure with the current boards')]),
sheet('motor', 'Technical project', 'Three-Phase Linear Induction Motor',
 'A small linear induction motor that uses three-phase AC to produce a travelling magnetic field and accelerate a magnetically suspended cart.',
 [('My work', ['Designed and soldered the motor\'s three-phase power stage on perfboard, deriving the RLC component values from the transfer function to produce ±120° phase shifts at matched amplitude from a single function generator.',
   'Measured 2 to 3 m/s² cart acceleration against a 2.15 m/s² prediction after tracing low coil current (78 mA) and switching to synchronized generators with a 300 W amplifier.']),
  ('Circuit values', 'Network 1: 100 Ω, 10 µF, 174 mH, output across the capacitor, −120°. Network 2: 65 Ω, 10 µF, 73 mH, output across the inductor, +120°. Operating frequency 150 Hz.')],
 [('induction-motor-bench.jpg','Track, power supplies and amplifier on the bench'),('lim-bench-scope.jpg','Oscilloscope and breadboard during testing'),('lim-coils.jpg','Coils under the track'),('lim-multimeter.jpg','Coil current measurement')]),
sheet('robot', 'Technical project', 'Vision-Guided Sorting Robot',
 'A Raspberry Pi robot arm that detects objects with a camera and sorts them.',
 [('My work', ['Deployed a YOLOX object detector (C++, ncnn) on a Raspberry Pi and connected it to the robot\'s Python arm controller through a named pipe.',
   'Fixed camera buffering, pipe communication, and detection-threshold bugs to run detection at full frame rate.',
   'Added runtime model selection across three YOLOX model sizes with frame-rate measurement.',
   'Sequenced servo moves one at a time to stay within the power supply\'s current limit.'])],
 [('robot-run.mp4','The robot on a line-tracking and obstacle-avoidance run')]),
sheet('braille', 'Technical project', 'Speech-to-Braille Converter',
 'Schematic, PCB layout and case design for a speech-to-braille device with a 2×10 braille cell array.',
 [('My work', ['Developed the schematic and PCB layout in Altium Designer for an assistive device driving a 2×10 braille cell array from an STM32 microcontroller through a UDN2981A/ULN2803A driver stage.'])],
 [('braille-assembly.jpg','Exploded assembly'),('braille-sketch.jpg','Case layout sketch'),('braille-top-case.jpg','Top case drawing'),('braille-bottom-case.jpg','Bottom case drawing')]),
sheet('fuselage', 'SFU Rocketry · Active Fin Stabilization', 'Parametric Rocket Fuselage',
 'A 100 mm sample fuselage assembly in SolidWorks, built for SFU Rocketry\'s 18-inch, 200 kg sounding rocket and laid out to carry the active fin stabilization module.',
 [('My work', ['Built a parametric SolidWorks fuselage assembly driven by a 23-variable equation file, so one edit rescales the airframe.',
   'Modelled four 240 mm body sections joined by coupler sleeves, with canard slots in section 3 and through-wall fin slots in section 4.',
   'Corrected three specification errors during the build (coupler length, coupler wall thickness and fin slot clearance) by checking each dimension against published rocket reports.',
   'Wrote the fuselage design overview for the vehicle: section layout, mass budget, nose cone profile, fin options and stability margins.',
   'Modelled the canard control module packaging: four bushings with ±15° hard stops, the flight computer mount and the servo wiring.',
   'Selected the FeeTech STS3215 servo, which has a built-in 12-bit encoder and removes the need for external encoders.']),
  ('Design basis', 'Coupler length 200 mm, one caliber of engagement per side. Four bolts per side at 90° spacing. 0.5 mm coupler slip clearance. 3.2 mm slots for 3 mm fins and canards.')],
 [('SVG','Sample fuselage, four sections with coupler sleeves at each joint'),('rocket-layout.jpg','Vehicle layout from the conceptual design')]),
]

def tile(id, title, line, media):
    return f'<button class="sys" data-open="{id}" style="background: var(--bg)">{media}<h3>{title}</h3><p>{line}</p><span class="more">View details</span></button>'
TI = 'display: block; width: 100%; height: 170px; object-fit: cover; object-position: {}; border-radius: 10px; margin-bottom: 14px'
tiles = '\n'.join([
 tile('vcu','Vehicle Control Unit','Leading the firmware migration to an STM32H7.', img('vcu-3d.jpg','VCU, Altium 3D view',TI.format('center'))),
 tile('daq','Data Acquisition','Leading the PCB design and sensor implementation.', img('daq-perfboard.jpg','Current DAQ perfboard build',TI.format('center 40%'))),
 tile('pdb','Power Distribution Board','Debugged and tested.', img('pdb-3d.jpg','PDB, Altium 3D view',TI.format('center'))),
 tile('lvsdb','Low-Voltage Shutdown Board','Soldered the replacement board. Bring-up and troubleshooting.', img('lvsdb-3d.jpg','LVSDB, Altium 3D view',TI.format('center 30%'))),
 tile('lvsdb','Brake System Plausibility Device','Schematic and datasheet review. Five design faults identified.', img('bspd-schematic.jpg','BSPD schematic',TI.format('center 55%'))),
 tile('carrier','Carrier Board and Wiring Harness','Designed in Altium Designer. 150+ pin interface documented.', img('carrier-board-schematic.jpg','Carrier board schematic',TI.format('left top'))),
])

def project(n, id, label, num, h2, pts, stats, visual, alt=False, scene=False):
    cls = 'sec' + (' alt' if alt else '') + (' scene' if scene else '')
    idattr = ' id="work"' if scene else ''
    inner = f'''<div class="wrap row">
<div class="col rv">
<div class="eyebrow">{n} · {label}</div>
<div class="num">{num}</div>
<h2 class="h2">{h2}</h2>
<ul class="pts">{''.join(f'<li>{p}</li>' for p in pts)}</ul>
<div class="stats">{''.join(f'<span><b{c}>{b}</b>{t}</span>' for b,t,c in stats)}</div>
<button class="btn" data-open="{id}">Full details</button>
</div>
{visual}
</div>'''
    if scene: inner = f'<div class="stick">\n{inner}\n</div>'
    return f'<div class="{cls}"{idattr}>\n{inner}\n</div>'

nine = '<div class="nine" role="img" aria-label="Nine small boards merging into one">' + ''.join(f'<i style="--x: {x}px; --y: {y}px"></i>' for y in (-22,0,22) for x in (-22,0,22)) + '</div>'
RENDER = img('carrier-board-schematic.jpg','Carrier board schematic in Altium Designer','width: 100%; border-radius: 12px; border: 1px solid var(--line)').replace('<img ','<img class="render" ')
FIG = 'flex: 1 1 400px; min-width: 0; margin: 0; display: flex; flex-direction: column; gap: 10px'
projects = '\n\n'.join([
 project('01','carrier','Carrier board · Team Phantom','9 → 1','Carrier board consolidating 9 PCBs and 20+ vehicle signals.',
  ['Designed a carrier board in Altium Designer that consolidates 9 PCBs and 20+ vehicle signals for a 400 V race car, with sealed Samtec connectors at the enclosure.',
   'Documented the full low-voltage wiring interface (150+ pins) from harness drawings and board schematics, now the team\'s reference for harness integration and debugging.'],
  [('20+','vehicle signals',''),('150+','pins documented',''),('400 V','vehicle',''),('Complete','design status','')],
  f'<div class="ph stage" style="flex-direction: column; gap: 28px; border: none; padding: 28px">{nine}{RENDER}</div>', scene=True),
 project('02','lvsdb','Shutdown circuit and BSPD · Team Phantom','<span data-count="5">5</span> faults','Bring-up and troubleshooting on two safety systems.',
  ['Performed bring-up and troubleshooting on two safety systems, the low-voltage shutdown circuit and the brake system plausibility device, soldered the replacement board, identified five design faults through a schematic and datasheet review, and replaced the overvolted logic IC.',
   'Built low-voltage wire harnesses and verified continuity and signal integrity with oscilloscopes and multimeters, including pin-by-pin checks of 30-pin connectors.'],
  [('5','design faults',' data-count="5"'),('3.6 V','part on a 5 V rail',''),('Working','board status','')],
  f'<figure style="{FIG}">{img("bspd-schematic.jpg","BSPD schematic","width: 100%; border-radius: 20px; border: 1px solid var(--line)")}<figcaption class="grey" style="font-size: 14px">BSPD schematic.</figcaption></figure>', alt=True),
 project('03','motor','Three-phase linear induction motor','<span data-count="2.15">2.15</span> m/s²','Predicted cart acceleration. Measured 2 to 3 m/s².',
  ['Designed and soldered the motor\'s three-phase power stage on perfboard, deriving the RLC component values from the transfer function to produce ±120° phase shifts at matched amplitude from a single function generator.',
   'Measured 2 to 3 m/s² cart acceleration against a 2.15 m/s² prediction after tracing low coil current (78 mA) and switching to synchronized generators with a 300 W amplifier.'],
  [('±120°','phase shifts',''),('150 Hz','operating frequency',''),('300 W','amplifier','')],
  img('induction-motor-bench.jpg','Linear induction motor track on the lab bench with oscilloscope, power supplies and amplifier board','flex: 1 1 400px; min-width: 0; width: 100%; max-width: 560px; height: 420px; object-fit: cover; object-position: 60% 60%; border-radius: 28px')),
 project('04','robot','Vision-guided sorting robot','<span data-count="3">3</span> bugs fixed','YOLOX object detection on a Raspberry Pi robot arm.',
  ['Deployed a YOLOX object detector (C++, ncnn) on a Raspberry Pi and connected it to the robot\'s Python arm controller through a named pipe.',
   'Fixed camera buffering, pipe communication, and detection-threshold bugs to run detection at full frame rate.'],
  [('C++, Python','languages',''),('ncnn','inference framework',''),('3','model sizes tested','')],
  f'<figure style="{FIG}"><video src="assets/robot-run.mp4" poster="assets/robot-still.jpg" controls muted loop playsinline preload="metadata" aria-label="The robot driving a taped line track and steering around an obstacle" style="width: 100%; border-radius: 28px; background: #000000"></video><figcaption class="grey" style="font-size: 14px">The robot on a line-tracking and obstacle-avoidance run.</figcaption></figure>', alt=True),
])

body = f'''<div class="pf" style="--bg: #ffffff; --surface: #f5f5f7; --card: #f5f5f7; --ink: #1d1d1f; --grey: #5f5f65; --line: #d2d2d7; --dash: #86868b; --accent: #2449e8; --on-accent: #ffffff">

<div style="--bg: #000000; --ink: #f5f5f7; --grey: #a1a1a6; --dash: #86868b; --accent: #5b8cff; --on-accent: #000000; background: #000000; color: #f5f5f7">
<div class="wrap" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px 24px; padding-top: 16px; padding-bottom: 16px; font-size: 14px">
<span style="font-weight: 600">Sam Patel</span>
<div style="display: flex; flex-wrap: wrap; gap: 4px 28px; align-items: center">
<a href="#boards" style="display: inline-flex; align-items: center; min-height: 44px; text-decoration: none">Boards</a>
<a href="#work" style="display: inline-flex; align-items: center; min-height: 44px; text-decoration: none">Projects</a>
<a href="https://www.linkedin.com/in/samarthnpatel/" style="display: inline-flex; align-items: center; min-height: 44px; text-decoration: none">LinkedIn</a>
<a href="https://github.com/samarthnpatel" style="display: inline-flex; align-items: center; min-height: 44px; text-decoration: none">GitHub</a>
</div>
</div>
<div class="sec" style="padding: 120px 0 136px">
<div class="wrap" style="display: flex; flex-direction: column; align-items: center; text-align: center; gap: 28px">
<div class="eyebrow">Available for co-op, Summer 2027</div>
<h1 style="font-size: clamp(44px, 7.4vw, 88px); line-height: 1.02; letter-spacing: -0.04em; max-width: 940px">Low-voltage electronics for a 400&nbsp;V race car.</h1>
<p class="grey" style="font-size: 21px; line-height: 1.4; max-width: 700px">Sam Patel. Hardware Engineer and Lead, Grounded Low Voltage Team, SFU Formula SAE Electric. Mechatronic Systems Engineering &amp; Business Administration, Simon Fraser University.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center">
<a href="mailto:samarth_patel@sfu.ca" class="btn" style="background: var(--accent); color: var(--on-accent)">Email me</a>
<a href="#work" class="btn" style="border: 1px solid var(--dash)">See the work</a>
</div>
</div>
</div>
</div>

<div class="sec alt" id="boards">
<div class="wrap" style="display: flex; flex-direction: column; gap: 40px">
<div class="row rv" style="align-items: flex-end">
<div class="col">
<div class="eyebrow">Team Phantom · Grounded Low Voltage</div>
<h2 class="h2">Lead of the 10+ member low-voltage team.</h2>
<p class="grey">Lead a 10+ member hardware and firmware team, assigning tasks, setting deadlines, reviewing designs and test results, and managing the budget and BOM. The team is responsible for the six systems below. Select a board for details.</p>
</div>
<figure style="flex: 1 1 360px; margin: 0; display: flex; flex-direction: column; gap: 10px">
{img('glv-enclosure.jpg','Low-voltage enclosure with the control and safety boards mounted','width: 100%; height: 560px; object-fit: cover; border-radius: 28px')}
<figcaption class="grey" style="font-size: 14px">Low-voltage enclosure. Power distribution board in red, vehicle control unit in blue, shutdown and BSPD board at bottom right.</figcaption>
</figure>
</div>
<div class="rv" style="display: flex; flex-wrap: wrap; gap: 16px">
{tiles}
</div>
</div>
</div>

{projects}

<div class="sec">
<div class="wrap" style="display: flex; flex-direction: column; gap: 32px">
<h2 class="h2 rv">More work</h2>
<div class="rv" style="display: flex; flex-wrap: wrap; gap: 16px">
<div class="tile" style="flex: 2 1 560px; min-height: 240px; background: var(--ink); color: var(--bg)"><h3 style="font-size: 32px">Lead, Grounded Low Voltage Team</h3><p style="color: var(--bg); opacity: .8">10+ member hardware and firmware team. Manage the budget and BOM. Interviewed and hired six new members in Fall 2026.</p></div>
<div class="tile"><h3>Finance Lead</h3><p>Managed approximately $20,000 in finances for the 40-member team.</p></div>
<div class="tile" style="flex: 2 1 560px; gap: 14px; justify-content: flex-start">
{FUS}
<h3>Parametric rocket fuselage</h3><p>SolidWorks assembly driven by a 23-variable equation file. SFU Rocketry.</p>
<button class="btn" data-open="fuselage">Full details</button>
</div>
<div class="tile"><h3>Dean's Honour Roll</h3><p>2026, Simon Fraser University.</p></div>
<div class="tile" style="flex: 2 1 560px; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 24px">
{img('braille-assembly.jpg','Exploded assembly drawing of the speech-to-braille device','flex: 1 1 260px; min-width: 0; max-width: 360px; width: 100%; border-radius: 12px')}
<div style="flex: 1 1 200px; display: flex; flex-direction: column; gap: 8px"><h3>Speech-to-braille converter</h3><p>Schematic and PCB layout in Altium Designer for a 2×10 braille cell array driven from an STM32.</p><button class="btn" data-open="braille" style="margin-top: 6px">Full details</button></div>
</div>
<div class="tile" style="flex: 1 1 100%; background: var(--accent); color: var(--on-accent)"><h3 style="font-size: 32px">Available for co-op, Summer 2027</h3><p style="color: var(--on-accent)"><a href="mailto:samarth_patel@sfu.ca">samarth_patel@sfu.ca</a> · <a href="https://www.linkedin.com/in/samarthnpatel/">LinkedIn</a> · <a href="https://github.com/samarthnpatel">GitHub</a></p></div>
</div>
</div>
</div>

{chr(10).join(sheets)}

</div>'''

doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sam Patel | Hardware Portfolio</title>
<meta name="description" content="Sam Patel. Hardware Engineer and Lead, Grounded Low Voltage Team, SFU Formula SAE Electric. Mechatronic Systems Engineering and Business Administration, Simon Fraser University.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://samarthnpatel.github.io/">
<meta property="og:site_name" content="Sam Patel">
<meta property="og:title" content="Sam Patel | Hardware Portfolio">
<meta property="og:description" content="Hardware Engineer and Lead, Grounded Low Voltage Team, SFU Formula SAE Electric. Mechatronic Systems Engineering and Business Administration, Simon Fraser University.">
<meta property="og:image" content="https://samarthnpatel.github.io/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Sam Patel, Hardware Portfolio. Low-voltage electronics for a 400 V race car.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://samarthnpatel.github.io/assets/og-image.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@500;600&display=swap">
<style>{css}</style>
</head>
<body>
{body}
<script>{js}</script>
</body>
</html>
'''
assert '—' not in doc and 'pretrained' not in doc.lower() and 'My part' not in doc
open(os.path.join(HERE, '..', 'index.html'), 'w').write(doc)
print(len(doc))
