"""Subpage illustrations for the Good to Grow kit. All decorative (aria-hidden), brand colours only."""
import pathlib, shutil, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import gen_svgs as g
SL, DP, RJ, CN, CH, WM = g.SL, g.DP, g.RJ, g.CN, g.CH, g.WM
OUT = pathlib.Path(__file__).resolve().parents[2] / 'kit-src' / 'svg'; OUT.mkdir(parents=True, exist_ok=True)
A = 'aria-hidden="true" focusable="false"'

def wrap(vb, body, cls='art'):
    return f'<svg class="{cls}" viewBox="{vb}" {A}>{body}</svg>'

# ---- About: seed packet with a plant growing out of it ----
def seed_packet():
    b = [f'<circle cx="230" cy="190" r="150" fill="{WM}"/>',
         f'<circle cx="230" cy="190" r="172" fill="none" stroke="{RJ}" stroke-width="2.5" stroke-dasharray="2 12" stroke-linecap="round"/>',
         # packet back + front
         f'<g transform="rotate(-6 230 300)">',
         f'<rect x="140" y="170" width="190" height="250" rx="10" fill="{SL}" stroke="{DP}" stroke-width="3"/>',
         f'<path d="M140 200h190" stroke="{DP}" stroke-width="3"/>',
         f'<path d="M150 182h170" stroke="{WM}" stroke-width="2" stroke-dasharray="6 6" opacity=".6"/>',
         f'<rect x="162" y="222" width="146" height="120" rx="8" fill="{CH}" stroke="{DP}" stroke-width="3"/>',
         f'<circle cx="235" cy="300" r="34" fill="{RJ}"/>',
         f'<path d="M235 330c-2-22 4-40 0-58" fill="none" stroke="{DP}" stroke-width="5" stroke-linecap="round"/>',
         g.leaf(236, 300, -30, .45, SL, DP), g.leaf(234, 288, 210, .45, WM, CH),
         f'<rect x="162" y="356" width="100" height="10" rx="5" fill="{CH}" opacity=".85"/>',
         f'<rect x="162" y="376" width="140" height="10" rx="5" fill="{CH}" opacity=".5"/>',
         f'<rect x="162" y="396" width="80" height="10" rx="5" fill="{CH}" opacity=".5"/>',
         '</g>',
         # seeds spilling
         *[f'<ellipse cx="{x}" cy="{y}" rx="7" ry="5" transform="rotate({r} {x} {y})" fill="{RJ}" stroke="{DP}" stroke-width="2"/>'
           for x, y, r in [(352, 418, 20), (372, 432, -30), (338, 440, 60), (392, 446, 10)]],
         # sprout bursting from the packet top
         f'<path d="M232 176C226 140 240 110 234 70" fill="none" stroke="{DP}" stroke-width="10" stroke-linecap="round"/>',
         f'<path d="M232 176C226 140 240 110 234 70" fill="none" stroke="{SL}" stroke-width="4" stroke-linecap="round"/>',
         g.leaf(234, 140, -30, .95, RJ, CH), g.leaf(232, 118, 206, .95, SL, DP), g.leaf(235, 76, -62, .8, WM, CH), g.leaf(235, 76, 242, .8, SL, DP),
         f'<g stroke="{RJ}" stroke-width="3" stroke-linecap="round"><path d="M290 64l12-12M298 92h16M270 40l-2-14"/></g>',
         f'<path d="M60 470H420" stroke="{DP}" stroke-width="3"/>']
    return wrap('0 0 460 480', ''.join(b))

# ---- Partner: clipboard with checklist + pencil ----
def clipboard():
    rows = ''.join(f'<rect x="140" y="{y}" width="26" height="26" rx="5" fill="{WM}" stroke="{DP}" stroke-width="2.5"/>'
                   f'<rect x="182" y="{y+8}" width="{w}" height="10" rx="5" fill="{SL}" opacity=".35"/>'
                   for y, w in [(200, 150), (256, 120), (312, 160), (368, 110)])
    ticks = ''.join(f'<path d="M{144} {y+13}l7 7 14-18" fill="none" stroke="{CN}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' for y in (200, 256, 312))
    b = [f'<circle cx="230" cy="230" r="170" fill="{WM}"/>',
         f'<g transform="rotate(4 230 260)">',
         f'<rect x="96" y="96" width="268" height="350" rx="18" fill="{SL}" stroke="{DP}" stroke-width="3"/>',
         f'<rect x="116" y="130" width="228" height="300" rx="6" fill="{WM}" stroke="{DP}" stroke-width="2.5"/>',
         f'<rect x="182" y="80" width="96" height="40" rx="10" fill="{DP}"/><rect x="206" y="68" width="48" height="24" rx="12" fill="none" stroke="{DP}" stroke-width="6"/>',
         f'<rect x="140" y="152" width="120" height="14" rx="7" fill="{RJ}"/>',
         rows, ticks, '</g>',
         '<g transform="translate(300 420) rotate(-52)">'
         f'<path d="M0 0l24-9v18z" fill="{CH}" stroke="{DP}" stroke-width="2.5" stroke-linejoin="round"/><path d="M0 0l8-3v6z" fill="{DP}"/>'
         f'<rect x="24" y="-9" width="120" height="18" fill="{RJ}" stroke="{DP}" stroke-width="2.5"/>'
         f'<rect x="144" y="-9" width="14" height="18" fill="{CH}" stroke="{DP}" stroke-width="2.5"/>'
         f'<rect x="158" y="-9" width="16" height="18" rx="5" fill="{CN}" stroke="{DP}" stroke-width="2.5"/></g>',
         f'<g stroke="{RJ}" stroke-width="3" stroke-linecap="round"><path d="M390 120l14-10M396 150h18M60 300h-16M66 330l-12 8"/></g>']
    return wrap('0 0 460 480', ''.join(b))

# ---- Join: chalk-style badge with sprout (for dark intro) ----
def chalk_badge():
    b = ['<defs><filter id="chalk2" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="7" result="n"/>'
         '<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter></defs>',
         f'<g filter="url(#chalk2)" fill="none" stroke="{CH}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">',
         '<path pathLength="1" d="M190 20v70"/><path pathLength="1" d="M150 20l40 70 40-70"/>',
         '<rect pathLength="1" x="100" y="90" width="180" height="250" rx="18"/>',
         '<rect pathLength="1" x="166" y="104" width="48" height="12" rx="6"/>',
         '<circle pathLength="1" cx="190" cy="190" r="46"/>',
         '<path pathLength="1" d="M190 226c-2-20 4-36 0-56"/>',
         *[f'<path pathLength="1" transform="translate({x} {y}) rotate({r}) scale(.42)" d="{g.LEAF}" stroke-width="9.5"/>' for x, y, r in [(191, 206, -30), (190, 194, 206), (190, 174, -60), (190, 174, 240)]],
         '<path pathLength="1" d="M130 270h120M130 296h90M130 318h60"/>',
         f'<path pathLength="1" d="M300 120l18-12M306 150h22M40 230h-18M48 256l-14 10" stroke="{RJ}"/>',
         f'<path pathLength="1" d="M248 300l8 10 18-22" stroke="{RJ}" stroke-width="5"/>',
         '</g>']
    return wrap('0 0 380 360', ''.join(b), cls='art chalkart')

# ---- Contact: paper airplane with dashed flight path ----
def airplane():
    b = [f'<circle cx="250" cy="220" r="160" fill="{WM}"/>',
         f'<path d="M40 380C110 380 120 300 180 300s60 70 120 40 40-130 110-160" fill="none" stroke="{CN}" stroke-width="3.5" stroke-dasharray="3 12" stroke-linecap="round"/>',
         f'<g transform="translate(300 90) rotate(-14)" stroke="{DP}" stroke-width="3" stroke-linejoin="round">'
         f'<path d="M0 60L150 0 70 120z" fill="{WM}"/><path d="M150 0L56 82 70 120z" fill="{CH}"/>'
         f'<path d="M0 60l56 22L150 0z" fill="{RJ}"/><path d="M56 82l-6 46 20-8" fill="{SL}"/></g>',
         # envelope
         f'<g transform="translate(70 170) rotate(-8)" stroke="{DP}" stroke-width="3" stroke-linejoin="round">'
         f'<rect x="0" y="0" width="170" height="112" rx="8" fill="{RJ}"/><path d="M0 8l85 60 85-60" fill="none"/>'
         f'<path d="M0 104l62-44M170 104l-62-44" fill="none" opacity=".5"/>'
         f'<circle cx="140" cy="28" r="14" fill="{CN}"/></g>',
         g.leaf(150, 182, -70, .5, SL, DP), g.leaf(150, 182, 250, .5, WM, CH),
         f'<g stroke="{RJ}" stroke-width="3" stroke-linecap="round"><path d="M440 100l14-8M444 130h18"/></g>']
    return wrap('0 0 480 440', ''.join(b))

# ---- Compliance: binders on a shelf ----
def binders():
    cols = [(110, 70, SL, 0), (186, 70, RJ, 0), (262, 70, CN, 0), (338, 70, WM, 8)]
    b = [f'<circle cx="240" cy="220" r="170" fill="{WM}"/>']
    for x, w, c, rot in cols:
        b.append(f'<g transform="rotate({rot} {x+w} 380)"><rect x="{x}" y="120" width="{w}" height="260" rx="8" fill="{c}" stroke="{DP}" stroke-width="3"/>'
                 f'<rect x="{x+14}" y="160" width="{w-28}" height="60" rx="4" fill="{WM}" stroke="{DP}" stroke-width="2.5"/>'
                 f'<circle cx="{x+w/2}" cy="320" r="11" fill="{WM}" stroke="{DP}" stroke-width="2.5"/></g>')
    b += [f'<rect x="70" y="380" width="350" height="18" rx="4" fill="{DP}"/>',
          g.leaf(420, 380, -70, .7, SL, DP), g.leaf(420, 380, 250, .7, RJ, CH),
          f'<path d="M420 380c0-14 2-24 0-34" stroke="{DP}" stroke-width="4" fill="none"/>',
          f'<g stroke="{RJ}" stroke-width="3" stroke-linecap="round"><path d="M80 110l-12-10M74 140h-18"/></g>']
    return wrap('0 0 480 440', ''.join(b))

# ---- Card icons (laptop for virtual, school for in-person) ----
ICON = 'viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" ' + A
laptop = f'<svg class="ico" {ICON}><rect x="12" y="14" width="40" height="28" rx="4"/><path d="M6 48h52l-4 6H10z"/><path d="M32 36c0-6 1-10 0-14"/><path d="M32 26c4-5 9-5 11-3-3 4-8 5-11 3zM32 30c-4-4-8-4-10-2 3 3 7 4 10 2z"/></svg>'
school = f'<svg class="ico" {ICON}><path d="M8 28L32 12l24 16"/><path d="M14 26v28h36V26"/><path d="M27 54V42a5 5 0 0 1 10 0v12"/><circle cx="32" cy="28" r="4"/><path d="M4 54h56"/></svg>'

files = {'about.svg': seed_packet(), 'partner.svg': clipboard(), 'join.svg': chalk_badge(),
         'contact.svg': airplane(), 'compliance.svg': binders(), 'ico-laptop.svg': laptop, 'ico-school.svg': school}
for k, v in files.items():
    (OUT/k).write_text(v)
print({k: len(v) for k, v in files.items()})
