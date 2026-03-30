import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, _toast, DatePicker, confirm
from constants import MED_FREQUENCIES


class MedicationsFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"💊  {self.cname} — İlaç Takibi").pack(anchor="w", padx=24, pady=(18,10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        _lbl(form, "Yeni İlaç", size=14, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12,4))
        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=4)
        _lbl(r1, "İlaç Adı:").pack(side="left")
        self.name_v = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.name_v, width=200).pack(side="left", padx=(6,14))
        _lbl(r1, "Dozaj:").pack(side="left")
        self.dosage_v = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.dosage_v, width=140).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=4)
        _lbl(r2, "Sıklık:").pack(side="left")
        self.freq_v = ctk.StringVar(value="Günde 1")
        ctk.CTkComboBox(r2, variable=self.freq_v, values=MED_FREQUENCIES, width=160).pack(side="left", padx=(6,14))
        _lbl(r2, "Başlangıç:").pack(side="left")
        self.dp_start = DatePicker(r2); self.dp_start.pack(side="left", padx=6)

        r3 = ctk.CTkFrame(form, fg_color="transparent"); r3.pack(fill="x", padx=16, pady=4)
        _lbl(r3, "Bitiş:").pack(side="left")
        self.dp_end = DatePicker(r3); self.dp_end.pack(side="left", padx=(6,14))
        _lbl(r3, "Not:").pack(side="left")
        self.notes_v = ctk.StringVar()
        ctk.CTkEntry(r3, textvariable=self.notes_v, width=260).pack(side="left", padx=6)

        r4 = ctk.CTkFrame(form, fg_color="transparent"); r4.pack(fill="x", padx=16, pady=(4,12))
        _btn(r4, "+ Ekle", self._add, width=100).pack(side="right", padx=8)

        _lbl(sc, "Aktif İlaçlar", size=15, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(8,4))
        self.active_lf = ctk.CTkScrollableFrame(sc, height=160)
        self.active_lf.pack(fill="both", expand=True, padx=24, pady=(0,8))

        _lbl(sc, "Geçmiş İlaçlar", size=15, bold=True, color=T.TEXT_SECONDARY).pack(anchor="w", padx=24, pady=(8,4))
        self.past_lf = ctk.CTkScrollableFrame(sc, height=140)
        self.past_lf.pack(fill="both", expand=True, padx=24, pady=(0,16))
        self._refresh()

    def _add(self):
        n = self.name_v.get().strip()
        if not n: _toast(self._sc, "İlaç adı gerekli!", T.ERROR); return
        db.add_medication(self.cid, n, self.dosage_v.get(), self.freq_v.get(),
                          self.dp_start.get(), self.dp_end.get(), self.notes_v.get())
        self.name_v.set(""); self.dosage_v.set(""); self.notes_v.set(""); self._refresh()

    def _refresh(self):
        for w in self.active_lf.winfo_children(): w.destroy()
        for w in self.past_lf.winfo_children(): w.destroy()
        rows = db.get_medications(self.cid)
        active = [r for r in rows if r[7]]
        past = [r for r in rows if not r[7]]

        if not active:
            _lbl(self.active_lf, "Aktif ilaç yok.", color=T.TEXT_MUTED).pack(pady=10)
        for r in active:
            self._row(self.active_lf, r, True)
        if not past:
            _lbl(self.past_lf, "Geçmiş ilaç yok.", color=T.TEXT_MUTED).pack(pady=10)
        for r in past:
            self._row(self.past_lf, r, False)

    def _row(self, parent, r, active):
        mid, _, name, dosage, freq, start, end, _, notes = r
        c = _card(parent); c.pack(fill="x", pady=3)
        t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=12, pady=8)
        status_color = T.ACCENT if active else T.TEXT_MUTED
        ctk.CTkLabel(t, text=f" {'●' if active else '○'} {name} ", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=status_color).pack(side="left")
        if dosage: _lbl(t, f"  {dosage}", size=11, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
        _lbl(t, f"  {freq}", size=11, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
        _lbl(t, f"  {start} → {end}", size=10, color=T.TEXT_MUTED).pack(side="left", padx=4)
        _del_btn(t, command=lambda m=mid: self._del(m)).pack(side="right")
        if active:
            ctk.CTkButton(t, text="Bitir", width=50, height=24, fg_color=T.BADGE_ORANGE,
                          hover_color=T.ERROR, font=ctk.CTkFont(size=11),
                          command=lambda m=mid: self._toggle(m, 0)).pack(side="right", padx=4)

    def _toggle(self, mid, val):
        db.toggle_medication(mid, val); self._refresh()

    def _del(self, mid):
        if confirm(self): db.delete_medication(mid); self._refresh()
