import customtkinter as ctk
from tkinter import messagebox
import theme as T, database as db
from utils import _title, _lbl, _card, _del_btn, _btn, DatePicker, days_remaining, remaining_badge, calc_next, confirm
from constants import VACCINE_GUIDELINES, DOG_VACCINE_GUIDELINES, BIRD_VACCINE_GUIDELINES


class VaccineFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        pt = db.get_pet_type(self.cid)
        if pt == "dog":
            self._vax_guide = DOG_VACCINE_GUIDELINES
        elif pt == "bird":
            self._vax_guide = BIRD_VACCINE_GUIDELINES
        else:
            self._vax_guide = {k: v for k, v in VACCINE_GUIDELINES.items()
                               if v["category"] != "not_recommended"}

        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"💉  {self.cname} — Aşı Takvimi").pack(anchor="w", padx=24, pady=(18,10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        _lbl(form, "Yeni Aşı Kaydı", size=14, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=16, pady=(12,4))

        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=4)
        _lbl(r1, "Aşı:").pack(side="left")
        opts = [f"{v['tr_name']} ({v['category_tr']})" for v in self._vax_guide.values()]
        self.vax_var = ctk.StringVar(value=opts[0] if opts else "")
        ctk.CTkComboBox(r1, variable=self.vax_var, values=opts, width=300).pack(side="left", padx=(6,14))
        _lbl(r1, "Doz:").pack(side="left")
        self.dose_var = ctk.StringVar(value="1")
        ctk.CTkEntry(r1, textvariable=self.dose_var, width=50).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=4)
        _lbl(r2, "Yapıldı:").pack(side="left")
        self.dp = DatePicker(r2); self.dp.pack(side="left", padx=(6,14))
        _lbl(r2, "Veteriner:").pack(side="left")
        vets = db.get_vets(); vn = [v[1] for v in vets] if vets else [""]
        self.vet_var = ctk.StringVar()
        ctk.CTkComboBox(r2, variable=self.vet_var, values=vn or [""], width=180).pack(side="left", padx=6)

        r2b = ctk.CTkFrame(form, fg_color="transparent"); r2b.pack(fill="x", padx=16, pady=4)
        _lbl(r2b, "Sonraki Aşı:").pack(side="left")
        self.nd_dp = DatePicker(r2b); self.nd_dp.pack(side="left", padx=(6,14))
        self._nd_hint = _lbl(r2b, "", size=11, color=T.TEXT_MUTED)
        self._nd_hint.pack(side="left")

        r3 = ctk.CTkFrame(form, fg_color="transparent"); r3.pack(fill="x", padx=16, pady=(4,12))
        _lbl(r3, "Not:").pack(side="left")
        self.notes_var = ctk.StringVar()
        ctk.CTkEntry(r3, textvariable=self.notes_var, width=400).pack(side="left", padx=6)
        _btn(r3, "+ Ekle", self._add, width=90).pack(side="right", padx=8)

        # Otomatik güncelleme bağlamaları
        self.vax_var.trace_add("write", self._update_nd)
        self.dp.y.trace_add("write", self._update_nd)
        self.dp.m.trace_add("write", self._update_nd)
        self.dp.d.trace_add("write", self._update_nd)
        self._update_nd()

        self.lf = ctk.CTkScrollableFrame(sc, height=320)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(6,16))
        self._refresh()

    def _get_guide(self):
        sel = self.vax_var.get()
        for k, v in self._vax_guide.items():
            if v["tr_name"] in sel: return k, v
        return None, None

    def _update_nd(self, *_):
        k, g = self._get_guide()
        if not g:
            return
        interval = g.get("adult_interval_days", 0)
        if interval > 0:
            nd = calc_next(self.dp.get(), interval)
            self.nd_dp.set(nd)
            self._nd_hint.configure(text=f"(Önerilen: {g['adult_interval_label']})")
        else:
            self._nd_hint.configure(text="(Sonraki aşı önerilmiyor)")

    def _add(self):
        k, g = self._get_guide()
        if not g: return
        applied = self.dp.get()
        interval = g.get("adult_interval_days", 0)
        auto_nd = calc_next(applied, interval) if interval > 0 else ""
        selected_nd = self.nd_dp.get()

        # Kullanıcı önerilen tarihten farklı bir tarih seçtiyse onay iste
        if auto_nd and selected_nd != auto_nd:
            ok = messagebox.askyesno(
                "Tarih Onayı",
                f"Önerilen sonraki aşı tarihi: {auto_nd}\n"
                f"(Aralık: {g['adult_interval_label']})\n\n"
                f"Seçtiğiniz tarih: {selected_nd}\n\n"
                f"Yine de bu tarihi kullanmak istiyor musunuz?",
                parent=self
            )
            if not ok:
                return
            nd = selected_nd
        else:
            nd = selected_nd if selected_nd else auto_nd

        db.add_vaccine(self.cid, k, g["tr_name"], g["category"],
                       int(self.dose_var.get() or 1), applied, nd, self.vet_var.get(), self.notes_var.get())
        self.notes_var.set(""); self.dose_var.set(str(int(self.dose_var.get() or 0) + 1)); self._refresh()

    def _refresh(self):
        for w in self.lf.winfo_children(): w.destroy()
        rows = db.get_vaccines(self.cid)
        if not rows: _lbl(self.lf, "Kayıt yok.", color=T.TEXT_MUTED).pack(pady=20); return
        for row in sorted(rows, key=lambda r: days_remaining(r[7]) if r[7] and days_remaining(r[7]) is not None else 9999):
            vid, _, vk, vl, cat, dose, app_d, nd, vet, notes = row
            rem = days_remaining(nd); bt, bc = remaining_badge(rem)
            vc = T.VACCINE_COLORS.get(vk, T.TEXT_SECONDARY)
            c = _card(self.lf); c.pack(fill="x", pady=3)
            t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=12, pady=(8,4))
            ctk.CTkLabel(t, text=f" {vl} ", fg_color=vc, corner_radius=6, text_color="white",
                         font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
            _lbl(t, f" Doz #{dose} • {app_d}", size=11, color=T.TEXT_PRIMARY).pack(side="left", padx=6)
            if nd: _lbl(t, f"→ {nd}", size=11, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            _lbl(t, bt, size=11, bold=True, color=bc).pack(side="left", padx=8)
            if vet: _lbl(t, f"[{vet}]", size=10, color=T.TEXT_MUTED).pack(side="left", padx=4)
            _del_btn(t, command=lambda v=vid: self._del(v)).pack(side="right")

    def _del(self, vid):
        if confirm(self): db.delete_vaccine(vid); self._refresh()
