"""Tiny helpers that emit Elementor 4.4 element JSON (containers + stock widgets)."""
import random

_seen = set()
def rid():
    while True:
        s = ''.join(random.choices('0123456789abcdef', k=7))
        if s not in _seen:
            _seen.add(s); return s

def link(url, external=False):
    return {'url': url, 'is_external': 'on' if external else '', 'nofollow': '', 'custom_attributes': ''}

def C(cls, *children, tag=None, title=None):
    s = {'content_width': 'full', 'css_classes': cls}
    if tag: s['html_tag'] = tag
    if title: s['_title'] = title
    return {'id': rid(), 'elType': 'container', 'isInner': True, 'settings': s, 'elements': [c for c in children if c]}

def W(wtype, settings, cls=''):
    s = dict(settings)
    if cls: s['_css_classes'] = cls
    return {'id': rid(), 'elType': 'widget', 'widgetType': wtype, 'isInner': False, 'settings': s, 'elements': []}

def H(text, tag='h2', cls='', url=None):
    s = {'title': text, 'header_size': tag}
    if url: s['link'] = link(url)
    return W('heading', s, cls)

def EYE(text):
    return H(text, 'p', 'eyebrow')

def T(html, cls=''):
    return W('text-editor', {'editor': html}, cls)

def B(text, url, cls='btn-r'):
    return W('button', {'text': text, 'link': link(url), 'size': 'md'}, cls)

def X(html, cls=''):
    return W('html', {'html': html}, cls)

NO_ICON = {'value': '', 'library': ''}

def ACC(items, cls, title_tag='h3'):
    """items: list of (title_html, [child elements])"""
    w = W('n-accordion', {
        'items': [{'item_title': t, '_id': rid()} for t, _ in items],
        'accordion_item_title_icon': NO_ICON, 'accordion_item_title_icon_active': NO_ICON,
        'title_tag': title_tag, 'default_state': 'all_collapsed', 'max_items_expended': 'one',
    }, cls)
    w['elements'] = [{'id': rid(), 'elType': 'container', 'isInner': True,
                      'settings': {'_title': f'item #{i+1}', 'content_width': 'full'}, 'elements': kids}
                     for i, (_, kids) in enumerate(items)]
    return w

def field(ftype, cid, label='', required=False, width='100', **extra):
    f = {'_id': rid(), 'custom_id': cid, 'field_type': ftype, 'field_label': label, 'placeholder': '',
         'required': 'true' if required else '', 'width': width}
    f.update(extra)
    return f

def FORM(name, fields, redirect, button='Send'):
    return W('form', {
        'form_name': name, 'form_fields': fields, 'show_labels': 'true', 'mark_required': '',
        'input_size': 'md', 'button_text': button, 'button_size': 'md', 'button_width': '',
        'column_gap': {'unit': 'px', 'size': 18, 'sizes': []}, 'row_gap': {'unit': 'px', 'size': 20, 'sizes': []},
        'submit_actions': ['email', 'redirect'], 'redirect_to': redirect,
        'email_subject': f'New {name} from the website', 'email_content': '[all-fields]',
        'success_message': 'Thank you. We got your message.',
        'error_message': 'Something went wrong. Please try again.',
        'required_field_message': 'Please fill in this field.',
        'invalid_message': 'Please check this field.',
    }, 'g2g-form')

def NAV(menu_slug='main-menu'):
    return W('nav-menu', {
        'menu': menu_slug, 'layout': 'horizontal', 'align_items': 'right', 'pointer': 'none',
        'dropdown': 'tablet', 'full_width': 'stretch', 'toggle': 'burger', 'text_align': 'aside',
    }, 'nav')

def ICONLIST(items, cls):
    return W('icon-list', {'view': 'inline', 'icon_list': [
        {'_id': rid(), 'text': t, 'selected_icon': NO_ICON, 'link': link(u)} for t, u in items]}, cls)

def top(*sections):
    """Top-level containers are not 'inner'."""
    out = []
    for s in sections:
        s = dict(s); s['isInner'] = False; out.append(s)
    return out
