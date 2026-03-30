import os, shutil, customtkinter as ctk
from tkinter import filedialog, messagebox
import theme as T, database as db
from utils import _title, _lbl, _card, _toast, _btn, DatePicker, calc_age, export_csv, confirm, PHOTOS_DIR
from constants import CAT_BREEDS, CAT_COLORS, CAT_GENDERS, CAT_BLOOD_TYPES
try:
    from PIL import Image; HAS_PIL = True
except ImportError: HAS_PIL = False

try:
    import qrcode; HAS_QR = True
except ImportError: HAS_QR = False


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname, self.app = cid, cname, app
        self._photo_path = ""; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"🐱  {self.cname} — Profil").pack(anchor="w", padx=24, pady=(18,10))

        # Fotoğraf
        pc = _card(sc); pc.pack(fill="x", padx=24, pady=(0,10))
        pi = ctk.CTkFrame(pc, fg_color="transparent"); pi.pack(padx=16, pady=14)
        self._plbl = ctk.CTkLabel(pi, text="🐱", font=ctk.CTkFont(size=60))
        self._plbl.pack(side="left", padx=(0,16))
        bc = ctk.CTkFrame(pi, fg_color="transparent"); bc.pack(side="left")
        _btn(bc, "📷 Fotoğraf Seç", self._pick_photo, width=160).pack(pady=3)
        _btn(bc, "❌ Kaldır", self._rm_photo, primary=False, width=160).pack(pady=3)
        if HAS_QR:
            _btn(bc, "📱 QR Kod", self._gen_qr, primary=False, width=160).pack(pady=3)
        self._age_lbl = _lbl(bc, "Yaş: —", size=13, bold=True)
        self._age_lbl.pack(pady=(6,0))

        # Form
        card = _card(sc); card.pack(fill="x", padx=24, pady=8)
        card.columnconfigure(1, weight=1); self.vars = {}; r = 0
        self._fe(card, r, "İsim", "name"); r+=1
        self._fc(card, r, "Irk", "breed", CAT_BREEDS); r+=1
        ctk.CTkLabel(card, text="Doğum Tarihi:", anchor="e", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=r, column=0, sticky="e", padx=(18,8), pady=9)
        self._dp = DatePicker(card); self._dp.grid(row=r, column=1, sticky="w", padx=(0,18), pady=9); r+=1
        self._fc(card, r, "Renk / Desen", "color", CAT_COLORS); r+=1
        self._fc(card, r, "Cinsiyet", "gender", CAT_GENDERS); r+=1
        self._fc(card, r, "Kan Grubu", "blood_type", CAT_BLOOD_TYPES); r+=1
        self._fe(card, r, "Çip No", "chip_no"); r+=1

        ctk.CTkLabel(card, text="Kısırlaştırıldı:", anchor="e", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=r, column=0, sticky="e", padx=(18,8), pady=9)
        self.steril_var = ctk.BooleanVar()
        ctk.CTkCheckBox(card, text="Evet", variable=self.steril_var,
                        fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER).grid(
            row=r, column=1, sticky="w", padx=(0,18), pady=9); r+=1

        ctk.CTkLabel(card, text="Notlar:", anchor="ne", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=r, column=0, sticky="ne", padx=(18,8), pady=9)
        self.notes_box = ctk.CTkTextbox(card, height=70, width=300)
        self.notes_box.grid(row=r, column=1, sticky="w", padx=(0,18), pady=9); r+=1

        br = ctk.CTkFrame(card, fg_color="transparent")
        br.grid(row=r, column=0, columnspan=2, pady=14)
        _btn(br, "💾 Kaydet", self._save, width=130).pack(side="left", padx=6)
        _btn(br, "📤 CSV", self._export, primary=False, width=100).pack(side="left", padx=6)
        _btn(br, "🗑️ Kediyi Sil", self._delete_cat, primary=False, width=120).pack(side="left", padx=6)
        self._load()

    def _fe(self, card, r, label, key):
        ctk.CTkLabel(card, text=label+":", anchor="e", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=r, column=0, sticky="e", padx=(18,8), pady=9)
        v = ctk.StringVar(); self.vars[key] = v
        ctk.CTkEntry(card, textvariable=v, width=300).grid(row=r, column=1, sticky="w", padx=(0,18), pady=9)

    def _fc(self, card, r, label, key, values):
        ctk.CTkLabel(card, text=label+":", anchor="e", font=ctk.CTkFont(size=13),
                     text_color=T.TEXT_PRIMARY).grid(row=r, column=0, sticky="e", padx=(18,8), pady=9)
        v = ctk.StringVar(); self.vars[key] = v
        ctk.CTkComboBox(card, variable=v, values=values, width=300).grid(
            row=r, column=1, sticky="w", padx=(0,18), pady=9)

    def _load(self):
        row = db.get_cat(self.cid)
        if not row: return
        self.vars["name"].set(row[1] or ""); self.vars["breed"].set(row[2] or "")
        if row[3]: self._dp.set(row[3])
        self.vars["color"].set(row[4] or ""); self.vars["gender"].set(row[5] or "")
        self.vars["blood_type"].set(row[6] or "Bilinmiyor"); self.steril_var.set(bool(row[7]))
        self.vars["chip_no"].set(row[8] or ""); self._photo_path = row[9] or ""
        self.notes_box.delete("1.0","end"); self.notes_box.insert("1.0", row[10] or "")
        self._show_photo(); self._update_age()

    def _show_photo(self):
        if HAS_PIL and self._photo_path and os.path.exists(self._photo_path):
            img = Image.open(self._photo_path).resize((100,100))
            self._ctkimg = ctk.CTkImage(light_image=img, dark_image=img, size=(100,100))
            self._plbl.configure(image=self._ctkimg, text="")
        else: self._plbl.configure(image=None, text="🐱")

    def _pick_photo(self):
        p = filedialog.askopenfilename(filetypes=[("Resim","*.png *.jpg *.jpeg *.gif *.bmp *.webp")])
        if not p: return
        dest = os.path.join(PHOTOS_DIR, f"cat_{self.cid}{os.path.splitext(p)[1]}")
        shutil.copy2(p, dest); self._photo_path = dest; self._show_photo()

    def _rm_photo(self): self._photo_path = ""; self._show_photo()

    def _update_age(self): self._age_lbl.configure(text=f"Yaş: {calc_age(self._dp.get())}")

    def _gen_qr(self):
        cat = db.get_cat(self.cid)
        if not cat: return
        info = f"İsim: {cat[1]}\nIrk: {cat[2]}\nDoğum: {cat[3]}\nÇip: {cat[8]}\nKan: {cat[6]}"
        qr = qrcode.make(info)
        path = os.path.join(PHOTOS_DIR, f"qr_{self.cid}.png")
        qr.save(path)
        _toast(self._sc, f"QR kaydedildi: {path}")

    def _save(self):
        data = {k: v.get() for k, v in self.vars.items()}
        data["birthdate"] = self._dp.get(); data["sterilized"] = int(self.steril_var.get())
        data["photo_path"] = self._photo_path; data["notes"] = self.notes_box.get("1.0","end-1c")
        db.save_cat(self.cid, data)
        if self.app: self.app.refresh_sidebar()
        _toast(self._sc, "Kaydedildi ✓")

    def _delete_cat(self):
        if len(db.get_cats()) <= 1:
            messagebox.showwarning("Uyarı", "En az 1 kedi olmalı!", parent=self); return
        if confirm(self, f"{self.cname} ve tüm kayıtları silinecek. Emin misiniz?"):
            db.delete_cat(self.cid)
            if self.app: self.app.on_cat_deleted()

    def _export(self):
        cat = db.get_cat(self.cid)
        if not cat: return
        h = ["Alan","Değer"]
        d = [("İsim",cat[1]),("Irk",cat[2]),("Doğum",cat[3]),("Renk",cat[4]),
             ("Cinsiyet",cat[5]),("Kan Grubu",cat[6]),("Kısır","Evet" if cat[7] else "Hayır"),("Çip",cat[8])]
        _toast(self._sc, f"CSV: {export_csv(f'{self.cname}_profil.csv', h, d)}")
