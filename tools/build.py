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
.num small{font-size:.42em;letter-spacing:-.02em;white-space:nowrap}
.tile.c{justify-content:center;align-items:center;text-align:center}
.tile.c .btn{align-self:center}
.spec{width:100%;border-collapse:collapse;font-size:15px}
.spec th,.spec td{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-bottom:1px solid var(--line)}
.spec th{width:34%;font-weight:600;color:var(--ink)}
.spec td{color:var(--grey)}
.sheet .lead-c{text-align:center;align-items:center}
.tw{overflow-x:auto}
.spec.grid th{width:auto;color:var(--grey);font-size:13px;font-weight:600}
.spec.grid td{color:var(--ink);min-width:70px}
.spec.grid td:first-child{font-weight:600;white-space:nowrap}
.kpis{display:flex;flex-wrap:wrap;gap:12px}
.kpis span{flex:1 1 150px;background:var(--surface);border-radius:14px;padding:16px 18px;font-size:13px;color:var(--grey)}
.kpis b{display:block;font-family:'Inter Tight',sans-serif;font-size:24px;color:var(--ink)}
@media (max-width:600px){.sheet-in{padding:24px}.spec.grid td:first-child{white-space:normal}.kpis span{flex-basis:120px}.spec.grid{font-size:14px}}
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
        elif isinstance(items, dict):
            out.append('<div class="tw"><table class="spec grid"><thead><tr>' + ''.join(f'<th scope="col">{c}</th>' for c in items['head']) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in items['rows']) + '</tbody></table></div>')
            if items.get('note'): out.append(f'<p class="grey" style="font-size:14px">{items["note"]}</p>')
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
FUS = '''<svg class="fus" viewBox="0 0 900 240" role="img" aria-label="Side view of the five-section sample fuselage" style="width:100%;height:auto">
<g fill="var(--accent)" opacity=".22"><path d="M70 85 L230 85 L230 145 L70 145 L20 115 Z"/><rect x="230" y="85" width="150" height="60"/><rect x="680" y="85" width="150" height="60"/></g>
<g fill="none" stroke="var(--ink)" stroke-width="2">
<path d="M230 85 L70 85 L20 115 L70 145 L230 145"/>
<rect x="230" y="85" width="150" height="60"/><rect x="380" y="85" width="150" height="60"/><rect x="530" y="85" width="150" height="60"/><rect x="680" y="85" width="150" height="60"/>
<path d="M745 85 L775 40 L820 40 L830 85 Z"/><path d="M745 145 L775 190 L820 190 L830 145 Z"/>
<rect x="430" y="67" width="40" height="18"/><rect x="430" y="145" width="40" height="18"/>
</g>
<g stroke="var(--grey)" stroke-dasharray="4 4"><line x1="230" y1="78" x2="230" y2="152"/><line x1="380" y1="78" x2="380" y2="152"/><line x1="530" y1="78" x2="530" y2="152"/><line x1="680" y1="78" x2="680" y2="152"/></g>
<text x="125" y="222" text-anchor="middle">1 Nose</text><text x="305" y="222" text-anchor="middle">2 Upper body</text><text x="455" y="222" text-anchor="middle">3 Canard</text><text x="605" y="222" text-anchor="middle">4 Sensor bay</text><text x="755" y="222" text-anchor="middle">5 Fin can</text>
<text x="455" y="24" text-anchor="middle">Coupler sleeves at each joint</text>
</svg>'''

TP = 'Team Phantom · Grounded Low Voltage'
sheets = [
sheet('lead', TP, 'Lead, Grounded Low Voltage Team',
 'Lead the 10+ member hardware and firmware team responsible for the car\'s low-voltage electronics: vehicle control, data acquisition, power distribution, the shutdown circuit and BSPD, and the carrier board and wiring harness.',
 [('KPI', [('10+','members, hardware and firmware'),('6','new members hired, Fall 2026'),('215','2027 rules in GLV scope')]),
  ('What the role covers', ['Assign tasks, set deadlines, and review designs and test results across the five GLV projects.',
   'Manage the GLV budget and BOM.',
   'Run a weekly update tracker with one tab per project: VCU, DAQ and dash, PDB, shutdown board and BSPD, and wiring harness and carrier board.',
   'Sign off board status reports as lead. A board counts as working only after every test passes on two to three separate runs, with photo or video evidence.',
   'Onboard new members into the team Altium workspace and assign each one a first task.']),
  ('Hiring, Fall 2026', ['Used fresher projects as the entry test: a 12 V brushed DC motor controller PCB, and a diagnostic task on the shutdown board schematic that includes the overvolted logic IC.',
   'Scored 15 hardware submissions blind on a 25-point rubric (PCB 10, diagnostic 10, report 5) against a verified answer key.',
   'Interviewed hardware candidates and hired six new members: five hardware and one firmware.',
   'Onboarded the new members in November 2026 and assigned their first projects.']),
  ('2027 rules compliance', ['Built a compliance register from the Formula SAE 2027 rules (version 1.0): all 1,825 rules logged word for word, 215 in GLV scope, each allocated to the board responsible for it.',
   'Rules per system: shutdown board 80, carrier board and harness 78, VCU 67, PDB 32, DAQ and dash 31, BSPD 7, and 40 that apply to all GLV boards.',
   'Audited the BSPD, PDB, VCU and carrier board against the register.'])],
 [('glv-enclosure.jpg','Low-voltage enclosure with the PDB, VCU, DAQ and shutdown board')]),
sheet('vcu', TP, 'Vehicle Control Unit',
 'Main controller for the car. A TI TMS570LS1227 on a ten-sheet Altium design (PHANTOM_VCU_rev4). It reads the pedal and dash inputs, talks to the BMS and the rest of the car over CAN and UART, and drives the ready-to-drive buzzer, brake light and precharge through low-side switches.',
 [('My work', ['Leading the firmware migration from the TMS570 to an STM32H755, prototyping on a NUCLEO-H755ZI-Q evaluation board ordered in October 2026.',
   'Assigning tasks and reviewing designs for the hardware and firmware members working on the board.',
   'On the carrier board in Fall 2025, added the VCU connectors and footprints and completed the VCU X2 internal and external connections.']),
  ('Hardware on the schematic', [('Microcontroller','TI TMS570LS1227'),
   ('Power','12 V input with a PSMN022 reverse-polarity FET. AP65550 buck converters step 12 V to 5 V and 5 V to 3.3 V. TPS2115A power multiplexer.'),
   ('Monitoring','INA226 current monitor, STWD100 watchdog, TMP36 temperature sensor'),
   ('Communication','MCP2562 CAN transceiver, FT230X USB to UART, BMS UART'),
   ('Inputs','Two accelerator pedal position sensors and the brake sensor, BSPD and IMD fault inputs'),
   ('Outputs','Low-side switches K1 ready-to-drive buzzer, K2 brake light, K3 precharge. MCP48FVB01 DAC.'),
   ('Connectors','Two 20-pin headers, X1 and X2, to the carrier board')]),
],
 [('vcu-3d.jpg','VCU, Altium 3D view'),('vcu-schematic.jpg','VCU schematic, microcontroller signals sheet'),('vcu-power.jpg','VCU schematic, power and current sensing sheet'),('vcu-contactor.jpg','VCU schematic, low-side switching sheet'),('vcu-can.jpg','VCU schematic, CAN sheet')]),
sheet('daq', TP, 'Data Acquisition',
 'Reads the car\'s sensors, sends the data over CAN to the VCU and dashboard, logs it to an SD card and sends telemetry over a UART radio. It also detects a cooling fault and reports it to the VCU. The current build is an ESP32 with an ADS1115 16-bit ADC on perfboard.',
 [('My work', ['Leading the PCB design that replaces the perfboard build.',
   'Responsible for sensor implementation on the redesign.',
   'Proposed the redesign at the September 2026 leads meeting: the analog runs from the sensors are long enough that the data degrades before it reaches the ADC, so the fix is small modules next to the sensors that send their data over CAN. The DAQ was added to the next-car project list.']),
  ('Sensors', [('Wheel speed','4'),('Coolant pressure','2, Sensata 116CP31-M04S2-50'),('Coolant temperature','2, Amphenol CTTS-302651-F01 (10 kΩ NTC)'),('IMU','1'),('Output','CAN to the VCU and dashboard')]),
  ('Current hardware', [('Controller','ESP32 with an integrated CAN controller'),('ADC','ADS1115, 16-bit, I2C'),('CAN transceiver','MCP2562'),('Storage','microSD card'),('Telemetry','UART radio')])],
 [('daq-perfboard.jpg','Current DAQ perfboard build'),('daq-perfboard-2.jpg','DAQ perfboard, side view')]),
sheet('pdb', TP, 'Power Distribution Board',
 'Takes the 13.2 V supply from the high-voltage side and distributes protected 13.2 V and a regulated 5 V rail to the low-voltage boards.',
 [('My work', ['Debugged and tested the board.']),
  ('Circuit', [('Input','13.2 V from the HV board DC-DC converter (12 V nominal)'),
   ('Protection','LT4363 over- and under-voltage stage with a series MOSFET. Cutoffs at 17.22 V and 9.535 V.'),
   ('Current monitoring','INA226 with I2C output across a 0.002 Ω shunt, rated for about 20 to 22 A continuous'),
   ('5 V rail','LM3489 buck converter with a 10 µH inductor, 4.85 to 5.15 V window'),
   ('Outputs','Two 20-pin headers, X1 and X2')]),
  ('Bench test, October 2026', ['X1 measured 13.20 V and X2 measured 5.02 V.',
   'Status LEDs correct and no shorts.',
   'I2C current-monitor lines still to be tested.']),
],
 [('pdb-3d.jpg','PDB, Altium 3D view'),('pdb-protection.jpg','PDB schematic, protection sheet'),('pdb-supply.jpg','PDB schematic, current monitor and 12 V to 5 V buck sheet'),('pdb-bench-13v.jpg','Bench test, 13.20 V at X1'),('pdb-bench-5v.jpg','Bench test, 5.02 V at X2')]),
sheet('lvsdb', TP, 'Low-Voltage Shutdown Board and BSPD',
 'One PCB with two safety systems: the low-voltage shutdown circuit, driven from the VCU fault line, and the brake system plausibility device (BSPD), which opens the shutdown circuit under hard braking at high current. A 5 V and 12 V design with 5 V active-low fault lines and two RTE44012F relays.',
 [('KPI', [('5','design faults found'),('8 × 3','bring-up tests passed'),('349 Ω','relay coil, 324 to 396 Ω rated'),('NC7WZ32','5 V-rated logic IC in the design')]),
  ('My work', ['Performed bring-up and troubleshooting on both safety systems and soldered the replacement board.',
   'Identified five design faults through a schematic and datasheet review, listed below, and replaced the overvolted logic IC in the design with the 5 V-rated NC7WZ32.',
   'Tested both relays in circuit and isolated, and confirmed coil resistance against the datasheet: 349 Ω against a 360 Ω ±10% rating.',
   'October 2026 bring-up: traced a relay that would not latch to an open MOSFET (Q1) by driving each gate with 5 V and checking drain-source continuity, then replaced it. Both channels then latched.',
   'Ran 8 fault and reset tests three times each, all passing: the relay opens on a fault, stays open until SET/RESET, and both relays drop when 5 V is removed.',
   'Ordered the BSPD rebuild parts, including the NC7WZ32 logic IC and the correct 15 µF timing capacitor.']),
  ('Five faults from the schematic and datasheet review', ['U3 (NC7WP32 dual OR gate) sits on the 5 V rail. It is rated for 0.9 to 3.6 V with a 4.6 V absolute maximum.',
   'Q7 (BSS138) is wired drain to source swapped. The symbol uses standard pin numbering, but the shared SOT-23-3 footprint numbers its pads differently. Found by checking the PCB footprint against the schematic symbol.',
   'The Q1 and Q2 gates tie straight to the relay coil low-side node with no series resistor or clamp, so flyback reaches the gate.',
   'BSPD_OUT drives the Q5 gate directly and is also exposed on connector M2 pin 1.',
   'The sensor inputs go straight into the MAX989 comparators with no series protection.']),
  ('History', ['March 2026: the first build failed. Diodes D1 to D4 were fitted reversed and C12 was 20 µF instead of 15 µF. The team built a new board.',
   'July 2026: rebuilt board working on the VCU side. Every BSPD IC was checked against its datasheet, and U3 was found over its rating.',
   'October 2026: shutdown circuit brought up and passed all tests. The BSPD circuit traces were damaged during integration.',
   'November 2026: new BSPD board being soldered.']),
  ('Status', 'Shutdown circuit working. New BSPD board being soldered.')],
 [('lvsdb-3d.jpg','LVSDB, Altium 3D view'),('lvsdb-schematic.jpg','Shutdown circuit schematic'),('bspd-schematic.jpg','BSPD schematic')]),
sheet('carrier', TP, 'Carrier Board and Wiring Harness',
 'One board inside the low-voltage enclosure that the VCU, PDB, shutdown board and DAQ plug into. It connects them to each other and to sealed Samtec connectors on the enclosure, which cuts the external wiring. Consolidates 9 PCBs and 20+ vehicle signals on a 400 V race car.',
 [('KPI', [('9 → 1','PCBs consolidated'),('20+','vehicle signals'),('150+','pins documented'),('84','harness connector positions')]),
  ('My work', ['Designed the carrier board in Altium Designer: created the project, imported every board connector, and connected all the boards in the enclosure on the schematic.',
   'Documented the full low-voltage wiring interface (150+ pins) from harness drawings and board schematics, now the team\'s reference for harness integration and debugging.',
   'Selected sealed Samtec connectors for the enclosure: IPL1 board headers (two 30-pin, one 20-pin) that mate with the harness\'s ACPK-22 plugs.',
   'Designed the back and left harness port (internal to external pin assignment) and completed the VCU X2 internal and external connections.',
   'Mapped connections for the BMS, fault relay, inverter control board, VCU, PDB and shutdown board, and flagged mislabelled and miswired pins in the team\'s connection spreadsheet.',
   'Built low-voltage wire harnesses and verified continuity and signal integrity with oscilloscopes and multimeters, including pin-by-pin checks of 30-pin connectors.',
   'Integrated the Samtec connectors and fit the PCBs into the enclosure.']),
  ('External harness ports', {'head': ['Port','Pins','Signals'], 'rows': [
   ['Front','30','Accelerator pedal and brake sensors, dashboard CAN and power, ready-to-drive switch and buzzer, set/reset, BOTS, front wheel speed'],
   ['Back and left','30','Inverter CAN, rear wheel speed, coolant pressure and temperature, TSAL enable, HV current transducer, brake light, inverter 12 V'],
   ['Right','20','Shutdown circuit out, BMS CAN and power, IMD PWM, HV sensing SPI, HV board I2C, TSAL supply, set/reset'],
   ['E-stop and HVCC','4','GLV master switch loop, HVCC 12 V and ground']]}),
  ('Connections on the schematic', ['Power from the PDB: 5 V to the accelerator pedal sensors, dashboard, pedal box, DAQ and HV current transducer; 12 V to the BMS, inverter, TSAL, dashboard and HV board.',
   'Faults and safety: BMS fault, IMD fault, BSPD fault, VCU fault, shutdown circuit in and out, set/reset and TSAL enable.',
   'Driver controls: two accelerator pedal position signals, brake signal, ready-to-drive switch and buzzer, and brake light.',
   'Communication: CAN high and low to the dashboard and DAQ, and SPI.',
   'Sensors: four wheel speed, two coolant pressure, two coolant temperature and an IMU.',
   'Connectors: two 30-pin and one 20-pin Samtec, plus headers for the VCU, PDB, shutdown board and DAQ.']),
  ('Status', 'Schematic complete. PCB layout and build planned for the next vehicle.')],
 [('carrier-board-schematic.jpg','Carrier board schematic'),('carrier-board-3d.jpg','Carrier board, Altium 3D view'),('glv-enclosure.jpg','Low-voltage enclosure with the current boards')]),
sheet('motor', 'Technical project', 'Three-Phase Linear Induction Motor',
 'A small linear induction motor that uses three-phase AC to produce a travelling magnetic field and accelerate a magnetically suspended cart. PHYS 141 team project, January to April 2026.',
 [('KPI', [('±120°','phase shifts from one generator'),('78 mA','coil current, RLC stage alone'),('2.15 m/s²','predicted'),('2 to 3 m/s²','measured')]),
  ('My work', ['Designed and soldered the motor\'s three-phase power stage on perfboard, deriving the RLC component values from the transfer function to produce ±120° phase shifts at matched amplitude from a single function generator.',
   'Measured 2 to 3 m/s² cart acceleration against a 2.15 m/s² prediction after tracing low coil current (78 mA) and switching to synchronized generators with a 300 W amplifier.']),
  ('Design method', 'Each network is a series RLC with transfer function D = (1 − ω²LC) + jωRC. Setting the ratio of the imaginary and real parts of D to tan 60° = √3 and solving for L gives the 120° shift. R₂ was set to 65 Ω so both outputs match at about 0.92 of the input amplitude.'),
  ('Circuit values', {'head': ['Network','R','C','L','Output','Phase','Amplitude'], 'rows': [
   ['1 (phase C)','100 Ω','10 µF','174 mH','across C','−120°','0.919'],
   ['2 (phase B)','65 Ω','10 µF','73 mH','across L','+120°','0.914']],
   'note': 'Inductors hand-wound on iron cores. Drive frequency 150 Hz.'}),
  ('Iterations', ['RLC networks alone: outputs noisy and unbalanced, 78 mA through a coil, no motion.',
   'Audio amplifier added: the coils vibrated, but the supply could not drive them.',
   'Three function generators phase-synced on one oscilloscope, with a 300 W supply on the amplifier: the cart accelerated.']),
  ('Result', 'One run with measured acceleration between 2 and 3 m/s², against a 2.15 m/s² prediction for the as-built 175-turn coils. The coils and aluminium bar heated from induced eddy currents, and the enamel burned off the coils after the run.')],
 [('induction-motor-bench.jpg','Track, power supplies and amplifier on the bench'),('lim-generators.jpg','Three function generators synced at 150 Hz'),('lim-rlc-amp.jpg','Perfboard RLC stage with the amplifier'),('lim-multimeter.jpg','77.7 mA through a coil with the RLC stage alone'),('lim-coils.jpg','Coils under the track'),('lim-bench-scope.jpg','Oscilloscope and breadboard during testing')]),
sheet('robot', 'Technical project', 'Vision-Guided Sorting Robot',
 'A Raspberry Pi 4 robot (Hiwonder MasterPi: mecanum chassis, 5-DOF arm, camera) that detects printed cat and dog markers with a YOLOX neural network and sorts the target to one side. MSE 112, Summer 2026.',
 [('KPI', [('7.52 FPS','YOLOX-Nano on the Pi'),('3','model sizes compared'),('4.44 V','battery sag found under load'),('4 of 4','correct runs at the end')]),
  ('My work', ['Deployed a YOLOX object detector (C++, ncnn) on a Raspberry Pi and connected it to the robot\'s Python arm controller through a named pipe.',
   'Fixed camera buffering, pipe communication, and detection-threshold bugs to run detection at full frame rate.',
   'Added runtime model selection across three YOLOX model sizes with frame-rate measurement.',
   'Built ncnn from source on the Pi after the supplied detector binary failed against the installed OpenCV version.',
   'Traced servo failures to the battery sagging to 4.44 V when several servos moved at once, and sequenced servo moves one at a time to stay within the supply\'s limit.',
   'Replaced inverse kinematics with fixed pose tables after the IK pick drove a servo to 2495 of its 2500 travel limit.']),
  ('Architecture', 'Two processes. A C++ YOLOX detector (ncnn, GStreamer camera capture) writes one word per frame, cat, dog or none, to a named pipe. A Python arm controller reads the pipe and runs pick, look left, look right and place. The Python side never touches the neural network.'),
  ('Model comparison on the robot', {'head': ['Model','Input','ms per frame','FPS','COCO mAP'], 'rows': [
   ['Nano','416','133.0','7.52','25.8'],['Tiny','416','293.9','3.40','32.8'],['Small','640','999.0','1.00','40.5']],
   'note': 'Nano chosen: 7.5× faster than Small and 2.2× faster than Tiny.'}),
  ('Bugs fixed', ['Camera buffering: the capture queue fed old frames. Limited the appsink to the newest frame (max-buffers=1, drop=true).',
   'Pipe communication: the pipe was reopened every frame, so the detector blocked and ran only a few frames per sweep. Holding it open for the whole run brought detection to full frame rate.',
   'Detection threshold: a flat 0.50 confidence cut discarded every dog marker, which peaked near 38%. Replaced it with a best-of-class decision over a 0.25 floor.',
   'Camera focus: measured sharpness at six arm poses and refocused the lens, raising the focus score from 22 to 29 to between 265 and 1041.']),
  ('Earlier project on the same robot', 'Line tracking with PID on the line centroid (P 0.28, I 0.16, D 0.18), sonar obstacle detection with a median filter, and a strafe-around avoidance manoeuvre driven wheel by wheel. The clip is that run.')],
 [('robot-run.mp4','The robot on a line-tracking and obstacle-avoidance run'),('robot-avoid.jpg','Strafing around the obstacle')]),
sheet('braille', 'Technical project', 'Speech-to-Braille Converter',
 'A handheld device that turns speech into braille on a 20-cell (2×10) refreshable display, designed for under $80 against $2,000 to $6,000 commercial displays. MSE 102 team project, January to April 2026.',
 [('My work', ['Developed the schematic and PCB layout in Altium Designer for an assistive device driving a 2×10 braille cell array from an STM32 microcontroller through a UDN2981A/ULN2803A driver stage.',
   'Designed the PCB to drive 120 solenoid pins across the 20 braille cells.',
   'Modified the open-source braille cell modules with a teammate.',
   'Presented the design concept and component selection at the final review.']),
  ('PCB parts', [('Microcontroller','STM32F103C8T6'),('Source drivers','2 × UDN2981A'),('Sink drivers','2 × ULN2803A'),('Diodes','4 × BAV99'),('Microphone','INMP441 I2S'),('Board','2-layer FR-4, off-the-shelf SMD parts')]),
  ('Device', [('Size','150 × 83 × 25 mm'),('Display','2 × 10 braille cells'),('Controls','Power, forward and back, reset, record'),('Power','AA batteries'),('Bill of materials','$77')]),
  ('Status', 'Design complete. No physical prototype.')],
 [('braille-assembly.jpg','Exploded assembly (team CAD)'),('braille-sketch.jpg','Case layout sketch'),('braille-top-case.jpg','Top case drawing'),('braille-bottom-case.jpg','Bottom case drawing')]),
sheet('fuselage', 'SFU Rocketry · Active Fin Stabilization', 'Parametric Rocket Fuselage',
 'A sample fuselage assembly in SolidWorks for SFU Rocketry\'s active fin stabilization group, laid out to carry the canard module. It proves a design method that scales to the team\'s 18-inch, 200 kg sounding rocket. CAD only.',
 [('KPI', [('23','driving variables'),('7','parametric parts'),('5 × 200 mm','body sections'),('131.62 mm','outer diameter')]),
  ('My work', ['Built a 7-part parametric SolidWorks assembly (nose, nose cap, upper body, coupler, fin can, fins and hardware) driven by a 23-variable equation file, so one edit rescales the airframe.',
   'Modelled the two ends of the airframe: section 1 nose, section 2 upper body and section 5 fin can, plus the couplers, fins and cap.',
   'Ran flex tests at build gates. One caught a dimensioning bug before it reached the assembly.',
   'Placed the fixed fins at the tail after checking the layout against the Leeds Pathfinder reference rocket.',
   'Wrote the fuselage design brief for the vehicle: section layout, mass budget, nose cone profile, fin options and stability margins.',
   'Modelled the canard control module packaging: four bushings with ±15° hard stops, the flight computer mount and the servo wiring.',
   'Selected the FeeTech STS3215 servo, which has a built-in 12-bit encoder and removes the need for external encoders.']),
  ('Design basis', [('Length','About 1000 mm'),('Sections','5 × 200 mm'),('Diameter','131.62 mm outer, 3 mm wall'),('Joints','Coupler sleeves, four M3 radial bolts per side, 50 mm engagement per side'),('Fins','4 trapezoidal, 90° cruciform, through-wall 3.2 mm slots for 3 mm fins')])],
 [('SVG','Sample fuselage, five sections. Shaded sections are the ones I modelled.'),('rocket-layout.jpg','Vehicle layout from the conceptual design')]),
sheet('finance', 'Team Phantom · Business', 'Finance Lead',
 'Ran the finances for the 40-member team from May 2026: the bank and student-society trust accounts, reimbursements, receipts and grant funding. Over $20,000 moved through the team\'s accounts in 2026.',
 [('KPI', [('$20,000+','through team accounts in 2026'),('70','bank transactions booked'),('$3,820','reimbursement backlog cleared'),('21 of 32','card purchases matched to receipts')]),
  ('My work', ['Built the team\'s finance tools: completed the double-entry general ledger with running balances for the bank and trust accounts, added a merchandise expense account, and set up the card receipt and bank reconciliation workbooks.',
   'Booked all 70 bank transactions for January to July 2026 as double entries. The ledger ties to the bank and trust balances to the cent, and the trial balance foots at $28,992.44.',
   'Linked 29 receipt files across 23 transactions.',
   'Consolidated a $3,820 reimbursement backlog from two trackers and cleared it with batched payouts in August 2026.',
   'Matched every card purchase against the submitted receipts: read 24 receipt files and matched 21 of 32 purchases to the cent. The rest are subscriptions, refunds and six purchases with missing receipts.',
   'Reconciled the student-society trust account from $2,024.64 to $501.45 and traced the difference to an unrecorded $1,523.19 drawdown.',
   'Traced a grant deposit that had been applied to a member\'s tuition account and drafted its withdrawal.']),
  ('Chart of accounts', {'head': ['Type','Accounts'], 'rows': [
   ['Assets','1000 Cash, Scotiabank · 1010 Cash, SFSS Trust · 1020 SFSS Resource · 1030 SFSS Petty Cash · 1100 Grant Receivable · 1110 Sponsorship Receivable'],
   ['Liabilities','2000 Reimbursements Payable · 2100 Accounts Payable'],
   ['Equity','3000 Opening Balance Equity'],
   ['Revenue','4000 Grant Revenue · 4100 Sponsorship · 4200 Ticket Sales · 4300 Fundraising · 4400 Clothing'],
   ['Expenses','5000 Engineering · 5010 Engineering Equipment · 5100 Manufacturing · 5150 Merchandise · 5200 External Events · 5300 to 5340 Internal Events (AV and venue, food, gifts, merch, other) · 5400 Marketing · 5500 Operations · 5600 Travel · 5700 Miscellaneous']],
   'note': '28 accounts.'}),
  ('Ledger structure', 'Each entry has a debit line and a credit line with entry ID, date, account code and name, debit, credit, funding source, counterparty, description, subteam, reference, receipt link and notes, plus running balances for the bank and trust accounts. Funding sources: SFSS grant, SFSS petty cash, sponsorship, fundraising, ticket sales, FAS, ESSEF and unrestricted.'),
  ('Sample entries', {'head': ['Entry','Date','Account','Debit','Credit','Description'], 'rows': [
   ['JE-2026-101','2026-09-03','1000 Cash, Scotiabank','$4,500.00','','SFU funding (FAS)'],
   ['JE-2026-101','2026-09-03','4000 Grant Revenue','','$4,500.00','SFU funding (FAS)'],
   ['JE-2026-110','2026-10-22','5010 Engineering Equipment','$178.33','','DigiKey, LVSDB and BSPD parts'],
   ['JE-2026-110','2026-10-22','1000 Cash, Scotiabank','','$178.33','DigiKey, LVSDB and BSPD parts']],
   'note': 'Member names, account numbers and receipt links removed.'}),
  ('Card receipt reconciliation, January to July 2026', {'head': ['Result','Purchases','Amount'], 'rows': [
   ['All card purchases','32','$5,662.50'],['Matched to a receipt','21','$3,835.03'],['Subscriptions','3','$261.51'],['Refunded','2','$1,418.27'],['Receipt missing','6','$147.69']]})],
 []),
sheet('honour', 'Simon Fraser University', 'Dean\'s Honour Roll, Summer 2026',
 'Awarded for the Summer 2026 term and recorded on my SFU academic record.',
 [('KPI', [('3.87','term GPA, 4.33 scale'),('15','units that term'),('3.50','minimum term GPA')]),
  ('Criteria', 'SFU admits students to the Dean\'s Honour Roll with a term GPA of 3.50 or higher, at least 30 units completed at SFU, and at least 12 graded units in the term.'),
  ('Program', 'Double degree in Mechatronic Systems Engineering and Business Administration, Simon Fraser University. Expected June 2030.')],
 []),
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
 tile('carrier','Carrier Board and Wiring Harness','Designed the schematic in Altium Designer. 150+ pin interface documented.', img('carrier-board-schematic.jpg','Carrier board schematic',TI.format('left top'))),
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
  [('20+','vehicle signals',''),('150+','pins documented',''),('400 V','vehicle','')],
  f'<div class="ph stage" style="flex-direction: column; gap: 28px; border: none; padding: 28px">{nine}{RENDER}</div>', scene=True),
 project('02','lvsdb','Shutdown circuit and BSPD · Team Phantom','<span data-count="5">5</span> faults','Bring-up and troubleshooting on two safety systems.',
  ['Performed bring-up and troubleshooting on two safety systems, the low-voltage shutdown circuit and the brake system plausibility device, soldered the replacement board, identified five design faults through a schematic and datasheet review, and replaced the overvolted logic IC.',
   'Built low-voltage wire harnesses and verified continuity and signal integrity with oscilloscopes and multimeters, including pin-by-pin checks of 30-pin connectors.'],
  [('5','design faults',' data-count="5"'),('3.6 V','part on a 5 V rail',''),('8 × 3','bring-up tests passed','')],
  f'<figure style="{FIG}">{img("bspd-schematic.jpg","BSPD schematic","width: 100%; border-radius: 20px; border: 1px solid var(--line)")}<figcaption class="grey" style="font-size: 14px">BSPD schematic.</figcaption></figure>', alt=True),
 project('03','motor','Three-phase linear induction motor','<span data-count="2.15">2.15</span><small> m/s²</small>','Predicted cart acceleration. Measured 2 to 3 m/s².',
  ['Designed and soldered the motor\'s three-phase power stage on perfboard, deriving the RLC component values from the transfer function to produce ±120° phase shifts at matched amplitude from a single function generator.',
   'Measured 2 to 3 m/s² cart acceleration against a 2.15 m/s² prediction after tracing low coil current (78 mA) and switching to synchronized generators with a 300 W amplifier.'],
  [('±120°','phase shifts',''),('150 Hz','operating frequency',''),('300 W','amplifier','')],
  img('induction-motor-bench.jpg','Linear induction motor track on the lab bench with oscilloscope, power supplies and amplifier board','flex: 1 1 400px; min-width: 0; width: 100%; max-width: 560px; height: 420px; object-fit: cover; object-position: 60% 60%; border-radius: 28px')),
 project('04','robot','Vision-guided sorting robot','<span data-count="3">3</span><small> bugs fixed</small>','YOLOX object detection on a Raspberry Pi robot arm.',
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
<div class="eyebrow">Available for co-op from May 2027</div>
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
<div class="row rv" style="align-items: center">
<div class="col">
<div class="eyebrow">Team Phantom · Grounded Low Voltage</div>
<h2 class="h2">Lead of the 10+ member low-voltage team.</h2>
<p class="grey">Lead a 10+ member hardware and firmware team, assigning tasks, setting deadlines, reviewing designs and test results, and managing the budget and BOM. The team is responsible for the six systems below. Select a board for details.</p>
<button class="btn" data-open="lead">Role details</button>
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
<div class="tile c" style="flex: 2 1 560px; min-height: 260px; background: var(--ink); color: var(--bg)"><h3 style="font-size: 32px">Lead, Grounded Low Voltage Team</h3><p style="color: var(--bg); opacity: .8; max-width: 520px">10+ member hardware and firmware team. Manage the budget and BOM. Interviewed and hired six new members in Fall 2026.</p><button class="btn" data-open="lead" style="border-color: var(--grey); margin-top: 8px">Full details</button></div>
<div class="tile c" style="min-height: 260px"><h3>Finance Lead</h3><p>Ran the finances for the 40-member team. Over $20,000 through the team's accounts in 2026.</p><button class="btn" data-open="finance" style="margin-top: 8px">Full details</button></div>
<div class="tile c" style="flex: 2 1 560px; gap: 14px">
{FUS}
<h3>Parametric rocket fuselage</h3><p>SolidWorks assembly driven by a 23-variable equation file. SFU Rocketry.</p>
<button class="btn" data-open="fuselage" style="margin-top: 4px">Full details</button>
</div>
<div class="tile c"><h3>Dean's Honour Roll</h3><p>Summer 2026, Simon Fraser University. Term GPA 3.87.</p><button class="btn" data-open="honour" style="margin-top: 8px">Full details</button></div>
<div class="tile" style="flex: 2 1 560px; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 24px">
{img('braille-assembly.jpg','Exploded assembly drawing of the speech-to-braille device','flex: 1 1 260px; min-width: 0; max-width: 360px; width: 100%; border-radius: 12px')}
<div style="flex: 1 1 200px; display: flex; flex-direction: column; gap: 8px"><h3>Speech-to-braille converter</h3><p>Schematic and PCB layout in Altium Designer for a 2×10 braille cell array driven from an STM32.</p><button class="btn" data-open="braille" style="margin-top: 6px">Full details</button></div>
</div>
<div class="tile c" style="flex: 1 1 100%; min-height: 220px; background: var(--accent); color: var(--on-accent)"><h3 style="font-size: 32px">Available for co-op from May 2027</h3><p style="color: var(--on-accent)"><a href="mailto:samarth_patel@sfu.ca">samarth_patel@sfu.ca</a> · <a href="https://www.linkedin.com/in/samarthnpatel/">LinkedIn</a> · <a href="https://github.com/samarthnpatel">GitHub</a></p></div>
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
