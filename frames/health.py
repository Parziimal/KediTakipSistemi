import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, _toast, DatePicker, export_csv, confirm
from constants import HEALTH_NOTE_TYPES


class HealthFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"🏥  {self.cname} — Sağlık Notları").pack(anchor="w", padx=24, pady=(18,10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=(12,4))
        _lbl(r1, "Tarih:").pack(side="left")
        self.dp = DatePicker(r1); self.dp.pack(side="left", padx=(6,14))
        _lbl(r1, "Tür:").pack(side="left")
        self.nt = ctk.StringVar(value="Genel")
        ctk.CTkComboBox(r1, variable=self.nt, values=HEALTH_NOTE_TYPES, width=130).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=4)
        _lbl(r2, "Başlık:").pack(side="left")
        self.title_v = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.title_v, width=500).pack(side="left", padx=6)

        r3 = ctk.CTkFrame(form, fg_color="transparent"); r3.pack(fill="x", padx=16, pady=(4,12))
        _lbl(r3, "İçerik:").pack(side="left", anchor="n", pady=6)
        self.cb = ctk.CTkTextbox(r3, height=65, width=440); self.cb.pack(side="left", padx=6)
        _btn(r3, "+ Ekle", self._add, width=90).pack(side="left", padx=8, anchor="s")

        sr = ctk.CTkFrame(sc, fg_color="transparent"); sr.pack(fill="x", padx=24, pady=(6,4))
        _lbl(sr, "Geçmiş", size=15, bold=True, color=T.TEXT_PRIMARY).pack(side="left")
        self.q = ctk.StringVar(); self.q.trace_add("write", lambda *_: self._refresh())
        ctk.CTkEntry(sr, textvariable=self.q, width=200, placeholder_text="🔍 Ara...").pack(side="right")
        _btn(sr, "📤 CSV", self._export, primary=False, width=80, height=28).pack(side="right", padx=6)

        self.lf = ctk.CTkScrollableFrame(sc, height=260)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(4,16)); self._refresh()

    def _add(self):
        t = self.title_v.get().strip()
        if not t: _toast(self._sc, "Başlık boş!", T.ERROR); return
        db.add_health(self.cid, self.dp.get(), t, self.cb.get("1.0","end-1c"), self.nt.get())
        self.title_v.set(""); self.cb.delete("1.0","end"); self._refresh()

    def _refresh(self):
        for w in self.lf.winfo_children(): w.destroy()
        rows = db.get_health(self.cid)
        q = self.q.get().lower().strip()
        if q: rows = [r for r in rows if q in r[3].lower() or q in (r[4]or"").lower() or q in r[5].lower()]
        if not rows: _lbl(self.lf, "Sonuç yok." if q else "Kayıt yok.", color=T.TEXT_MUTED).pack(pady=20); return
        for row in rows:
            nid, _, nd, title, content, nt = row
            nc = T.NOTE_COLORS.get(nt, T.TEXT_MUTED)
            c = _card(self.lf); c.pack(fill="x", pady=4)
            t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=14, pady=(10,4))
            ctk.CTkLabel(t, text=f" {nt} ", fg_color=nc, corner_radius=6, text_color="white",
                         font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
            _lbl(t, f"  {nd} — {title}", size=13, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=6)
            _del_btn(t, command=lambda n=nid: self._del(n)).pack(side="right")
            if content and content.strip():
                _lbl(c, content, size=12, color=T.TEXT_SECONDARY, wraplength=700, justify="left",
                     anchor="w").pack(anchor="w", padx=16, pady=(0,10))

    def _del(self, nid):
        if confirm(self): db.delete_health(nid); self._refresh()

    def _export(self):
        rows = db.get_health(self.cid)
        if not rows: return
        _toast(self._sc, f"CSV: {export_csv(f'{self.cname}_saglik.csv', ['Tarih','Tür','Başlık','İçerik'], [(r[2],r[5],r[3],r[4]) for r in rows])}")
