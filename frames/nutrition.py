import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card, _btn, _del_btn, _toast, DatePicker, export_csv, confirm
from constants import FOOD_TYPES

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


class NutritionFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True); self._sc = sc
        _title(sc, text=f"🍽️  {self.cname} — Beslenme & Kilo").pack(anchor="w", padx=24, pady=(18,10))

        form = _card(sc); form.pack(fill="x", padx=24, pady=(0,10))
        r1 = ctk.CTkFrame(form, fg_color="transparent"); r1.pack(fill="x", padx=16, pady=(12,4))
        _lbl(r1, "Tarih:").pack(side="left")
        self.dp = DatePicker(r1); self.dp.pack(side="left", padx=(6,14))
        _lbl(r1, "Kilo (kg):").pack(side="left")
        self.wt = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.wt, width=80).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=(4,4))
        _lbl(r2, "Mama:").pack(side="left")
        self.food = ctk.StringVar()
        ctk.CTkComboBox(r2, variable=self.food, values=FOOD_TYPES, width=200).pack(side="left", padx=(6,14))
        _lbl(r2, "Miktar (g):").pack(side="left")
        self.amt = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.amt, width=80).pack(side="left", padx=6)

        r3 = ctk.CTkFrame(form, fg_color="transparent"); r3.pack(fill="x", padx=16, pady=(4,12))
        _lbl(r3, "Not:").pack(side="left")
        self.notes = ctk.StringVar()
        ctk.CTkEntry(r3, textvariable=self.notes, width=340).pack(side="left", padx=6)
        _btn(r3, "+ Ekle", self._add, width=90).pack(side="left", padx=10)

        # Mama hesaplayıcı
        calc = _card(sc); calc.pack(fill="x", padx=24, pady=(0, 8))
        _lbl(calc, "🧮  Günlük Mama Hesaplayıcı", size=14, bold=True,
             color=T.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10, 4))

        cr1 = ctk.CTkFrame(calc, fg_color="transparent"); cr1.pack(fill="x", padx=14, pady=4)
        _lbl(cr1, "Kilo (kg):").pack(side="left")
        self.calc_wt = ctk.StringVar(value="4.0")
        ctk.CTkEntry(cr1, textvariable=self.calc_wt, width=70).pack(side="left", padx=(6, 14))

        _lbl(cr1, "Aktivite:").pack(side="left")
        self.calc_act = ctk.StringVar(value="Normal (Ev kedisi)")
        ctk.CTkComboBox(cr1, variable=self.calc_act, width=200, values=[
            "Az hareketli / Kısır", "Normal (Ev kedisi)", "Aktif / Çok hareketli",
            "Yavru (< 1 yaş)", "Kilolu (Diyet)"
        ]).pack(side="left", padx=(6, 14))

        _lbl(cr1, "Mama tipi:").pack(side="left")
        self.calc_food = ctk.StringVar(value="Kuru Mama (~3.5 kcal/g)")
        ctk.CTkComboBox(cr1, variable=self.calc_food, width=210, values=[
            "Kuru Mama (~3.5 kcal/g)", "Yaş Mama (~1.0 kcal/g)", "Karışık (Kuru + Yaş)"
        ]).pack(side="left", padx=6)

        cr2 = ctk.CTkFrame(calc, fg_color="transparent"); cr2.pack(fill="x", padx=14, pady=(4, 10))
        _btn(cr2, "Hesapla", self._calc_food, width=100).pack(side="left")
        self._calc_result = ctk.CTkFrame(cr2, fg_color="transparent")
        self._calc_result.pack(side="left", padx=14)

        # Son kilo varsa otomatik doldur
        rows = db.get_weights(self.cid)
        if rows:
            last_w = next((r[3] for r in rows if r[3] > 0), None)
            if last_w:
                self.calc_wt.set(f"{last_w:.1f}")

        # Kilo özeti
        self._summary = ctk.CTkFrame(sc, fg_color="transparent")
        self._summary.pack(fill="x", padx=24, pady=4)

        # Grafik
        if HAS_MPL:
            self._chart_frame = ctk.CTkFrame(sc, fg_color=T.CARD_BG, corner_radius=12, height=220)
            self._chart_frame.pack(fill="x", padx=24, pady=(4,8))
        else:
            self._chart_frame = None

        _lbl(sc, "Kayıtlar", size=15, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=24, pady=(6,4))
        btn_r = ctk.CTkFrame(sc, fg_color="transparent"); btn_r.pack(anchor="e", padx=24)
        _btn(btn_r, "📤 CSV", self._export, primary=False, width=100, height=28).pack()
        self.lf = ctk.CTkScrollableFrame(sc, height=200)
        self.lf.pack(fill="both", expand=True, padx=24, pady=(4,16))
        self._refresh()

    def _calc_food(self):
        for w in self._calc_result.winfo_children():
            w.destroy()
        try:
            kg = float(self.calc_wt.get())
        except ValueError:
            _lbl(self._calc_result, "Geçerli kilo girin!", color=T.ERROR).pack(side="left")
            return
        if kg <= 0:
            _lbl(self._calc_result, "Kilo 0'dan büyük olmalı!", color=T.ERROR).pack(side="left")
            return

        # RER = 70 × kg^0.75
        rer = 70 * (kg ** 0.75)

        # Aktivite faktörü
        act = self.calc_act.get()
        factors = {
            "Az hareketli / Kısır": 1.2,
            "Normal (Ev kedisi)": 1.4,
            "Aktif / Çok hareketli": 1.6,
            "Yavru (< 1 yaş)": 2.5,
            "Kilolu (Diyet)": 1.0,
        }
        factor = factors.get(act, 1.4)
        daily_kcal = rer * factor

        # Mama tipi kcal/g
        food = self.calc_food.get()
        if "Yaş" in food:
            kcal_g = 1.0
        elif "Karışık" in food:
            kcal_g = 2.25
        else:
            kcal_g = 3.5

        daily_g = daily_kcal / kcal_g

        _lbl(self._calc_result, f"≈ {daily_kcal:.0f} kcal/gün", size=14, bold=True,
             color=T.ACCENT).pack(side="left", padx=(0, 12))
        _lbl(self._calc_result, f"→  {daily_g:.0f} g mama/gün", size=14, bold=True,
             color=T.BADGE_YELLOW).pack(side="left", padx=(0, 12))

        # Öğün önerisi
        if daily_g > 0:
            per2 = daily_g / 2
            per3 = daily_g / 3
            _lbl(self._calc_result, f"(2 öğün: {per2:.0f}g  ·  3 öğün: {per3:.0f}g)",
                 size=11, color=T.TEXT_SECONDARY).pack(side="left")

    def _add(self):
        try:
            w = float(self.wt.get()) if self.wt.get() else 0.0
            a = float(self.amt.get()) if self.amt.get() else 0.0
        except ValueError:
            _toast(self._sc, "Sayısal değer girin!", T.ERROR); return
        db.add_weight(self.cid, self.dp.get(), w, self.food.get(), a, self.notes.get())
        self.wt.set(""); self.amt.set(""); self.notes.set(""); self._refresh()

    def _refresh(self):
        rows = db.get_weights(self.cid)

        # Özet
        for w in self._summary.winfo_children(): w.destroy()
        if rows:
            ws = [r[3] for r in rows if r[3] > 0]
            if ws:
                c = _card(self._summary); c.pack(fill="x")
                _lbl(c, f"Son: {ws[0]:.2f} kg", size=14, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=14, pady=10)
                if len(ws) >= 2:
                    d = ws[0] - ws[1]; s = "+" if d > 0 else ""
                    _lbl(c, f"{s}{d:.2f} kg", size=13, bold=True,
                         color=T.ERROR if abs(d) > 0.5 else T.ACCENT).pack(side="left", padx=10)
                _lbl(c, f"Min:{min(ws):.2f} Max:{max(ws):.2f} Ort:{sum(ws)/len(ws):.2f}",
                     size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=10)

        # Grafik
        if HAS_MPL and self._chart_frame:
            for w in self._chart_frame.winfo_children(): w.destroy()
            if rows and len(rows) >= 2:
                dates = [r[2] for r in reversed(rows) if r[3] > 0]
                weights = [r[3] for r in reversed(rows) if r[3] > 0]
                fig = Figure(figsize=(7, 2.2), dpi=100, facecolor="#1B2B21")
                ax = fig.add_subplot(111)
                ax.set_facecolor("#1B2B21")
                ax.plot(dates, weights, color="#4CAF50", linewidth=2, marker="o", markersize=4)
                ax.fill_between(range(len(dates)), weights, alpha=0.15, color="#4CAF50")
                ax.set_ylabel("kg", color="#8FA896", fontsize=9)
                ax.tick_params(colors="#8FA896", labelsize=8)
                ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
                ax.spines["bottom"].set_color("#2A3D30"); ax.spines["left"].set_color("#2A3D30")
                if len(dates) > 10:
                    ax.set_xticks(ax.get_xticks()[::len(dates)//5])
                fig.tight_layout(pad=1)
                canvas = FigureCanvasTkAgg(fig, self._chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

        # Liste
        for w in self.lf.winfo_children(): w.destroy()
        if not rows: _lbl(self.lf, "Kayıt yok.", color=T.TEXT_MUTED).pack(pady=20); return
        for row in rows:
            lid, _, ld, wt, ft, fa, notes = row
            c = _card(self.lf); c.pack(fill="x", pady=2)
            _lbl(c, ld, size=12, width=100, color=T.TEXT_PRIMARY).pack(side="left", padx=(12,6), pady=8)
            _lbl(c, f"{wt} kg" if wt else "—", size=12, bold=True, width=70, color=T.TEXT_PRIMARY).pack(side="left", padx=4)
            _lbl(c, ft or "—", size=12, width=140, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            _lbl(c, f"{fa}g" if fa else "—", size=12, width=70, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            _lbl(c, notes or "—", size=11, color=T.TEXT_MUTED, width=160).pack(side="left", padx=4)
            _del_btn(c, command=lambda l=lid: self._del(l)).pack(side="right", padx=8)

    def _del(self, lid):
        if confirm(self): db.delete_weight(lid); self._refresh()

    def _export(self):
        rows = db.get_weights(self.cid)
        if not rows: return
        _toast(self._sc, f"CSV: {export_csv(f'{self.cname}_kilo.csv', ['Tarih','Kilo','Mama','Miktar','Not'], [(r[2],r[3],r[4],r[5],r[6]) for r in rows])}")
