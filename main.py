"""
Hayvan Bakım Takip Uygulaması  v4.5
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
from constants import SECTION_MAP, SECTION_GROUPS
from frames import FRAME_MAP

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECTION_TITLES = {k: v[1] for k, v in SECTION_MAP.items()}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hayvan Bakım Takip Sistemi v4.5")
        self.geometry("1200x750")
        self.minsize(960, 600)
        self.configure(fg_color=T.MAIN_BG)

        db.init_db()
        set_app_icon(self)

        self._current_section = None
        self._current_frame = None
        self._build_layout()

    # ── Ana Düzen ────────────────────────────────────────────────────────────
    def _build_layout(self, initial_section="dashboard"):
        # ── Sidebar ──────────────────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=T.SIDEBAR_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_f.pack(fill="x", padx=14, pady=(16, 8))
        ctk.CTkLabel(logo_f, text="🐾", font=ctk.CTkFont(size=24)).pack(side="left", padx=(2, 6))
        ctk.CTkLabel(logo_f, text="Hayvan Takip", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=T.ACCENT).pack(side="left")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=(0, 8))

        # ── Hayvan listesi ────────────────────────────────────────────────────
        self.cat_var = ctk.StringVar()
        self._pet_btns = {}

        pet_hdr = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        pet_hdr.pack(fill="x", padx=12, pady=(0, 3))
        ctk.CTkLabel(pet_hdr, text="HAYVANLAR", font=ctk.CTkFont(size=10),
                     text_color=T.TEXT_MUTED).pack(side="left")
        ctk.CTkButton(pet_hdr, text="+ Yeni", width=52, height=22,
                      fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER,
                      text_color=T.BTN_TEXT, font=ctk.CTkFont(size=10, weight="bold"),
                      command=self._add_cat).pack(side="right")

        self._pet_list_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self._pet_list_frame.pack(fill="x", padx=8, pady=(0, 8))

        # ── Arama ────────────────────────────────────────────────────────────
        search_f = ctk.CTkFrame(self.sidebar, fg_color=T.CARD_BG, corner_radius=8)
        search_f.pack(fill="x", padx=12, pady=(0, 6))
        self.search_var = ctk.StringVar()
        se = ctk.CTkEntry(search_f, textvariable=self.search_var,
                          placeholder_text="Kayıtlarda ara...", height=30, border_width=0,
                          fg_color="transparent", font=ctk.CTkFont(size=12))
        se.pack(side="left", fill="x", expand=True, padx=(8, 0))
        se.bind("<Return>", lambda e: self._search())
        ctk.CTkButton(search_f, text="🔍", width=30, height=30,
                      fg_color="transparent", hover_color=T.SIDEBAR_HOVER,
                      text_color=T.ACCENT, font=ctk.CTkFont(size=14),
                      command=self._search).pack(side="right", padx=2)

        ctk.CTkFrame(self.sidebar, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=(0, 4))

        # ── Gruplu / katlanabilir menü ────────────────────────────────────────
        self._menu_btns = {}
        self._menu_indicators = {}
        self._group_expanded = {}
        self._group_containers = {}

        menu_sc = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent",
                                         scrollbar_button_color=T.BORDER,
                                         scrollbar_button_hover_color=T.SIDEBAR_HOVER)
        menu_sc.pack(fill="both", expand=True, padx=0, pady=0)

        for group_name, keys in SECTION_GROUPS:
            # İlk grup (Hayvan) açık, diğerleri kapalı
            expanded = (group_name == "Hayvan")
            self._group_expanded[group_name] = expanded

            # Grup başlığı — tıklanabilir
            hdr = ctk.CTkFrame(menu_sc, fg_color="transparent", cursor="hand2")
            hdr.pack(fill="x", padx=6, pady=(6, 0))

            arrow_lbl = ctk.CTkLabel(hdr, text="▾" if expanded else "›",
                                     font=ctk.CTkFont(size=10, weight="bold"),
                                     text_color=T.TEXT_MUTED, width=14)
            arrow_lbl.pack(side="left", padx=(6, 2))
            ctk.CTkLabel(hdr, text=group_name.upper(),
                         font=ctk.CTkFont(size=9, weight="bold"),
                         text_color=T.TEXT_MUTED).pack(side="left")

            # İçerik konteyneri
            container = ctk.CTkFrame(menu_sc, fg_color="transparent")
            if expanded:
                container.pack(fill="x", pady=(1, 0))
            self._group_containers[group_name] = container

            # Tıklama işlevi (closure)
            def _make_toggle(gname, cont, arrow):
                def toggle(e=None):
                    if self._group_expanded[gname]:
                        cont.pack_forget()
                        arrow.configure(text="›")
                        self._group_expanded[gname] = False
                    else:
                        # Konteyneri doğru yere ekle (kendi grubunun altına)
                        cont.pack(fill="x", pady=(1, 0),
                                  after=arrow.master)
                        arrow.configure(text="▾")
                        self._group_expanded[gname] = True
                return toggle

            fn = _make_toggle(group_name, container, arrow_lbl)
            hdr.bind("<Button-1>", fn)
            arrow_lbl.bind("<Button-1>", fn)
            for child in hdr.winfo_children():
                child.bind("<Button-1>", fn)

            # Menü butonları (konteynerin içine)
            for key in keys:
                icon, label = SECTION_MAP[key]

                row = ctk.CTkFrame(container, fg_color="transparent", corner_radius=7)
                row.pack(fill="x", padx=6, pady=1)

                ind = ctk.CTkFrame(row, width=3, height=32, fg_color="transparent", corner_radius=2)
                ind.pack(side="left", padx=(2, 0))
                ind.pack_propagate(False)

                btn = ctk.CTkButton(
                    row, text=f"{icon}  {label}", anchor="w", height=32,
                    fg_color="transparent", hover_color=T.SIDEBAR_HOVER,
                    text_color=T.TEXT_SECONDARY, font=ctk.CTkFont(size=12),
                    command=lambda k=key: self._show(k))
                btn.pack(side="left", fill="x", expand=True, padx=(2, 4))

                self._menu_btns[key] = btn
                self._menu_indicators[key] = ind

        # ── Alt kısım ─────────────────────────────────────────────────────────
        bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=12, pady=(4, 10))

        # Yedekle + Tema butonu yan yana
        ctk.CTkButton(bottom, text="💾 Yedekle", height=28,
                      fg_color=T.SIDEBAR_HOVER, hover_color=T.ACCENT_DARK,
                      text_color=T.TEXT_SECONDARY, font=ctk.CTkFont(size=11),
                      command=self._backup).pack(side="left", fill="x", expand=True, padx=(0, 4))

        ctk.CTkButton(bottom, text="🎨", width=32, height=28,
                      fg_color=T.SIDEBAR_HOVER, hover_color=T.ACCENT_DARK,
                      text_color=T.TEXT_SECONDARY, font=ctk.CTkFont(size=14),
                      command=lambda: self._show("settings")).pack(side="right")

        ctk.CTkLabel(self.sidebar, text="v4.5  ·  WSAVA 2024",
                     font=ctk.CTkFont(size=9), text_color=T.TEXT_MUTED).pack(side="bottom", pady=(0, 4))

        # ── Sağ alan ─────────────────────────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=T.MAIN_BG, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        self._right = right

        self.header = ctk.CTkFrame(right, height=48, fg_color=T.CARD_BG, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self._header_section = ctk.CTkLabel(self.header, text="Pano",
                                            font=ctk.CTkFont(size=15, weight="bold"),
                                            text_color=T.TEXT_PRIMARY)
        self._header_section.pack(side="left", padx=20)

        ctk.CTkLabel(self.header, text="›", font=ctk.CTkFont(size=14),
                     text_color=T.TEXT_MUTED).pack(side="left", padx=4)

        self._header_cat = ctk.CTkLabel(self.header, text="",
                                        font=ctk.CTkFont(size=13),
                                        text_color=T.ACCENT)
        self._header_cat.pack(side="left")

        ctk.CTkLabel(self.header, text=date.today().strftime("%d %B %Y"),
                     font=ctk.CTkFont(size=11),
                     text_color=T.TEXT_MUTED).pack(side="right", padx=20)

        ctk.CTkFrame(right, height=1, fg_color=T.BORDER).pack(fill="x")

        self.content = ctk.CTkFrame(right, fg_color=T.MAIN_BG, corner_radius=0)
        self.content.pack(fill="both", expand=True)

        self._load_cats()
        self._show(initial_section)

    def _update_header(self, section_key):
        title = SECTION_TITLES.get(section_key, section_key)
        self._header_section.configure(text=title)
        cname = self._get_cname()
        if section_key in ("stats", "vets", "settings"):
            self._header_cat.configure(text="")
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
                         text_color=T.TEXT_MUTED).pack(pady=6, padx=8)
            self.cat_var.set("")
            return

        for c in cats:
            cid, name = c[0], c[1]
            ptype = c[2] if len(c) > 2 else "cat"
            emoji = self._PET_EMOJIS.get(ptype, "🐾")

            row = ctk.CTkFrame(self._pet_list_frame, fg_color="transparent", corner_radius=6)
            row.pack(fill="x", pady=1)

            btn = ctk.CTkButton(
                row, text=f"{emoji}  {name}", anchor="w", height=28, corner_radius=6,
                fg_color="transparent", hover_color=T.SIDEBAR_HOVER,
                text_color=T.TEXT_SECONDARY, font=ctk.CTkFont(size=12),
                command=lambda c=cid, n=name: self._select_pet(c, n))
            btn.pack(side="left", fill="x", expand=True)

            # × butonu — her zaman görünür, hover'da kırmızı
            del_btn = ctk.CTkButton(
                row, text="×", width=22, height=22, corner_radius=4,
                fg_color="transparent", hover_color=T.ERROR,
                text_color=T.TEXT_MUTED, font=ctk.CTkFont(size=15, weight="bold"),
                command=lambda c=cid, n=name: self._del_cat_by(c, n))
            del_btn.pack(side="right", padx=(0, 2))

            self._pet_btns[cid] = btn

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
        return self._cats.get(self.cat_var.get())

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

    def _del_cat_by(self, cid, name):
        if messagebox.askyesno("Hayvan Sil",
                               f"'{name}' ve tüm kayıtları silinecek.\nEmin misiniz?",
                               parent=self):
            db.delete_cat(cid)
            self._load_cats()
            self._show("dashboard")

    # ── Bölüm göster ─────────────────────────────────────────────────────────
    def _show(self, key):
        # Menü vurgulama + sol çubuk göstergesi
        for k, b in self._menu_btns.items():
            ind = self._menu_indicators.get(k)
            if k == key:
                b.configure(fg_color=T.SIDEBAR_ACTIVE, text_color=T.ACCENT,
                            font=ctk.CTkFont(size=12, weight="bold"))
                if ind:
                    ind.configure(fg_color=T.ACCENT)
            else:
                b.configure(fg_color="transparent", text_color=T.TEXT_SECONDARY,
                            font=ctk.CTkFont(size=12, weight="normal"))
                if ind:
                    ind.configure(fg_color="transparent")

        self._current_section = key
        self._update_header(key)

        old_frame = self._current_frame

        frame_cls = FRAME_MAP.get(key)
        if frame_cls is None:
            new_frame = ctk.CTkFrame(self.content, fg_color="transparent")
            ctk.CTkLabel(new_frame, text="Bölüm bulunamadı.",
                         text_color=T.TEXT_MUTED).pack(pady=40)
            new_frame.pack(fill="both", expand=True)
            self._current_frame = new_frame
            if old_frame:
                old_frame.destroy()
            return

        cid = self._get_cid()
        cname = self._get_cname()

        if key in ("stats", "vets", "settings"):
            new_frame = frame_cls(self.content, app=self)
        elif cid:
            new_frame = frame_cls(self.content, cid=cid, cname=cname, app=self)
        else:
            new_frame = ctk.CTkFrame(self.content, fg_color="transparent")
            _empty_state(new_frame, "🐾", "Henüz hayvan eklenmemiş",
                         "Soldaki '+ Yeni' butonu ile ilk hayvanınızı ekleyin")

        new_frame.pack(fill="both", expand=True)
        self._current_frame = new_frame
        if old_frame:
            old_frame.destroy()

    # ── Arama ────────────────────────────────────────────────────────────────
    def _search(self):
        q = self.search_var.get().strip()
        if not q:
            return
        cid = self._get_cid()
        if not cid:
            return

        for k, b in self._menu_btns.items():
            b.configure(fg_color="transparent", text_color=T.TEXT_SECONDARY,
                        font=ctk.CTkFont(size=12, weight="normal"))
            ind = self._menu_indicators.get(k)
            if ind:
                ind.configure(fg_color="transparent")

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
        self._load_cats()

    def on_cat_deleted(self):
        self._load_cats()
        self._show("dashboard")

    # ── Tema değiştir ────────────────────────────────────────────────────────
    def _change_theme(self, theme_key):
        if T.get_current() == theme_key:
            return
        restore_section = self._current_section or "dashboard"
        T.set_theme(theme_key)
        self.sidebar.destroy()
        self._right.destroy()
        self.configure(fg_color=T.MAIN_BG)
        self._current_frame = None
        self._build_layout(restore_section)

    # ── Yedekleme ────────────────────────────────────────────────────────────
    def _backup(self):
        dest = filedialog.askdirectory(title="Yedek Klasörü Seçin", parent=self)
        if not dest:
            return
        ts = date.today().isoformat()
        backup_path = os.path.join(dest, f"hayvan_bakim_yedek_{ts}.db")
        try:
            shutil.copy2(db.DB_PATH, backup_path)
            messagebox.showinfo("Yedekleme", f"Yedek kaydedildi:\n{backup_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Hata", f"Yedekleme başarısız:\n{e}", parent=self)


def _empty_state(parent, icon, title, subtitle):
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
