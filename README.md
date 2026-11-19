# Good to Grow Therapy · Elementor template kit

Private source for the Good to Grow Therapy website kit ("Growth Chart" design).
Built for **Elementor 4.4 + Elementor Pro** on the **Hello Elementor** theme, using stock widgets only.

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

## Notes

- Client material (build brief, copy) belongs to Good to Grow Therapy, LLC. Keep this repository **private**.
- Built with Claude (Anthropic) as an assistant; reviewed and maintained by Joy De Leon.
