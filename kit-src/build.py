"""Builds the Good to Grow Therapy Elementor kit (.zip) for Elementor 4.4.x + Pro."""
import json, pathlib, zipfile, datetime, random
from el import *

random.seed(2026)
VERSION = '1.0.0'
ROOT = pathlib.Path(__file__).resolve().parent
SVG = ROOT / 'svg'
OUT = ROOT / 'build'
svg = lambda n: (SVG / n).read_text()
TORN = (ROOT / 'torn.txt').read_text().strip()
CSS = (ROOT / 'elementor.css').read_text().replace('{{TORN}}', TORN)

U = {'home': '/', 'about': '/about/', 'partner': '/partner-with-us/', 'join': '/join-our-team/', 'contact': '/contact/',
     'faq': '/compliance-and-faq/', 'privacy': '/privacy-policy/', 'a11y': '/accessibility/'}

ic = lambda body: ('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                   f'stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')
I_SPEECH = ic('<path d="M7 6h18a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3H15l-6 5v-5H7a3 3 0 0 1-3-3V9a3 3 0 0 1 3-3z"/><path d="M12 12v4M16 10v8M20 12v4"/>')
I_OT = ic('<path d="M21 5l6 6L12 26H6v-6z"/><path d="M18 8l6 6"/><path d="M6 20l6 6"/>')
I_PT = ic('<path d="M11 4c3 0 5 3 5 7s-2 7-5 7-4-3-4-7 1-7 4-7z"/><path d="M7 21h8"/><path d="M21 12c3 0 4 3 4 7s-1.5 6-4 6-4-2.5-4-6 1-7 4-7z"/><path d="M17 28h8"/>')
I_HEART = ic('<path d="M16 27S6 20.8 6 14a5.5 5.5 0 0 1 10-3.2A5.5 5.5 0 0 1 26 14c0 6.8-10 13-10 13z"/><path d="M16 21v-5c0-2 1.5-3.5 4-3.5 0 2-1.5 3.5-4 3.5"/>')
BINDER_ICO = ('<svg viewBox="0 0 54 54" aria-hidden="true" focusable="false"><rect x="8" y="6" width="16" height="42" rx="3" fill="#325453" stroke="#1f3a39" stroke-width="2.5"/>'
              '<rect x="26" y="6" width="16" height="42" rx="3" fill="#f8ad5c" stroke="#1f3a39" stroke-width="2.5"/><rect x="11" y="12" width="10" height="10" rx="2" fill="#fffaf3"/>'
              '<rect x="29" y="12" width="10" height="10" rx="2" fill="#fffaf3"/><path d="M4 49h46" stroke="#1f3a39" stroke-width="3" stroke-linecap="round"/></svg>')
BINDER_CLIP = ('<svg class="binder" viewBox="0 0 92 60" aria-hidden="true" focusable="false"><path d="M8 24h76v30a6 6 0 0 1-6 6H14a6 6 0 0 1-6-6z" fill="#1f3a39"/>'
               '<path d="M26 26c0-14 4-22 20-22s20 8 20 22" fill="none" stroke="#1f3a39" stroke-width="5"/><path d="M14 30h64" stroke="#fffaf3" stroke-width="2" opacity=".25"/></svg>')
MARGIN_DOODLE = ('<svg class="margin-doodle" viewBox="0 0 110 80" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
                 '<path d="M70 10l5 11 12 2-9 8 2 12-10-6-11 6 2-12-9-8 12-2z"/><path d="M60 50C46 66 26 70 8 64M8 64l12-8M8 64l10 10"/></svg>')
NOTICE = ('<p class="notice"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true" focusable="false">'
          '<circle cx="12" cy="12" r="10"/><path d="M12 8v5M12 16.5v.5"/></svg>Please do not include student names or student information in this form.</p>')
TRAY = '<span class="tray" aria-hidden="true"></span><span class="chalk" aria-hidden="true"></span><span class="chalk b" aria-hidden="true"></span>'
STUB = '<div class="stub" aria-hidden="true"><span>Next step</span><i></i></div>'

# ---------------------------------------------------------------- shared sections
def page_intro(eyebrow, h1, lede, actions, art, extra=''):
    return C(f'pintro {extra}'.strip(),
             C('wrap pintro-grid',
               C('copy', EYE(eyebrow), H(h1, 'h1'), T(f'<p>{lede}</p>', 'lede'), actions),
               X(art, 'art-w') if art else None),
             tag='section', title='Page intro')

def steps_cards(steps, c3=False, stages=(1, 2, 3, 4)):
    cards = []
    for i, (title, text) in enumerate(steps):
        cards.append(C('card rv',
                       X(f'<div class="head"><span class="n" aria-hidden="true">{i+1}.</span>{svg(f"stage{stages[i]}.svg")}</div>'),
                       H(title, 'h3'), T(f'<p>{text}</p>'), title=f'Card {i+1}'))
    return C('cards c3' if c3 else 'cards', *cards, title='Cards')

def ticket(h2, btn, url, flush=False):
    return C('ticket rv' + (' flush' if flush else ''), X(STUB), C('tmain', H(h2, 'h2'), B(btn, url, 'btn-w')), title='Ticket CTA')

HOW_STEPS = [('Partner', 'Your school or district reaches out, and we talk through what your students need.'),
             ('Identify need', 'Your team identifies students and shares referrals through your usual process.'),
             ('Match and onboard', 'We size the support, match licensed clinicians and handle their onboarding.'),
             ('Serve and invoice', 'Clinicians work with your students, and we handle billing with your school.')]

def how_band(eyebrow, h2, note, steps, c3=False, stages=(1, 2, 3, 4), note_is_tag=False):
    right = H(note, 'p', 'tag') if note_is_tag else T(f'<p>{note}</p>', 'how-note')
    return C('how dark', C('wrap', C('how-top', C('', EYE(eyebrow), H(h2, 'h2')), right), steps_cards(steps, c3, stages)),
             tag='section', title='How it works')

def form_section(eyebrow, h2, intro, next_steps, form_title, form, side_extra=None, torn=True):
    ol = ''.join(f'<li><strong>{a}</strong>{b}</li>' for a, b in next_steps)
    side = [EYE(eyebrow), H(h2, 'h2'), T(f'<p>{intro}</p>')]
    if next_steps: side.append(T(f'<ol>{ol}</ol>', 'next'))
    if side_extra: side.append(side_extra)
    return C('formsec' + (' torn' if torn else ''),
             C('wrap form-grid', C('', *side), C('clipboard rv', C('paper', H(form_title, 'h2'), form))),
             tag='section', title='Form')

def common_fields_end(prefix):
    return [field('honeypot', 'hp', 'Leave this field empty'),
            field('acceptance', 'optin', '', acceptance_text='Send me occasional email updates from Good to Grow Therapy. You can unsubscribe at any time.'),
            field('html', 'privacy', '', field_html=f'<a href="{U["privacy"]}">Read our Privacy Policy</a>')]

# ---------------------------------------------------------------- HOME
def home():
    hero = C('hero',
             C('wrap hero-grid',
               C('hero-copy', EYE('School-based therapy for K-12'),
                 H('Virtual therapy for your students, <span class="it">handled</span> from <span class="circled">referral to invoice.</span>', 'h1'),
                 T('<p>We match licensed clinicians to your school, then take care of onboarding and billing, so your special education team can stay focused on students.</p>', 'lede'),
                 C('acts', B('Partner With Us', U['partner']), B('Join Our Team', U['join'], 'btn-link'))),
               X(svg('hero.svg'), 'hero-art')),
             tag='section', title='Hero')
    how = how_band('How it works', 'Four steps, from first call to <span class="it">first invoice.</span>',
                   'Every partnership grows the same way. Your team stays in charge of referrals, and we take care of the rest.', HOW_STEPS)
    services = [('Speech-language therapy', "Support for students' communication goals, from licensed speech-language pathologists matched to your school.", 'folder clip'),
                ('Occupational therapy', 'Support for fine motor, sensory and daily-living goals, from licensed occupational therapists.', 'folder f2'),
                ('Physical therapy', 'Support for movement, mobility and access to the school setting, from licensed physical therapists.', 'folder f3'),
                ('School counseling', 'Support for social and emotional goals, from licensed counselors working alongside your school team.', 'folder f4')]
    folders = [ACC([(f'<span class="lbl" aria-hidden="true">File 0{i+1}</span>{n}', [T(f'<p>{d}</p>')])], cls)
               for i, (n, d, cls) in enumerate(services)]
    svc = C('svc', C('wrap',
                     C('svc-top', C('', EYE('Services'), H('Support across the therapies your students need.', 'h2')),
                       T('<p>Draft list. Service names are placeholders until confirmed.</p>', 'sticky')),
                     C('folders', *folders)), tag='section', title='Services')
    schools = C('schools', C('wrap schools-grid',
                C('sheet rv', X(BINDER_CLIP), EYE('For schools and districts'),
                  H('One partner, from <span class="hl">referral to invoice.</span>', 'h2'),
                  T('<p>For special education directors and procurement teams looking for one therapy partner from start to finish.</p>'),
                  T('<ul><li>Clinician sizing and matching</li><li>Onboarding, handled for you</li><li>Billing with your school or district</li></ul>'),
                  B('Partner With Us', U['partner']), X(MARGIN_DOODLE), title='Notebook sheet'),
                C('note rv', H('Virtual today. In person as we grow.', 'p'),
                  T('<p>In-person services at schools and facilities will be added as we grow.</p>'), title='Sticky note')),
                tag='section', title='For schools')
    board = C('board-sec', C('wrap', C('board dark rv',
              C('', EYE('For clinicians'), H('Bring your license. Find <span class="chalk-ul">your fit</span> in school-based work.', 'h2'),
                T('<p>We are building a network of licensed speech-language pathologists, occupational and physical therapists and counselors who work with schools as independent contractors.</p>'
                  '<p>Tell us about your license and where you practice.</p>'),
                C('acts', B('Join Our Team', U['join']))),
              X(svg('doodle.svg') + TRAY, 'deco'), title='Chalkboard')), tag='section', title='For clinicians')
    proof = C('proof', C('wrap', C('ph', T('<p><strong>[PLACEHOLDER: proof, no content until approved]</strong>Reserved space. No numbers, logos or quotes.</p>'), title='Proof placeholder')),
              tag='section', title='Proof (placeholder)')
    qa = ACC([('Do you work with families directly?', [T('<p>No. We work with school systems, districts and institutions. Students are served through their school.</p>')]),
              ('What do you handle for our school?', [T('<p>We handle clinician sizing and matching, onboarding and billing. Your team keeps identifying need and assigning referrals.</p>')]),
              ('Does this website collect student information?', [T("<p>No. None of our forms ask for student names or student information, and we ask that you don't include any.</p>")])], 'qa-acc')
    faq = C('faq torn', C('wrap',
            C('faq-grid', C('', EYE('FAQ'), H('Questions schools <span class="it">ask us.</span>', 'h2'),
                            T('<p>Short answers here. More detail, and compliance documents when they are ready, live on one page.</p>'),
                            B('Read the Compliance and FAQ page', U['faq'], 'btn-link')), qa),
            ticket("Let's talk about what your <span class=\"it\">students need.</span>", 'Contact Us', U['contact'])),
            tag='section', title='FAQ and closing call to action')
    return top(hero, how, svc, schools, board, proof, faq)

# ---------------------------------------------------------------- ABOUT
def about():
    story = C('sec', C('wrap story',
              C('sheet rv', EYE('Our story'), H('Built around how schools <span class="hl">already work.</span>', 'h2'),
                T("<p>We work with school systems to size therapy support, match licensed clinicians to students' needs, and take care of onboarding and billing. Your team keeps identifying need and assigning referrals.</p>"
                  '<p>We serve students virtually today, and we will add in-person services at schools and facilities as we grow.</p>'), title='Story sheet'),
              C('note rv', H('Based in Canton, GA.', 'p'), T('<p>Working with K-12 school systems.</p>'), title='Sticky note')),
              tag='section', title='Story')
    pr = C('sec tight on-paper', C('wrap',
           C('sec-head row', C('', EYE('What guides us'), H('Three principles.', 'h2')), H('Placeholder principles', 'p', 'tag')),
           steps_cards([('[Principle one]', '[One or two sentences, to be written by the founders.]'),
                        ('[Principle two]', '[One or two sentences, to be written by the founders.]'),
                        ('[Principle three]', '[One or two sentences, to be written by the founders.]')], c3=True, stages=(2, 3, 4))),
           tag='section', title='Principles')
    cta = C('sec tight on-grid', C('wrap', ticket('Working with a school system? <span class="it">Let\'s talk.</span>', 'Partner With Us', U['partner'], flush=True)),
            tag='section', title='Closing call to action')
    return top(page_intro('About', 'Therapy for K-12 students, <span class="it">through their schools.</span>',
                          'Good to Grow Therapy is based in Canton, GA. We provide therapy to K-12 students through school systems.',
                          B('Partner With Us', U['partner']), svg('about.svg')), story, pr, cta)

# ---------------------------------------------------------------- PARTNER
def partner():
    ways = C('sec', C('wrap',
             C('sec-head', EYE('Ways to partner'), H('Two ways to work with us.', 'h2')),
             C('ways',
               C('way rv', X(f'<span class="flag">Available now</span><div class="ibox">{svg("ico-laptop.svg")}</div>'), H('Virtual services', 'h3'),
                 T('<p>Licensed clinicians work with your students virtually. We handle sizing, matching, onboarding and billing with your school.</p>'), title='Virtual'),
               C('way alt rv', X(f'<span class="flag">Placeholder</span><div class="ibox">{svg("ico-school.svg")}</div>'), H('In-person services at your school or facility', 'h3'),
                 T('<p>[Placeholder: in-person services wording, to be written by the founders.]</p>'), title='In person'))),
             tag='section', title='Ways to partner')
    proc = how_band('The process', 'Four steps, from first call to <span class="it">first invoice.</span>',
                    'Each step has one job. Your team stays in charge of referrals.', HOW_STEPS)
    split = C('sec', C('wrap',
              C('sec-head row', C('', EYE('Who does what'), H('What we handle, and what your team keeps.', 'h2')), H('Draft, to be confirmed', 'p', 'tag')),
              C('split',
                C('board dark rv', EYE('We handle'), T('<ul><li>Clinician sizing and matching</li><li>Clinician onboarding</li><li>Billing with your school or district</li></ul>'),
                  X(TRAY, 'deco'), title='We handle'),
                C('sheet rv', EYE('Your team keeps'), T('<ul><li>Identifying student need</li><li>Assigning referrals</li></ul>'), title='Your team keeps'))),
              tag='section', title='What we handle')
    pointer = C('sec tight', C('wrap', C('pointer rv',
                C('pointer-l', X(BINDER_ICO), T('<p>Vetting a vendor? Our compliance questions and answers are in one place.</p>')),
                B('Compliance and FAQ', U['faq'], 'btn-w'))), tag='section', title='Compliance pointer')
    form = FORM('Partner inquiry', [
        field('html', 'notice', '', field_html=NOTICE),
        field('text', 'name', 'Name', True, '50'),
        field('text', 'role', 'Role or title', True, '50'),
        field('text', 'organization', 'School or organization', True),
        field('email', 'email', 'Work email', True, '50'),
        field('tel', 'phone', 'Phone (optional)', False, '50'),
        field('textarea', 'message', 'Message', True, rows='5'),
        *common_fields_end('p')], '/thanks-partner/')
    fs = form_section('Partner inquiry', 'Tell us about your school.', 'Share a little about your school or organization, and we will follow up by email.',
                      [('You send the form', 'Name, role, organization and a short message.'), ('We follow up by email', 'To set up a first conversation.'),
                       ('We talk through your needs', 'Then we plan the support together.')], 'Partner inquiry', form)
    fs['settings']['_element_id'] = 'inquiry'
    return top(page_intro('Partner With Us', 'A therapy partner for your <span class="it">school or district.</span>',
                          'For school districts, brick-and-mortar schools, clinics and institutions that need therapy support for K-12 students.',
                          B('Start an inquiry', '#inquiry', 'btn-r btn-down'), svg('partner.svg')), ways, proc, split, pointer, fs)

# ---------------------------------------------------------------- JOIN
def join():
    roles = [('Speech-language pathology', 'Licensed speech-language pathologists.', I_SPEECH), ('Occupational therapy', 'Licensed occupational therapists.', I_OT),
             ('Physical therapy', 'Licensed physical therapists.', I_PT), ('Counseling', 'Licensed counselors.', I_HEART)]
    rl = C('sec', C('wrap',
           C('sec-head row', C('', EYE('Roles we are building toward'), H('Licensed clinicians we work with.', 'h2')), H('Placeholder roles', 'p', 'tag')),
           C('roles', *[C('rbadge rv', X(f'<span class="ibox">{i}</span>'), H(t, 'h3'), T(f'<p>{d}</p>'), title=t) for t, d, i in roles])),
           tag='section', title='Roles')
    hj = how_band('How joining works', 'Three plain steps.', 'Placeholder steps',
                  [('Share your interest', 'Tell us your license type and the states where you are licensed.'),
                   ('We follow up', 'We reach out by email to learn more about your practice.'),
                   ('Find your fit', 'We talk through school-based contract work that fits your license.')], c3=True, stages=(2, 3, 4), note_is_tag=True)
    form = FORM('Join Our Team interest', [
        field('html', 'notice', '', field_html=NOTICE),
        field('text', 'name', 'Name', True),
        field('email', 'email', 'Email', True, '50'),
        field('tel', 'phone', 'Phone (optional)', False, '50'),
        field('select', 'license', 'License or credential type', True, '50',
              field_options='Choose one|\nSpeech-language pathologist\nOccupational therapist\nPhysical therapist\nCounselor\nOther'),
        field('text', 'states', 'States licensed', True, '50'),
        field('textarea', 'message', 'Message', True, rows='5'),
        *common_fields_end('j')], '/thanks-careers/')
    note = C('note rv', H('Independent contractors.', 'p'), T('<p>Clinicians work with schools as independent contractors.</p>'), title='Sticky note')
    fs = form_section('Interest form', 'Tell us about your license.',
                      "We only ask for the basics. Please don't send credentials or verification documents through this site.", [], 'Join Our Team', form,
                      side_extra=note, torn=False)
    fs['settings']['_element_id'] = 'interest'
    return top(page_intro('Join Our Team', 'Bring your license. Find your fit in <span class="it">school-based work.</span>',
                          'For licensed clinicians who want to serve K-12 students as independent contractors.',
                          B('Share your interest', '#interest', 'btn-r btn-down'), svg('join.svg'), 'dark'), rl, hj, fs)

# ---------------------------------------------------------------- CONTACT
def contact():
    form = FORM('Contact', [
        field('html', 'notice', '', field_html=NOTICE),
        field('text', 'name', 'Name', True, '50'),
        field('email', 'email', 'Email', True, '50'),
        field('text', 'organization', 'Organization (optional)', False),
        field('textarea', 'message', 'Message', True, rows='5'),
        *common_fields_end('c')], '/thanks-contact/')
    fs = form_section('Contact form', 'Send us a message.',
                      'Schools and districts can also use the partner inquiry form. Clinicians can use the interest form on Join Our Team.',
                      [('You send a message', 'Your name, email and a short note.'), ('We follow up by email', 'We read every message.')], 'Contact us', form, torn=False)
    acts = C('acts', B('Schools: Partner With Us', U['partner'], 'btn-link'), B('Clinicians: Join Our Team', U['join'], 'btn-link'))
    return top(page_intro('Contact', 'One place to <span class="it">reach us.</span>', 'Send us a message and we will follow up by email.', acts, svg('contact.svg')), fs)

# ---------------------------------------------------------------- COMPLIANCE AND FAQ
def compliance():
    qa = ACC([('Do you work with families directly?', [T('<p>No. We work with school systems, districts and institutions. Students are served through their school.</p>')]),
              ('What do you handle for our school?', [T('<p>We handle clinician sizing and matching, onboarding and billing. Your team keeps identifying need and assigning referrals.</p>')]),
              ('Does this website collect student information?', [T("<p>No. None of our forms ask for student names or student information, and we ask that you don't include any.</p>")]),
              ('Do you provide services virtually or in person?', [T('<p>We serve students virtually today. We will add in-person services at schools and facilities as we grow.</p>')]),
              ('How do we get started?', [T('<p>Send a partner inquiry from our Partner With Us page, and we will follow up by email to set up a first conversation.</p>')])], 'qa-acc faq-list')
    faq = C('sec', C('wrap', C('sec-head', EYE('Section 1'), H('Frequently asked questions.', 'h2')), qa,
                     T('<p>[Room for more questions as the founders approve them.]</p>', 'slot-note')), tag='section', title='FAQ')
    docs = C('sec tight', C('wrap', C('cabinet dark rv',
             C('drawer', X('<div class="holder" aria-hidden="true"><span>Compliance</span></div>'),
               C('', EYE('Section 2'), H('Compliance documents.', 'h2'),
                 T('<p>This drawer will hold the documents districts ask for when they review a partner.</p>'),
                 C('ph', T('<p><strong>[PLACEHOLDER: compliance documents, none published until approved]</strong>A document list or a request-access form goes here later.</p>'))),
               X('<span class="handle" aria-hidden="true"></span>', 'deco')),
             X('<div class="closed-drawer" aria-hidden="true"><div class="holder"><span>Reserved</span></div><span class="handle"></span></div>'), title='Filing cabinet')),
             tag='section', title='Compliance documents')
    docs['settings']['_element_id'] = 'documents'
    cta = C('sec tight on-grid', C('wrap', ticket('Ready to talk about <span class="it">your students?</span>', 'Partner With Us', U['partner'], flush=True)),
            tag='section', title='Closing call to action')
    return top(page_intro('Compliance and FAQ', 'Questions and answers for <span class="it">school teams.</span>',
                          'Plain answers to the questions districts ask when they vet a therapy partner.',
                          B('Compliance documents', '#documents', 'btn-link'), svg('compliance.svg')), faq, docs, cta)

# ---------------------------------------------------------------- LEGAL + THANKS
def legal(name, what):
    skel = '<div class="skel" aria-hidden="true"><b></b>' + '<i></i>' * 5 + '<b></b>' + '<i></i>' * 4 + '<b></b>' + '<i></i>' * 6 + '</div>'
    return top(page_intro('Legal', f'{name} <span class="stamp">[DRAFT]</span>', what, None, None, 'compact'),
               C('sec', C('wrap', C('legal', C('sheet', T('<p class="meta">Last updated: [date]</p>'), H('[DRAFT]', 'h2'),
                                                  T('<p>Text is drafted separately and reviewed by counsel before launch.</p>'), X(skel), title='Legal text'))),
                 tag='section', title='Legal text'))

def thanks(h1, p):
    return top(C('thanks', C('wrap', C('thanks-card', X(svg('stage4.svg')), H(h1, 'h1'), T(f'<p>{p}</p>'), C('acts', B('Back to Home', U['home'])), title='Thank-you card')),
                 tag='section', title='Thank you'))

# ---------------------------------------------------------------- HEADER / FOOTER
def header():
    return top(C('hdr', C('wrap hdr-row',
                 H('<span>Good to Grow</span><span>THERAPY</span>', 'div', 'brand', url='/'),
                 C('hdr-nav', NAV(), B('Join Our Team', U['join'], 'btn-r btn-cta'))), title='Header'))

def footer():
    social = ('<div class="soc"><a href="https://www.instagram.com/goodtogrowtherapy/" target="_blank" rel="noopener noreferrer" '
              'aria-label="Good to Grow Therapy on Instagram, opens in a new tab"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false">'
              '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
              '<span aria-hidden="true">Instagram</span></a></div>')
    return top(C('ftr dark',
                 C('wrap',
                   C('ftop', C('', H('<span>Good to Grow</span><span>THERAPY</span>', 'div', 'brand', url='/'),
                               T('<p>Therapy for K-12 students, delivered through school systems.</p>')),
                     C('', ICONLIST([('Compliance and FAQ', U['faq']), ('Privacy Policy', U['privacy']),
                                     ('Accessibility Statement', U['a11y']), ('Contact', U['contact'])], 'fl'), tag='nav')),
                   C('fbot', T('<p>Good to Grow Therapy, LLC. Canton, GA.</p>'), X(social))), title='Footer'))

# ---------------------------------------------------------------- SITE SETTINGS
def border(px): return {'unit': 'px', 'top': str(px), 'right': str(px), 'bottom': str(px), 'left': str(px), 'isLinked': True}
def size(v, unit='px'): return {'unit': unit, 'size': v, 'sizes': []}
TYPO = lambda fam, w: {'typography_typography': 'custom', 'typography_font_family': fam, 'typography_font_weight': w}
settings = {
    'system_colors': [{'_id': 'primary', 'title': 'Primary · Dark slate', 'color': '#325453'},
                      {'_id': 'secondary', 'title': 'Secondary · Carnelian', 'color': '#B92A0F'},
                      {'_id': 'text', 'title': 'Text · Deep slate', 'color': '#1F3A39'},
                      {'_id': 'accent', 'title': 'Accent · Rajah', 'color': '#F8AD5C'}],
    'custom_colors': [{'_id': 'a1c2e3f', 'title': 'Champagne', 'color': '#F7E4CC'},
                      {'_id': 'b2d3f4a', 'title': 'Warm white', 'color': '#FFFAF3'}],
    'system_typography': [{'_id': 'primary', 'title': 'Headings · Newsreader', **TYPO('Newsreader', '500')},
                          {'_id': 'secondary', 'title': 'Labels · Source Sans 3', **TYPO('Source Sans 3', '700')},
                          {'_id': 'text', 'title': 'Body · Source Sans 3', **TYPO('Source Sans 3', '400')},
                          {'_id': 'accent', 'title': 'Buttons · Source Sans 3', **TYPO('Source Sans 3', '700')}],
    'custom_typography': [],
    'default_generic_fonts': 'Sans-serif',
    'body_background_background': 'classic', 'body_background_color': '#F7E4CC',
    'body_color': '#1F3A39', 'body_typography_typography': 'custom', 'body_typography_font_family': 'Source Sans 3',
    'body_typography_font_size': size(18), 'body_typography_font_size_mobile': size(16), 'body_typography_line_height': size(1.55, 'em'),
    'link_normal_color': '#B92A0F', 'link_hover_color': '#1F3A39',
    **{f'h{i}_typography_{k}': v for i in range(1, 7) for k, v in [('typography', 'custom'), ('font_family', 'Newsreader'), ('font_weight', '500')]},
    'button_typography_typography': 'custom', 'button_typography_font_family': 'Source Sans 3', 'button_typography_font_weight': '700',
    'button_text_color': '#1F3A39', 'button_background_background': 'classic', 'button_background_color': '#F8AD5C',
    'button_border_border': 'solid', 'button_border_width': border(2), 'button_border_color': '#1F3A39', 'button_border_radius': border(14),
    'button_hover_text_color': '#1F3A39', 'button_hover_background_background': 'classic', 'button_hover_background_color': '#F8AD5C',
    'container_width': size(1240), 'container_padding': border(0),
    'space_between_widgets': {'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px'},
    'page_title_selector': 'h1.entry-title',
    'custom_css': CSS,
}

# ---------------------------------------------------------------- PACKAGE
PAGES = [  # id, title (sets the slug), builder, extra manifest
    (201, 'Home', home, {'show_on_front': True}),
    (202, 'About', about, {}),
    (203, 'Partner With Us', partner, {}),
    (204, 'Join Our Team', join, {}),
    (205, 'Contact', contact, {}),
    (206, 'Compliance and FAQ', compliance, {}),
    (207, 'Privacy Policy', lambda: legal('Privacy Policy', 'How Good to Grow Therapy handles information sent through this website.'), {}),
    (208, 'Accessibility', lambda: legal('Accessibility Statement', 'Our commitment to an accessible website, and how to reach us about a barrier.'), {}),
    (209, 'Thanks Partner', lambda: thanks('Thank you. We got your inquiry.', 'Thanks for reaching out about your students. We read every inquiry and will follow up by email.'), {}),
    (210, 'Thanks Careers', lambda: thanks('Thank you for your interest.', 'Thanks for telling us about your license. We will follow up by email.'), {}),
    (211, 'Thanks Contact', lambda: thanks('Thank you. We got your message.', 'We read every message and will follow up by email.'), {}),
]
PAGE_SETTINGS = {'template': 'default', 'hide_title': 'yes'}
SITE = 'https://goodtogrowtherapy.thekolabmarketing.com'

def doc(content, settings_=None):
    return {'content': content, 'settings': settings_ or {}, 'metadata': []}

def build():
    if OUT.exists():
        import shutil; shutil.rmtree(OUT)
    (OUT / 'templates').mkdir(parents=True); (OUT / 'content' / 'page').mkdir(parents=True)
    whole_site = [{'type': 'include', 'name': 'general', 'sub_name': '', 'sub_id': ''}]
    manifest = {
        'name': 'good-to-grow-therapy', 'title': 'Good to Grow Therapy',
        'description': 'Growth Chart template kit: header, footer, 11 pages, global colors, fonts and styles. Elementor + Elementor Pro stock widgets only.',
        'author': 'Joy De Leon', 'version': '2.0', 'elementor_version': '4.4.1',
        'created': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), 'thumbnail': False, 'site': SITE,
        'templates': {
            '101': {'title': 'G2G Header', 'doc_type': 'header', 'thumbnail': False, 'location': 'header', 'conditions': whole_site},
            '102': {'title': 'G2G Footer', 'doc_type': 'footer', 'thumbnail': False, 'location': 'footer', 'conditions': whole_site},
        },
        'content': {'page': {}},
        'site-settings': ['global-colors', 'global-typography', 'theme-style-typography', 'theme-style-buttons',
                          'settings-background', 'settings-layout', 'settings-custom-css'],
    }
    (OUT / 'templates' / '101.json').write_text(json.dumps(doc(header())))
    (OUT / 'templates' / '102.json').write_text(json.dumps(doc(footer())))
    for pid, title, fn, extra in PAGES:
        slug = title.lower().replace(' ', '-')
        manifest['content']['page'][str(pid)] = {'title': title, 'excerpt': '', 'doc_type': 'wp-page', 'thumbnail': False,
                                                 'url': f'{SITE}/' if extra.get('show_on_front') else f'{SITE}/{slug}/', 'terms': [], **extra}
        (OUT / 'content' / 'page' / f'{pid}.json').write_text(json.dumps(doc(fn(), dict(PAGE_SETTINGS))))
    (OUT / 'site-settings.json').write_text(json.dumps({'content': [], 'settings': settings, 'metadata': []}))
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    zpath = ROOT.parent / 'dist' / f'good-to-grow-therapy-kit-v{VERSION}.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(OUT).as_posix())
    return zpath

if __name__ == '__main__':
    z = build()
    print(z, round(z.stat().st_size / 1024, 1), 'KB')
