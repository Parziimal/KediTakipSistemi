import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, _toast, DatePicker, days_remaining, remaining_badge, confirm


class AppointmentsFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"📆  {self.cname} — Randevular").pack(anchor="w", padx=24, pady=(18,10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=(12,4))
        _lbl(r1, "Tarih:").pack(side="left")
        self.dp = DatePicker(r1); self.dp.pack(side="left", padx=(6,14))
        _lbl(r1, "Saat:").pack(side="left")
        self.time_v = ctk.StringVar(value="10:00")
        ctk.CTkComboBox(r1, variable=self.time_v,
                        values=[f"{h:02d}:{m:02d}" for h in range(8,21) for m in (0,30)],
                        width=100).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=4)
        _lbl(r2, "Veteriner:").pack(side="left")
        vets = db.get_vets(); vn = [v[1] for v in vets] if vets else [""]
        self.vet_v = ctk.StringVar()
        ctk.CTkComboBox(r2, variable=self.vet_v, values=vn or [""], width=200).pack(side="left", padx=(6,14))
        _lbl(r2, "Neden:").pack(side="left")
        self.reason_v = ctk.StringVar()
        ctk.CTkComboBox(r2, variable=self.reason_v,
                        values=["Kontrol", "Aşı", "Ameliyat", "Acil", "Diş", "Tahlil", "Diğer"],
                        width=160).pack(side="left", padx=6)

        r3 = ctk.CTkFrame(form, fg_color="transparent"); r3.pack(fill="x", padx=16, pady=(4,12))
        _lbl(r3, "Not:").pack(side="left")
        self.notes_v = ctk.StringVar()
        ctk.CTkEntry(r3, textvariable=self.notes_v, width=380).pack(side="left", padx=6)
        _btn(r3, "+ Ekle", self._add, width=90).pack(side="right", padx=8)

        self.lf = ctk.CTkScrollableFrame(sc, height=340)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(6,16)); self._refresh()

    def _add(self):
        db.add_appointment(self.cid, self.dp.get(), self.time_v.get(), self.vet_v.get(),
                           self.reason_v.get(), "Planlandı", self.notes_v.get())
        self.notes_v.set(""); self._refresh()

    def _refresh(self):
        for w in self.lf.winfo_children(): w.destroy()
        rows = db.get_appointments(self.cid)
        if not rows: _lbl(self.lf, "Randevu yok.", color=T.TEXT_MUTED).pack(pady=20); return
        for r in rows:
            aid, _, ad, at, vet, reason, status, notes = r
            rem = days_remaining(ad); bt, bc = remaining_badge(rem)
            sc = {"Planlandı": T.BADGE_BLUE, "Tamamlandı": T.ACCENT, "İptal": T.ERROR}.get(status, T.TEXT_MUTED)
            c = _card(self.lf); c.pack(fill="x", pady=3)
            t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=12, pady=8)
            ctk.CTkLabel(t, text=f" {status} ", fg_color=sc, corner_radius=6, text_color="white",
                         font=ctk.CTkFont(size=10, weight="bold")).pack(side="left")
            _lbl(t, f"  {ad} {at}", size=12, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=4)
            if reason: _lbl(t, f"  {reason}", size=11, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            if vet: _lbl(t, f"  [{vet}]", size=10, color=T.TEXT_MUTED).pack(side="left", padx=4)
            if status == "Planlandı":
                _lbl(t, bt, size=11, bold=True, color=bc).pack(side="left", padx=6)
            _del_btn(t, command=lambda a=aid: self._del(a)).pack(side="right")
            if status == "Planlandı":
                ctk.CTkButton(t, text="✓", width=30, height=24, fg_color=T.ACCENT,
                              command=lambda a=aid: self._done(a)).pack(side="right", padx=2)
                ctk.CTkButton(t, text="✗", width=30, height=24, fg_color=T.ERROR,
                              command=lambda a=aid: self._cancel(a)).pack(side="right", padx=2)

    def _done(self, aid): db.update_appointment_status(aid, "Tamamlandı"); self._refresh()
    def _cancel(self, aid): db.update_appointment_status(aid, "İptal"); self._refresh()
    def _del(self, aid):
        if confirm(self): db.delete_appointment(aid); self._refresh()
