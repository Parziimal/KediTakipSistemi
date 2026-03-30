import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, _toast, DatePicker, export_csv, confirm
from constants import EXPENSE_CATEGORIES


class ExpenseFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"💰  {self.cname} — Harcamalar").pack(anchor="w", padx=24, pady=(18,10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=(12,4))
        _lbl(r1, "Tarih:").pack(side="left")
        self.dp = DatePicker(r1); self.dp.pack(side="left", padx=(6,14))
        _lbl(r1, "Kategori:").pack(side="left")
        self.cat_v = ctk.StringVar(value="Muayene")
        ctk.CTkComboBox(r1, variable=self.cat_v, values=EXPENSE_CATEGORIES, width=180).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=(4,12))
        _lbl(r2, "Tutar (₺):").pack(side="left")
        self.amt_v = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.amt_v, width=100).pack(side="left", padx=(6,14))
        _lbl(r2, "Açıklama:").pack(side="left")
        self.desc_v = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.desc_v, width=300).pack(side="left", padx=6)
        _btn(r2, "+ Ekle", self._add, width=90).pack(side="left", padx=10)

        self._summary = ctk.CTkFrame(sc, fg_color="transparent")
        self._summary.pack(fill="x", padx=24, pady=4)
        self.lf = ctk.CTkScrollableFrame(sc, height=300)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(4,16)); self._refresh()

    def _add(self):
        try: amt = float(self.amt_v.get())
        except ValueError: _toast(self._sc, "Geçerli tutar girin!", T.ERROR); return
        db.add_expense(self.cid, self.dp.get(), self.cat_v.get(), amt, self.desc_v.get())
        self.amt_v.set(""); self.desc_v.set(""); self._refresh()

    def _refresh(self):
        for w in self._summary.winfo_children(): w.destroy()
        rows = db.get_expenses(self.cid)
        if rows:
            total = sum(r[4] for r in rows)
            c = _card(self._summary); c.pack(fill="x")
            _lbl(c, f"Toplam: {total:,.2f} ₺", size=16, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=14, pady=10)
            _lbl(c, f"{len(rows)} kayıt", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=10)
            cats = {}
            for r in rows: cats[r[3]] = cats.get(r[3], 0) + r[4]
            if cats:
                tc = max(cats, key=cats.get)
                _lbl(c, f"En çok: {tc} ({cats[tc]:,.0f} ₺)", size=11, color=T.BADGE_YELLOW).pack(side="right", padx=14)

        for w in self.lf.winfo_children(): w.destroy()
        if not rows: _lbl(self.lf, "Kayıt yok.", color=T.TEXT_MUTED).pack(pady=20); return
        for row in rows:
            eid, _, ed, ecat, amt, desc, _ = row
            ec = T.EXPENSE_COLORS.get(ecat, T.TEXT_MUTED)
            c = _card(self.lf); c.pack(fill="x", pady=2)
            _lbl(c, ed, size=12, width=100, color=T.TEXT_PRIMARY).pack(side="left", padx=(12,6), pady=8)
            ctk.CTkLabel(c, text=f" {ecat} ", fg_color=ec, corner_radius=6,
                         font=ctk.CTkFont(size=10, weight="bold"), text_color="white").pack(side="left", padx=4)
            _lbl(c, f"{amt:,.2f} ₺", size=13, bold=True, color=T.ACCENT).pack(side="left", padx=8)
            _lbl(c, desc or "—", size=11, color=T.TEXT_MUTED).pack(side="left", padx=4)
            _del_btn(c, command=lambda e=eid: self._del(e)).pack(side="right", padx=8)

    def _del(self, eid):
        if confirm(self): db.delete_expense(eid); self._refresh()
