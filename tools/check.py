#!/usr/bin/env python3
"""
_data/*.yml dosyalarını yayına almadan önce denetler.

Kullanım (repo kökünden):
    python tools/check.py

Gerekli: PyYAML  (pip install pyyaml)

HATA   → çıkış kodu 1 (GitHub Action kırmızı olur): eksik zorunlu alan, olmayan PDF, bozuk YAML vb.
UYARI  → çıkış kodu 0: sıralama bozukluğu, kullanılmayan PDF, yinelenen başlık, bilinmeyen alan (yazım hatası) vb.
"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML gerekli:  pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data")
PDF_DIR = os.path.join(ROOT, "assets", "pdf")

errors, warnings = [], []
err = lambda msg: errors.append(msg)
warn = lambda msg: warnings.append(msg)


def load(name):
    path = os.path.join(DATA, name)
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        err(f"{name}: dosya bulunamadı")
    except yaml.YAMLError as e:
        err(f"{name}: YAML sözdizimi hatası → {e}")
    return None


def check_items(name, items, required, optional, label, translatable=()):
    """Zorunlu/isteğe bağlı alanları ve bilinmeyen anahtarları denetler."""
    if not isinstance(items, list):
        err(f"{name}: en üst düzey yapı bir liste olmalı")
        return []
    good = []
    for i, it in enumerate(items, 1):
        who = f"{name} #{i} ({str(it.get(label, '?'))[:50]})" if isinstance(it, dict) else f"{name} #{i}"
        if not isinstance(it, dict):
            err(f"{who}: girdi 'anahtar: değer' biçiminde olmalı")
            continue
        for k in required:
            if it.get(k) in (None, ""):
                err(f"{who}: zorunlu alan eksik → {k}")
        for k in it:
            base = k[:-3] if k.endswith("_tr") else k
            if base not in required and base not in optional:
                warn(f"{who}: bilinmeyen alan '{k}' (yazım hatası olabilir)")
        for k in translatable:
            if it.get(k) and not it.get(k + "_tr"):
                warn(f"{who}: Türkçe karşılık yok ({k}_tr); Türkçe sayfada İngilizcesi görünecek")
        for k, v in it.items():
            if v == "" and k.removesuffix("_tr") not in required:
                err(f"{who}: '{k}' boş bırakılmış, satırı sil ya da doldur")
        for k in ("url", "org_url", "code", "count_url"):
            v = it.get(k)
            if v and not re.match(r"^https?://", str(v)):
                err(f"{who}: {k} 'http://' veya 'https://' ile başlamalı → {v}")
        good.append(it)
    return good


def check_year(name, it, key="year"):
    y = it.get(key)
    if y is None:
        return None
    if not isinstance(y, int) or not 1990 <= y <= 2100:
        err(f"{name}: '{key}' dört haneli bir yıl olmalı → {y!r}")
        return None
    return y


def check_desc_order(name, items, key="year", group=None):
    """Yıllar yeniden eskiye sıralı olmalı (aynı yıl tekrar edebilir)."""
    prev = {}
    for it in items:
        y = it.get(key)
        g = it.get(group) if group else None
        if isinstance(y, int):
            if g in prev and y > prev[g]:
                warn(f"{name}: sıralama bozuk → {y} yılı, daha eski bir girdinin altında: '{str(it.get('title', it.get('event', '')))[:50]}'")
            prev[g] = y


def check_duplicates(name, items, key="title"):
    seen = {}
    for it in items:
        t = re.sub(r"\W+", " ", str(it.get(key, "")).lower()).strip()
        if t and t in seen:
            warn(f"{name}: yinelenen başlık → '{str(it.get(key))[:60]}'")
        seen[t] = True


used_pdfs = set()


def check_doi(name, it):
    doi = it.get("doi")
    if not doi:
        return
    if not re.match(r"^10\.\d{4,9}/\S+$", str(doi)):
        err(f"{name} ({str(it.get('title'))[:40]}): 'doi' yalnızca DOI olmalı, örn. 10.1109/... "
            f"(https://doi.org/ ekleme) → {doi}")


def check_pdf(name, it):
    pdf = it.get("pdf")
    if not pdf:
        return
    used_pdfs.add(pdf)
    if "/" in str(pdf):
        err(f"{name}: 'pdf' yalnızca dosya adı olmalı (klasör yazma) → {pdf}")
    elif not os.path.isfile(os.path.join(PDF_DIR, pdf)):
        err(f"{name}: assets/pdf/ içinde bulunamadı → {pdf}")


# ---- publications ----
pubs = load("publications.yml")
if pubs is not None:
    items = check_items("publications.yml", pubs, ["type", "title", "venue", "year"],
                        ["status", "doi", "url", "pdf", "code"], "title")
    for it in items:
        if it.get("type") not in ("journal", "conference"):
            err(f"publications.yml ({str(it.get('title'))[:40]}): type 'journal' veya 'conference' olmalı → {it.get('type')!r}")
        check_year("publications.yml", it)
        check_doi("publications.yml", it)
        check_pdf("publications.yml", it)
    check_desc_order("publications.yml", items, group="type")
    check_duplicates("publications.yml", items)

# ---- presentations ----
pres = load("presentations.yml")
if pres is not None:
    items = check_items("presentations.yml", pres, ["title", "description", "year"], ["pdf", "url"], "title",
                        translatable=["description"])
    for it in items:
        check_year("presentations.yml", it)
        check_pdf("presentations.yml", it)
    check_desc_order("presentations.yml", items)
    check_duplicates("presentations.yml", items)

# ---- projects ----
proj = load("projects.yml")
if proj is not None:
    items = check_items("projects.yml", proj, ["title", "org", "period"], ["url", "org_url"], "title")
    check_duplicates("projects.yml", items)

# ---- service ----
svc = load("service.yml")
if isinstance(svc, dict):
    for key in ("profiles", "reviews", "jury"):
        if key not in svc:
            err(f"service.yml: '{key}' bölümü eksik")
    check_items("service.yml (profiles)", svc.get("profiles", []), ["label", "url"], [], "label")
    check_items("service.yml (reviews)", svc.get("reviews", []), ["journal"], ["url"], "journal")
    jury = check_items("service.yml (jury)", svc.get("jury", []), ["event", "kind", "role", "year"], [], "event")
    for it in jury:
        check_year("service.yml (jury)", it)
    check_desc_order("service.yml (jury)", jury)
elif svc is not None:
    err("service.yml: 'profiles', 'reviews' ve 'jury' anahtarlarını içeren bir sözlük olmalı")

# ---- profile ----
prof = load("profile.yml")
if isinstance(prof, dict):
    for k in ("name", "title", "affiliation", "description"):
        if not prof.get(k):
            err(f"profile.yml: zorunlu alan eksik → {k}")
    for l in prof.get("links", []) or []:
        if not l.get("icon") or not l.get("title") or not (l.get("url") or l.get("email")):
            err(f"profile.yml: link girdisinde icon, title ve (url veya email) gerekli → {l}")
    for k in ("title", "affiliation", "bio", "description"):
        if prof.get(k) and not prof.get(k + "_tr"):
            warn(f"profile.yml: Türkçe karşılık yok ({k}_tr)")
    if prof.get("interests") and not prof.get("interests_tr"):
        warn("profile.yml: Türkçe karşılık yok (interests_tr)")
    for k in ("bio", "bio_tr"):
        v = prof.get(k)
        if v is not None and not (isinstance(v, list) and v and all(isinstance(x, str) and x.strip() for x in v)):
            err(f"profile.yml: '{k}' paragrafların listesi olmalı (her paragraf '- \"...\"' satırı)")
    photo = prof.get("photo")
    if photo:
        photo_path = os.path.join(ROOT, photo.lstrip("/"))
        if not os.path.isfile(photo_path):
            warn(f"profile.yml: fotoğraf dosyası henüz yok → {photo} (fotoğraf alanı gizli kalır)")
        elif os.path.getsize(photo_path) > 150 * 1024:
            warn(f"{photo}: dosya {os.path.getsize(photo_path) // 1024} KB; 400x400 piksele küçültüp ~100 KB altına indir (sayfa hızı için)")
elif prof is not None:
    err("profile.yml: bir sözlük olmalı")

# ---- i18n (arayüz metinleri) ----
i18n = load("i18n.yml")
if isinstance(i18n, dict):
    if not {"en", "tr"} <= set(i18n):
        err("i18n.yml: 'en' ve 'tr' bölümleri gerekli")
    else:
        en_keys, tr_keys = set(i18n["en"]), set(i18n["tr"])
        for k in sorted(en_keys - tr_keys):
            err(f"i18n.yml: '{k}' anahtarının Türkçesi (tr) eksik")
        for k in sorted(tr_keys - en_keys):
            err(f"i18n.yml: '{k}' anahtarının İngilizcesi (en) eksik")
        for lang in ("en", "tr"):
            if len(i18n[lang].get("months", [])) != 12:
                err(f"i18n.yml ({lang}): 'months' 12 ay içermeli")
elif i18n is not None:
    err("i18n.yml: bir sözlük olmalı")

# ---- kullanılmayan PDF'ler ----
if os.path.isdir(PDF_DIR):
    for f in sorted(os.listdir(PDF_DIR)):
        if f.lower().endswith(".pdf") and f not in used_pdfs:
            warn(f"assets/pdf/{f}: hiçbir girdi tarafından kullanılmıyor")

for w in warnings:
    print("UYARI ", w)
for e in errors:
    print("HATA  ", e)
print(f"\n{len(errors)} hata, {len(warnings)} uyarı.")
sys.exit(1 if errors else 0)
