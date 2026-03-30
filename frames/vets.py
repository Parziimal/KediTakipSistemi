import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, _toast, confirm


class VetFrame(ctk.CTkFrame):
    def __init__(self, parent, cid=None, cname=None, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text="🏥  Veteriner Rehberi").pack(anchor="w", padx=24, pady=(18, 10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(form, "Yeni Veteriner Ekle", size=14, bold=True, color=T.TEXT_PRIMARY).pack(
            anchor="w", padx=16, pady=(12, 4))

        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=4)
        _lbl(r1, "Ad Soyad:").pack(side="left")
        self.name_v = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.name_v, width=200).pack(side="left", padx=(6, 14))
        _lbl(r1, "Klinik:").pack(side="left")
        self.clinic_v = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.clinic_v, width=200).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=4)
        _lbl(r2, "Telefon:").pack(side="left")
        self.phone_v = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.phone_v, width=150).pack(side="left", padx=(6, 14))
        _lbl(r2, "Adres:").pack(side="left")
        self.addr_v = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.addr_v, width=300).pack(side="left", padx=6)

        r3 = ctk.CTkFrame(form, fg_color="transparent"); r3.pack(fill="x", padx=16, pady=(4, 12))
        _lbl(r3, "Not:").pack(side="left")
        self.notes_v = ctk.StringVar()
        ctk.CTkEntry(r3, textvariable=self.notes_v, width=380).pack(side="left", padx=6)
        _btn(r3, "+ Ekle", self._add, width=90).pack(side="right", padx=8)

        self.lf = ctk.CTkScrollableFrame(sc, height=360)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(6, 16))
        self._refresh()

    def _add(self):
        n = self.name_v.get().strip()
        if not n:
            _toast(self._sc, "Veteriner adı gerekli!", T.ERROR); return
        db.add_vet(n, self.clinic_v.get(), self.phone_v.get(),
                   self.addr_v.get(), self.notes_v.get())
        self.name_v.set(""); self.clinic_v.set(""); self.phone_v.set("")
        self.addr_v.set(""); self.notes_v.set("")
        self._refresh()

    def _refresh(self):
        for w in self.lf.winfo_children():
            w.destroy()
        rows = db.get_vets()
        if not rows:
            _lbl(self.lf, "Kayıtlı veteriner yok.", color=T.TEXT_MUTED).pack(pady=20)
            return
        for row in rows:
            vid, name, clinic, phone, addr, notes = row
            c = _card(self.lf); c.pack(fill="x", pady=4)
            t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=14, pady=(10, 4))
            _lbl(t, f"🩺  {name}", size=14, bold=True, color=T.TEXT_PRIMARY).pack(side="left")
            if clinic:
                _lbl(t, f"  —  {clinic}", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            _del_btn(t, command=lambda v=vid: self._del(v)).pack(side="right")

            d = ctk.CTkFrame(c, fg_color="transparent"); d.pack(fill="x", padx=16, pady=(0, 10))
            if phone:
                _lbl(d, f"📞 {phone}", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=(0, 12))
            if addr:
                _lbl(d, f"📍 {addr}", size=11, color=T.TEXT_MUTED).pack(side="left", padx=(0, 12))
            if notes:
                _lbl(d, f"📝 {notes}", size=11, color=T.TEXT_MUTED).pack(side="left")

    def _del(self, vid):
        if confirm(self):
            db.delete_vet(vid); self._refresh()
