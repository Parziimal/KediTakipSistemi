"""
Kedi Bakım Takip Uygulaması  v4.0
WSAVA 2024 & AAFP 2020 Entegreli

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

# Bölüm başlık haritası
SECTION_TITLES = {
    "dashboard": "Pano", "profile": "Profil", "vaccine": "Aşı Takvimi",
    "calendar": "Yıllık Takvim", "guide": "Aşı Rehberi", "parasite": "Parazit Takvimi",
    "medications": "İlaç Takibi", "appointments": "Randevular", "nutrition": "Beslenme & Kilo",
    "health": "Sağlık Notları", "expenses": "Harcamalar", "stats": "İstatistikler",
    "vets": "Veterinerler",
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kedi Bakım Takip Sistemi v4.0")
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
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=T.SIDEBAR_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / başlık
        logo_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_f.pack(fill="x", padx=14, pady=(18, 10))
        ctk.CTkLabel(logo_f, text="🐾", font=ctk.CTkFont(size=26)).pack(side="left", padx=(2, 6))
        ctk.CTkLabel(logo_f, text="Hayvan Takip", font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=T.ACCENT).pack(side="left")

        # Ayırıcı çizgi
        ctk.CTkFrame(self.sidebar, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=(0, 10))

        # Hayvan listesi başlığı
        self.cat_var = ctk.StringVar()
        self._pet_btns = {}

        pet_hdr = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        pet_hdr.pack(fill="x", padx=12, pady=(0, 3))
        ctk.CTkLabel(pet_hdr, text="Hayvanlar", font=ctk.CTkFont(size=11),
                     text_color=T.TEXT_MUTED).pack(side="left")
        ctk.CTkButton(pet_hdr, text="Sil", width=36, height=22, fg_color=T.SIDEBAR_HOVER,
                      hover_color=T.ERROR, font=ctk.CTkFont(size=10),
                      command=self._del_cat).pack(side="right", padx=(3, 0))
        ctk.CTkButton(pet_hdr, text="+ Yeni", width=52, height=22, fg_color=T.ACCENT,
                      hover_color=T.ACCENT_HOVER, text_color=T.BTN_TEXT,
                      font=ctk.CTkFont(size=10, weight="bold"),
                      command=self._add_cat).pack(side="right")

        # Hayvan listesi (içerik kadar büyür)
        self._pet_list_frame = ctk.CTkFrame(
            self.sidebar, fg_color=T.CARD_BG, corner_radius=8)
        self._pet_list_frame.pack(fill="x", padx=12, pady=(0, 10))

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

        # Ayırıcı çizgi
        ctk.CTkFrame(self.sidebar, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=(0, 6))

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
        ctk.CTkLabel(self.sidebar, text="v4.0  ·  WSAVA 2024", font=ctk.CTkFont(size=9),
                     text_color=T.TEXT_MUTED).pack(side="bottom", pady=6)

        # Tema küreleri
        orb_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        orb_frame.pack(side="bottom", pady=(0, 2))
        for tkey, tdata in T.THEMES.items():
            b = ctk.CTkButton(orb_frame, text="", width=24, height=24,
                              corner_radius=12, fg_color=tdata["orb"],
                              hover_color=tdata["ACCENT_HOVER"],
                              command=lambda k=tkey: self._change_theme(k))
            b.pack(side="left", padx=3)

        # Yedekleme butonu
        ctk.CTkButton(self.sidebar, text="💾 Yedekle", width=100, height=26,
                      fg_color=T.SIDEBAR_HOVER, hover_color=T.ACCENT_DARK,
                      font=ctk.CTkFont(size=10), command=self._backup).pack(side="bottom", pady=(0, 4))

        # Sağ taraf: header + content
        right = ctk.CTkFrame(self, fg_color=T.MAIN_BG, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        self._right = right

        # Üst bilgi çubuğu
        self.header = ctk.CTkFrame(right, height=48, fg_color=T.CARD_BG, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self._header_section = ctk.CTkLabel(self.header, text="Pano",
                                            font=ctk.CTkFont(size=15, weight="bold"),
                                            text_color=T.TEXT_PRIMARY)
        self._header_section.pack(side="left", padx=20)

        self._header_sep = ctk.CTkLabel(self.header, text="›",
                                        font=ctk.CTkFont(size=14),
                                        text_color=T.TEXT_MUTED)
        self._header_sep.pack(side="left", padx=4)

        self._header_cat = ctk.CTkLabel(self.header, text="",
                                        font=ctk.CTkFont(size=13),
                                        text_color=T.ACCENT)
        self._header_cat.pack(side="left")

        # Sağ tarafta tarih
        ctk.CTkLabel(self.header, text=date.today().strftime("%d %B %Y"),
                     font=ctk.CTkFont(size=11),
                     text_color=T.TEXT_MUTED).pack(side="right", padx=20)

        # İnce ayırıcı
        ctk.CTkFrame(right, height=1, fg_color=T.BORDER).pack(fill="x")

        # Ana içerik alanı
        self.content = ctk.CTkFrame(right, fg_color=T.MAIN_BG, corner_radius=0)
        self.content.pack(fill="both", expand=True)

        # Başlangıç
        self._load_cats()
        self._show("dashboard")

    def _update_header(self, section_key):
        title = SECTION_TITLES.get(section_key, section_key)
        self._header_section.configure(text=title)
        cname = self._get_cname()
        if section_key in ("stats", "vets"):
            self._header_cat.configure(text="Tümü")
        elif cname:
            self._header_cat.configure(text=cname)
        else:
            self._header_cat.configure(text="")

    # ── Hayvan yönetimi ──────────────────────────────────────────────────────
    _PET_EMOJIS = {"cat": "🐱", "dog": "🐶", "bird": "🦜"}

    def _load_cats(self):
        cats = db.get_cats()
        self._cats = {c[1]: c[0] for c in cats}
        self._pet_btns = {}

        for w in self._pet_list_frame.winfo_children():
            w.destroy()

        if not cats:
            ctk.CTkLabel(self._pet_list_frame, text="Henüz hayvan yok",
                         font=ctk.CTkFont(size=11),
                         text_color=T.TEXT_MUTED).pack(pady=6)
            self.cat_var.set("")
            return

        for c in cats:
            cid, name = c[0], c[1]
            ptype = c[2] if len(c) > 2 else "cat"
            emoji = self._PET_EMOJIS.get(ptype, "🐾")
            btn = ctk.CTkButton(
                self._pet_list_frame, text=f"{emoji}  {name}",
                anchor="w", height=28, corner_radius=6,
                fg_color="transparent", hover_color=T.SIDEBAR_HOVER,
                text_color=T.TEXT_SECONDARY, font=ctk.CTkFont(size=12),
                command=lambda cid=cid, name=name: self._select_pet(cid, name)
            )
            btn.pack(fill="x", padx=4, pady=2)
            self._pet_btns[cid] = btn

        # Mevcut seçimi koru ya da ilk hayvanı seç
        current_name = self.cat_var.get()
        current_cid = self._cats.get(current_name)
        if current_cid and current_cid in self._pet_btns:
            self._highlight_pet(current_cid)
        else:
            first = cats[0]
            self.cat_var.set(first[1])
            self._highlight_pet(first[0])

    def _select_pet(self, cid, name):
        self.cat_var.set(name)
        self._highlight_pet(cid)
        if self._current_section:
            self._show(self._current_section)

    def _highlight_pet(self, cid):
        for c, btn in self._pet_btns.items():
            if c == cid:
                btn.configure(fg_color=T.SIDEBAR_ACTIVE, text_color=T.ACCENT)
            else:
                btn.configure(fg_color="transparent", text_color=T.TEXT_SECONDARY)

    def _get_cid(self):
        name = self.cat_var.get()
        return self._cats.get(name)

    def _get_cname(self):
        return self.cat_var.get()

    def _add_cat(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Yeni Hayvan Ekle")
        dlg.geometry("300x185")
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.configure(fg_color=T.MAIN_BG)

        cf = ctk.CTkFrame(dlg, fg_color="transparent")
        cf.pack(fill="both", expand=True, padx=20, pady=12)

        ctk.CTkLabel(cf, text="İsim:", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=0, column=0, sticky="e", padx=6, pady=7)
        name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(cf, textvariable=name_var, width=160)
        name_entry.grid(row=0, column=1, sticky="w", pady=7)

        ctk.CTkLabel(cf, text="Tür:", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=1, column=0, sticky="e", padx=6, pady=7)
        type_var = ctk.StringVar(value="🐱 Kedi")
        ctk.CTkComboBox(cf, variable=type_var,
                        values=["🐱 Kedi", "🐶 Köpek", "🦜 Kuş"],
                        width=160).grid(row=1, column=1, sticky="w", pady=7)

        bf = ctk.CTkFrame(dlg, fg_color="transparent")
        bf.pack(pady=6)

        def on_ok():
            name = name_var.get().strip()
            pet_map = {"🐱 Kedi": "cat", "🐶 Köpek": "dog", "🦜 Kuş": "bird"}
            pet_type = pet_map.get(type_var.get(), "cat")
            if name:
                cid = db.add_cat(name, pet_type)
                self._load_cats()
                self._select_pet(cid, name)
            dlg.destroy()

        ctk.CTkButton(bf, text="✓ Ekle", command=on_ok,
                      fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER,
                      text_color=T.BTN_TEXT, font=ctk.CTkFont(size=12, weight="bold"),
                      width=90).pack(side="left", padx=6)
        ctk.CTkButton(bf, text="İptal", command=dlg.destroy,
                      fg_color=T.CARD_BG, hover_color=T.SIDEBAR_HOVER,
                      text_color=T.TEXT_PRIMARY, font=ctk.CTkFont(size=12),
                      width=80).pack(side="left", padx=6)

        dlg.after(100, name_entry.focus_set)
        dlg.bind("<Return>", lambda e: on_ok())

    def _del_cat(self):
        cid = self._get_cid()
        if not cid:
            return
        name = self._get_cname()
        if messagebox.askyesno("Hayvan Sil", f"'{name}' ve tüm kayıtları silinecek.\nEmin misiniz?", parent=self):
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
        self._update_header(key)

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
            _empty_state(self._current_frame, "🐾", "Henüz hayvan eklenmemiş",
                         "Soldaki '+ Yeni' butonu ile ilk hayvanınızı ekleyin")
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

        for b in self._menu_btns.values():
            b.configure(fg_color="transparent", text_color=T.TEXT_SECONDARY)
        self._current_section = None
        self._header_section.configure(text="Arama")
        self._header_cat.configure(text=f"\"{q}\"")

        if self._current_frame:
            self._current_frame.destroy()

        results = db.search_all(cid, q)

        f = ctk.CTkFrame(self.content, fg_color="transparent")
        f.pack(fill="both", expand=True)
        self._current_frame = f

        sc = ctk.CTkScrollableFrame(f, fg_color="transparent")
        sc.pack(fill="both", expand=True)

        ctk.CTkLabel(sc, text=f"{len(results)} sonuç bulundu",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 4))
        ctk.CTkLabel(sc, text=f"\"{q}\" araması · {self._get_cname()}",
                     font=ctk.CTkFont(size=12),
                     text_color=T.TEXT_MUTED).pack(anchor="w", padx=24, pady=(0, 12))

        if not results:
            _empty_state(sc, "🔍", "Sonuç bulunamadı",
                         "Farklı anahtar kelimeler deneyebilirsiniz")
            return

        for typ, col1, col2, col3 in results:
            card = ctk.CTkFrame(sc, fg_color=T.CARD_BG, corner_radius=10)
            card.pack(fill="x", padx=24, pady=3)
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(row, text=typ, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=T.ACCENT, width=110).pack(side="left")
            ctk.CTkLabel(row, text=col1 or "—", font=ctk.CTkFont(size=12),
                         text_color=T.TEXT_PRIMARY, width=180).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=col2 or "—", font=ctk.CTkFont(size=11),
                         text_color=T.TEXT_SECONDARY, width=120).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=col3 or "", font=ctk.CTkFont(size=11),
                         text_color=T.TEXT_MUTED).pack(side="left", padx=4)

    def refresh_sidebar(self):
        """Profil kaydedilince sidebar'ı güncelle (isim değişebilir)."""
        self._load_cats()

    def on_cat_deleted(self):
        """Profil ekranından hayvan silinince listeyi güncelle."""
        self._load_cats()
        self._show("dashboard")

    # ── Tema değiştir ────────────────────────────────────────────────────────
    def _change_theme(self, theme_key):
        if T.get_current() == theme_key:
            return
        T.set_theme(theme_key)
        self.sidebar.destroy()
        self._right.destroy()
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


def _empty_state(parent, icon, title, subtitle):
    """Boş durum ekranı — güzel görsel + yönlendirme."""
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(expand=True)
    ctk.CTkLabel(f, text=icon, font=ctk.CTkFont(size=48)).pack(pady=(30, 8))
    ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=18, weight="bold"),
                 text_color=T.TEXT_PRIMARY).pack(pady=(0, 4))
    ctk.CTkLabel(f, text=subtitle, font=ctk.CTkFont(size=13),
                 text_color=T.TEXT_MUTED).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
