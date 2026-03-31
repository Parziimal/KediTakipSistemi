"""Galeri bölümü — hayvan fotoğraf arşivi."""

import os
import shutil
from tkinter import filedialog

import customtkinter as ctk

import database as db
import theme as T
from utils import _btn, _card, _del_btn, _empty, _lbl, _title, _toast, confirm

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PHOTOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "photos")
THUMB_SIZE = (160, 160)
GRID_COLS = 4


class GalleryFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname, self.app = cid, cname, app
        self._thumbs = []  # CTkImage referanslarını tut (GC koruması)
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        self._sc = sc

        hdr = ctk.CTkFrame(sc, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(18, 10))
        _title(hdr, f"🖼  {self.cname} — Galeri").pack(side="left")
        if HAS_PIL:
            _btn(hdr, "+ Fotoğraf Ekle", self._add_photo, width=140).pack(side="right")

        if not HAS_PIL:
            _empty(sc, "🖼", "Pillow kütüphanesi gerekli",
                   "pip install Pillow komutuyla yükleyin")
            return

        self._grid = ctk.CTkFrame(sc, fg_color="transparent")
        self._grid.pack(fill="both", expand=True, padx=24)
        self._refresh()

    def _add_photo(self):
        path = filedialog.askopenfilename(
            title="Fotoğraf Seç",
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )
        if not path:
            return
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        ext = os.path.splitext(path)[1].lower() or ".jpg"
        idx = len(db.get_gallery(self.cid)) + 1
        fname = f"gallery_{self.cid}_{idx}{ext}"
        dest = os.path.join(PHOTOS_DIR, fname)
        shutil.copy2(path, dest)
        db.add_gallery_photo(self.cid, dest, "")
        self._refresh()
        _toast(self._sc, "Fotoğraf eklendi!", T.ACCENT)

    def _refresh(self):
        self._thumbs.clear()
        for w in self._grid.winfo_children():
            w.destroy()

        photos = db.get_gallery(self.cid)
        if not photos:
            _empty(self._grid, "📷", "Henüz fotoğraf yok",
                   "'+  Fotoğraf Ekle' ile fotoğraf ekleyin")
            return

        for col_idx in range(GRID_COLS):
            self._grid.columnconfigure(col_idx, weight=1)

        for i, row in enumerate(photos):
            gid, _, path, caption, added = row
            col_idx = i % GRID_COLS
            row_idx = i // GRID_COLS

            cell = _card(self._grid)
            cell.grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="nsew")

            # Thumbnail
            thumb_lbl = ctk.CTkLabel(
                cell, text="📷", font=ctk.CTkFont(size=36),
                width=THUMB_SIZE[0], height=THUMB_SIZE[1]
            )
            thumb_lbl.pack(padx=8, pady=(8, 4))

            if os.path.exists(path):
                try:
                    pil_img = Image.open(path)
                    pil_img.thumbnail(THUMB_SIZE)
                    ctk_img = ctk.CTkImage(
                        light_image=pil_img, dark_image=pil_img,
                        size=pil_img.size
                    )
                    self._thumbs.append(ctk_img)
                    thumb_lbl.configure(image=ctk_img, text="")
                except Exception:
                    thumb_lbl.configure(text="⚠ Yüklenemedi", font=ctk.CTkFont(size=11))
            else:
                thumb_lbl.configure(text="⚠ Bulunamadı", font=ctk.CTkFont(size=11))

            # Açıklama girişi
            cap_var = ctk.StringVar(value=caption or "")
            ctk.CTkEntry(
                cell, textvariable=cap_var,
                placeholder_text="Açıklama...",
                width=150, font=ctk.CTkFont(size=11)
            ).pack(padx=8, pady=(0, 2))

            # Eklenme tarihi
            _lbl(cell, added or "", size=10, color=T.TEXT_MUTED).pack(pady=(0, 4))

            # Kaydet / Sil butonları
            bf = ctk.CTkFrame(cell, fg_color="transparent")
            bf.pack(padx=8, pady=(0, 8))
            ctk.CTkButton(
                bf, text="💾", width=34, height=24,
                fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER,
                font=ctk.CTkFont(size=12),
                command=lambda g=gid, v=cap_var: self._save_caption(g, v.get())
            ).pack(side="left", padx=2)
            _del_btn(
                bf, command=lambda g=gid, p=path: self._del(g, p)
            ).pack(side="left", padx=2)

    def _save_caption(self, gid, caption):
        db.update_gallery_caption(gid, caption)
        _toast(self._sc, "Kaydedildi!", T.ACCENT)

    def _del(self, gid, path):
        if confirm(self):
            db.delete_gallery_photo(gid)
            try:
                if os.path.exists(path) and "photos" in path:
                    os.remove(path)
            except Exception:
                pass
            self._refresh()
