# Kedi Bakım Takip Sistemi — Geliştirici Rehberi

## Proje Yapısı

```
KediTakipSistemi/
├── main.py           # Uygulama girişi, App sınıfı, sidebar, header, tema, arama
├── theme.py          # 3 tema paleti (Teal/Gece/Pastel) + set_theme() ile dinamik değişim
├── constants.py      # Sabitler: ırklar, aşı kılavuzu (WSAVA/AAFP), parazit takvimi, menü listesi
├── database.py       # SQLite CRUD — 10 tablo, tüm veri işlemleri burada
├── utils.py          # Yardımcı widget'lar: _card(), _btn(), _title(), _empty(), DatePicker
├── icon.py           # Otomatik kedi pati ikonu oluşturucu (.ico)
└── frames/           # Her bölüm ayrı dosya
    ├── __init__.py       # Tüm frame'leri import eder, FRAME_MAP sözlüğü
    ├── dashboard.py      # Pano — özet kartlar, acil uyarılar, tıklanabilir kartlar
    ├── profile.py        # Profil — fotoğraf, QR kod, kedi bilgileri
    ├── vaccine.py        # Aşı Takvimi — WSAVA/AAFP bazlı
    ├── calendar_view.py  # Yıllık Takvim — Canvas ile 12 aylık grid
    ├── guide.py          # Aşı Rehberi — bilimsel referans
    ├── parasite.py       # Parazit Takvimi
    ├── medications.py    # İlaç Takibi
    ├── appointments.py   # Randevular
    ├── nutrition.py      # Beslenme & Kilo + mama hesaplayıcı + grafik
    ├── health.py         # Sağlık Notları
    ├── expenses.py       # Harcamalar
    ├── stats.py          # İstatistikler + pasta grafik
    └── vets.py           # Veteriner Rehberi
```

## Yeni Bölüm Ekleme (4 Adım)

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

### 2. frames/__init__.py'ye ekle:
```python
from frames.yeni_bolum import YeniBolumFrame
# FRAME_MAP'e ekle:
"yeni_bolum": YeniBolumFrame,
```

### 3. constants.py → SECTIONS listesine ekle:
```python
("🆕  Yeni Bölüm", "yeni_bolum"),
```

### 4. main.py → SECTION_TITLES'a ekle:
```python
"yeni_bolum": "Yeni Bölüm",
```

## Yeni DB Tablosu Ekleme

### 1. database.py → init_db() içine CREATE TABLE ekle
### 2. Aynı dosyaya CRUD fonksiyonları ekle (get_, add_, delete_)
### 3. Arama için search_all() fonksiyonuna yeni sorgu ekle

## Tema Sistemi

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
Küre otomatik eklenir (main.py THEMES üzerinde döner).

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
| `DatePicker(parent)` | Tarih seçici | Form'lar |

## Sık Yapılan İşlemler

**Kart rengi değiştir:** theme.py → ilgili ACCENT/CARD_BG değerini değiştir
**Yeni mama tipi ekle:** constants.py → FOOD_TYPES listesine ekle
**Yeni harcama kategorisi:** constants.py → EXPENSE_CATEGORIES + theme.py → EXPENSE_COLORS
**Font boyutu:** utils.py → _title/_lbl içindeki size değerini değiştir

## Çalıştırma

```bash
pip install customtkinter Pillow matplotlib qrcode[pil] fpdf2
cd KediTakipSistemi
python main.py
```

## Notlar
- DB dosyası: kedi_bakim.db (aynı klasörde otomatik oluşur)
- Fotoğraflar: photos/ klasörüne kopyalanır
- CSV export: exports/ klasörüne kaydedilir
- Opsiyonel kütüphaneler: Pillow (fotoğraf), matplotlib (grafik), qrcode (QR kod)
- Uygulama bunlar olmadan da çalışır, sadece ilgili özellikler devre dışı kalır
