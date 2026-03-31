"""Ayarlar & Hakkında bölümü."""

import os

import customtkinter as ctk

import database as db
import theme as T
from utils import _btn, _card, _lbl, _title, _toast


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.app = app
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        self._sc = sc

        _title(sc, "⚙  Ayarlar & Hakkında").pack(anchor="w", padx=24, pady=(18, 10))

        # ── Veritabanı Bilgisi ────────────────────────────────────────────────
        db_card = _card(sc)
        db_card.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(db_card, "Veritabanı", size=14, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12, 6))

        try:
            size_bytes = os.path.getsize(db.DB_PATH)
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes / 1024 / 1024:.1f} MB"
        except Exception:
            size_str = "—"

        for label, value in [
            ("Dosya", os.path.basename(db.DB_PATH)),
            ("Boyut", size_str),
            ("Konum", os.path.dirname(db.DB_PATH)),
        ]:
            r = ctk.CTkFrame(db_card, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=1)
            _lbl(r, f"{label}:", size=12, color=T.TEXT_SECONDARY).pack(side="left")
            _lbl(r, value, size=12, color=T.TEXT_MUTED).pack(side="left", padx=(6, 0))

        ctk.CTkFrame(db_card, height=10, fg_color="transparent").pack()

        # ── Veritabanı Özeti ─────────────────────────────────────────────────
        summary_card = _card(sc)
        summary_card.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(summary_card, "Kayıt Özeti", size=14, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12, 6))
        try:
            s = db.get_all_stats()
            for label, val, color in [
                ("Kayıtlı Hayvan",    s["cats"],         T.ACCENT),
                ("Toplam Aşı",        s["vaccines"],      T.ACCENT),
                ("Aktif İlaç",        s["active_meds"],   T.BADGE_ORANGE if s["active_meds"] else T.TEXT_MUTED),
                ("Bekleyen Randevu",  s["pending_apps"],  T.BADGE_ORANGE if s["pending_apps"] else T.TEXT_MUTED),
                ("Sağlık Notu",       s["health"],        T.TEXT_SECONDARY),
                ("Kilo Kaydı",        s["weights"],       T.TEXT_SECONDARY),
            ]:
                r = ctk.CTkFrame(summary_card, fg_color="transparent")
                r.pack(fill="x", padx=16, pady=2)
                _lbl(r, label, size=12, color=T.TEXT_SECONDARY).pack(side="left")
                _lbl(r, str(val), size=13, bold=True, color=color).pack(side="right")
        except Exception:
            _lbl(summary_card, "Veriler yüklenemedi.", size=11,
                 color=T.TEXT_MUTED).pack(padx=16, pady=8)

        ctk.CTkFrame(summary_card, height=10, fg_color="transparent").pack()

        # ── Tema ─────────────────────────────────────────────────────────────
        theme_card = _card(sc)
        theme_card.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(theme_card, "Tema", size=14, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12, 8))

        orb_row = ctk.CTkFrame(theme_card, fg_color="transparent")
        orb_row.pack(anchor="w", padx=16, pady=(0, 12))
        for tkey, tdata in T.THEMES.items():
            tf = ctk.CTkFrame(orb_row, fg_color="transparent")
            tf.pack(side="left", padx=10)
            ctk.CTkButton(
                tf, text="", width=44, height=44, corner_radius=22,
                fg_color=tdata["orb"], hover_color=tdata["ACCENT_HOVER"],
                command=lambda k=tkey: self.app._change_theme(k)
            ).pack()
            _lbl(tf, tdata.get("name", tkey), size=10, color=T.TEXT_MUTED).pack(pady=(3, 0))

        # ── Hakkında ─────────────────────────────────────────────────────────
        about_card = _card(sc)
        about_card.pack(fill="x", padx=24, pady=(0, 24))
        _lbl(about_card, "Uygulama Hakkında", size=14, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12, 6))

        for line, color in [
            ("Hayvan Bakım Takip Sistemi v4.5",          T.ACCENT),
            ("WSAVA 2024  ·  AAFP 2020  ·  AAHA 2022",  T.TEXT_SECONDARY),
            ("Kedi  ·  Köpek  ·  Kuş",                  T.TEXT_SECONDARY),
            ("Python 3  +  CustomTkinter  +  SQLite3",   T.TEXT_MUTED),
        ]:
            _lbl(about_card, line, size=12, color=color).pack(anchor="w", padx=16, pady=2)

        ctk.CTkFrame(about_card, height=12, fg_color="transparent").pack()
