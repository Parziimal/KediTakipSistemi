# Hayvan Bakım Takip Sistemi — Geliştirici Rehberi

## Proje Yapısı

```
KediTakipSistemi/
├── main.py           # Uygulama girişi, App sınıfı, sidebar, header, tema, arama
├── theme.py          # 6 tema paleti (Teal/The Lab/Pastel/Clinical/Earth/GitHub) + set_theme() ile dinamik değişim
├── constants.py      # Sabitler: ırklar, aşı kılavuzu (WSAVA/AAFP/AAHA/AAV), SECTIONS + SECTION_MAP + SECTION_GROUPS
├── database.py       # SQLite CRUD — 10 tablo + transaction() context manager
├── utils.py          # Yardımcı widget'lar: _card(), _btn(), _title(), _empty(), DatePicker
├── icon.py           # Otomatik kedi pati ikonu oluşturucu (.ico)
└── frames/           # Her bölüm ayrı dosya
    ├── __init__.py       # Tüm frame'leri import eder, FRAME_MAP sözlüğü (15 bölüm)
    ├── dashboard.py      # Pano — özet kartlar, acil uyarılar, tıklanabilir kartlar
    ├── profile.py        # Profil — fotoğraf, QR kod, hayvan bilgileri
    ├── vaccine.py        # Aşı Takvimi — WSAVA/AAFP/AAHA bazlı
    ├── calendar_view.py  # Yıllık Takvim — Canvas ile 12 aylık grid
    ├── guide.py          # Aşı Rehberi — bilimsel referans
    ├── parasite.py       # Parazit Takvimi
    ├── medications.py    # İlaç Takibi
    ├── appointments.py   # Randevular
    ├── nutrition.py      # Beslenme & Kilo + mama hesaplayıcı + grafik
    ├── health.py         # Sağlık Notları
    ├── expenses.py       # Harcamalar
    ├── gallery.py        # Fotoğraf Galerisi (Pillow gerekli)
    ├── stats.py          # İstatistikler + pasta grafik  [hayvan bağımsız]
    ├── vets.py           # Veteriner Rehberi            [hayvan bağımsız]
    └── settings.py       # Ayarlar & Hakkında           [hayvan bağımsız]
```

## Yeni Bölüm Ekleme (3 Adım)

> **Not:** `SECTION_TITLES` main.py'de `SECTION_MAP`'ten otomatik türetilir — manuel eklemeye gerek yok.

### 1. frames/yeni_bolum.py oluştur:
```python
import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _empty

class YeniBolumFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname, self.app = cid, cname, app
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        _title(sc, text="Başlık").pack(anchor="w", padx=24, pady=(18, 10))
        # ... içerik buraya
```

### 2. frames/__init__.py → FRAME_MAP'e ekle:
```python
from frames.yeni_bolum import YeniBolumFrame
# FRAME_MAP içinde:
"yeni_bolum": YeniBolumFrame,
```

### 3. constants.py → SECTION_MAP + SECTION_GROUPS'a ekle:
```python
# SECTION_MAP sözlüğüne:
"yeni_bolum": ("🆕", "Yeni Bölüm"),

# SECTION_GROUPS içindeki ilgili gruba (örn. "Bilgi" grubuna):
("Bilgi", ["guide", "stats", "vets", "settings", "yeni_bolum"]),
```

### Hayvan Bağımsız Bölüm (stats/vets/settings gibi):
- Frame `__init__` imzası: `(self, parent, app=None, **kw)` — `cid`/`cname` yok
- `main.py → _show()` içindeki tuple'a ekle:
  ```python
  if key in ("stats", "vets", "settings", "yeni_bolum"):
  ```

## Yeni DB Tablosu Ekleme

### 1. database.py → init_db() içine CREATE TABLE ekle
### 2. Aynı dosyaya CRUD fonksiyonları ekle (get_, add_, delete_)
### 3. Arama için search_all() fonksiyonuna yeni sorgu ekle
### 4. Performans için `CREATE INDEX IF NOT EXISTS` satırı ekle

## Çok Adımlı Atomik DB İşlemi

```python
import database as db

# Tek transaction içinde birden fazla işlem — hata olursa tümü geri alınır
with db.transaction() as c:
    c.execute("INSERT INTO cats (name) VALUES (?)", ("Boncuk",))
    cat_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.execute(
        "INSERT INTO health_notes (cat_id, note_date, title, note_type) VALUES (?,?,?,?)",
        (cat_id, "2026-01-01", "İlk kayıt", "Genel")
    )
```

## Tema Sistemi

Mevcut 6 tema: `"green"` (Teal) · `"lab"` (The Lab) · `"pink"` (Pastel) · `"clinical"` (Clinical) · `"earth"` (Earth) · `"github"` (GitHub)

theme.py'deki THEMES sözlüğüne yeni tema ekle:
```python
"mavi": {
    "name": "Mavi", "orb": "#4488FF",
    "SIDEBAR_BG": "#...", "SIDEBAR_HOVER": "#...", "SIDEBAR_ACTIVE": "#...",
    "MAIN_BG": "#...", "CARD_BG": "#...", "BORDER": "#...",
    "ACCENT": "#...", "ACCENT_HOVER": "#...", "ACCENT_DARK": "#...",
    "TEXT_PRIMARY": "#...", "TEXT_SECONDARY": "#...", "TEXT_MUTED": "#...",
    "BADGE_GREEN": "#...", "BADGE_TEAL": "#...",
    "BTN_TEXT": "#...",
},
```
Küre otomatik eklenir (settings.py THEMES üzerinde döner).

## Widget Kılavuzu (utils.py)

| Fonksiyon | Ne yapar | Kullanım |
|-----------|----------|----------|
| `_title(parent, "Metin")` | Büyük başlık | Bölüm üstü |
| `_lbl(parent, "Metin", size=13, bold=True, color=T.ACCENT)` | Etiket | Her yerde |
| `_card(parent, hover=True)` | Hover efektli kart | Liste öğeleri |
| `_btn(parent, "Metin", command, primary=True)` | Buton | Form'lar |
| `_del_btn(parent, command)` | Kırmızı "Sil" butonu | Kayıt silme |
| `_empty(parent, "icon", "başlık", "alt yazı")` | Boş durum ekranı | Kayıt yokken |
| `_toast(parent, "mesaj", renk)` | Geçici bildirim | Kayıt sonrası |
| `DatePicker(parent)` | Tarih seçici (validasyonlu) | Form'lar |

### DatePicker Notları
- `dp.get()` → `"YYYY-MM-DD"` döner
- Geçersiz günleri (Şubat 31 → Şubat 28) otomatik düzeltir
- `dp.set("2026-05-15")` ile programatik değer atanabilir

## Sık Yapılan İşlemler

**Kart rengi değiştir:** theme.py → ilgili ACCENT/CARD_BG değerini değiştir
**Yeni mama tipi ekle:** constants.py → FOOD_TYPES listesine ekle
**Yeni harcama kategorisi:** constants.py → EXPENSE_CATEGORIES
**Font boyutu:** utils.py → _title/_lbl içindeki size değerini değiştir

## Çalıştırma

```bash
pip install customtkinter Pillow matplotlib qrcode[pil] fpdf2
cd KediTakipSistemi
python main.py
```

## Notlar
- DB dosyası: kedi_bakim.db (aynı klasörde otomatik oluşur)
- DB'de test verisi yok — uygulama ilk açıldığında boş gelir, kullanıcı hayvan ekler
- Fotoğraflar: photos/ klasörüne kopyalanır (mutlak yol saklanır)
- CSV export: exports/ klasörüne kaydedilir
- Opsiyonel kütüphaneler: Pillow (galeri/profil fotoğrafı), matplotlib (grafik), qrcode (QR kod)
- Uygulama bunlar olmadan da çalışır, sadece ilgili özellikler devre dışı kalır
- Frame geçişlerinde double-buffer: `new_frame.pack()` → `old_frame.destroy()` sırası titremeyi önler
