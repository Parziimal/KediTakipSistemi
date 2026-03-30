"""
Kedi Bakım Takip Uygulaması  v4.0
WSAVA 2024 & AAFP 2020 Entegreli  ·  Meadow Green Theme

Gereksinimler:
    pip install customtkinter Pillow matplotlib qrcode[pil] fpdf2
"""

import os
import shutil
import sys
from datetime import date
from tkinter import filedialog, messagebox, simpledialog

import customtkinter as ctk

import theme as T
import database as db
from icon import set_app_icon
from constants import SECTIONS
from frames import FRAME_MAP

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🐱 Kedi Bakım Takip Sistemi v4.0")
        self.geometry("1200x750")
        self.minsize(960, 600)
        self.configure(fg_color=T.MAIN_BG)

        db.init_db()
        set_app_icon(self)

        self._current_section = None
        self._current_frame = None
        self._build_layout()

    # ── Ana Düzen ────────────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=230, fg_color=T.SIDEBAR_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / başlık
        logo_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_f.pack(fill="x", padx=12, pady=(16, 8))
        ctk.CTkLabel(logo_f, text="🐾", font=ctk.CTkFont(size=28)).pack(side="left", padx=(4, 6))
        ctk.CTkLabel(logo_f, text="Kedi Takip", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=T.ACCENT).pack(side="left")

        # Kedi seçici
        cat_frame = ctk.CTkFrame(self.sidebar, fg_color=T.SIDEBAR_ACTIVE, corner_radius=8)
        cat_frame.pack(fill="x", padx=12, pady=(4, 12))

        sel_row = ctk.CTkFrame(cat_frame, fg_color="transparent")
        sel_row.pack(fill="x", padx=8, pady=(8, 4))
        ctk.CTkLabel(sel_row, text="Kedi:", font=ctk.CTkFont(size=12),
                     text_color=T.TEXT_SECONDARY).pack(side="left")
        self.cat_var = ctk.StringVar()
        self.cat_combo = ctk.CTkComboBox(sel_row, variable=self.cat_var, width=120,
                                         font=ctk.CTkFont(size=12),
                                         command=self._on_cat_change)
        self.cat_combo.pack(side="left", padx=6)

        btn_row = ctk.CTkFrame(cat_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=8, pady=(0, 8))
        ctk.CTkButton(btn_row, text="+ Yeni", width=65, height=26, fg_color=T.ACCENT,
                      hover_color=T.ACCENT_HOVER, text_color=T.BTN_TEXT,
                      font=ctk.CTkFont(size=11, weight="bold"),
                      command=self._add_cat).pack(side="left", padx=(0, 4))
        ctk.CTkButton(btn_row, text="Sil", width=45, height=26, fg_color=T.SIDEBAR_HOVER,
                      hover_color=T.ERROR, font=ctk.CTkFont(size=11),
                      command=self._del_cat).pack(side="left")

        # Arama kutusu
        search_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        search_f.pack(fill="x", padx=12, pady=(0, 8))
        self.search_var = ctk.StringVar()
        se = ctk.CTkEntry(search_f, textvariable=self.search_var, width=160,
                          placeholder_text="Ara...", height=30,
                          font=ctk.CTkFont(size=12))
        se.pack(side="left", fill="x", expand=True, padx=(0, 4))
        se.bind("<Return>", lambda e: self._search())
        ctk.CTkButton(search_f, text="🔍", width=34, height=30, fg_color=T.ACCENT,
                      hover_color=T.ACCENT_HOVER, text_color=T.BTN_TEXT,
                      font=ctk.CTkFont(size=14), command=self._search).pack(side="right")

        # Menü butonları
        self._menu_btns = {}
        menu_sc = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        menu_sc.pack(fill="both", expand=True, padx=0, pady=0)

        for label, key in SECTIONS:
            b = ctk.CTkButton(
                menu_sc, text=label, anchor="w", height=34,
                fg_color="transparent", hover_color=T.SIDEBAR_HOVER,
                text_color=T.TEXT_SECONDARY, font=ctk.CTkFont(size=13),
                command=lambda k=key: self._show(k))
            b.pack(fill="x", padx=8, pady=1)
            self._menu_btns[key] = b

        # Alt bilgi
        ctk.CTkLabel(self.sidebar, text="v4.0 · WSAVA 2024", font=ctk.CTkFont(size=10),
                     text_color=T.TEXT_MUTED).pack(side="bottom", pady=8)

        # Tema küreleri
        orb_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        orb_frame.pack(side="bottom", pady=(0, 4))
        for tkey, tdata in T.THEMES.items():
            b = ctk.CTkButton(orb_frame, text="", width=26, height=26,
                              corner_radius=13, fg_color=tdata["orb"],
                              hover_color=tdata["ACCENT_HOVER"],
                              command=lambda k=tkey: self._change_theme(k))
            b.pack(side="left", padx=4)

        # Yedekleme butonu
        ctk.CTkButton(self.sidebar, text="💾 Yedekle", width=100, height=28,
                      fg_color=T.SIDEBAR_HOVER, hover_color=T.ACCENT_DARK,
                      font=ctk.CTkFont(size=11), command=self._backup).pack(side="bottom", pady=(0, 4))

        # Ana içerik alanı
        self.content = ctk.CTkFrame(self, fg_color=T.MAIN_BG, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        # Başlangıç
        self._load_cats()
        self._show("dashboard")

    # ── Kedi yönetimi ────────────────────────────────────────────────────────
    def _load_cats(self):
        cats = db.get_cats()
        self._cats = {c[1]: c[0] for c in cats}
        names = [c[1] for c in cats]
        self.cat_combo.configure(values=names if names else [""])
        if names:
            if self.cat_var.get() not in names:
                self.cat_var.set(names[0])
        else:
            self.cat_var.set("")

    def _get_cid(self):
        name = self.cat_var.get()
        return self._cats.get(name)

    def _get_cname(self):
        return self.cat_var.get()

    def _on_cat_change(self, _=None):
        if self._current_section:
            self._show(self._current_section)

    def _add_cat(self):
        name = simpledialog.askstring("Yeni Kedi", "Kedi adı:", parent=self)
        if name and name.strip():
            db.add_cat(name.strip())
            self._load_cats()
            self.cat_var.set(name.strip())
            self._show(self._current_section or "dashboard")

    def _del_cat(self):
        cid = self._get_cid()
        if not cid:
            return
        name = self._get_cname()
        if messagebox.askyesno("Kedi Sil", f"'{name}' ve tüm kayıtları silinecek.\nEmin misiniz?", parent=self):
            db.delete_cat(cid)
            self._load_cats()
            self._show("dashboard")

    # ── Bölüm göster ─────────────────────────────────────────────────────────
    def _show(self, key):
        # Menü vurgulama
        for k, b in self._menu_btns.items():
            if k == key:
                b.configure(fg_color=T.SIDEBAR_ACTIVE, text_color=T.ACCENT)
            else:
                b.configure(fg_color="transparent", text_color=T.TEXT_SECONDARY)

        self._current_section = key

        # Eski frame'i kaldır
        if self._current_frame:
            self._current_frame.destroy()

        # Yeni frame oluştur
        frame_cls = FRAME_MAP.get(key)
        if frame_cls is None:
            self._current_frame = ctk.CTkFrame(self.content, fg_color="transparent")
            self._current_frame.pack(fill="both", expand=True)
            ctk.CTkLabel(self._current_frame, text="Bölüm bulunamadı.",
                         text_color=T.TEXT_MUTED).pack(pady=40)
            return

        cid = self._get_cid()
        cname = self._get_cname()

        # stats ve vets kedi bağımsız
        if key in ("stats", "vets"):
            self._current_frame = frame_cls(self.content, app=self)
        elif cid:
            self._current_frame = frame_cls(self.content, cid=cid, cname=cname, app=self)
        else:
            self._current_frame = ctk.CTkFrame(self.content, fg_color="transparent")
            self._current_frame.pack(fill="both", expand=True)
            ctk.CTkLabel(self._current_frame, text="Lütfen önce bir kedi ekleyin.",
                         text_color=T.TEXT_MUTED, font=ctk.CTkFont(size=16)).pack(pady=60)
            return

        self._current_frame.pack(fill="both", expand=True)

    # ── Arama ────────────────────────────────────────────────────────────────
    def _search(self):
        q = self.search_var.get().strip()
        if not q:
            return
        cid = self._get_cid()
        if not cid:
            return

        # Menü vurgulamasını temizle
        for b in self._menu_btns.values():
            b.configure(fg_color="transparent", text_color=T.TEXT_SECONDARY)
        self._current_section = None

        if self._current_frame:
            self._current_frame.destroy()

        results = db.search_all(cid, q)

        f = ctk.CTkFrame(self.content, fg_color="transparent")
        f.pack(fill="both", expand=True)
        self._current_frame = f

        sc = ctk.CTkScrollableFrame(f, fg_color="transparent")
        sc.pack(fill="both", expand=True)

        ctk.CTkLabel(sc, text=f"🔍  \"{q}\" için {len(results)} sonuç",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=T.ACCENT).pack(anchor="w", padx=24, pady=(18, 12))

        if not results:
            ctk.CTkLabel(sc, text="Sonuç bulunamadı.", text_color=T.TEXT_MUTED,
                         font=ctk.CTkFont(size=14)).pack(pady=30)
            return

        for typ, col1, col2, col3 in results:
            card = ctk.CTkFrame(sc, fg_color=T.CARD_BG, corner_radius=10)
            card.pack(fill="x", padx=24, pady=3)
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=8)
            ctk.CTkLabel(row, text=typ, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=T.ACCENT, width=110).pack(side="left")
            ctk.CTkLabel(row, text=col1 or "—", font=ctk.CTkFont(size=12),
                         text_color=T.TEXT_PRIMARY, width=180).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=col2 or "—", font=ctk.CTkFont(size=11),
                         text_color=T.TEXT_SECONDARY, width=120).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=col3 or "", font=ctk.CTkFont(size=11),
                         text_color=T.TEXT_MUTED).pack(side="left", padx=4)

    # ── Tema değiştir ────────────────────────────────────────────────────────
    def _change_theme(self, theme_key):
        if T.get_current() == theme_key:
            return
        T.set_theme(theme_key)
        # Tüm UI'ı yeniden çiz
        self.sidebar.destroy()
        self.content.destroy()
        self.configure(fg_color=T.MAIN_BG)
        self._current_frame = None
        self._build_layout()

    # ── Yedekleme ────────────────────────────────────────────────────────────
    def _backup(self):
        dest = filedialog.askdirectory(title="Yedek Klasörü Seçin", parent=self)
        if not dest:
            return
        ts = date.today().isoformat()
        backup_name = f"kedi_bakim_yedek_{ts}.db"
        backup_path = os.path.join(dest, backup_name)
        try:
            shutil.copy2(db.DB_PATH, backup_path)
            messagebox.showinfo("Yedekleme", f"Yedek kaydedildi:\n{backup_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Hata", f"Yedekleme başarısız:\n{e}", parent=self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
