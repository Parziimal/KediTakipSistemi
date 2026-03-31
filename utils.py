"""Yardımcı fonksiyonlar ve widget'lar."""

import calendar
import csv
import os
import shutil
from datetime import date, datetime, timedelta
from tkinter import messagebox

import customtkinter as ctk
import theme as T

EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
PHOTOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)


def calc_age(bd_str):
    try:
        bd = datetime.strptime(bd_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return "—"
    td = date.today()
    y, m = td.year - bd.year, td.month - bd.month
    if td.day < bd.day: m -= 1
    if m < 0: y -= 1; m += 12
    if y > 0: return f"{y} yıl {m} ay"
    if m > 0: return f"{m} ay"
    return f"{(td - bd).days} gün"


def days_remaining(ds):
    try:
        return (datetime.strptime(ds, "%Y-%m-%d").date() - date.today()).days
    except (ValueError, TypeError):
        return None


def calc_next(applied_str, interval):
    try:
        return (datetime.strptime(applied_str, "%Y-%m-%d").date() + timedelta(days=interval)).isoformat()
    except (ValueError, TypeError):
        return ""


def remaining_badge(d):
    if d is None: return "?", "gray"
    if d < 0:    return f"⚠ {abs(d)} gün geçti!", T.ERROR
    if d == 0:   return "BUGÜN!", T.ERROR
    if d <= 7:   return f"🔴 {d} gün", T.BADGE_ORANGE
    if d <= 30:  return f"🟡 {d} gün", T.BADGE_YELLOW
    return f"🟢 {d} gün", T.ACCENT


def export_csv(filename, headers, rows):
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(rows)
    return path


def confirm(parent, msg="Bu kaydı silmek istediğinize emin misiniz?"):
    return messagebox.askyesno("Onay", msg, parent=parent)


# ── Widget'lar ────────────────────────────────────────────────────────────────

def _title(p, text, **kw):
    return ctk.CTkLabel(p, text=text, font=ctk.CTkFont(size=18, weight="bold"),
                        text_color=T.TEXT_PRIMARY, **kw)

def _subtitle(p, text, **kw):
    return ctk.CTkLabel(p, text=text, font=ctk.CTkFont(size=12),
                        text_color=T.TEXT_MUTED, **kw)

def _lbl(p, text, size=13, bold=False, color=None, **kw):
    f = ctk.CTkFont(size=size, weight="bold" if bold else "normal")
    o = dict(text=text, font=f, **kw)
    if color: o["text_color"] = color
    return ctk.CTkLabel(p, **o)

def _card(p, hover=True, **kw):
    c = ctk.CTkFrame(p, fg_color=T.CARD_BG, corner_radius=10,
                     border_width=1, border_color=T.BORDER, **kw)
    if hover:
        c.bind("<Enter>", lambda e: c.configure(border_color=T.ACCENT))
        c.bind("<Leave>", lambda e: c.configure(border_color=T.BORDER))
    return c

def _empty(p, icon, title, subtitle=""):
    """Boş durum widget'ı — kayıt yokken gösterilir."""
    f = ctk.CTkFrame(p, fg_color="transparent")
    f.pack(pady=24)
    ctk.CTkLabel(f, text=icon, font=ctk.CTkFont(size=36)).pack(pady=(0, 6))
    ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=T.TEXT_SECONDARY).pack()
    if subtitle:
        ctk.CTkLabel(f, text=subtitle, font=ctk.CTkFont(size=11),
                     text_color=T.TEXT_MUTED).pack(pady=(2, 0))
    return f

def _toast(w, msg, color=T.ACCENT):
    l = ctk.CTkLabel(w, text=msg, text_color=color, font=ctk.CTkFont(size=13, weight="bold"))
    l.pack(pady=(0, 4)); w.after(2500, l.destroy)

def _btn(p, text, command, primary=True, **kw):
    fg = T.ACCENT if primary else T.CARD_BG
    hv = T.ACCENT_HOVER if primary else T.SIDEBAR_ACTIVE
    tc = T.BTN_TEXT if primary else T.TEXT_PRIMARY
    return ctk.CTkButton(p, text=text, command=command, fg_color=fg, hover_color=hv,
                         text_color=tc, font=ctk.CTkFont(size=12, weight="bold"), **kw)

def _del_btn(p, command, **kw):
    return ctk.CTkButton(p, text="Sil", width=50, height=24, fg_color=T.SIDEBAR_ACTIVE,
                         hover_color=T.ERROR, font=ctk.CTkFont(size=11), command=command, **kw)


class DatePicker(ctk.CTkFrame):
    def __init__(self, parent, default=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        d = default or date.today()
        self.y = ctk.StringVar(value=str(d.year))
        self.m = ctk.StringVar(value=f"{d.month:02d}")
        self.d = ctk.StringVar(value=f"{d.day:02d}")
        ctk.CTkComboBox(self, variable=self.y, values=[str(y) for y in range(2015,2036)],
                        width=80, font=ctk.CTkFont(size=12)).pack(side="left", padx=(0,2))
        _lbl(self, "/").pack(side="left")
        ctk.CTkComboBox(self, variable=self.m, values=[f"{i:02d}" for i in range(1,13)],
                        width=62, font=ctk.CTkFont(size=12)).pack(side="left", padx=2)
        _lbl(self, "/").pack(side="left")
        ctk.CTkComboBox(self, variable=self.d, values=[f"{i:02d}" for i in range(1,32)],
                        width=62, font=ctk.CTkFont(size=12)).pack(side="left", padx=2)

    def get(self):
        """Geçerli tarihi YYYY-MM-DD formatında döner.
        Geçersiz günleri (Şubat 31 gibi) otomatik olarak ayın son gününe sabitler."""
        try:
            y, m, d = int(self.y.get()), int(self.m.get()), int(self.d.get())
        except (ValueError, TypeError):
            return date.today().isoformat()
        max_day = calendar.monthrange(y, m)[1]
        d = min(d, max_day)
        try:
            date(y, m, d)  # Son geçerlilik kontrolü
        except ValueError:
            return date.today().isoformat()
        return f"{y:04d}-{m:02d}-{d:02d}"

    def set(self, ds):
        try:
            p = ds.split("-"); self.y.set(p[0]); self.m.set(p[1]); self.d.set(p[2])
        except (IndexError, ValueError): pass
