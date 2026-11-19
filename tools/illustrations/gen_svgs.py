"""Generates the inline SVGs for Direction B v2 (Growth Chart)."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parents[2] / 'kit-src' / 'svg'; OUT.mkdir(exist_ok=True)
SL, DP, RJ, CN, CH, WM = '#325453', '#1f3a39', '#f8ad5c', '#b92a0f', '#f7e4cc', '#fffaf3'
LEAF = 'M0 0c18-26 62-26 80 0-18 26-62 26-80 0z'
HALF = 'M0 0c18-26 62-26 80 0z'

def leaf(x, y, rot, s, base, top, cls='lf'):
    return (f'<g class="{cls}" transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="{LEAF}" fill="{base}"/><path d="{HALF}" fill="{top}"/>'
            f'<path d="{LEAF}" fill="none" stroke="{DP}" stroke-width="{2.6/s:.2f}" stroke-linejoin="round"/>'
            f'<path d="M4 0h66" stroke="{DP}" stroke-width="{1.4/s:.2f}" stroke-linecap="round" opacity=".55"/></g>')

def flower(cx, cy, r=13):
    import math
    petals = ''.join(f'<circle cx="{cx+r*1.05*math.cos(a):.1f}" cy="{cy+r*1.05*math.sin(a):.1f}" r="{r}" fill="{RJ}" stroke="{DP}" stroke-width="2.5"/>'
                     for a in [i*2*math.pi/5 - math.pi/2 for i in range(5)])
    return f'<g class="bloom">{petals}<circle cx="{cx}" cy="{cy}" r="{r*.75:.1f}" fill="{CN}" stroke="{DP}" stroke-width="2.5"/><circle cx="{cx-3}" cy="{cy-3}" r="{r*.22:.1f}" fill="{WM}" opacity=".8"/></g>'

def pot(cx, top, w, h, rimh, dots=True, shadow=True):
    x0 = cx - w/2
    s = ''
    if shadow:
        s += f'<ellipse cx="{cx}" cy="{top+rimh+h+4}" rx="{w*.62:.0f}" ry="{max(4,w*.06):.0f}" fill="{DP}" opacity=".16"/>'
    s += (f'<path d="M{x0+w*.08:.1f} {top+rimh}H{x0+w*.92:.1f}L{x0+w*.8:.1f} {top+rimh+h}H{x0+w*.2:.1f}z" fill="{CN}" stroke="{DP}" stroke-width="3" stroke-linejoin="round"/>'
          f'<rect x="{x0}" y="{top}" width="{w}" height="{rimh}" rx="4" fill="{CN}" stroke="{DP}" stroke-width="3"/>'
          f'<path d="M{x0+6} {top+5}h{w-12}" stroke="{WM}" stroke-width="2" opacity=".35" stroke-linecap="round"/>')
    if dots:
        n = 5; y = top + rimh + h*.42
        s += ''.join(f'<circle cx="{x0+w*.27 + i*(w*.46)/(n-1):.1f}" cy="{y:.1f}" r="{w*.028:.1f}" fill="{RJ}"/>' for i in range(n))
    return s

# ---------------- HERO ----------------
def hero():
    W, H = 600, 660
    p = [f'<svg class="scene" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">']
    # halo
    p.append(f'<circle cx="172" cy="160" r="126" fill="{WM}"/>')
    p.append(f'<circle cx="172" cy="160" r="144" fill="none" stroke="{RJ}" stroke-width="2.5" stroke-dasharray="2 12" stroke-linecap="round" class="ring"/>')
    # floor
    p.append(f'<rect x="0" y="604" width="{W}" height="56" fill="{RJ}" opacity=".22"/>')
    p.append(f'<path d="M0 604H{W}" stroke="{DP}" stroke-width="3"/>')
    # doorframe
    fx, fw, ftop = 300, 80, 18
    p.append(f'<rect x="{fx+8}" y="{ftop+8}" width="{fw}" height="{604-ftop-8}" rx="6" fill="{SL}"/>')
    p.append(f'<rect x="{fx}" y="{ftop}" width="{fw}" height="{604-ftop}" rx="6" fill="{WM}" stroke="{DP}" stroke-width="3"/>')
    p.append(f'<path d="M{fx+fw-16} {ftop+10}V598" stroke="{DP}" stroke-width="1.5" opacity=".2"/>')
    for gx, d in [(fx+28, 'c4 40-4 80 0 120s-3 70 1 110'), (fx+44, 'c-3 50 4 90 0 140s3 60-1 100'), (fx+36, 'c3 30-3 60 1 90')]:
        p.append(f'<path d="M{gx} {ftop+40}{d}" fill="none" stroke="{RJ}" stroke-width="1.6" opacity=".55"/>')
    ticks = []
    y = 596
    i = 0
    while y > ftop + 14:
        L = 22 if i % 5 == 0 else 11
        ticks.append(f'M{fx} {y}h{L}')
        y -= 11; i += 1
    p.append(f'<path d="{"".join(ticks)}" stroke="{DP}" stroke-width="2"/>')
    # step marks (bottom -> top)
    marks = [(520, 'partner', 2), (418, 'identify need', -3), (306, 'match &amp; onboard', 2), (186, 'serve &amp; invoice', -2)]
    for k, (my, label, tilt) in enumerate(marks, 1):
        tw = {1: 74, 2: 128, 3: 160, 4: 150}[k]
        p.append(f'<g class="m m{k}">'
                 f'<path d="M{fx-16} {my+tilt}L{fx+fw+22} {my-tilt}" stroke="{CN}" stroke-width="4.5" stroke-linecap="round"/>'
                 f'<circle cx="{fx+fw+22}" cy="{my-tilt}" r="5" fill="{CN}"/>'
                 f'<text x="{fx+fw+36}" y="{my+7}" class="lbl">{label}</text>'
                 f'<path class="ul" d="M{fx+fw+36} {my+16}c{tw*.3:.0f}-5 {tw*.7:.0f}-5 {tw}-1" fill="none" stroke="{RJ}" stroke-width="4" stroke-linecap="round" pathLength="1"/>'
                 '</g>')
    # star near top label
    p.append(f'<g class="star" transform="translate(548 150)"><path d="M0-13V13M-13 0H13M-9-9L9 9M9-9L-9 9" stroke="{CN}" stroke-width="3" stroke-linecap="round"/></g>')
    # pencil lying on the floor
    p.append('<g transform="translate(372 592) rotate(-7)">'
             f'<path d="M0 0l24-9v18z" fill="{CH}" stroke="{DP}" stroke-width="2.5" stroke-linejoin="round"/>'
             f'<path d="M0 0l8-3v6z" fill="{DP}"/>'
             f'<rect x="24" y="-9" width="120" height="18" fill="{RJ}" stroke="{DP}" stroke-width="2.5"/>'
             f'<path d="M24-3h120M24 3h120" stroke="{DP}" stroke-width="1" opacity=".35"/>'
             f'<rect x="144" y="-9" width="14" height="18" fill="{CH}" stroke="{DP}" stroke-width="2.5"/>'
             f'<rect x="158" y="-9" width="16" height="18" rx="5" fill="{CN}" stroke="{DP}" stroke-width="2.5"/></g>')
    # plant (sways on hover)
    p.append('<g class="plant">')
    stem = 'M160 524C150 470 176 430 164 370S148 270 168 210S180 150 172 112'
    p.append(f'<path d="{stem}" fill="none" stroke="{DP}" stroke-width="11" stroke-linecap="round"/>')
    p.append(f'<path d="{stem}" fill="none" stroke="{SL}" stroke-width="5" stroke-linecap="round"/>')
    leaves = [(163, 478, -18, .95, SL, DP), (158, 446, 198, .9, RJ, CH), (166, 384, -28, 1.1, WM, CH),
              (160, 336, 204, 1.1, SL, DP), (162, 272, -34, 1.15, RJ, CH), (164, 228, 210, 1.05, SL, DP),
              (170, 176, -40, .9, WM, CH), (170, 160, 214, .7, RJ, CH)]
    for x, y, r, s, b, t in leaves:
        p.append(leaf(x, y, r, s, b, t))
    p.append(flower(172, 104, 13))
    p.append(f'<g stroke="{RJ}" stroke-width="3" stroke-linecap="round" class="spark"><path d="M214 74l12-12M222 100h16M196 52l-2-16"/></g>')
    p.append('</g>')
    p.append(pot(160, 520, 132, 72, 26))
    p.append(f'<ellipse cx="160" cy="521" rx="56" ry="5" fill="{DP}"/>')
    p.append('</svg>')
    return ''.join(p)

# ---------------- STAGES (how it works) ----------------
def stage(n):
    p = [f'<svg class="stage" viewBox="0 0 120 132" aria-hidden="true" focusable="false">']
    p.append(f'<circle cx="60" cy="62" r="46" fill="{CH}"/>')
    if n == 1:
        p.append(f'<ellipse cx="60" cy="88" rx="7" ry="5" fill="{RJ}" stroke="{DP}" stroke-width="2"/>')
        p.append(f'<path d="M60 84c0-6 2-10 6-12" fill="none" stroke="{SL}" stroke-width="3" stroke-linecap="round"/>')
    else:
        top = {2: 62, 3: 40, 4: 30}[n]
        p.append(f'<path d="M60 92C58 {top+30} 63 {top+15} 61 {top}" fill="none" stroke="{DP}" stroke-width="6" stroke-linecap="round"/>')
        p.append(f'<path d="M60 92C58 {top+30} 63 {top+15} 61 {top}" fill="none" stroke="{SL}" stroke-width="2.5" stroke-linecap="round"/>')
        L = [(61, top+4, -40, .32, SL, DP), (61, top+4, 220, .32, RJ, CH)]
        if n >= 3:
            L += [(60, top+24, -20, .34, WM, CH), (60, top+30, 200, .34, SL, DP)]
        for x, y, r, s, b, t in L:
            p.append(leaf(x, y, r, s, b, t, cls='slf'))
        if n == 4:
            p.append(flower(61, top - 6, 7))
    p.append(pot(60, 88, 54, 30, 10, dots=False, shadow=False))
    p.append(f'<ellipse cx="60" cy="89" rx="23" ry="2.5" fill="{DP}"/>')
    p.append('</svg>')
    return ''.join(p)

# ---------------- CHALK DOODLE ----------------
def doodle():
    c = CH
    p = ['<svg class="doodle" viewBox="0 0 300 330" aria-hidden="true" focusable="false">',
         '<defs><filter id="chalk" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="3" result="n"/>'
         '<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter></defs>',
         f'<g filter="url(#chalk)" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">',
         '<rect x="190" y="20" width="44" height="290" rx="4"/>']
    t = ''.join(f'M190 {y}h{16 if (300-y)//14 % 5 == 0 else 8}' for y in range(300, 30, -14))
    p.append(f'<path d="{t}" stroke-width="2.5"/>')
    for y, w in [(250, 0), (190, 0), (130, 0), (70, 0)]:
        p.append(f'<path d="M180 {y}h66" stroke="{RJ}" stroke-width="5"/>')
    p.append('<path d="M60 296h90l-10 30H70z"/><path d="M52 284h106v12H52z"/>')
    p.append('<path d="M105 284C100 230 112 190 104 140S110 80 108 56"/>')
    for x, y, r, s in [(106, 246, -24, .6), (104, 220, 200, .6), (106, 170, -30, .65), (104, 140, 206, .62), (108, 92, -40, .55), (108, 74, 220, .5)]:
        p.append(f'<path transform="translate({x} {y}) rotate({r}) scale({s})" d="{LEAF}" stroke-width="{4/s:.1f}"/>')
    p.append(f'<g stroke="{RJ}"><circle cx="108" cy="46" r="9"/><path d="M134 30l8-8M140 52h12M118 16l1-10"/></g>')
    p.append(f'<path d="M20 130c10-20 34-28 50-20M58 100l12 10-14 6" stroke="{RJ}"/>')
    p.append('</g></svg>')
    s=''.join(p)
    head,body=s.split('<g filter=',1)
    body=body.replace('<path ','<path pathLength="1" ').replace('<rect ','<rect pathLength="1" ').replace('<circle ','<circle pathLength="1" ')
    return head+'<g filter='+body

files = {'hero.svg': hero(), 'doodle.svg': doodle(), **{f'stage{n}.svg': stage(n) for n in range(1, 5)}}
for k, v in files.items():
    (OUT/k).write_text(v)
    print(k, len(v.encode()), 'bytes')
