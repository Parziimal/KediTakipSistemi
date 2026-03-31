# Hayvan Bakım Takip Sistemi v4.5

Python + CustomTkinter + SQLite3 masaüstü uygulaması. Kedi, köpek ve kuş için sağlık takibi.

## Teknoloji
- Python 3.14, customtkinter, SQLite3
- Opsiyonel: Pillow, matplotlib, qrcode, fpdf2
- Windows 11, dark theme

## Mimari
Modüler yapı: main.py (App sınıfı + sidebar) → frames/ (15 bölüm her biri ayrı dosya) → database.py (CRUD) → theme.py (6 dinamik tema)

## Önemli Dosyalar
- `theme.py`: 6 tema (Teal / The Lab / Pastel / Clinical / Earth / GitHub), `set_theme()` ile runtime değişim
- `constants.py`: WSAVA 2024 & AAFP 2020 & AAHA 2022 & AAV aşı verileri, ırk/renk/kategori listeleri, SECTIONS + SECTION_MAP + SECTION_GROUPS menü yapısı
- `database.py`: 10 tablo (cats, vaccines, parasite_logs, weight_logs, health_notes, expenses, vets, medications, appointments, gallery) + search_all() + `transaction()` context manager
- `utils.py`: _card() hover efektli, _btn() tema uyumlu, _empty() boş durum ekranı, DatePicker widget (tarih validasyonlu)
- `frames/__init__.py`: FRAME_MAP sözlüğü tüm 15 bölümü eşler

## Bölümler (15 adet)
| Key | Frame | Tip |
|-----|-------|-----|
| dashboard | DashboardFrame | hayvan bazlı |
| profile | ProfileFrame | hayvan bazlı |
| vaccine | VaccineFrame | hayvan bazlı |
| calendar | CalendarFrame | hayvan bazlı |
| guide | GuideFrame | hayvan bazlı |
| parasite | ParasiteFrame | hayvan bazlı |
| medications | MedicationsFrame | hayvan bazlı |
| appointments | AppointmentsFrame | hayvan bazlı |
| nutrition | NutritionFrame | hayvan bazlı |
| health | HealthFrame | hayvan bazlı |
| expenses | ExpenseFrame | hayvan bazlı |
| gallery | GalleryFrame | hayvan bazlı |
| stats | StatsFrame | bağımsız |
| vets | VetFrame | bağımsız |
| settings | SettingsFrame | bağımsız |

Bağımsız bölümler `_show()` içinde `key in ("stats", "vets", "settings")` ile algılanır.

## Kullanıcı Tercihleri
- Türkçe arayüz
- Şirin/pastel renk tonları tercih ediyor
- Buton yazıları okunabilir olmalı (koyu text on accent)
- Profesyonel görünüm: header bar, hover efekt, boş durum ekranları, tipografi hiyerarşisi
- Token tasarrufu önemli: kısa cevaplar, toplu işlem

## Geliştirme Notları
- Yeni bölüm (3 adım): frames/yeni.py → frames/__init__.py FRAME_MAP → constants.py SECTION_MAP + SECTION_GROUPS
  - `SECTION_TITLES` main.py'de `SECTION_MAP`'ten **otomatik** türetilir, manuel eklemeye gerek yok
- Hayvan bağımsız bölüm eklenirse main.py `_show()` içindeki `("stats", "vets", "settings")` tuple'ına ekle
- DB şema değişikliğinde kedi_bakim.db silinip yeniden oluşturulabilir (CREATE IF NOT EXISTS)
- `GELISTIRICI_REHBERI.md` dosyasında detaylı şablonlar var
- Çok adımlı DB işlemleri için `with db.transaction() as c:` kullan
- DatePicker.get() otomatik tarih validasyonu yapar (Şubat 31 → Şubat 28 gibi)
- Frame geçişlerinde double-buffer uygulanır: yeni frame pack edilir, sonra eski destroy edilir
