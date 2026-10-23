# ahmetkasif.github.io

Kişisel akademik sayfa. Jekyll ile yazıldı, GitHub Pages doğrudan derler (kurulum gerekmez).
İçerik HTML'de değil, `_data/*.yml` dosyalarında durur. Yeni makale, sunum veya proje eklemek
bir YAML bloğu kopyalamaktan ibarettir.

## Yapı

```
_data/
  profile.yml         ad, unvan, kısa tanıtım, ilgi alanları, iletişim, ikon bağlantıları
  publications.yml    dergi makaleleri + konferans bildirileri
  presentations.yml   sunumlar
  projects.yml        projeler
  service.yml         hakem profilleri (WoS, DergiPark), hakemlik yapılan dergiler, jüri görevleri
  i18n.yml            arayüz metinleri (menü, başlıklar, düğmeler) İngilizce + Türkçe
assets/
  img/profile.jpg     ← profil fotoğrafını buraya yükle (yoksa fotoğraf alanı gösterilmez)
  img/bg.jpg          İSTEĞE BAĞLI kendi arka plan fotoğrafın (yoksa mavi gradyan kullanılır)
  pdf/                sunum PDF'leri
  css/main.css        stiller (renkler en üstteki :root bloğunda)
_layouts/, _includes/ sayfa iskeleti
index.html            İngilizce sayfa (/)
tr/index.html         Türkçe sayfa (/tr/)
_includes/home.html   iki sayfanın ortak gövdesi, bölümlerin şablonu (nadiren değişir)
tools/check.py        veri denetimi
```

## İlk yayına alma

1. Bu klasörün içeriğini `ahmetkasif.github.io` reposuna kopyala. Eski `images/` klasörünü, eski
   `LICENSE.txt` dosyasını (yerine `LICENSE` ve `NOTICE.md` geliyor), eski `assets/js/` ve
   `assets/css/` dosyalarını sil (yenileri zaten bu pakette).
2. Fotoğrafını `assets/img/profile.jpg` olarak ekle: kare kırp, 400×400 px, ~100 KB altı. Bu boyutta sayfa hızını
   etkilemez (ekranda 168 px görünür, 400 px yüksek çözünürlüklü ekranlara yeter). `check.py` 150 KB üstünü uyarır.
3. GitHub'da **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch
   `main` (veya kullandığın dal), klasör `/ (root)`.
4. Commit/push et. Yayın 1-2 dakika içinde güncellenir.

## Günlük güncelleme iş akışı

Her güncelleme aynı üç adım: **dosyayı aç → bloğu ekle/düzenle → commit.** GitHub'ın web arayüzü
yeterli (telefondan bile olur): dosyayı aç, kalem simgesine bas, düzenle, *Commit changes*.

| Ne oldu? | Ne yapacaksın? |
|---|---|
| Makale kabul edildi | `publications.yml`'in **en üstüne** yeni blok ekle, `status: "In press"` yaz |
| Makale yayımlandı | `status` satırını sil, `year`'ı düzelt, `# doi:` satırının başındaki `#` işaretini kaldırıp **yalnızca DOI'yi** yaz (örn. `doi: "10.1109/TR.2021.1234567"`; `https://doi.org/` yazma, otomatik eklenir) |
| Yeni sunum | `presentations.yml`'in en üstüne ekle. PDF varsa önce `assets/pdf/` altına yükle, sonra `pdf: "dosya-adi.pdf"` yaz |
| Yeni proje | `projects.yml`'in en üstüne ekle (devam edenler üstte) |
| Yeni hakemlik yapılan dergi | `service.yml` → `reviews` altına `journal:` (ve varsa `url:`) ile blok ekle |
| WoS / DergiPark profil adresi değişti | `service.yml` → `profiles` |
| Unvan / bio / iletişim değişti | `profile.yml` |

Örnek yeni makale bloğu:

```yaml
- type: journal            # journal veya conference
  title: "Makale başlığı"
  venue: "Dergi adı"
  year: 2026
  status: "In press"       # isteğe bağlı
  url: "https://doi.org/..."   # isteğe bağlı
```

Kurallar:

- **Sıra = ekrandaki sıra.** Yeni girdiyi listenin en üstüne ekle. Aynı yıldaki girdilerin yılı sayfada
  bir kez gösterilir.
- Metinleri **çift tırnak içine** al, özellikle `:` veya `&` içerenleri.
- Girintiyi **boşlukla** yap (Tab kullanma), bloğun satırları aynı hizada olsun.
- Her bloğun başında `- ` işareti bulunur, diğer satırlar iki boşlukla girintilenir.

## Türkçe / İngilizce

Site iki ayrı sayfadan oluşur: `/` (İngilizce) ve `/tr/` (Türkçe). Menüdeki **EN | TR** düğmesi ikisi arasında
geçiş yapar. Arama motorları için `hreflang` bağlantıları otomatik eklenir.

- **Kural:** Her metnin İngilizcesi normal alandadır, Türkçesi aynı adın sonuna `_tr` eklenerek yazılır.
  Örnek: `description:` / `description_tr:`. `_tr` yoksa Türkçe sayfada İngilizcesi görünür.
- **Çevrilmeyenler:** Makale başlıkları, dergi ve konferans adları, kişi/kurum adları olduğu gibi kalır.
- **Çevrilenler:** `profile.yml` (unvan, bölüm, tanıtım, ilgi alanları, hobi notu, adres, eğitim etiketleri),
  `presentations.yml` (`description_tr`), `projects.yml` (`title_tr`, `org_tr`), `service.yml` (jüri için `event_tr`,
  `kind_tr`, `role_tr`), yayınlarda isteğe bağlı `status_tr`.
- **Arayüz metinleri** (menü, bölüm başlıkları, düğme etiketleri, alt bilgi, ay adları) `_data/i18n.yml` içindedir.
  `en` ve `tr` bölümlerinin anahtarları aynı olmalı; `tools/check.py` eksiği yakalar.
- Yeni makale eklemek için çeviri gerekmez. Yeni sunum eklerken `description_tr` yazmayı unutma, yoksa Türkçe
  sayfada İngilizce görünür (betik uyarı verir).
- Sayfa yapısı değişirse yalnızca `_includes/home.html` düzenlenir, iki dil birden güncellenir.

### Hata önleme: `tools/check.py`

Repo her push'ta otomatik denetlenir (**Actions** sekmesi → "Veri denetimi"). Yeşil ✓ ise sorun yok.
Kırmızı ✗ ise tıklayıp hangi satırda hata olduğunu oku. Betik şunları yakalar: eksik zorunlu alan,
olmayan PDF, bozuk YAML, `http` ile başlamayan bağlantı, yanlış `type`, bozuk yıl sırası, yinelenen
başlık, yazım hatası olabilecek alan adı. Bilgisayarında da çalıştırabilirsin:

```bash
pip install pyyaml
python tools/check.py
```

### Cursor ile güncelleme (isteğe bağlı)

Repoyu Cursor'da açıp şöyle bir istek yeterli:
*"`_data/publications.yml` en üstüne şu makaleyi ekle: <başlık, dergi, yıl, DOI>. Mevcut girdilerin
biçimini koru, sonra `python tools/check.py` çalıştır."*

## Yerelde önizleme (isteğe bağlı)

Ruby ile:

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

Docker ile (Windows PowerShell, proje klasöründeyken). `Gemfile` Docker imajıyla uyumsuz olduğundan önce adını
değiştir (`Rename-Item Gemfile Gemfile.bak`), işin bitince geri al:

```powershell
docker run --rm -p 4000:4000 -v "${PWD}:/srv/jekyll" jekyll/jekyll jekyll serve --host 0.0.0.0
```

Yerel önizleme, GitHub'ın canlı yayınından yavaş hissettirebilir (Windows'ta Docker dosya paylaşımı yavaştır). Asıl
hız ölçütü yayındaki sitedir.

## Görünümü değiştirmek

- Renkler: `assets/css/main.css` en üst `:root` bloğu (`--ak-primary`, `--ak-accent`). Koyu tema aynı dosyada
  `[data-bs-theme="dark"]` altında.
- Arka plan: varsayılan olarak görselsiz, sisli mavi bir gradyan kullanılır (`main.css` → `body::before`). Kendi
  fotoğrafını kullanmak için `assets/img/bg.jpg` olarak yükle (1920-2048 px genişlik, 150 KB altı iyi olur,
  **hakkı sende olan** bir görsel seç). Dosya varsa otomatik kullanılır, silersen gradyana döner.
- Yeni bölüm: `index.html` içindeki bir bölümü kopyala, `_includes/nav.html`'e menü bağlantısını ekle.
- Ek ikon bağlantısı (GitHub, ORCID…): `profile.yml` → `links`. İkon adları: https://icons.getbootstrap.com
- Bootstrap, ikonlar ve Raleway yazı tipi `assets/` altında kendi sunucundan yüklenir (CDN yok).

## Sorun giderme

- **Değişiklik görünmüyor:** Actions sekmesinde *pages build and deployment* tamamlandı mı? Tarayıcıda
  Ctrl+F5 dene.
- **Sayfa bozuk / stiller yok:** `_config.yml` içinde `baseurl: ""` olmalı (kullanıcı sitesi).
- **Actions kırmızı:** Hata mesajı hangi dosya ve girdiyi gösteriyor, ona bak (yukarıdaki kurallar).
- **E-posta adresleri:** Sayfa kaynağında bütün hâlde yazmaz, tarayıcıda birleştirilir; JavaScript kapalıysa
  `ad [at] alanadi` biçiminde görünür.

## Lisans

- **Kod: MIT** (`LICENSE`). Kapsamı `NOTICE.md` içinde dosya dosya yazılı.
- **Diğer her şey: tüm hakları saklıdır.** Yani `_data/` içindeki metinler, `assets/img/` altındaki görseller
  (fotoğrafın dahil) ve `assets/pdf/` altındaki sunumlar izinsiz kullanılamaz.
- Bootstrap, Bootstrap Icons ve Raleway kendi lisanslarıyla gelir (`THIRD_PARTY_LICENSES.md`). Bu dosyayı silme.
- Makalelerin telifi yayıncılardadır, sitede yalnızca DOI/yayıncı bağlantısı verilir; makale PDF'lerini siteye koyma.
- `LICENSE` içindeki telif yılı 2026. Kodun ilk yazıldığı yıl daha eskiyse `2017-2026` gibi bir aralık yaz.
- Alt bilgideki "Site code: MIT license" bağlantısı `_config.yml` içindeki `repo_url` değerinden gelir.

## Notlar

- Tanıtım yazısı (`bio`, `bio_tr`) `profile.yml` içinde paragraf listesidir, her paragraf ayrı bir `- "..."` satırıdır.
- Satranç gibi kısa açıklamalar (`note`, `note_tr`) bağlantının üzerine gelince ipucu balonu olarak görünür.
