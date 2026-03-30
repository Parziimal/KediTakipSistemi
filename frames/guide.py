import customtkinter as ctk
import theme as T
from utils import _title, _lbl, _card
from constants import VACCINE_GUIDELINES, KITTEN_SCHEDULE


class GuideFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        _title(sc, text="📋  WSAVA 2024 & AAFP 2020 — Kedi Aşı Rehberi").pack(anchor="w", padx=24, pady=(18,6))
        _lbl(sc, "Kaynak: WSAVA 2024 • AAHA/AAFP 2020", size=11, color=T.TEXT_MUTED).pack(anchor="w", padx=24, pady=(0,14))

        for ct, ck in [("🟢 TEMEL (Core)","core"),("🟡 OPSİYONEL","non-core"),("🔴 ÖNERİLMEYEN","not_recommended")]:
            _lbl(sc, ct, size=15, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(12,6))
            for k, v in VACCINE_GUIDELINES.items():
                if v["category"] != ck: continue
                c = _card(sc); c.pack(fill="x", padx=24, pady=4)
                t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=14, pady=(10,4))
                vc = T.VACCINE_COLORS.get(k, T.TEXT_MUTED)
                ctk.CTkLabel(t, text=f" {v['category_tr']} ", fg_color=vc, corner_radius=6,
                             text_color="white", font=ctk.CTkFont(size=10, weight="bold")).pack(side="left")
                _lbl(t, f"  {v['tr_name']}", size=14, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=6)
                _lbl(c, f"  {v['full_name']}", size=11, color=T.TEXT_SECONDARY).pack(anchor="w", padx=14)
                _lbl(c, f"  Bileşenler: {v['components']}", size=11, color=T.TEXT_MUTED).pack(anchor="w", padx=14, pady=2)
                if v["adult_interval_days"] > 0:
                    _lbl(c, f"  Yetişkin: {v['adult_interval_label']}", size=12, bold=True,
                         color=T.ACCENT).pack(anchor="w", padx=14, pady=2)
                if v["kitten_weeks"]:
                    ws = ", ".join(f"{w}. hafta" for w in v["kitten_weeks"])
                    _lbl(c, f"  Yavru: {ws}", size=11, color=T.TEXT_SECONDARY).pack(anchor="w", padx=14, pady=2)
                _lbl(c, f"  {v['notes']}", size=11, color=T.TEXT_MUTED, wraplength=700).pack(anchor="w", padx=14, pady=(2,10))

        _lbl(sc, "🗓️  YAVRU KEDİ AŞI TAKVİMİ", size=15, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18,8))
        for age, vax in KITTEN_SCHEDULE:
            r = _card(sc); r.pack(fill="x", padx=24, pady=2)
            _lbl(r, age, size=12, bold=True, width=140, color=T.TEXT_PRIMARY).pack(side="left", padx=12, pady=8)
            _lbl(r, vax, size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=8)
        ctk.CTkFrame(sc, height=20, fg_color="transparent").pack()
