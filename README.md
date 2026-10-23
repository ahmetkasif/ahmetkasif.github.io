# ahmetkasif.github.io

Source of my personal academic website: <https://ahmetkasif.github.io/> ([Türkçe](https://ahmetkasif.github.io/tr/)).

It is a small [Jekyll](https://jekyllrb.com/) site that GitHub Pages builds directly. All content lives in YAML
files under `_data/`; the templates render it in English and Turkish.

## Features

- Content as data: publications (with DOI buttons), presentations, projects, peer-review and jury service
- English and Turkish pages generated from the same templates
- Light and dark theme, responsive layout, print stylesheet
- Bootstrap 5.3, Bootstrap Icons and Raleway are self-hosted: no CDN, no jQuery, no tracking
- `tools/check.py` validates the data files and runs on every push (GitHub Actions)

## Repository layout

```
_data/                 profile, publications, presentations, projects, service, i18n (YAML)
_includes/             home.html (page body shared by both languages), nav.html, entry-links.html
_layouts/default.html  page shell
index.html, tr/        English and Turkish home pages (thin wrappers around home.html)
assets/                css, js, fonts, img, pdf, vendor (Bootstrap, Bootstrap Icons)
tools/check.py         data validation
```

## Run locally

Requires Ruby. The `Gemfile` uses the same gem set as GitHub Pages.

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

Validate the data files (needs Python and PyYAML):

```bash
pip install pyyaml
python tools/check.py
```

## Data model

| File | What it holds |
|---|---|
| `profile.yml` | name, title, affiliation, bio (list of paragraphs), links, education, interests, hobbies, contact |
| `publications.yml` | `type` (`journal` or `conference`), `title`, `venue`, `year`; optional `doi`, `url`, `pdf`, `code`, `status` |
| `presentations.yml` | `title`, `description`, `year`; optional `pdf`, `url` |
| `projects.yml` | `title`, `org`, `period`; optional `url`, `org_url` |
| `service.yml` | reviewer `profiles`, reviewed `reviews`, `jury` roles |
| `i18n.yml` | interface strings (menu, headings, buttons) per language |

Lists are rendered in file order, newest first. Translations use a suffix: English is the base field and the Turkish
text goes into the same field with `_tr` (for example `description` and `description_tr`). A missing `_tr` falls back
to English.

## Using this as a template

The code is MIT licensed, the content is not (see [License](#license)). To build your own site from it:

1. Fork or clone the repository.
2. **Remove everything personal.** Replace the files in `_data/` (except `i18n.yml`) with your own, delete
   `assets/pdf/*`, and replace everything in `assets/img/` (portrait, background, favicon). Rewrite `NOTICE.md` for
   your own site.
3. Edit `_config.yml`: `title`, `url` (`https://<username>.github.io`), `repo_url`. For a user site keep
   `baseurl: ""`.
4. Optional images: add `assets/img/profile.jpg` (square, about 400 px, under 100 KB) for the portrait and
   `assets/img/bg.jpg` for a background photo. Without them the portrait block is hidden and a plain gradient is used.
5. For a single-language site, delete `tr/`, the language switch in `_includes/nav.html` and the `hreflang` links in
   `_layouts/default.html`. For another language, add a section to `_data/i18n.yml`, a `<lang>/index.html` wrapper
   and `_<lang>` fields; the switch in `nav.html` lists EN and TR explicitly.
6. Keep `LICENSE` and `THIRD_PARTY_LICENSES.md` with the code, and add your own copyright line if you like.
7. Publish with **Settings → Pages → Deploy from a branch**.

Comments inside the data files and `tools/check.py` output are in Turkish; the field names are self-explanatory and
the check script reports missing or unknown fields.

## License

| Part | License |
|---|---|
| Source code (templates, styles, scripts, tooling, configuration, this README, the interface strings in `_data/i18n.yml`) | [MIT](LICENSE) |
| Content: text and data in `_data/`, images in `assets/img/`, slides and documents in `assets/pdf/` | All rights reserved |
| Bootstrap, Bootstrap Icons, Raleway | Their own licenses, see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) |

The exact scope is listed in [NOTICE.md](NOTICE.md). A public repository is not a license: GitHub's Terms of Service
let others view and fork public repositories on GitHub, but that grants no right to reuse the content (biography,
publication list, photographs, slides) elsewhere. Papers linked from the site belong to their publishers and authors.
For any other use of the content, please ask first.
