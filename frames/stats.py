import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl, _card

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


class StatsFrame(ctk.CTkFrame):
    def __init__(self, parent, cid=None, cname=None, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        _title(sc, text="📊  Genel İstatistikler").pack(anchor="w", padx=24, pady=(18, 10))

        self._content = ctk.CTkFrame(sc, fg_color="transparent")
        self._content.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self._refresh()

    def _refresh(self):
        for w in self._content.winfo_children():
            w.destroy()

        s = db.get_all_stats()

        # Özet kartları
        top = ctk.CTkFrame(self._content, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        cards = [
            ("🐱 Kedi", str(s["cats"]), T.ACCENT),
            ("💉 Aşı", str(s["vaccines"]), T.BADGE_BLUE),
            ("💊 Aktif İlaç", str(s["active_meds"]), T.BADGE_PURPLE),
            ("📆 Bekleyen Randevu", str(s["pending_apps"]), T.BADGE_ORANGE),
            ("🏥 Sağlık Notu", str(s["health"]), T.BADGE_TEAL),
            ("⚖️ Kilo Kaydı", str(s["weights"]), T.BADGE_GREEN),
            ("💰 Toplam Harcama", f"{s['expenses_total']:,.2f} ₺", T.BADGE_YELLOW),
        ]
        for i, (label, val, color) in enumerate(cards):
            c = _card(top)
            c.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 4, 4 if i < len(cards) - 1 else 0), pady=4)
            _lbl(c, label, size=11, color=T.TEXT_SECONDARY).pack(anchor="w", padx=12, pady=(10, 0))
            _lbl(c, val, size=18, bold=True, color=color).pack(anchor="w", padx=12, pady=(2, 10))

        # Kedi bazlı harcama
        if s["exp_by_cat"]:
            sec = _card(self._content)
            sec.pack(fill="x", pady=6)
            _lbl(sec, "Kedi Bazlı Harcamalar", size=14, bold=True, color=T.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(12, 6))
            for name, total in s["exp_by_cat"]:
                r = ctk.CTkFrame(sec, fg_color="transparent")
                r.pack(fill="x", padx=16, pady=2)
                _lbl(r, name, size=12, color=T.TEXT_PRIMARY).pack(side="left")
                _lbl(r, f"{total:,.2f} ₺", size=12, bold=True, color=T.ACCENT).pack(side="right", padx=8)

            # Pasta grafik
            if HAS_MPL and len(s["exp_by_cat"]) > 0:
                names = [x[0] for x in s["exp_by_cat"] if x[1] > 0]
                vals = [x[1] for x in s["exp_by_cat"] if x[1] > 0]
                if vals:
                    fig = Figure(figsize=(3.5, 2.5), dpi=100, facecolor="#1B2B21")
                    ax = fig.add_subplot(111)
                    ax.set_facecolor("#1B2B21")
                    colors = [T.ACCENT, T.BADGE_BLUE, T.BADGE_ORANGE, T.BADGE_PURPLE, T.BADGE_TEAL,
                              T.BADGE_YELLOW, T.BADGE_PINK, T.BADGE_GREEN]
                    ax.pie(vals, labels=names, autopct="%1.0f%%", startangle=90,
                           colors=colors[:len(vals)],
                           textprops={"color": T.TEXT_PRIMARY, "fontsize": 9})
                    fig.tight_layout(pad=1)
                    canvas = FigureCanvasTkAgg(fig, sec)
                    canvas.draw()
                    canvas.get_tk_widget().pack(padx=12, pady=(4, 12))

            _lbl(sec, "", size=1).pack(pady=4)  # spacer

        # Kategori bazlı harcama
        if s["exp_by_category"]:
            sec2 = _card(self._content)
            sec2.pack(fill="x", pady=6)
            _lbl(sec2, "Kategori Bazlı Harcamalar (Top 5)", size=14, bold=True,
                 color=T.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(12, 6))
            max_val = max(x[1] for x in s["exp_by_category"]) if s["exp_by_category"] else 1
            for cat, total in s["exp_by_category"]:
                r = ctk.CTkFrame(sec2, fg_color="transparent")
                r.pack(fill="x", padx=16, pady=3)
                _lbl(r, cat, size=12, color=T.TEXT_PRIMARY, width=140).pack(side="left")
                bar_w = max(int(250 * total / max_val), 10)
                bc = T.EXPENSE_COLORS.get(cat, T.ACCENT)
                ctk.CTkFrame(r, fg_color=bc, height=18, width=bar_w, corner_radius=4).pack(side="left", padx=6)
                _lbl(r, f"{total:,.0f} ₺", size=11, bold=True, color=T.TEXT_SECONDARY).pack(side="left", padx=4)
            _lbl(sec2, "", size=1).pack(pady=6)
