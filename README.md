# Seedling · No-add-on Elementor Pro template kit

A complete website template kit built **only with stock Elementor and Elementor Pro widgets**: no add-on plugins, no image files, no page-builder extras.
First built for **Good to Grow Therapy**, a K-12 school-based therapy provider ("Growth Chart" design).

- **Stack:** WordPress, Hello Elementor theme, Elementor 4.4 + Elementor Pro
- **Accessibility:** built to WCAG 2.1 AA (contrast-checked palette, keyboard-friendly menu and accordions, visible focus, labelled form fields, reduced-motion support)
- **Performance:** illustrations are inline SVG drawn from code, motion is CSS-only and runs only on hover or scroll, two font families, no sliders or autoplay
- **Kit contents:** Theme Builder header and footer, 11 pages, global colors and fonts, three Elementor Pro forms with thank-you redirects

Open `prototype/index.html` for a static preview of every page.

## What's here

| Folder | Contents |
|---|---|
| `kit-src/` | Kit source: `build.py` (page and template definitions), `el.py` (Elementor JSON helpers), `elementor.css` (Site Settings custom CSS), `svg/` (illustrations) |
| `dist/` | Built kit `.zip` files, one per version. Import these into WordPress |
| `tools/illustrations/` | Python scripts that generate the SVG illustrations |
| `prototype/` | Static HTML preview of every page (open `prototype/index.html`) |

## Build a new version

```bash
cd kit-src
# 1. bump VERSION at the top of build.py
# 2. make your changes (build.py for content/structure, elementor.css for styling)
python3 build.py        # writes dist/good-to-grow-therapy-kit-v<VERSION>.zip
```

Then add an entry to `CHANGELOG.md`, commit, and tag:

```bash
git add -A
git commit -m "v1.0.1: short description"
git tag v1.0.1
git push && git push --tags
```

## Import into WordPress

1. Delete the default Sample Page and draft Privacy Policy page (and empty the trash) on a fresh site.
2. **Elementor → Tools → Website Templates → Import**, upload the zip from `dist/`, keep all parts checked.
3. **Appearance → Menus**: create **Main Menu** with About, Partner With Us, Contact.
4. **Elementor → Tools → Regenerate CSS & Data**, then purge the host cache.
5. Rank Math: noindex the three thank-you pages and exclude them from the sitemap.

**Styling-only change?** You can skip a full re-import: paste `kit-src/elementor.css` into **Site Settings → Custom CSS** (replace `{{TORN}}` with the contents of `kit-src/torn.txt`, or copy the CSS from the built zip's `site-settings.json`).

## License and credits

- **Code** (Python build scripts, CSS, SVG generators) is released under the [MIT License](LICENSE).
- **The Good to Grow Therapy name, website copy and brand** belong to Good to Grow Therapy, LLC and are **not** covered by the MIT License. Shown here as a case study with permission.
- Designed and built by Joy De Leon ([@joydlion](https://github.com/joydlion)), with Claude (Anthropic) as an AI assistant. All output was directed and reviewed by Joy.
