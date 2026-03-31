import customtkinter as ctk
import theme as T
import database as db
from utils import _title, _lbl, _card
from constants import (
    VACCINE_GUIDELINES, KITTEN_SCHEDULE,
    DOG_VACCINE_GUIDELINES, DOG_PUPPY_SCHEDULE, DOG_PARASITE_SCHEDULE,
    BIRD_VACCINE_GUIDELINES, BIRD_CARE_SCHEDULE,
)


class GuideFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid = cid
        self._build()

    def _build(self):
        pt = db.get_pet_type(self.cid) if self.cid else "cat"
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        if pt == "dog":
            self._build_dog(sc)
        elif pt == "bird":
            self._build_bird(sc)
        else:
            self._build_cat(sc)

    # ── Kedi Rehberi ─────────────────────────────────────────────────────────
    def _build_cat(self, sc):
        _title(sc, text="📋  WSAVA 2024 & AAFP 2020 — Kedi Aşı Rehberi").pack(
            anchor="w", padx=24, pady=(18, 4))
        _lbl(sc, "Kaynak: WSAVA 2024 • AAHA/AAFP 2020", size=11,
             color=T.TEXT_MUTED).pack(anchor="w", padx=24, pady=(0, 14))

        for ct, ck in [("🟢 TEMEL (Core)", "core"),
                       ("🟡 OPSİYONEL", "non-core"),
                       ("🔴 ÖNERİLMEYEN", "not_recommended")]:
            _lbl(sc, ct, size=15, bold=True, color=T.TEXT_PRIMARY).pack(
                anchor="w", padx=24, pady=(12, 6))
            for k, v in VACCINE_GUIDELINES.items():
                if v["category"] != ck:
                    continue
                self._vaccine_card(sc, k, v, "Yavru")

        _lbl(sc, "🗓️  YAVRU KEDİ AŞI TAKVİMİ", size=15, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 8))
        for age, vax in KITTEN_SCHEDULE:
            r = _card(sc); r.pack(fill="x", padx=24, pady=2)
            _lbl(r, age, size=12, bold=True, width=140,
                 color=T.TEXT_PRIMARY).pack(side="left", padx=12, pady=8)
            _lbl(r, vax, size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=8)
        ctk.CTkFrame(sc, height=20, fg_color="transparent").pack()

    # ── Köpek Rehberi ────────────────────────────────────────────────────────
    def _build_dog(self, sc):
        _title(sc, text="📋  WSAVA 2024 & AAHA 2022 — Köpek Aşı Rehberi").pack(
            anchor="w", padx=24, pady=(18, 4))
        _lbl(sc, "Kaynak: WSAVA 2024 • AAHA 2022 Canine Vaccination Guidelines",
             size=11, color=T.TEXT_MUTED).pack(anchor="w", padx=24, pady=(0, 14))

        for ct, ck in [("🟢 TEMEL (Core)", "core"),
                       ("🟡 OPSİYONEL", "non-core"),
                       ("🔴 ÖNERİLMEYEN", "not_recommended")]:
            _lbl(sc, ct, size=15, bold=True, color=T.TEXT_PRIMARY).pack(
                anchor="w", padx=24, pady=(12, 6))
            for k, v in DOG_VACCINE_GUIDELINES.items():
                if v["category"] != ck:
                    continue
                self._vaccine_card(sc, k, v, "Yavru Köpek")

        _lbl(sc, "🗓️  YAVRU KÖPEK AŞI TAKVİMİ", size=15, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 8))
        for age, vax in DOG_PUPPY_SCHEDULE:
            r = _card(sc); r.pack(fill="x", padx=24, pady=2)
            _lbl(r, age, size=12, bold=True, width=200,
                 color=T.TEXT_PRIMARY).pack(side="left", padx=12, pady=8)
            _lbl(r, vax, size=12, color=T.TEXT_SECONDARY,
                 wraplength=480).pack(side="left", padx=8)

        _lbl(sc, "🛡️  PARAZİT ÖNLEME TAKVİMİ", size=15, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 6))
        _lbl(sc, "Kaynak: CAPC (Companion Animal Parasite Council) • ESCCAP GL1",
             size=11, color=T.TEXT_MUTED).pack(anchor="w", padx=24, pady=(0, 8))
        for pname, pdata in DOG_PARASITE_SCHEDULE.items():
            r = _card(sc); r.pack(fill="x", padx=24, pady=2)
            row = ctk.CTkFrame(r, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=8)
            _lbl(row, pname, size=12, bold=True, width=230,
                 color=T.TEXT_PRIMARY).pack(side="left")
            _lbl(row, pdata["label"], size=12, bold=True,
                 color=T.ACCENT).pack(side="left", padx=8)

        _lbl(sc, "💡  YILLIK SAĞLIK TARAMASI", size=15, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 6))
        for info in [
            "🩸  Heartworm antijen testi — yılda bir (önleme kullansalar dahi)",
            "🦟  Kene kaynaklı hastalık paneli (Ehrlichia, Anaplasma, Borrelia) — yılda bir",
            "🔬  Dışkı muayenesi — yılda en az 2 kez (yüksek riskli köpeklerde 4 kez)",
            "⚖️  Kilo ve vücut kondisyon skoru — her veteriner ziyaretinde",
        ]:
            r = _card(sc); r.pack(fill="x", padx=24, pady=2)
            _lbl(r, info, size=12, color=T.TEXT_SECONDARY,
                 wraplength=680).pack(anchor="w", padx=14, pady=8)
        ctk.CTkFrame(sc, height=20, fg_color="transparent").pack()

    # ── Kuş Rehberi ──────────────────────────────────────────────────────────
    def _build_bird(self, sc):
        _title(sc, text="📋  AAV — Evcil Kuş Sağlık ve Aşı Rehberi").pack(
            anchor="w", padx=24, pady=(18, 4))
        _lbl(sc, "Kaynak: AAV (Association of Avian Veterinarians) • Merck Vet Manual",
             size=11, color=T.TEXT_MUTED).pack(anchor="w", padx=24, pady=(0, 14))

        for ct, ck in [("🟢 TEMEL AŞI", "core"),
                       ("🟡 OPSİYONEL", "non-core"),
                       ("🔴 ÖNERİLMEYEN / SADECE ZOO", "not_recommended")]:
            _lbl(sc, ct, size=15, bold=True, color=T.TEXT_PRIMARY).pack(
                anchor="w", padx=24, pady=(12, 6))
            for k, v in BIRD_VACCINE_GUIDELINES.items():
                if v["category"] != ck:
                    continue
                self._vaccine_card(sc, k, v, "Yavru")

        _lbl(sc, "🗓️  RUTİN BAKIM TAKVİMİ", size=15, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 8))
        for period, desc in BIRD_CARE_SCHEDULE:
            r = _card(sc); r.pack(fill="x", padx=24, pady=3)
            top = ctk.CTkFrame(r, fg_color="transparent")
            top.pack(fill="x", padx=14, pady=(8, 2))
            _lbl(top, period, size=12, bold=True,
                 color=T.ACCENT).pack(side="left")
            _lbl(r, desc, size=12, color=T.TEXT_SECONDARY,
                 wraplength=680).pack(anchor="w", padx=14, pady=(0, 8))

        _lbl(sc, "⚠️  ÖNEMLİ NOTLAR", size=15, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(18, 6))
        for note in [
            "🚫  Muhabbet kuşuna (Melopsittacus undulatus) Polyomavirus aşısı yapılmaz — kontrendike.",
            "🔬  Yeni edinilen kuşlar için ilk 2–3 gün içinde veteriner kontrolü ve dışkı testi yapılmalı.",
            "🦜  Gaga büyümesi her zaman altta yatan hastalığa işaret eder (karaciğer, PBFD, besin eksikliği). Rutin tıraş yapılmaz.",
            "💊  İç mekân kuşlarına rutin antiparazitik tedavi uygulanmaz; yalnızca doğrulanmış enfeksiyonda tedavi yapılır.",
            "🌿  Tüm tohum diyeti yetersizdir — formüle pelet + taze sebze/meyve dengeli diyet için temel.",
        ]:
            r = _card(sc); r.pack(fill="x", padx=24, pady=2)
            _lbl(r, note, size=12, color=T.TEXT_SECONDARY,
                 wraplength=680).pack(anchor="w", padx=14, pady=8)
        ctk.CTkFrame(sc, height=20, fg_color="transparent").pack()

    # ── Ortak aşı kartı ──────────────────────────────────────────────────────
    def _vaccine_card(self, sc, k, v, juvenile_label):
        c = _card(sc); c.pack(fill="x", padx=24, pady=4)
        t = ctk.CTkFrame(c, fg_color="transparent"); t.pack(fill="x", padx=14, pady=(10, 4))
        vc = T.VACCINE_COLORS.get(k, T.TEXT_MUTED)
        ctk.CTkLabel(t, text=f" {v['category_tr']} ", fg_color=vc, corner_radius=6,
                     text_color="white",
                     font=ctk.CTkFont(size=10, weight="bold")).pack(side="left")
        _lbl(t, f"  {v['tr_name']}", size=14, bold=True,
             color=T.TEXT_PRIMARY).pack(side="left", padx=6)
        _lbl(c, f"  {v['full_name']}", size=11,
             color=T.TEXT_SECONDARY).pack(anchor="w", padx=14)
        _lbl(c, f"  Bileşenler: {v['components']}", size=11,
             color=T.TEXT_MUTED).pack(anchor="w", padx=14, pady=2)
        if v["adult_interval_days"] > 0:
            _lbl(c, f"  Yetişkin: {v['adult_interval_label']}", size=12, bold=True,
                 color=T.ACCENT).pack(anchor="w", padx=14, pady=2)
        if v.get("kitten_weeks"):
            ws = ", ".join(f"{w}. hafta" for w in v["kitten_weeks"])
            _lbl(c, f"  {juvenile_label}: {ws}", size=11,
                 color=T.TEXT_SECONDARY).pack(anchor="w", padx=14, pady=2)
        _lbl(c, f"  {v['notes']}", size=11, color=T.TEXT_MUTED,
             wraplength=700).pack(anchor="w", padx=14, pady=(2, 10))
