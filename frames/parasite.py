import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, DatePicker, days_remaining, remaining_badge, calc_next, confirm
from constants import PARASITE_SCHEDULE


class ParasiteFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"🐛  {self.cname} — Parazit Takvimi").pack(anchor="w", padx=24, pady=(18,10))
        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=(12,4))
        _lbl(r1, "Tür:").pack(side="left")
        self.pt = ctk.StringVar(value=list(PARASITE_SCHEDULE.keys())[0])
        ctk.CTkComboBox(r1, variable=self.pt, values=list(PARASITE_SCHEDULE.keys()), width=220).pack(side="left", padx=(6,14))
        _lbl(r1, "Tarih:").pack(side="left")
        self.dp = DatePicker(r1); self.dp.pack(side="left", padx=6)
        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=(4,12))
        _lbl(r2, "Ürün:").pack(side="left")
        self.prod = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.prod, width=200).pack(side="left", padx=(6,14))
        _lbl(r2, "Not:").pack(side="left")
        self.notes = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.notes, width=200).pack(side="left", padx=6)
        _btn(r2, "+ Ekle", self._add, width=90).pack(side="left", padx=10)
        self.lf = ctk.CTkScrollableFrame(sc, height=300)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(6,16)); self._refresh()

    def _add(self):
        pt = self.pt.get(); s = PARASITE_SCHEDULE.get(pt, {})
        nd = calc_next(self.dp.get(), s.get("interval_days", 30))
        db.add_parasite(self.cid, pt, self.dp.get(), self.prod.get(), nd, self.notes.get())
        self.prod.set(""); self.notes.set(""); self._refresh()

    def _refresh(self):
        for w in self.lf.winfo_children(): w.destroy()
        rows = db.get_parasites(self.cid)
        if not rows: _lbl(self.lf, "Kayıt yok.", color=T.TEXT_MUTED).pack(pady=20); return
        for row in sorted(rows, key=lambda r: days_remaining(r[5]) if r[5] and days_remaining(r[5]) is not None else 9999):
            pid, _, pt, ad, prod, nd, notes = row
            rem = days_remaining(nd); bt, bc = remaining_badge(rem)
            pc = T.PARASITE_COLORS.get(pt, T.BADGE_ORANGE)
            c = _card(self.lf); c.pack(fill="x", pady=3)
            t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=12, pady=8)
            ctk.CTkLabel(t, text=f" {pt} ", fg_color=pc, corner_radius=6, text_color="white",
                         font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
            _lbl(t, f"  {ad}", size=11, color=T.TEXT_PRIMARY).pack(side="left", padx=6)
            if nd: _lbl(t, f"→ {nd}", size=11, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            _lbl(t, bt, size=11, bold=True, color=bc).pack(side="left", padx=8)
            if prod: _lbl(t, f"[{prod}]", size=10, color=T.TEXT_MUTED).pack(side="left", padx=4)
            _del_btn(t, command=lambda p=pid: self._del(p)).pack(side="right")

    def _del(self, pid):
        if confirm(self): db.delete_parasite(pid); self._refresh()
