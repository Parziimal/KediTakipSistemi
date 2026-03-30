# Kedi Bakım Takip Sistemi v4.0

Python + CustomTkinter + SQLite3 masaüstü uygulaması. Loki ve Yuumi kedileri için sağlık takibi.

## Teknoloji
- Python 3.14, customtkinter, SQLite3
- Opsiyonel: Pillow, matplotlib, qrcode, fpdf2
- Windows 11, dark theme

## Mimari
Modüler yapı: main.py (App sınıfı + sidebar) → frames/ (13 bölüm her biri ayrı dosya) → database.py (CRUD) → theme.py (3 dinamik tema)

## Önemli Dosyalar
- `theme.py`: 3 tema (Teal/Gece/Pastel), `set_theme()` ile runtime değişim
- `constants.py`: WSAVA 2024 & AAFP 2020 aşı verileri, ırk/renk/kategori listeleri
- `database.py`: 10 tablo (cats, vaccines, parasite_logs, weight_logs, health_notes, expenses, vets, medications, appointments, gallery) + search_all()
- `utils.py`: _card() hover efektli, _btn() tema uyumlu, _empty() boş durum ekranı, DatePicker widget
- `frames/__init__.py`: FRAME_MAP sözlüğü tüm bölümleri eşler

## Kullanıcı Tercihleri
- Türkçe arayüz
- Şirin/pastel renk tonları tercih ediyor
- Buton yazıları okunabilir olmalı (koyu text on accent)
- Profesyonel görünüm: header bar, hover efekt, boş durum ekranları, tipografi hiyerarşisi
- Token tasarrufu önemli: kısa cevaplar, toplu işlem

## Geliştirme Notları
- Yeni bölüm: frames/yeni.py + __init__.py + constants.py SECTIONS + main.py SECTION_TITLES
- DB şema değişikliğinde kedi_bakim.db silinip yeniden oluşturulabilir (CREATE IF NOT EXISTS)
- `GELISTIRICI_REHBERI.md` dosyasında detaylı şablonlar var
