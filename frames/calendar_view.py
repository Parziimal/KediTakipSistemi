import calendar
from datetime import date, datetime
from tkinter import Canvas
import customtkinter as ctk
import theme as T, database as db
from utils import _title, _lbl
from constants import MONTHS_TR
import theme


class CalendarFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname
        self._year = date.today().year
        self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)

        top = ctk.CTkFrame(sc, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(18, 10))
        _title(top, text=f"📅  {self.cname} — Yıllık Takvim").pack(side="left")
        ctk.CTkButton(top, text="◀", width=40, fg_color=T.CARD_BG,
                      hover_color=T.SIDEBAR_HOVER, command=lambda: self._nav(-1)).pack(side="right", padx=2)
        self._yl = _lbl(top, str(self._year), size=16, bold=True, color=T.ACCENT)
        self._yl.pack(side="right", padx=8)
        ctk.CTkButton(top, text="▶", width=40, fg_color=T.CARD_BG,
                      hover_color=T.SIDEBAR_HOVER, command=lambda: self._nav(1)).pack(side="right", padx=2)

        # Lejant
        leg = ctk.CTkFrame(sc, fg_color="transparent")
        leg.pack(fill="x", padx=28, pady=(0, 8))
        for symbol, desc, color in [
            ("●", "Aşı yapıldı", T.BADGE_BLUE),
            ("○", "Sonraki aşı", T.ACCENT_SECONDARY),
            ("●", "Parazit yapıldı", T.BADGE_ORANGE),
            ("○", "Sonraki parazit", T.BADGE_YELLOW),
            ("★", "Randevu", T.BADGE_PINK),
        ]:
            _lbl(leg, f"{symbol} {desc}", size=10, color=color).pack(side="left", padx=(0, 14))

        self._grid = ctk.CTkFrame(sc, fg_color="transparent")
        self._grid.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        for c in range(4):
            self._grid.columnconfigure(c, weight=1)
        for r in range(3):
            self._grid.rowconfigure(r, weight=1)
        self._render()

    def _nav(self, d):
        self._year += d
        self._yl.configure(text=str(self._year))
        self._render()

    def _collect_events(self):
        applied = {}
        upcoming = {}
        specials = {}

        for v in db.get_vaccines(self.cid):
            self._add_date(applied, v[6], T.VACCINE_COLORS.get(v[2], T.BADGE_BLUE))
            if v[7]:
                self._add_date(upcoming, v[7], T.ACCENT_SECONDARY)

        for p in db.get_parasites(self.cid):
            self._add_date(applied, p[3], theme.PARASITE_COLORS.get(p[2], T.BADGE_ORANGE))
            if p[5]:
                self._add_date(upcoming, p[5], T.BADGE_YELLOW)

        for a in db.get_appointments(self.cid):
            self._add_date(specials, a[2], T.BADGE_PINK)

        return applied, upcoming, specials

    def _add_date(self, d, ds, color):
        try:
            dt = datetime.strptime(ds, "%Y-%m-%d").date()
            if dt.year == self._year:
                d.setdefault((dt.month, dt.day), []).append(color)
        except (ValueError, TypeError):
            pass

    def _render(self):
        for w in self._grid.winfo_children():
            w.destroy()

        applied, upcoming, specials = self._collect_events()
        today = date.today()
        days_tr = ["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pz"]

        CW = 30   # hücre genişliği
        CH = 20   # hücre yüksekliği
        HDR = 24  # ay başlığı + gün isimleri yüksekliği
        PAD = 6

        for mi in range(12):
            gr, gc = divmod(mi, 4)
            month = mi + 1
            is_current = (today.year == self._year and today.month == month)
            mc = calendar.monthcalendar(self._year, month)
            rows = len(mc)

            canvas_w = 7 * CW + PAD * 2
            canvas_h = HDR + 18 + rows * CH + PAD
            bg = T.SIDEBAR_ACTIVE if is_current else T.CARD_BG

            wrapper = ctk.CTkFrame(self._grid, fg_color=bg, corner_radius=10,
                                   border_width=2 if is_current else 0,
                                   border_color=T.ACCENT if is_current else bg)
            wrapper.grid(row=gr, column=gc, padx=4, pady=4, sticky="nsew")

            cv = Canvas(wrapper, width=canvas_w, height=canvas_h,
                        bg=bg, highlightthickness=0, bd=0)
            cv.pack(padx=2, pady=2)

            # Ay başlığı
            cv.create_text(PAD + 4, 8, text=MONTHS_TR[mi], anchor="nw",
                           fill=T.ACCENT if is_current else T.TEXT_SECONDARY,
                           font=("Segoe UI", 11, "bold"))

            # Gün isimleri
            y0 = HDR
            for di, dn in enumerate(days_tr):
                x = PAD + di * CW + CW // 2
                cv.create_text(x, y0, text=dn, anchor="n",
                               fill=T.TEXT_MUTED, font=("Segoe UI", 8))

            # Gün hücreleri
            y_start = y0 + 18
            for wi, week in enumerate(mc):
                for di, day in enumerate(week):
                    if day == 0:
                        continue

                    cx = PAD + di * CW + CW // 2
                    cy = y_start + wi * CH + CH // 2
                    key = (month, day)
                    is_today = (today.year == self._year and today.month == month and today.day == day)
                    has_applied = key in applied
                    has_upcoming = key in upcoming
                    has_special = key in specials
                    r = 9  # daire yarıçapı

                    # Bugün → yeşil dolu daire
                    if is_today:
                        cv.create_oval(cx - r, cy - r, cx + r, cy + r, fill=T.ACCENT, outline="")
                        cv.create_text(cx, cy, text=str(day), fill="#FFFFFF",
                                       font=("Segoe UI", 9, "bold"))
                    # Sonraki aşı/parazit → renkli çerçeve daire
                    elif has_upcoming:
                        ring_color = upcoming[key][0]
                        cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                                       fill="", outline=ring_color, width=2)
                        txt_c = ring_color if not has_applied else applied[key][0]
                        cv.create_text(cx, cy, text=str(day), fill=txt_c,
                                       font=("Segoe UI", 9, "bold"))
                    # Normal gün
                    else:
                        txt_c = T.TEXT_PRIMARY
                        font_w = "normal"
                        if has_applied:
                            txt_c = applied[key][0]
                            font_w = "bold"
                        elif has_special:
                            txt_c = specials[key][0]
                            font_w = "bold"
                        cv.create_text(cx, cy, text=str(day), fill=txt_c,
                                       font=("Segoe UI", 9, font_w))

                    # Aşı/parazit yapılan gün → altında küçük renkli nokta
                    if has_applied:
                        dot_color = applied[key][0]
                        cv.create_oval(cx - 2, cy + r + 1, cx + 2, cy + r + 5,
                                       fill=dot_color, outline="")

                    # Randevu → üstünde küçük yıldız
                    if has_special and not has_applied and not has_upcoming:
                        cv.create_text(cx, cy - r - 3, text="★", fill=specials[key][0],
                                       font=("Segoe UI", 6))
